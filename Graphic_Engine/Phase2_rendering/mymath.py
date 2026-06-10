
import math
import copy

class Vector2:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

  #벡터끼리 더하기
  def add(self, other_vector):
    return Vector2(self.x + other_vector.x, self.y + other_vector.y)

  #벡터끼리 빼기
  def minus(self, other_vector):
    return Vector2(self.x - other_vector.x, self.y - other_vector.y)

  #벡터의 곱셈
  def multiply(self, factor):
    return Vector2(self.x *factor, self.y * factor)

  #벡터의 길이
  def magnitude(self):
    return math.sqrt((self.x ** 2) + (self.y ** 2))

  #벡터 정보 출력
  def status(self):
    print(f"x: {self.x}, y: {self.y}")

  #벡터 정규화 (방향을 알기 위한 용도)
  def normalize(self):
    mag = self.magnitude()
    if mag == 0:
      return Vector2(0,0)
    else:
      return Vector2(self.x/mag, self.y/mag)

  #벡터 내적 (+-0의 상태에 따라 방향의 일치성 확인, 양에 따라 빛의 반사율 확인)
  def dot(self, other_vector):
    return ((self.x*other_vector.x) + (self.y * other_vector.y))

  #벡터 외적
  def cross(self, other_vector):
    return (self.x * other_vector.y) - (self.y * other_vector.x)

  #출력
  def __repr__(self):
    return f"x: {self.x:.2f}, y: {self.y:.2f}"



class Vector3:
  # 1. 생성자 (z축 추가)
  def __init__(self, x=0, y=0, z=0):
    self.x = x
    self.y = y
    self.z = z

  # 2. 덧셈 (z축 끼리도 더해주세요)
  def add(self, other):
    return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

  # 3. 뺄셈
  def minus(self, other):
    return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

  # 4. 스칼라 곱셈
  def multiply(self, scalar):
    return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

  # 5. 길이 구하기
  def magnitude(self):
    return math.sqrt(self.x ** 2 + self.y ** 2 + self.z **2)

  # 6. 정규화 (방향 벡터로 만들기)
  def normalize(self):
    mag = self.magnitude()
    if mag == 0:
      return Vector3(0, 0, 0)
    else:
      return Vector3(self.x / mag, self.y / mag, self.z / mag)

  # 7. 내적 (조명 계산의 핵심)(인식 범위)
  def dot(self, other):
    return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

  # 8. 벡터 좌표 출력 (:.2f는 소수점 2자리까지만 출력한다는 뜻)
  def status(self):
    print(f"Vector3(x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f})")

  #  9. 위치 벡터끼리의 거리 (서로 뺀 값의 길이)
  def distance(self, other):
    return self.minus(other).magnitude()

  #  10. 벡터끼리의 각도 (서로 정규화한 벡터의 내적의 아크코사인)(적이 인식 각도 확인 가능)
  def angle(self, other):
     dot_product = self.normalize().dot(other.normalize())
     # 1.0001등의 값을 내어 acos가 오류를 내지 않기 위해 -1.0 ~ 1.0으로 바꾸기
     dot_product = max(-1.0, min(1.0, dot_product))
     radian = math.acos(dot_product)
     return math.degrees(radian)

  # 11. 외적 (두 벡터의 수직인 법선 벡터)(삼각 폴리곤의 수직을 구하여 빛 반사 및 culling 최적화)
  def cross(self, other):
    normal_vector = Vector3()
    normal_vector.x = self.y * other.z - self.z * other.y
    normal_vector.y = self.z * other.x - self.x * other.z
    normal_vector.z = self.x * other.y - self.y * other.x
    return normal_vector

  #출력
  def __repr__(self):
    return f"x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}"



# 3D 공간에서 TRS(Translation, Rotation, Scale)을 조정하는 4*4 매트릭스
class Matrix4:
  # 1. 생성자 (단위 행렬(identity matrix))
  def __init__(self, matrix = None):

    self.matrix = [
      [1.0, 0.0, 0.0, 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
      ]

  # 2. 행렬 출력 (소수점 두자리수까지)
  def status(self):
    for row in self.matrix:
      print(f"{row[0]:.2f},{row[1]:.2f},{row[2]:.2f},{row[3]:.2f}")
    print("--"*10)

  # 3. 스케일 조절 (첫 세 행의 각 x, y, z 변형)
  def scale(self,scale_x,scale_y,scale_z):
    result = Matrix4()
    result.matrix[0][0] = scale_x
    result.matrix[1][1] = scale_y
    result.matrix[2][2] = scale_z
    return result

  # 4, 13. 행렬을 벡터에 적용 ((New) 각 MVP 행렬을 곱해서 모니터 상에 물체가 어느 픽셀에 표현되는지 표시)
  def mul_vector(self, vector):
    # w는 3차원 벡터를 4*4 행렬에서 구현하기 위해 가상으로 만든 개념, 벡터에서 이동값을 담당
    # w가 z의 깊이를 담당하여 원근감 표현을 위해 각 좌표를 나눔
    w = (self.matrix[3][0] * vector.x +
         self.matrix[3][1] * vector.y +
         self.matrix[3][2] * vector.z +
         self.matrix[3][3] * 1.0
         )
    #zero division을 회피 (간단한 클리핑)
    if w == 0:
      w = 0.000001
    new_x = (self.matrix[0][0] * vector.x + self.matrix[0][1] * vector.y + self.matrix[0][2] * vector.z + self.matrix[0][3] * 1.0) / w
    new_y = (self.matrix[1][0] * vector.x + self.matrix[1][1] * vector.y + self.matrix[1][2] * vector.z + self.matrix[1][3] * 1.0) / w
    new_z = (self.matrix[2][0] * vector.x + self.matrix[2][1] * vector.y + self.matrix[2][2] * vector.z + self.matrix[2][3] * 1.0) / w
    return Vector3(new_x, new_y, new_z)

  # 5. 이동 행렬 (mul_vector의 w의 값을 이용하여 위치 벡터를 이동)
  def translate(self, translate_x, translate_y, translate_z):
    # 이러면 기존의 0이었던 4번째 열의 값이 변형되어 x,y,z값이 바뀜
    result = Matrix4()
    result.matrix[0][3] = translate_x
    result.matrix[1][3] = translate_y
    result.matrix[2][3] = translate_z
    return result

  # 6. z축 회전 행렬 (x, y 행만 변형)
  def rotate_z(self, degree):
    rad = math.radians(degree)
    cos = math.cos(rad)
    sin = math.sin(rad)
    result = Matrix4()
    result.matrix[0][0] = cos
    result.matrix[0][1] = -sin
    result.matrix[1][0] = sin
    result.matrix[1][1] = cos
    return result

  #7. y축 회전 행렬 (x, z 행만 변형)
  def rotate_y(self, degree):
    rad = math.radians(degree)
    cos = math.cos(rad)
    sin = math.sin(rad)
    result = Matrix4()
    result.matrix[0][0] = cos
    result.matrix[0][2] = sin
    result.matrix[2][0] = -sin
    result.matrix[2][2] = cos
    return result

  #8. x축 회전 행렬 (y, z 행만 변형)
  def rotate_x(self, degree):
    rad = math.radians(degree)
    cos = math.cos(rad)
    sin = math.sin(rad)
    result = Matrix4()
    result.matrix[1][1] = cos
    result.matrix[1][2] = -sin
    result.matrix[2][1] = sin
    result.matrix[2][2] = cos
    return result

  #9. 행렬 곱 (수많은 버텍스에 대한 TRS를 동시에 하기 위함(최적화))
  def mul_matrix(self, other):
    result = Matrix4()
    # i = 가로줄(4), j = 세로줄(4)
    for i in range(4):
      for j in range(4):
        # 결과 행렬의 [i][j]는 행렬의 i번째 줄과 다른 행렬의 j번째 줄의 요소끼리의 곱을 더한 값
        result.matrix[i][j] = (
        self.matrix[i][0] * other.matrix[0][j]
        + self.matrix[i][1] * other.matrix[1][j]
        + self.matrix[i][2] * other.matrix[2][j]
        + self.matrix[i][3] * other.matrix[3][j])
    return result

  #10. 오일러 회전 엔진 (약간의 부작용(짐벌락)이 있는 xyz 통합식 회전)
  def euler_rotation(self, x_ang, y_ang, z_ang):
    mat_x = Matrix4().rotate_x(x_ang)
    mat_y = Matrix4().rotate_y(y_ang)
    mat_z = Matrix4().rotate_z(z_ang)
    #X*Y*Z 순서로 회전 행렬들의 곱셈 반환 (회전 순서에 따라 변화가 다름, 엔진마다 순서가 다름)
    mat_yz = mat_z.mul_matrix(mat_y)
    mat_xyz = mat_yz.mul_matrix(mat_x)
    self.matrix = mat_xyz.matrix

  # 11. View 행렬 (카메라의 방향을 확인)
  def view_matrix(self, eye, target, world_yaxis = Vector3(0,1,0)):
    #eye = 월드내 카메라 위치, target = 월드내 목표 위치, world_yaxis = 월드 y축(보통 (0,1,0) 벡터)
    forward = target.minus(eye)            #카메라 정면 방향(z축)
    forward = forward.normalize()
    right = world_yaxis.cross(forward)     #카메라 우측 방향(x축)
    right = right.normalize()
    camera_yaxis = forward.cross(right)    #카메라 상단 방향(y축)
    camera_yaxis = camera_yaxis.normalize()
    #view 행렬 조립
    #카메라는 원점에 고정되어 있기 때문에 세상이 카메라로 와야 함(월드내 카메라 위치를 기준으로 내적 후 카메라 방향으로 다가옴)
    self.matrix = [
        [right.x, right.y, right.z, -right.dot(eye)],
        [camera_yaxis.x, camera_yaxis.y, camera_yaxis.z, -camera_yaxis.dot(eye)],
        [forward.x, forward.y, forward.z, -forward.dot(eye)],
        [0, 0, 0, 1],
    ]

  #12. Projection 행렬
  def project_matrix(self, fov_degree, aspect_ratio, near, far):
    # fov_degree = 시야각, x와 y의 스케일 조정(S), 시야각이 클수록 x, y는 작아짐
    fov_rad = math.radians(fov_degree)
    S = 1.0 / math.tan(fov_rad / 2.0)
    # near, far로 z의 최대 거리, 최소거리 조정
    z_range = far - near
    # 투영 행렬 조립
    self.matrix = [
        [S/aspect_ratio, 0, 0, 0],                # X 크기 (스케일 / 모니터 비율만큼 키움(모니터는 보통 옆으로 길쭉하니까))
        [0, S, 0, 0],                             # Y 크기 (스케일만큼 키움)
        [0,0, far/z_range, -(far*near)/z_range],  # Z-buffer(최소거리와 최대거리 설정)
        [0,0,1,0]                                 # 1이 z의 크기를 복사 후 조정
    ]

  # 스카이박스 (26.06.05)
  def skybox_view_matrix(self, eye, target, world_yaxis = Vector3(0,1,0)):
    forward = target.minus(eye)            #카메라 정면 방향(z축)
    forward = forward.normalize()
    right = world_yaxis.cross(forward)     #카메라 우측 방향(x축)
    right = right.normalize()
    camera_yaxis = forward.cross(right)    #카메라 상단 방향(y축)
    camera_yaxis = camera_yaxis.normalize()
    self.matrix = [
        [right.x, right.y, right.z, 0],
        [camera_yaxis.x, camera_yaxis.y, camera_yaxis.z, 0],
        [forward.x, forward.y, forward.z, 0],
        [0, 0, 0, 1]
        ]

#Quaternion 클래스
class Quaternion:
  # q = w + xi + yj + zk
  def __init__(self, w = 1, x = 0, y = 0, z = 0):
    self.w = w
    self.x = x
    self.y = y
    self.z = z

  # 길이 (sqrt(w^2 + x^2 + y^2+ z^2)
  def magnitude(self):
    mag = math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)
    return mag

  #정규화 (단위화해야 일그러지지 않음)
  def normalize(self):
    mag = self.magnitude()
    if mag == 0:
      return Quaternion()
    else:
      return Quaternion(self.w/mag, self.x/mag, self.y/mag, self.z/mag)

  #축과 각도를 통한 쿼터니언 생성(입력된 각도의 절반만을 사용)(26.06.04)
  @classmethod
  def axis_angle(self, axis, degree):
    rad = math.radians(degree)
    axis = axis.normalize()
    w = math.cos(rad/2)
    x = axis.x * math.sin(rad/2)
    y = axis.y * math.sin(rad/2)
    z = axis.z * math.sin(rad/2)
    return Quaternion(w,x,y,z)

  #쿼터니언끼리의 곱을 통한 최종회전상태(26.06.04)
  def __mul__(self, other):
    final_w = (self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z)
    final_x = (self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y)
    final_y = (self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x)
    final_z = (self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w)
    return Quaternion(final_w, final_x, final_y, final_z)

  def __add__(self, other):
    return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(self, other):
    return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

  def scalar(self, scalar):
    return Quaternion(self.w * scalar, self.x * scalar, self.y * scalar, self.z * scalar)

  #두 쿼터니언 사이의 각을 알기 위한 내적 연산 (쿼터니언의 내적 = cos(theta))(26.06.04)
  def dot_product(self, other):
    dot = self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z
    return dot

  #등속도 구형 선형 보간(26.06.04)
  def slerp(self, other, t):
    dot = self.dot_product(other)
    target_quat = Quaternion(other.w, other.x, other.y, other.z)

    # 내적이 음수일 경우 먼 방향으로 움직인다는 뜻이므로 양수로 전환
    if dot < 0:
      target_quat = Quaternion(-other.w, -other.x, -other.y, -other.z)
      dot = -dot

    theta = math.acos(dot)

    # 0나누기 방지 (내적 값이 1에 가까우면 단순 lerp)
    if dot > 0.9995:
      lerp = self.scalar(1 - t) + target_quat.scalar(t)
      return lerp.normalize()

    else:
      weight1 = self.scalar((math.sin(theta * (1-t))) / math.sin(theta))
      weight2 = target_quat.scalar((math.sin(theta * t)) / math.sin(theta))
      return weight1 + weight2

  def to_matrix(self):
    mat = Matrix4()
    mat.matrix = [
        [1 - (2 * self.y ** 2) - (2 * self.z ** 2), (2 * self.x * self.y) - (2 * self.w * self.z), (2 * self.x * self.z) + (2 * self.w * self.y), 0],
        [(2 * self.x * self.y) + (2 * self.w * self.z), 1 - (2 * self.x ** 2) - (2 * self.z ** 2),  (2 * self.y * self.z) - (2 * self.w * self.x), 0],
        [(2 * self.x * self.z) - (2 * self.w * self.y),  (2 * self.y * self.z) + (2 * self.w * self.x), 1 - (2 * self.x ** 2) - (2 * self.y ** 2), 0],
        [0, 0, 0, 1]
    ]
    return mat
