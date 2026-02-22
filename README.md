# Military Service Coding Project
> 군 복무 기간을 활용한 테크니컬 아티스트(TA) 및 그래픽스 엔진 개발자 로드맵 이행 저장소

## 프로젝트 개요
본 프로젝트는 상용 게임 엔진(Unreal, Unity)의 내부 작동 원리를 깊이 있게 이해하기 위해, 외부 라이브러리 없이 파이썬만으로 **3D 그래픽스 수학 엔진**을 구축하는 것을 목표로 합니다.

## 핵심 구현 사항
- **Vector3 Class**: 3D 공간에서의 위치와 방향 제어 (내적, 외적, 정규화 등)
- **Matrix4x4 Class**: TRS(Translation, Rotation, Scale) 변환 행렬 구현
- **Rendering Pipeline**: MVP(Model-View-Projection) 행렬 연산 및 짐벌 락(Gimbal Lock) 해결 (진행 중)

## 학습 로드맵
- [x] Phase 1: 3D 벡터 및 기초 행렬 엔진 구축
- [ ] Phase 2: 쉐이더 수학 (조명 및 카툰 렌더링)
- [ ] Phase 3: C++ 전환 및 메모리 관리 (포인터)
- [ ] Phase 4: 자료구조 및 알고리즘 (C++)

---
Contact: https://velog.io/@paulko100/posts
