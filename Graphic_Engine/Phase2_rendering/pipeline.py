from myrenderer import *
import numpy as np
from PIL import Image
from tqdm.notebook import tqdm

#파이프라인 클래스(main 함수 간결하게 하기)
class Pipeline:
  def __init__(self,width, height):
    self.width = width
    self.height = height

    # 1. 엔진 메모리(버퍼) 할당
    self.frame_buffer = np.zeros((height, width, 3), dtype = np.uint8)
    self.z_buffer = np.full((height, width), float('inf'))

    # 2. 카메라 기본 세팅
    self.camera = Camera(Vector3(0, 0, 0), 0, 0)

    # 3. 조명 기본 세팅
    self.light_pos = Vector3(1, 2, 3)
    self.light_intensity = 50
    self.ambient_light = 0.35
    self.lights = []

  #픽셀 하나하나의 색상을 결정
  def fragment_shader(self, u, v, face_normal, tangent_vector, interp_pos, view_dir, diffuse_map, normal_map, specular_map):
    # 1. 텍스처에서 기본 색상 추출
    base_color = diffuse_map.get_color(u, v)
    nm_color = normal_map.get_color(u, v)
    sp_color = specular_map.get_color(u, v)

    # 2. 노멀 맵 TBN 디코딩 및 월드 노멀 벡터 도출
    nx = (nm_color.r / 127.5) - 1
    ny = (nm_color.g / 127.5) - 1
    nz = (nm_color.b / 127.5) - 1
    local_normal = Vector3(nx, ny, nz).normalize()

    normal = face_normal.normalize()
    tangent = tangent_vector.minus(normal.multiply(tangent_vector.dot(normal))).normalize()
    bitangent = normal.cross(tangent).normalize()

    world_normal = Vector3(
        tangent.x * local_normal.x + bitangent.x * local_normal.y + normal.x * local_normal.z,
        tangent.y * local_normal.x + bitangent.y * local_normal.y + normal.y * local_normal.z,
        tangent.z * local_normal.x + bitangent.z * local_normal.y + normal.z * local_normal.z
    ).normalize()

    # 3. 조명 누적 변수 초기화
    total_diffuse_r, total_diffuse_g, total_diffuse_b = 0.0, 0.0, 0.0
    total_specular = 0.0

    # 4. 씬에 있는 모든 조명을 순회하며 빛 누적 (모듈화된 함수 사용)
    for light in self.lights:
        light_dir = None
        attenuation = 1.0

        if isinstance(light, Pointlight):
            light_vector = light.position.minus(interp_pos)
            light_distance = light_vector.magnitude()
            attenuation = 1.0 / (1.0 + 0.1 * light_distance + 0.05 * (light_distance ** 2))
            light_dir = light_vector.normalize()

        elif isinstance(light, Directlight):
            light_dir = light.direction.multiply(-1).normalize()
            attenuation = 1.0

        if light_dir is None:
            continue

        # 🚨 분리한 헬퍼 함수를 사용하여 코드 가독성 극대화!
        diff_factor = calc_lambert_factor(world_normal, light_dir)
        spec_factor = calc_phong_factor(world_normal, light_dir, view_dir)

        # 빛의 강도와 색상 적용하여 누적
        total_diffuse_r += diff_factor * attenuation * light.intensity * (light.color.r / 255.0)
        total_diffuse_g += diff_factor * attenuation * light.intensity * (light.color.g / 255.0)
        total_diffuse_b += diff_factor * attenuation * light.intensity * (light.color.b / 255.0)
        total_specular += spec_factor * attenuation * light.intensity

    # 5. 최종 픽셀 색상 합성 (Ambient + Diffuse + Specular)
    ambient_r = base_color.r * self.ambient_light
    ambient_g = base_color.g * self.ambient_light
    ambient_b = base_color.b * self.ambient_light

    final_r = ambient_r + (base_color.r * total_diffuse_r)
    final_g = ambient_g + (base_color.g * total_diffuse_g)
    final_b = ambient_b + (base_color.b * total_diffuse_b)

    spec_map_intensity = sp_color.r / 255.0
    final_r += (255.0 * total_specular * spec_map_intensity)
    final_g += (255.0 * total_specular * spec_map_intensity)
    final_b += (255.0 * total_specular * spec_map_intensity)

    final_r = max(0, min(255, int(final_r)))
    final_g = max(0, min(255, int(final_g)))
    final_b = max(0, min(255, int(final_b)))

    return (final_r, final_g, final_b)

  def clear(self):
    #매 프레임 렌더링마다 캔버스와 z버퍼 클리어
    self.frame_buffer.fill(0) #검은색으로 초기화
    self.z_buffer.fill(float('inf')) #z버퍼 초기화

  def render_mesh(self, model, diffuse_map, normal_map, specular_map, world_matrix = None, object_alpha = 1.0):
    # MVP 행렬 생성
    # 추가: 월드 매트릭스 추가
    model_matrix = world_matrix if world_matrix else Matrix4()
    view_matrix = self.camera.get_view_matrix()

    project_matrix = Matrix4()
    aspect_ratio = self.width / self.height
    project_matrix.project_matrix(45, aspect_ratio, 0.1, 100)


    matrix_VM = view_matrix.mul_matrix(model_matrix)

    #알파블렌딩 테스트 (투명인지 불투명인지)(26.06.06)
    is_transparent = object_alpha < 1.0

    #각 삼각 폴리곤에서 연산 과정
    for triangle in tqdm(model.triangles, desc="메쉬", unit="tri"):
      vA, vB, vC = triangle

      view_A = matrix_VM.mul_vector(vA.position)
      view_B = matrix_VM.mul_vector(vB.position)
      view_C = matrix_VM.mul_vector(vC.position)

      # ===== [백페이스 컬링] =====
      # 두 변을 외적한 법선벡터
      line1 = view_B.minus(view_A)
      line2 = view_C.minus(view_A)
      face_normal = line1.cross(line2).normalize()

      # 카메라에서 삼각형을 향하는 시선 벡터
      camera_ray = view_A.normalize()

      # 시선 벡터와 면의 법선의 내적이 0이면 뒷면 = 계산 필요 x
      if face_normal.dot(camera_ray) >= 0:
          continue

      # ====  [노멀 매핑] =====
      # 3d 공간에서 두변의 길이 변화
      edge1 = vB.position.minus(vA.position)
      edge2 = vC.position.minus(vA.position)

      # 2d 공간에서 두변의 길이 변화
      deltaU1 = vB.uv.x - vA.uv.x
      deltaV1 = vB.uv.y - vA.uv.y
      deltaU2 = vC.uv.x - vA.uv.x
      deltaV2 = vC.uv.y - vA.uv.y

      # determinant 구하기
      det = (deltaU1 * deltaV2 - deltaU2 * deltaV1)
      if det == 0:
        det = 0.0001
      inv_det = 1.0 / det

      # 탄젠트 벡터 계산
      tanx = inv_det * (deltaV2 * edge1.x - deltaV1 * edge2.x)
      tany = inv_det * (deltaV2 * edge1.y - deltaV1 * edge2.y)
      tanz = inv_det * (deltaV2 * edge1.z - deltaV1 * edge2.z)
      tangent_vector = Vector3(
          matrix_VM.matrix[0][0]*tanx + matrix_VM.matrix[0][1]*tany + matrix_VM.matrix[0][2]*tanz,
          matrix_VM.matrix[1][0]*tanx + matrix_VM.matrix[1][1]*tany + matrix_VM.matrix[1][2]*tanz,
          matrix_VM.matrix[2][0]*tanx + matrix_VM.matrix[2][1]*tany + matrix_VM.matrix[2][2]*tanz,
      ).normalize()

      #==== [클리핑] ====
      # 0.1보다 작으면 바로 눈앞이거나 뒤에 있음 = 꼭지점 중 하나라도 포함된다면 제거 대상
      NEAR_CLIP = 0.1
      if view_A.z < NEAR_CLIP or view_B.z < NEAR_CLIP or view_C.z < NEAR_CLIP:
        continue

      #클리핑 이후에 P 행렬(원근감)을 곱해서 최종 ndc_pos로 전환
      ndc_A = project_matrix.mul_vector(view_A)
      ndc_B = project_matrix.mul_vector(view_B)
      ndc_C = project_matrix.mul_vector(view_C)

      #실제 화면에 맞춰 조정
      pixel_A = pixel_pos(ndc_A, self.width, self.height)
      pixel_B = pixel_pos(ndc_B, self.width, self.height)
      pixel_C = pixel_pos(ndc_C, self.width, self.height)

      # 바운딩 박스 (화면 전체 500x500을 다 돌지 않고, 삼각형이 있는 최소한의 사각형만 탐색)
      min_x = max(0, min(pixel_A.x, pixel_B.x, pixel_C.x))
      max_x = min(self.width - 1, max(pixel_A.x, pixel_B.x, pixel_C.x))
      min_y = max(0, min(pixel_A.y, pixel_B.y, pixel_C.y))
      max_y = min(self.height - 1, max(pixel_A.y, pixel_B.y, pixel_C.y))


      # ==== 래스터화 및 깊이 테스트 ====
      for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # 이전에 만드신 무게중심 보간 함수 호출
            alpha, beta, gamma = get_bycentric(pixel_A, pixel_B, pixel_C, Vector2(x, y))
            # 픽셀이 삼각형 내부에 있다면
            if alpha >= 0 and beta >= 0 and gamma >= 0:
              # 현재 픽셀의 깊이(Z) 보간
              current_z = alpha * pixel_A.z + beta * pixel_B.z + gamma * pixel_C.z

              # [Z-버퍼 테스트]
              if current_z < self.z_buffer[y][x]:
                #픽셀 단위 UV 보간
                current_u = alpha * vA.uv.x + beta * vB.uv.x + gamma * vC.uv.x
                current_v = alpha * vA.uv.y + beta * vB.uv.y + gamma * vC.uv.y

                #동적 조명 및 시선 방향 계산을 위한 3d 좌표 보간
                interp_pos = Vector3(
                    alpha * view_A.x + beta * view_B.x + gamma * view_C.x,
                    alpha * view_A.y + beta * view_B.y + gamma * view_C.y,
                    alpha * view_A.z + beta * view_B.z + gamma * view_C.z
                )

                #뷰 공간에서의 빛 위치 조정
                view_light = view_matrix.mul_vector(self.light_pos)
                light_vector = view_light.minus(interp_pos)
                light_distance = light_vector.magnitude()
                attenuation =  1.0 / (1.0 / 0.1 * light_distance + 0.05 *(light_distance*light_distance))
                light_dir = light_vector.normalize()

                #카메라는 (0,0,0)에 있으므로 시선은 (0 - 보간 위치)
                view_dir = Vector3().minus(interp_pos).normalize()
                new_color = self.fragment_shader(
                current_u, current_v, face_normal, tangent_vector, interp_pos,
                view_dir, diffuse_map, normal_map, specular_map
                )
                #추가: 불투명 물체만 z_버퍼 적용(26.06.06)
                if not is_transparent:
                  self.z_buffer[y][x] = current_z
                  #프레임 버퍼에 값을 기록
                  self.frame_buffer[y][x] = new_color

                else:
                  #배경색 가져오기
                  bg_color = self.frame_buffer[y][x]
                  self.frame_buffer[y][x] = (
                    #블렌딩 공식: (새 색상 * 알파) + (배경색 * (1 - 알파))
                    int(new_color[0] * object_alpha + bg_color[0] * (1 - object_alpha)),
                    int(new_color[1] * object_alpha + bg_color[1] * (1 - object_alpha)),
                    int(new_color[2] * object_alpha + bg_color[2] * (1 - object_alpha)),
                  )

  #프레임 버퍼의 데이터를 PIL 이미지로 변환
  def show(self):
    return Image.fromarray(self.frame_buffer, 'RGB')

  #추가: 스카이박스를 월드 매트릭스에 적용(26.06.07)
  def render_skybox(self, model, diffuse):
    sky_view = Matrix4()
    sky_view.skybox_view_matrix(self.camera.eye, self.camera.target, self.camera.true_up)

    sky_project = Matrix4()
    aspect_ratio = self.width / self.height
    sky_project.project_matrix(45, aspect_ratio, 0.1, 100)

    matrix_VM = sky_view.mul_matrix(Matrix4())

    for triangle in tqdm(model.triangles, desc="스카이박스", unit="tri"):
      vA, vB, vC = triangle

      #스카이박스는 안에서 보기 때문에 백페이스 컬링을 반전(이미 자체적인 경우도 있음)

      line1 = vB.position.minus(vA.position)
      line2 = vC.position.minus(vA.position)
      face_normal = line1.cross(line2).normalize()

      #camera_ray = vA.position.minus(self.camera.eye).normalize()
      camera_ray = vA.position.normalize()

      view_A = matrix_VM.mul_vector(vA.position)
      view_B = matrix_VM.mul_vector(vB.position)
      view_C = matrix_VM.mul_vector(vC.position)

      if view_A.z <= 0.1 or view_B.z <= 0.1 or view_C.z <= 0.1:
        continue

      ndc_A = sky_project.mul_vector(view_A)
      ndc_B = sky_project.mul_vector(view_B)
      ndc_C = sky_project.mul_vector(view_C)

      pixel_A = pixel_pos(ndc_A, self.width, self.height)
      pixel_B = pixel_pos(ndc_B, self.width, self.height)
      pixel_C = pixel_pos(ndc_C, self.width, self.height)

      min_x = max(0, min(pixel_A.x, pixel_B.x, pixel_C.x))
      max_x = min(self.width - 1, max(pixel_A.x, pixel_B.x, pixel_C.x))
      min_y = max(0, min(pixel_A.y, pixel_B.y, pixel_C.y))
      max_y = min(self.height - 1, max(pixel_A.y, pixel_B.y, pixel_C.y))

      for y in range(min_y,max_y + 1):
        for x in range(min_x, max_x + 1):
          alpha, beta, gamma = get_bycentric(pixel_A, pixel_B, pixel_C, Vector2(x, y))

          if alpha >= 0 and beta >= 0 and gamma >= 0:
            # 1. 뷰 공간의 Z값을 이용해 1/Z 보간 (w 대신 사용)
            # 0으로 나누는 것을 방지하기 위해 아주 작은 값을 더해주는 것도 좋습니다.
            inv_z = alpha * (1.0 / view_A.z) + beta * (1.0 / view_B.z) + gamma * (1.0 / view_C.z)

            # 2. UV 좌표 원근 보정
            current_u = (alpha * (vA.uv.x / view_A.z) + beta * (vB.uv.x / view_B.z) + gamma * (vC.uv.x / view_C.z)) / inv_z
            current_v = (alpha * (vA.uv.y / view_A.z) + beta * (vB.uv.y / view_B.z) + gamma * (vC.uv.y / view_C.z)) / inv_z

            # (선택 사항) 만약 Z-버퍼 처리가 필요하다면 보간된 깊이값을 복원하여 사용할 수 있습니다.
            # current_depth = 1.0 / inv_z

            self.frame_buffer[y][x] = diffuse.get_color(current_u, current_v).to_tuple()
