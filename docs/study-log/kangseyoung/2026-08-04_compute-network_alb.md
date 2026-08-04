# 2026-08-04 공부기록 - 강세영

## 1. 담당 파트

Compute + Network

## 2. 오늘 공부한 개념

- EC2 Instance Connect Endpoint를 사용한 Private IPv4 SSH 접속
- Security Group 참조 규칙을 이용한 EICE에서 EC2로의 SSH 22 허용
- Docker 컨테이너의 host port와 container port 매핑
- Target Group 생성과 EC2 Instance target 등록
- Internet-facing ALB, HTTP 80 Listener, Target Group 연결
- ALB DNS를 통한 애플리케이션 health check 검증

## 3. 내가 이해한 내용

- EC2에 Public IPv4가 없어도 EC2 Instance Connect Endpoint를 사용하면 Private IPv4로 SSH 접속할 수 있다.
- EICE에서 EC2로 SSH 접속하려면 EC2 Security Group에 EICE Security Group에서 오는 TCP 22 규칙이 필요하다.
- MiniPEP 컨테이너는 EC2 Host Port `80`을 Docker Container Port `8000`으로 연결해서 실행한다.
- Target Group은 EC2의 Host Port `80`으로 트래픽을 전달하고, EC2 내부 Docker가 MiniPEP `8000` 포트로 연결한다.
- ALB HTTP 80 Listener의 default action이 Target Group으로 연결되어야 외부 사용자의 요청이 앱까지 도달한다.

## 4. GPT에게 물어본 질문

- EICE와 Security Group ID를 어떻게 구분하는지 질문했다.
- EC2 Instance Connect Endpoint로 Private IPv4 SSH 접속할 때 필요한 Security Group 규칙을 질문했다.
- ALB에서 404가 나왔을 때 요청이 어디까지 도달한 것으로 볼 수 있는지 질문했다.
- `/healty`와 `/health`처럼 경로가 다를 때 health check 결과가 달라지는 이유를 질문했다.

## 5. 새로 알게 된 점

- EICE ID는 `eice-`로 시작하고 SG ID는 `sg-`로 시작한다.
- EC2 SG에는 EICE SG에서 오는 SSH 22를 허용해야 한다.
- 404라도 Uvicorn 응답이 왔다면 ALB부터 앱까지 요청이 도달한 것이다.
- 정확한 경로 `/health`가 중요하다.

## 6. Must / Optional 후보

### Must 후보

- EC2 Instance Connect Endpoint를 통한 Private IPv4 SSH 접속 절차 기록
- MiniPEP Docker 컨테이너 상태 확인
- EC2 localhost `/health` HTTP 200 확인
- Target Group 생성 및 EC2 target 등록
- Internet-facing ALB 생성
- HTTP 80 Listener와 Target Group 연결
- ALB DNS `/health` HTTP 200 확인

### Optional 후보

- ALB 및 Target Group의 ARN과 Target Health 상태를 AWS CLI로 재확인
- ALB와 EC2 CloudWatch 지표 확인
- 장애 주입 시나리오 추가
- Terraform import 또는 재현 방식 정리

## 7. 아직 헷갈리는 부분

- Target Health `healthy` 상태를 어떤 증거 화면이나 CLI 출력으로 남기는 것이 가장 좋은지 정리해야 한다.
- Console로 만든 ALB와 Target Group을 Terraform에 반영할 때 import할지, 별도 재생성할지 결정이 필요하다.
- CloudWatch에서 ALB와 EC2 지표를 어떤 기준으로 확인해야 하는지 추가 학습이 필요하다.

## 8. 내일 할 일

- Target Health healthy 상태 증거 저장
- ALB 및 EC2 CloudWatch 지표 확인
- 장애 주입 및 Runbook 검증
- Terraform 반영 및 전체 재현
- 비용 정리

## 9. 참고한 자료

- AWS Console에서 확인한 ALB, Target Group, EC2, EICE 정보
- EC2 내부 `docker ps` 확인 결과
- EC2 localhost `/health` HTTP 200 확인 결과
- ALB DNS `/health` HTTP 200 확인 결과
