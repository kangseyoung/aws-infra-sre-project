# MiniPEP 컨테이너 중지로 인한 서비스 응답 실패

**담당:** Observability / Platform — 권태욱  
**환경:** `dev`  
**Region:** `ap-northeast-2`  
**검증 상태:** 실제 장애 재현 및 복구 완료

이 Runbook은 MiniPEP Docker 컨테이너가 중지되어 ALB Health Check와 서비스 요청이 실패하는 경우에 사용한다.

정상 요청 흐름:

```text
사용자
→ Internet-facing ALB:80
→ Target Group:80
→ EC2 Host:80
→ Docker Container:8000
→ MiniPEP FastAPI
```

---

## 증상

다음 중 하나 이상이 나타날 수 있다.

- ALB DNS의 `/health` 요청이 HTTP 200을 반환하지 않는다.
- ALB DNS에서 MiniPEP 메인 페이지 또는 API 요청이 실패한다.
- EC2 내부 `http://localhost/health` 요청이 실패한다.
- Docker의 `minipep` 컨테이너가 `Exited` 또는 중지 상태이다.
- Target Group의 EC2 Target이 `Unhealthy` 상태이다.
- `HealthyHostCount`가 `1`에서 `0`으로 감소한다.
- `UnHealthyHostCount`가 `0`에서 `1`로 증가한다.
- CloudWatch Dashboard에서 요청 실패 또는 Target 상태 변화가 확인된다.

현재 프로젝트는 Target이 EC2 한 대이므로 해당 Target이 `Unhealthy`가 되면 전체 서비스 요청이 실패할 수 있다.

---

## 먼저 확인할 것

아래 순서대로 확인한다.

1. ALB DNS의 `/health` 응답
2. Target Group의 Target Health와 Health Reason
3. `HealthyHostCount`와 `UnHealthyHostCount`
4. EC2 인스턴스 상태와 Status Check
5. Docker의 `minipep` 컨테이너 상태
6. Host Port `80` → Container Port `8000` 매핑
7. EC2 내부 `/health` 응답
8. MiniPEP Application Log
9. ALB와 EC2 Security Group 규칙

정상 기준:

```text
EC2: Running
EC2 Status Check: 2/2
Docker Container: Running
EC2 내부 /health: HTTP 200
ALB /health: HTTP 200
Target Health: Healthy
HealthyHostCount: 1
UnHealthyHostCount: 0
StatusCheckFailed: 0
```

---

## 확인 명령어 또는 AWS Console 위치

### 1. ALB 외부 응답 확인

```bash
ALB_DNS="aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com"

curl -i "http://${ALB_DNS}/"
curl -i "http://${ALB_DNS}/health"
curl -i "http://${ALB_DNS}/api/equipment"
curl -i "http://${ALB_DNS}/api/jobs"
```

정상 `/health` 응답:

```text
HTTP/1.1 200 OK
```

```json
{"status":"ok","service":"minipep"}
```

### 2. Target Group 상태 확인

AWS Console:

```text
EC2
→ Target Groups
→ aws-infra-sre-dev-app-tg
→ Targets
```

확인 항목:

- Registered Target: `i-07d3895c10c0706be`
- Target Port: `80`
- Health Check Protocol: HTTP
- Health Check Path: `/health`
- Success Code: `200`
- Target Health
- Target Health Reason

CloudWatch Metric:

- `HealthyHostCount`
- `UnHealthyHostCount`

### 3. EC2 상태 확인

AWS Console:

```text
EC2
→ Instances
→ i-07d3895c10c0706be
```

확인 항목:

- Instance State: `Running`
- Status Check: `2/2`
- Security Group: `sg-03a67f4bd0610147e`
- Subnet: `subnet-0da0e473f97b614fa`

CloudWatch EC2 Metric:

- `CPUUtilization`
- `NetworkIn`
- `NetworkOut`
- `StatusCheckFailed`

정상 상태에서는 `StatusCheckFailed = 0`이어야 한다.

### 4. Docker 상태 확인

EC2 Instance Connect Endpoint를 통해 EC2에 접속한다.

```text
EICE: eice-077f856f79efd6170
EC2 Private IPv4: 10.0.1.93
SSH User: ec2-user
```

Docker Compose 파일이 있는 MiniPEP 프로젝트 디렉터리에서 실행한다.

```bash
docker compose ps
docker ps -a --filter name=minipep
```

추가 확인:

```bash
docker inspect minipep --format '{{.State.Status}}'
docker inspect minipep --format '{{.State.Restarting}}'
docker inspect minipep --format '{{.RestartCount}}'
docker port minipep
```

정상 Port Mapping:

```text
Host 80 → Container 8000
```

### 5. EC2 내부 응답 확인

```bash
curl -i http://localhost/
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

### 6. Application Log 확인

```bash
docker compose logs --tail=100 minipep
docker compose logs --since=15m minipep
```

실시간 확인:

```bash
docker compose logs -f minipep
```

로그에서 확인할 내용:

- 애플리케이션 시작 오류
- 반복 재시작
- `GET /health`
- `GET /api/equipment`
- `GET /api/jobs`
- HTTP Status Code
- Stack Trace 또는 Error Message
- SQLite 경로 또는 권한 오류
- Port Binding 오류

### 7. Security Group 확인

ALB Security Group:

```text
SG: sg-053e06d50216483fe
Inbound: TCP 80
Source: 0.0.0.0/0
```

EC2 Security Group:

```text
SG: sg-03a67f4bd0610147e
Inbound: TCP 80
Source: ALB Security Group sg-053e06d50216483fe
```

장애 해결을 위해 EC2 Port `80`이나 Container Port `8000`을 `0.0.0.0/0`에 직접 개방하지 않는다.

---

## 가능한 원인

### 1. MiniPEP 컨테이너 중지

`minipep` 컨테이너가 중지되어 EC2 Host Port `80`에서 응답하지 못한다.

실제 장애 재현에서 확인된 원인이다.

### 2. 컨테이너 반복 재시작

애플리케이션 시작 오류, 잘못된 환경변수, SQLite 경로 또는 권한 문제로 컨테이너가 반복 재시작할 수 있다.

### 3. Port Mapping 오류

다음 연결이 잘못되었을 수 있다.

```text
EC2 Host 80 → Docker Container 8000
```

### 4. Health Check 설정 오류

- Health Check Path가 `/health`가 아님
- Target Port가 `80`이 아님
- Success Code가 `200`이 아님

### 5. Security Group 오류

- ALB SG에서 HTTP `80`이 허용되지 않음
- EC2 SG의 Port `80` Source가 ALB SG가 아님
- 불필요한 규칙 변경으로 정상 연결이 차단됨

### 6. 잘못된 Target 등록

Target Group에 다른 EC2가 등록되었거나 `i-07d3895c10c0706be`가 등록 해제되었을 수 있다.

### 7. EC2 상태 이상

EC2가 중지되었거나 Status Check가 실패한 경우 Docker와 MiniPEP도 정상 응답할 수 없다.

---

## 대응 방법

### 1. 장애 발생 시간과 현재 상태 기록

변경 전에 시간을 기록한다.

```bash
date
docker compose ps
curl -i http://localhost/health
curl -i "http://${ALB_DNS}/health"
```

AWS Console에서 다음 상태를 캡처한다.

- Target Health
- Target Health Reason
- `HealthyHostCount`
- `UnHealthyHostCount`
- CloudWatch Dashboard

### 2. 중지된 MiniPEP 컨테이너 시작

```bash
docker compose start minipep
```

`start`로 복구되지 않는 경우:

```bash
docker compose up -d minipep
```

이미지 또는 설정 변경 후 재생성이 필요한 경우에만 실행한다.

```bash
docker compose up -d --build minipep
```

### 3. Docker 상태와 로그 확인

```bash
docker compose ps
docker compose logs --tail=100 minipep
```

확인 사항:

- 컨테이너가 `Running` 또는 `Up` 상태
- 반복 재시작 없음
- Host `80` → Container `8000` 연결
- 애플리케이션 시작 오류 없음

### 4. EC2 내부 복구 확인

```bash
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

`/health`가 HTTP 200과 다음 응답을 반환해야 한다.

```json
{"status":"ok","service":"minipep"}
```

### 5. ALB 외부 복구 확인

```bash
curl -i "http://${ALB_DNS}/health"
curl -i "http://${ALB_DNS}/api/equipment"
curl -i "http://${ALB_DNS}/api/jobs"
```

### 6. Target Group 복구 확인

Health Check 반영에는 시간이 걸릴 수 있으므로 잠시 기다린 후 확인한다.

복구 완료 기준:

```text
Target Health: Healthy
HealthyHostCount: 1
UnHealthyHostCount: 0
```

### 7. 최종 상태 기록

```bash
date
docker compose ps
curl -i http://localhost/health
curl -i "http://${ALB_DNS}/health"
```

최종 확인 항목:

- [ ] MiniPEP Container가 Running 상태이다.
- [ ] 반복 재시작이 없다.
- [ ] Host `80` → Container `8000` 매핑이 정상이다.
- [ ] EC2 내부 `/health`가 HTTP 200이다.
- [ ] ALB `/health`가 HTTP 200이다.
- [ ] Main Page가 정상 표시된다.
- [ ] Equipment API가 정상 응답한다.
- [ ] Jobs API가 정상 응답한다.
- [ ] Target Health가 `Healthy`이다.
- [ ] `HealthyHostCount = 1`이다.
- [ ] `UnHealthyHostCount = 0`이다.
- [ ] `StatusCheckFailed = 0`이다.
- [ ] 정상 요청이 Application Log에 나타난다.
- [ ] 복구 시간과 증거 자료를 저장했다.

### 실제 검증 결과

다음 장애 흐름을 실제로 확인했다.

```text
MiniPEP Container Stop
→ EC2 Host Port 80 응답 실패
→ ALB /health 실패
→ Target Unhealthy
→ HealthyHostCount 감소
→ UnHealthyHostCount 증가
→ docker compose start minipep
→ EC2 /health HTTP 200 복구
→ ALB /health HTTP 200 복구
→ Target Healthy 복구
```

---

## 재발 방지

- Docker Compose의 `restart: unless-stopped` 설정을 유지한다.
- 배포 후 `docker compose ps`와 `/health`를 반드시 확인한다.
- Target Group의 Health Check Path를 `/health`로 유지한다.
- Target Port와 EC2 Host Port를 `80`으로 유지한다.
- Host `80` → Container `8000` Port Mapping 변경 시 팀에 공유한다.
- EC2 SG의 Port `80` Source는 ALB SG로 제한한다.
- 정상, 장애, 복구 상태의 Dashboard와 Target Health를 증거로 남긴다.
- `UnHealthyHostCount >= 1` 또는 `HealthyHostCount < 1` CloudWatch Alarm 추가를 검토한다.
- `StatusCheckFailed >= 1` CloudWatch Alarm 추가를 검토한다.
- 장애 발생 시간, 원인, 복구 명령, 복구 시간을 기록한다.
- 실습 종료 후 EC2, ALB, EICE 등 비용 발생 리소스 유지 여부를 팀과 확인한다.

### 관련 문서

```text
docs/checklists/observability-checklist.md
docs/evidence/observability/
docs/handoff/compute-network-resources.md
```

### 보안 주의사항

다음 정보는 Runbook이나 증거 자료에 기록하지 않는다.

- AWS Access Key
- AWS Secret Access Key
- Session Token
- `.pem`
- `.env`
- `terraform.tfstate`
- `.terraform/`
- SSH Private Key
