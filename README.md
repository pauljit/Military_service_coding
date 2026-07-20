# 
> 테크니컬 아티스트(TA) 및 그래픽스 엔진 개발자 로드맵 이행 저장소

## 프로젝트 개요
본 프로젝트는 상용 게임 엔진(Unreal, Unity)의 내부 작동 원리를 깊이 있게 이해하기 위해, 외부 라이브러리 없이 파이썬만으로 **3D 그래픽스 수학 엔진**을 구축하는 것을 목표로 함

## 핵심 구현 사항
- **Vector3 Class**: 3D 공간에서의 위치와 방향 제어 (내적, 외적, 정규화 등)
- **Matrix4x4 Class**: TRS(Translation, Rotation, Scale) 변환 행렬 구현
- **Rendering Pipeline**: MVP(Model-View-Projection) 행렬 연산
- **Camera class**: 월드 내 카메라 배치 및 이동
- **Vertex&Texture class**: uv좌표, 버텍스 위치 읽기, 노멀 텍스쳐, 스펙큘러 텍스쳐 등
- **Show**: 화면 내 실제 구현, 조명, 텍스쳐 매핑에 의한 최종 색상 구현 
<img width="1091" height="564" alt="image" src="https://github.com/user-attachments/assets/2d5fc21d-c10a-4167-9194-85802b0a41ec" />

---
Contact: https://velog.io/@paulko100/posts
