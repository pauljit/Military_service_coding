from mymath import *

#노드 (부모 - 자식으로 종속된 클래스)(26.06.04)
class Node:
  def __init__(self, model= None, object_alpha = 1.0, light = None):
    self.local_position = Vector3()
    self.local_rotation = Quaternion()
    self.local_scale = Vector3(1,1,1)
    self.local_matrix = Matrix4()
    self.world_matrix = Matrix4()
    self.parent = None
    self.children = []
    #추가: 불러온 모델을 월드값에 전시(26.06.06)
    self.model = model
    self.object_alpha = object_alpha
    #추가: 조명도 노드로 추가할 수 있도록 light 속성 추가(26.06.20)
    self.light = light


  #종속되는 자식 계층 생성
  def add_child(self, child):
    child.parent = self
    self.children.append(child)

  # TRS행렬 적용 및 부모행렬에 대한 영향 반영(26.06.04)
  def update_transform(self):
    t_mat = self.local_matrix.translate(self.local_position.x, self.local_position.y, self.local_position.z)
    r_mat = self.local_rotation.to_matrix()
    s_mat = Matrix4().scale(self.local_scale.x, self.local_scale.y, self.local_scale.z)

    #T * R * S 순서로 행렬 곱
    self.local_matrix = t_mat.mul_matrix(r_mat).mul_matrix(s_mat)
    #부모 노드가 있을 경우 로컬행렬에 부모행렬의 영향을 반영함
    if self.parent:
      self.world_matrix = self.parent.world_matrix.mul_matrix(self.local_matrix)
    #부모 노드가 없을 경우 로컬행렬이 월드행렬임
    else:
      self.world_matrix = self.local_matrix
    #자기의 자식 노드이 실행할 재귀함수
    for child in self.children:
      child.update_transform()

  def get_world_position(self):
    x = self.world_matrix.matrix[0][3]
    y = self.world_matrix.matrix[1][3]
    z = self.world_matrix.matrix[2][3]
    return Vector3(x, y, z)
