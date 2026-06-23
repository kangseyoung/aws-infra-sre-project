# 아키텍처 설명 초안

## 개요
이번 프로젝트는 정적 웹 페이지 하나를 AWS 인프라 위에 올리면서, 네트워크부터 로드밸런서, 컴퓨트, 모니터링까지 이어지는 흐름을 직접 이해하는 것을 목표로 합니다.

기본 구조는 다음과 같습니다.

`사용자 -> ALB -> Target Group -> EC2 -> Docker -> Nginx -> 정적 페이지`

여기에 CloudWatch를 연결해 상태를 관찰하고, 장애 상황에서 무엇을 먼저 확인해야 하는지도 함께 정리합니다.

## 핵심 구성 요소
### 네트워크 계층
- VPC를 프로젝트의 기본 네트워크 경계로 사용
- ALB가 위치할 Public Subnet 구성
- 필요 시 Private Subnet을 추가해 구조 확장 가능
- Route Table로 인터넷 및 내부 통신 경로 관리
- Internet Gateway로 외부 접근 허용
- NAT Gateway는 비용과 필요성을 고려해 선택적으로 사용

### 컴퓨트 계층
- EC2 인스턴스를 웹 서버 호스트로 사용
- EC2 내부에 Docker 설치
- Docker 컨테이너로 Nginx 실행
- Nginx가 테스트용 정적 HTML 페이지 제공

### 트래픽 계층
- ALB가 외부 사용자의 진입점 역할 수행
- Target Group이 EC2를 백엔드 대상으로 관리
- Health Check를 통해 백엔드 정상 여부 판단

### 보안 계층
- ALB와 EC2에 서로 다른 Security Group 적용
- 필요한 경우 EC2에 IAM Role 부여
- 포트는 실제 필요한 범위만 개방

### 관측성 계층
- CloudWatch Metrics로 EC2, ALB 상태 확인
- CloudWatch Logs로 로그 수집 경로 정리
- CloudWatch Alarm으로 장애 조건 알림

## 요청 흐름 설명
1. 사용자가 ALB DNS 주소로 접속합니다.
2. ALB가 80 포트에서 요청을 받습니다.
3. ALB는 Target Group을 통해 EC2로 요청을 전달합니다.
4. EC2 내부 Docker 컨테이너에서 Nginx가 동작합니다.
5. Nginx가 정적 테스트 페이지를 반환합니다.
6. CloudWatch는 메트릭과 알람을 통해 상태를 관찰합니다.

## 설계 시 고려사항
- 첫 버전은 수동 구축이 가능한 수준으로 단순하게 시작합니다.
- Private Subnet과 NAT Gateway는 학습 목표와 예산을 보고 선택합니다.
- 구조를 복잡하게 만드는 것보다, 왜 이런 구성을 택했는지 설명 가능한 것이 더 중요합니다.
- 모니터링과 비용 정리는 아키텍처 바깥의 작업이 아니라 운영 설계의 일부로 봅니다.

## 확장 아이디어
- HTTPS + ACM 적용
- Private Subnet 확장
- SSM 기반 접속 구조
- Auto Scaling Group 실험
- Terraform 리소스 확장
- `diagrams/` 폴더에 아키텍처 다이어그램 추가

