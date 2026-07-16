# Observability / Platform Must / Optional

**담당자:** 권태욱  
**파트:** Observability / Platform

> 이 문서는 `AWS Infra / SRE 14-Day Project Plan`에서 확정한 범위를 기준으로 작성한다.
>
> 최종 애플리케이션은 EC2의 Docker 환경에서 실행되는 **MiniPEP FastAPI**이다.
> Nginx는 필요한 경우 초기 네트워크 연결 검증에만 사용하며, 최종 시연 및 운영 검증 대상에는 포함하지 않는다.
>
> Must에서는 AWS 기본 Metric, Target Health, Docker/Application Log, 운영 체크리스트, 장애 재현 및 복구를 수행한다.
>
> CloudWatch Dashboard, CloudWatch Alarm + SNS, CloudWatch Agent, CloudWatch Logs 중앙 수집은 Optional이다.

---

## 1. 파트 목표

Observability / Platform 파트의 목표는 다음과 같다.

1. 배포된 MiniPEP 서비스가 정상적으로 동작하는지 확인한다.
2. ALB, Target Group, EC2, Docker, MiniPEP의 상태를 단계별로 확인한다.
3. 장애가 발생했을 때 Metric, Target Health, Application Log를 이용해 원인을 좁힌다.
4. 팀원이 반복해서 사용할 수 있는 운영 체크리스트와 장애 대응 Runbook을 작성한다.
5. 장애 한 건을 실제로 재현하고, 탐지부터 복구까지의 과정을 검증한다.
6. 운영과 장애 대응에 필요한 리소스 정보를 Resource Handoff에 기록한다.

Observability는 단순히 서버가 켜져 있는지 확인하는 역할이 아니다.

다음 질문에 답할 수 있어야 한다.

- 사용자의 요청이 ALB까지 들어오고 있는가?
- ALB가 요청을 올바른 Target Group으로 전달하고 있는가?
- Target Group은 EC2를 Healthy 상태로 인식하고 있는가?
- EC2 인스턴스는 정상 상태인가?
- EC2 Security Group과 포트 연결은 올바른가?
- Docker 컨테이너는 실행 중인가?
- EC2 Host 80번 포트가 Container 8000번 포트로 연결되어 있는가?
- MiniPEP의 `/health`가 HTTP 200을 반환하는가?
- 애플리케이션 요청과 오류는 어디에서 확인할 수 있는가?
- 장애가 발생했을 때 어떤 순서로 확인하고 복구해야 하는가?

---

## 2. 최종 아키텍처

### 2.1 서비스 요청 흐름

```text
사용자
  ↓ HTTP :80
Internet-facing ALB
  ↓ Listener :80
Target Group
  ↓ Target Port :80
EC2 Host
  ↓ Host Port 80 → Container Port 8000
Docker Container
  ↓
MiniPEP FastAPI
```

### 2.2 최종 애플리케이션 기준

| 항목 | 기준 |
| --- | --- |
| Main Page | `/` |
| Health Check Path | `/health` |
| Expected Response | HTTP 200 |
| Container Port | `8000` |
| EC2 Host Port | `80` |
| ALB Listener Port | `80` |
| Target Group Port | `80` |
| Application Log | Docker stdout |
| Persistence | Local SQLite |

### 2.3 관측 경로

```text
EC2
 └─ CloudWatch EC2 Metrics

ALB / Target Group
 └─ CloudWatch ApplicationELB Metrics

MiniPEP FastAPI
 └─ Docker stdout
     └─ docker compose logs minipep
```

CloudWatch는 사용자의 요청이 통과하는 구성 요소가 아니다.

서비스 요청 경로와 관측 경로를 구분한다.

### 2.4 Nginx 사용 원칙

Nginx는 Day 4에서 EC2의 기본 포트 80 연결 여부를 확인하기 위한 초기 테스트 용도로만 사용할 수 있다.

최종 검증에서는 다음을 기준으로 한다.

```text
ALB → Target Group → EC2 Host 80 → Docker Container 8000 → MiniPEP FastAPI
```

최종 운영 체크리스트, 로그 확인, 장애 대응, Runbook에서는 Nginx를 기준으로 사용하지 않는다.

---

## 3. 핵심 개념

### 3.1 Metric

시간에 따른 시스템 상태를 숫자로 표현한 값이다.

예시:

- EC2 CPU 사용률
- EC2 네트워크 송수신량
- ALB 요청 수
- ALB 응답 시간
- Target Group의 Healthy Target 수
- ALB 또는 Target에서 발생한 4xx/5xx 응답 수

### 3.2 Log

시스템 또는 애플리케이션에서 발생한 이벤트 기록이다.

이번 프로젝트의 Must 로그 기준은 다음과 같다.

- Docker Container Log
- MiniPEP Application Log
- MiniPEP HTTP 요청 로그
- MiniPEP Error Log

Must에서는 Docker stdout을 직접 확인한다.

```bash
docker compose logs minipep
```

### 3.3 Health Check

ALB가 Target Group에 등록된 EC2의 애플리케이션 상태를 주기적으로 확인하는 기능이다.

이번 프로젝트의 기준은 다음과 같다.

| 항목 | 값 |
| --- | --- |
| Protocol | HTTP |
| Port | 80 |
| Path | `/health` |
| Success Code | `200` |

### 3.4 Target Health

Target Group에 등록된 EC2가 ALB의 요청을 받을 수 있는 상태인지 나타낸다.

주요 상태:

- `healthy`
- `unhealthy`
- `initial`
- `draining`
- `unused`

Target이 `unhealthy`인 경우 상태값만 보는 것이 아니라 Target Health Reason도 확인한다.

### 3.5 Dashboard

여러 Metric을 한 화면에서 확인하도록 구성한 CloudWatch 화면이다.

Dashboard 구현은 Optional이다.

Must에서는 개별 EC2, ALB, Target Group Metric을 AWS 콘솔에서 직접 확인한다.

### 3.6 Alarm

특정 Metric이 임계치를 넘었을 때 상태를 변경하거나 SNS 알림을 발생시키는 기능이다.

Alarm 구현은 Optional이다.

### 3.7 Runbook

장애가 발생했을 때 확인 순서, 원인 분석 방법, 복구 방법, 복구 검증 방법을 정리한 운영 문서이다.

이번 프로젝트에서는 공통 장애 Runbook 작성과 실제 검증이 Must이다.

### 3.8 Resource Handoff

다른 파트가 생성한 AWS 리소스를 정확하게 전달받기 위한 기록이다.

Observability / Platform 파트는 다음 값을 전달받아야 한다.

- Region
- VPC ID
- Public Subnet ID
- EC2 Instance ID
- EC2 Public IP
- ALB ARN
- ALB DNS
- Target Group ARN
- Target Group Name
- ALB Security Group ID
- EC2 Security Group ID
- Listener Port
- Target Port
- Health Check Path
- Health Check Success Code
- Docker Container Name
- Docker Compose Service Name

---

## 4. Must 범위

## 4.1 EC2 기본 Metric 확인

다음 EC2 Metric을 실제 AWS CloudWatch 콘솔에서 확인한다.

### 필수 Metric

- `CPUUtilization`
- `NetworkIn`
- `NetworkOut`
- `StatusCheckFailed`

### 확인 항목

- 올바른 EC2 Instance ID를 선택했는가?
- Metric 그래프가 정상적으로 표시되는가?
- 조회 기간이 올바른가?
- Statistic이 무엇인지 확인했는가?
- 요청 또는 장애 전후에 Metric 변화가 나타나는가?
- `StatusCheckFailed`가 0인지 확인했는가?

### 완료 기준

- 네 가지 Metric의 위치를 찾을 수 있어야 한다.
- 각 Metric이 무엇을 의미하는지 설명할 수 있어야 한다.
- Metric 확인 화면을 캡처해야 한다.
- 장애 전후 차이가 있는 경우 해당 변화를 기록해야 한다.

---

## 4.2 ALB 기본 Metric 확인

다음 ALB Metric을 실제 CloudWatch 콘솔에서 확인한다.

### 필수 Metric

- `RequestCount`
- `TargetResponseTime`
- `HTTPCode_ELB_4XX_Count`
- `HTTPCode_ELB_5XX_Count`
- `HTTPCode_Target_4XX_Count`
- `HTTPCode_Target_5XX_Count`

### Metric 구분

#### ELB 4xx / 5xx

ALB 자체에서 발생한 응답이다.

예시:

- 잘못된 요청
- Listener 또는 요청 처리 문제
- ALB가 생성한 오류 응답

#### Target 4xx / 5xx

MiniPEP 애플리케이션이 반환한 응답이다.

예시:

- 존재하지 않는 API
- 애플리케이션 내부 오류
- FastAPI Route 또는 처리 로직 오류

### 확인 항목

- 올바른 LoadBalancer 차원을 선택했는가?
- `RequestCount`가 실제 요청 후 증가하는가?
- `TargetResponseTime`이 표시되는가?
- 4xx와 5xx Metric을 ELB와 Target으로 구분할 수 있는가?
- 요청 전후 화면을 비교했는가?

### 테스트 요청

```bash
curl -i http://<ALB-DNS>/
curl -i http://<ALB-DNS>/health
curl -i http://<ALB-DNS>/api/equipment
curl -i http://<ALB-DNS>/api/jobs
```

### 완료 기준

- 각 Metric의 위치를 찾을 수 있어야 한다.
- 실제 요청 후 `RequestCount` 변화를 확인해야 한다.
- ALB 오류와 Target 오류의 차이를 설명할 수 있어야 한다.
- 관련 화면을 캡처해야 한다.

---

## 4.3 Target Group 상태와 Metric 확인

### 필수 Metric

- `HealthyHostCount`
- `UnHealthyHostCount`

### 필수 확인 항목

- Target Group에 EC2가 등록되어 있는가?
- Target Port가 `80`인가?
- Health Check Protocol이 HTTP인가?
- Health Check Path가 `/health`인가?
- Success Code가 `200`인가?
- Target 상태가 `healthy`인가?
- Target Health Reason을 확인할 수 있는가?

### Healthy 기준

다음 조건을 모두 만족해야 한다.

```text
EC2 Running
+ EC2 SG에서 ALB SG의 Port 80 요청 허용
+ EC2 Host Port 80 Listening
+ Docker Container Running
+ Host 80 → Container 8000 Port Mapping
+ MiniPEP /health HTTP 200
```

### Target이 Unhealthy가 될 수 있는 원인

- MiniPEP 컨테이너가 중지됨
- Host Port 80이 열려 있지 않음
- Host 80 → Container 8000 매핑이 잘못됨
- Health Check Path가 잘못됨
- `/health` 응답이 HTTP 200이 아님
- EC2 Security Group이 ALB Security Group을 허용하지 않음
- 잘못된 EC2가 Target Group에 등록됨
- Target Port가 잘못됨
- MiniPEP 시작 시간이 오래 걸림
- 애플리케이션 내부 오류 발생

### 완료 기준

- Target 상태가 Healthy여야 한다.
- `HealthyHostCount`와 `UnHealthyHostCount`를 확인할 수 있어야 한다.
- Target Health Reason 확인 방법을 문서화해야 한다.
- Target Group 설정 화면을 캡처해야 한다.

---

## 4.4 Docker / Application Log 확인

Must에서는 CloudWatch Logs 중앙 수집을 요구하지 않는다.

MiniPEP의 Docker stdout을 직접 확인한다.

### 컨테이너 상태 확인

```bash
docker compose ps
```

또는:

```bash
docker ps
```

### 전체 로그 확인

```bash
docker compose logs minipep
```

### 최근 로그 확인

```bash
docker compose logs --tail=100 minipep
```

### 실시간 로그 확인

```bash
docker compose logs -f minipep
```

### 요청과 로그 연결 검증

다음 요청을 실행한다.

```bash
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

외부 ALB 경로도 확인한다.

```bash
curl -i http://<ALB-DNS>/health
curl -i http://<ALB-DNS>/api/equipment
curl -i http://<ALB-DNS>/api/jobs
```

그 후 다음 요청이 MiniPEP 로그에 나타나는지 확인한다.

- `GET /health`
- `GET /api/equipment`
- `GET /api/jobs`

### 확인 항목

- MiniPEP 컨테이너가 실행 중인가?
- 컨테이너가 반복 재시작되고 있지 않은가?
- 애플리케이션 시작 오류가 없는가?
- 요청 경로가 로그에 표시되는가?
- HTTP Status Code가 로그에 표시되는가?
- Stack Trace 또는 Error Message가 있는가?
- SQLite 파일 권한 또는 경로 오류가 없는가?

### 완료 기준

- `docker compose ps` 결과가 정상이어야 한다.
- `docker compose logs minipep`로 로그를 확인할 수 있어야 한다.
- `/health`, `/api/equipment`, `/api/jobs` 요청을 로그에서 확인해야 한다.
- 정상 요청 로그 캡처 또는 텍스트 기록을 남겨야 한다.

---

## 4.5 서비스 연결성 검증

### EC2 내부 검증

```bash
curl -i http://localhost/
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

### ALB 외부 검증

```bash
curl -i http://<ALB-DNS>/
curl -i http://<ALB-DNS>/health
curl -i http://<ALB-DNS>/api/equipment
curl -i http://<ALB-DNS>/api/jobs
```

### 필수 결과

| 요청 | 기대 결과 |
| --- | --- |
| `GET /` | MiniPEP Main Page |
| `GET /health` | HTTP 200 |
| `GET /api/equipment` | 정상 API 응답 |
| `GET /api/jobs` | 정상 API 응답 |

### 완료 기준

- EC2 내부 `/health`가 HTTP 200을 반환해야 한다.
- ALB DNS `/health`가 HTTP 200을 반환해야 한다.
- ALB DNS에서 MiniPEP 화면을 볼 수 있어야 한다.
- Equipment와 Jobs API가 정상 응답해야 한다.

---

## 4.6 운영 체크리스트 작성

다음 항목을 반복 가능한 체크리스트로 작성한다.

### EC2

- Instance 상태
- Instance Status Check
- CPUUtilization
- NetworkIn
- NetworkOut
- StatusCheckFailed
- SSH 접속
- Docker 실행 상태

### ALB

- ALB 상태
- ALB DNS
- Listener 80
- Forward Action
- RequestCount
- TargetResponseTime
- ELB 4xx/5xx
- Target 4xx/5xx

### Target Group

- 등록된 Target
- Target Port 80
- Health Check Path `/health`
- Matcher 200
- Target Health
- Target Health Reason
- HealthyHostCount
- UnHealthyHostCount

### MiniPEP

- Docker Container Running
- Host 80 → Container 8000
- `/health` HTTP 200
- Main Page 표시
- Equipment API 응답
- Jobs API 응답
- Application Log 확인

### 완료 기준

- `docs/checklists/observability-checklist.md`를 작성한다.
- 다른 팀원이 문서만 보고 검증 절차를 수행할 수 있어야 한다.

---

## 4.7 장애 한 건 재현 및 복구

Day 9에 실제 장애 한 건을 발생시키고 탐지, 원인 확인, 복구 절차를 검증한다.

### 선택 가능한 장애

다음 중 하나를 선택한다.

#### 시나리오 A: MiniPEP 컨테이너 중지

```bash
docker compose stop minipep
```

#### 시나리오 B: 잘못된 Health Check Path 설정

예시:

```text
/health → /wrong-health
```

가장 단순하고 안전한 방식은 MiniPEP 컨테이너 중지이다.

### 장애 발생 전 기록

- Target 상태
- `HealthyHostCount`
- `UnHealthyHostCount`
- ALB `/health` 결과
- Docker Container 상태
- MiniPEP 로그
- 발생 시간

### 장애 발생 후 확인

- Target이 `unhealthy`로 변경되는가?
- `HealthyHostCount`가 감소하는가?
- `UnHealthyHostCount`가 증가하는가?
- ALB `/health` 요청이 실패하는가?
- ALB 또는 Target Metric에 변화가 나타나는가?
- Docker 컨테이너가 중지된 상태인가?
- Application Log에 관련 흔적이 남는가?

### 복구

컨테이너 중지 시:

```bash
docker compose start minipep
```

필요한 경우:

```bash
docker compose restart minipep
```

Health Check Path 변경 시:

```text
Health Check Path를 /health로 복구
```

### 복구 후 확인

```bash
docker compose ps
curl -i http://localhost/health
curl -i http://<ALB-DNS>/health
```

다음도 확인한다.

- Target이 다시 `healthy`가 되었는가?
- `HealthyHostCount`가 정상값으로 복구되었는가?
- `UnHealthyHostCount`가 0으로 돌아왔는가?
- MiniPEP 화면이 다시 표시되는가?
- 정상 요청이 Application Log에 표시되는가?

### 완료 기준

- 장애를 실제로 재현해야 한다.
- 장애 원인을 확인해야 한다.
- Runbook에 따라 복구해야 한다.
- 장애 전후 Metric, Target Health, Log 증거를 저장해야 한다.
- 장애 발생 시각과 복구 시각을 기록해야 한다.
- 복구 후 `/health`가 HTTP 200을 반환해야 한다.

---

## 4.8 공통 장애 Runbook 작성

Runbook은 다음 순서로 작성한다.

### 공통 확인 순서

1. ALB DNS 접속 결과 확인
2. ALB Listener와 Forwarding Rule 확인
3. Target Group에 EC2가 등록되어 있는지 확인
4. Target Health와 Target Health Reason 확인
5. `HealthyHostCount`와 `UnHealthyHostCount` 확인
6. EC2 Instance 상태 확인
7. EC2 Status Check 확인
8. ALB Security Group 확인
9. EC2 Security Group 확인
10. ALB SG → EC2 SG Port 80 허용 여부 확인
11. Target Port 80 확인
12. EC2 Host Port 80 Listening 여부 확인
13. Docker Container 실행 상태 확인
14. Host 80 → Container 8000 Port Mapping 확인
15. MiniPEP `/health` 확인
16. Docker/Application Log 확인
17. 원인 수정
18. Target Healthy 복귀 확인
19. ALB DNS `/health` HTTP 200 확인
20. 장애 원인과 복구 결과 기록

### Runbook에 기록할 항목

- 장애 이름
- 장애 발생 시간
- 최초 발견 방법
- 사용자 증상
- ALB 상태
- Target Health
- EC2 상태
- Security Group 상태
- Docker 상태
- MiniPEP 상태
- 관련 Metric
- 관련 Log
- Root Cause
- Resolution
- 복구 완료 시간
- 재발 방지 항목
- 증거 자료 링크

### 완료 기준

- `docs/runbook/common-incident-runbook.md`를 작성한다.
- 실제 장애 재현 결과를 Runbook에 반영한다.
- 문서의 확인 순서가 실제 아키텍처와 일치해야 한다.

---

## 4.9 Resource Handoff 반영

Observability / Platform 파트가 실제 운영 검증을 하기 위해 다음 정보를 최종 Handoff에 기록한다.

```markdown
## Resource Handoff

- Region:
- VPC ID:
- Public Subnet A:
- Public Subnet B:
- EC2 Instance ID:
- EC2 Public IP:
- ALB Name:
- ALB ARN:
- ALB DNS:
- Listener Port:
- Target Group Name:
- Target Group ARN:
- Target Port:
- Health Check Path:
- Success Code:
- ALB Security Group:
- EC2 Security Group:
- Docker Compose Service:
- Container Name:
- Host Port:
- Container Port:
- 검증 결과:
- Terraform 반영 여부:
```

### 완료 기준

- 리소스 ID와 이름이 실제 AWS 콘솔과 일치해야 한다.
- ALB DNS와 `/health` 검증 결과가 포함되어야 한다.
- Terraform Output과 실제 리소스를 비교할 수 있어야 한다.

---

## 5. Must 완료 체크리스트

## 5.1 EC2 Metric

- [ ] `CPUUtilization`을 확인했다.
- [ ] `NetworkIn`을 확인했다.
- [ ] `NetworkOut`을 확인했다.
- [ ] `StatusCheckFailed`를 확인했다.
- [ ] 올바른 EC2 Instance ID를 선택했다.
- [ ] Metric 화면을 캡처했다.

## 5.2 ALB Metric

- [ ] `RequestCount`를 확인했다.
- [ ] `TargetResponseTime`을 확인했다.
- [ ] `HTTPCode_ELB_4XX_Count`를 확인했다.
- [ ] `HTTPCode_ELB_5XX_Count`를 확인했다.
- [ ] `HTTPCode_Target_4XX_Count`를 확인했다.
- [ ] `HTTPCode_Target_5XX_Count`를 확인했다.
- [ ] 실제 요청 후 `RequestCount` 변화를 확인했다.
- [ ] 관련 화면을 캡처했다.

## 5.3 Target Group

- [ ] EC2가 올바른 Target Group에 등록되어 있다.
- [ ] Target Port가 80이다.
- [ ] Health Check Path가 `/health`이다.
- [ ] Success Code가 `200`이다.
- [ ] Target 상태가 Healthy이다.
- [ ] `HealthyHostCount`를 확인했다.
- [ ] `UnHealthyHostCount`를 확인했다.
- [ ] Target Health Reason 확인 방법을 기록했다.

## 5.4 MiniPEP

- [ ] Docker에서 MiniPEP가 실행 중이다.
- [ ] Host 80 → Container 8000 매핑이 적용되어 있다.
- [ ] `docker compose ps`를 확인했다.
- [ ] `docker compose logs minipep`를 확인했다.
- [ ] EC2 내부 `/health`가 HTTP 200이다.
- [ ] ALB `/health`가 HTTP 200이다.
- [ ] ALB DNS에서 MiniPEP 화면이 보인다.
- [ ] Equipment API가 정상 응답한다.
- [ ] Jobs API가 정상 응답한다.
- [ ] 주요 API 요청이 Application Log에 표시된다.

## 5.5 장애 대응

- [ ] 장애 한 건을 재현했다.
- [ ] 장애 발생 시간을 기록했다.
- [ ] Target이 Unhealthy로 변하는 것을 확인했다.
- [ ] `HealthyHostCount` 변화를 확인했다.
- [ ] `UnHealthyHostCount` 변화를 확인했다.
- [ ] Docker/Application Log를 확인했다.
- [ ] Runbook에 따라 원인을 확인했다.
- [ ] 장애를 복구했다.
- [ ] Target이 Healthy로 복구되었다.
- [ ] ALB `/health`가 다시 HTTP 200이다.
- [ ] 장애 전후 증거 자료를 저장했다.

## 5.6 문서

- [ ] Observability 체크리스트를 작성했다.
- [ ] 공통 장애 Runbook을 작성했다.
- [ ] Resource Handoff를 업데이트했다.
- [ ] Metric 확인 방법을 문서화했다.
- [ ] Target Health 확인 방법을 문서화했다.
- [ ] Docker/Application Log 확인 방법을 문서화했다.

---

## 6. Optional 범위

Optional은 팀 전체에서 1~2개를 선택한다.

Must 작업이 지연된 경우 Optional보다 Must 완료를 우선한다.

## 6.1 Optional 우선순위

### 1순위

1. CloudWatch Dashboard
2. CloudWatch Alarm + SNS
3. SSM Session Manager

### 2순위

1. HTTPS + ACM
2. Terraform Module
3. Remote Backend

### 3순위

1. Auto Scaling Group
2. WAF
3. GitHub Actions `fmt` / `validate`
4. Prometheus / Grafana

Prometheus / Grafana는 MiniPEP에 `/metrics` Endpoint가 준비된 경우에만 진행한다.

---

## 6.2 CloudWatch Dashboard

### 목표

EC2, ALB, Target Group의 핵심 Metric을 한 화면에서 확인한다.

### 추천 위젯

#### EC2

- CPUUtilization
- NetworkIn
- NetworkOut
- StatusCheckFailed

#### ALB

- RequestCount
- TargetResponseTime
- HTTPCode_ELB_4XX_Count
- HTTPCode_ELB_5XX_Count
- HTTPCode_Target_4XX_Count
- HTTPCode_Target_5XX_Count

#### Target Group

- HealthyHostCount
- UnHealthyHostCount

### 완료 기준

- Dashboard가 생성되어야 한다.
- 올바른 리소스 차원을 사용해야 한다.
- Metric이 정상 표시되어야 한다.
- Dashboard 캡처를 저장해야 한다.
- 기존 ALB → MiniPEP 구조가 정상 동작해야 한다.

---

## 6.3 CloudWatch Alarm + SNS

### 추천 Alarm

- `StatusCheckFailed >= 1`
- `UnHealthyHostCount >= 1`
- `HTTPCode_ELB_5XX_Count` 증가
- `HTTPCode_Target_5XX_Count` 증가
- `CPUUtilization` 임계치 초과
- `TargetResponseTime` 증가

### SNS 구성

- SNS Topic 생성
- 이메일 Subscription 생성
- 이메일 인증
- CloudWatch Alarm과 SNS Topic 연결
- 실제 Alarm 상태 발생
- 이메일 수신 확인

### 완료 기준

- Alarm이 실제로 상태 변경되어야 한다.
- SNS 이메일을 수신해야 한다.
- 테스트 과정과 결과를 문서화해야 한다.
- 테스트 후 불필요한 Alarm과 SNS 리소스를 정리해야 한다.

---

## 6.4 CloudWatch Agent와 중앙 로그 수집

### 목표

EC2 또는 MiniPEP 로그를 CloudWatch Logs로 중앙 수집한다.

### 구현 후보

- CloudWatch Agent 설치
- IAM Role 연결
- Log Group 생성
- Log Stream 생성
- MiniPEP Application Log 전송
- Docker Log 수집 가능 여부 검토
- 로그 보존 기간 설정

### 추가 Metric

기본 EC2 Metric에 포함되지 않는 다음 항목을 수집할 수 있다.

- Memory 사용률
- Disk 사용률
- Disk 사용 가능 공간

### 완료 기준

- CloudWatch Logs에 실제 로그가 표시되어야 한다.
- Log Group과 Log Stream 구조를 설명할 수 있어야 한다.
- IAM 권한이 최소 권한 기준이어야 한다.
- 로그 보존 기간을 확인해야 한다.

---

## 6.5 Log Metric Filter

### 목표

CloudWatch Logs의 특정 에러 패턴을 Metric으로 변환한다.

### 예시 패턴

- `ERROR`
- `Exception`
- HTTP 500
- 특정 FastAPI 오류 메시지

### 구성 흐름

```text
MiniPEP Log
→ CloudWatch Logs
→ Metric Filter
→ Custom Metric
→ CloudWatch Alarm
→ SNS
```

### 완료 기준

- 테스트 에러가 Log Group에 기록되어야 한다.
- Metric Filter가 패턴을 탐지해야 한다.
- Custom Metric 값이 증가해야 한다.
- 선택한 경우 Alarm과 연결되어야 한다.

---

## 6.6 추가 장애 시나리오

Must 장애 한 건 외에 시간이 남으면 다음을 추가로 실습할 수 있다.

- 잘못된 Health Check Path
- EC2 SG에서 ALB SG의 Port 80 허용 제거
- Target Group에서 EC2 제거
- 잘못된 Target Port
- MiniPEP Container 반복 재시작
- MiniPEP `/health`가 500을 반환하도록 변경
- EC2 Instance Stop
- ALB Listener Forwarding 설정 오류

각 실습에서는 다음을 기록한다.

- 사용자 증상
- Target Health
- Metric 변화
- Log 변화
- Root Cause
- Resolution
- Recovery Validation

---

## 6.7 Prometheus / Grafana

MiniPEP에 `/metrics` Endpoint가 준비된 경우에만 진행한다.

### 검토 항목

- Prometheus Metric 노출
- Application Metric 수집
- Grafana Dashboard 연결
- CloudWatch와의 역할 차이
- 추가 운영 비용
- EC2 자원 사용량

Must 완료에 영향을 주지 않는 범위에서만 진행한다.

---

## 7. Must와 Optional 구분 이유

## 7.1 Must로 정한 이유

Must는 최종 구조가 실제로 동작하고 있으며, 문제가 발생했을 때 원인을 확인하고 복구하기 위해 반드시 필요한 항목이다.

다음 항목은 운영 검증의 최소 기준이다.

- EC2 기본 Metric
- ALB 기본 Metric
- Target Health
- Docker/Application Log
- `/health` 검증
- 운영 체크리스트
- 장애 한 건 재현
- Runbook 작성 및 검증

이번 프로젝트는 EC2 한 대를 사용하는 구조이므로 무중단 또는 고가용성 보장을 Must 성공 기준으로 사용하지 않는다.

핵심은 단일 인스턴스 환경에서도 다음 흐름을 직접 검증하는 것이다.

```text
장애 발생
→ 사용자 증상 확인
→ Metric 확인
→ Target Health 확인
→ EC2 / SG / Port 확인
→ Docker / App 확인
→ 로그 확인
→ 원인 수정
→ 복구 검증
```

## 7.2 Optional로 정한 이유

다음 기능은 운영 완성도를 높이지만 기본 서비스 연결과 장애 대응에 필수는 아니다.

- CloudWatch Dashboard
- CloudWatch Alarm
- SNS
- CloudWatch Agent
- CloudWatch Logs 중앙 수집
- Memory / Disk Metric
- Metric Filter
- Prometheus / Grafana

Optional은 Must 구조가 완성된 후 진행한다.

Optional 구현이 실패하더라도 기존 ALB → MiniPEP 구조를 깨뜨리지 않아야 한다.

---

## 8. 다른 파트와의 연결

## 8.1 Compute + Network와 연결

Compute + Network 담당자에게 다음 정보를 전달받는다.

- EC2 Instance ID
- EC2 Public IP
- ALB DNS
- Target Group ARN
- Listener Port
- Target Port
- ALB Security Group
- EC2 Security Group
- Health Check Path
- Port Mapping

Observability / Platform은 전달받은 정보로 다음을 검증한다.

- ALB 요청
- Target Health
- EC2 상태
- Security Group 연결
- Docker 상태
- MiniPEP 응답

## 8.2 Security + SRE와 연결

Security + SRE 담당자와 다음 항목을 함께 확인한다.

- SSH 22번이 My IP로 제한되어 있는가?
- ALB SG와 EC2 SG가 분리되어 있는가?
- EC2 Port 80은 ALB SG에서만 접근 가능한가?
- 사용하지 않는 포트가 열려 있지 않은가?
- Access Key, `.env`, SQLite DB가 Git에 포함되지 않았는가?
- 장애 Runbook의 확인 순서가 보안 설정과 일치하는가?

## 8.3 Terraform / IaC와 연결

Terraform 담당자에게 다음 Output을 요청한다.

- VPC ID
- Public Subnet ID
- EC2 Instance ID
- ALB DNS
- Target Group ARN
- ALB Security Group ID
- EC2 Security Group ID

Observability / Platform은 Terraform 반영 후 다음을 다시 확인한다.

- Metric이 새 리소스와 연결되는가?
- Target Group이 Healthy인가?
- ALB DNS `/health`가 HTTP 200인가?
- Output과 AWS 콘솔 값이 일치하는가?
- Terraform 적용 후에도 Docker/Application Log를 확인할 수 있는가?

## 8.4 Application과 연결

MiniPEP 애플리케이션에서 다음 기준이 유지되어야 한다.

- `/health` 존재
- `/health` HTTP 200
- Container Port 8000
- Docker stdout에 요청 로그 출력
- Application Error가 로그에 출력
- `/api/equipment` 정상 응답
- `/api/jobs` 정상 응답

---

## 9. GitHub 산출물

## 9.1 Must 산출물

### Observability 문서

```text
docs/observability.md
```

포함 내용:

- 최종 관측 구조
- EC2 Metric
- ALB Metric
- Target Group Metric
- Target Health 확인 방법
- Docker/Application Log 확인 방법
- 검증 명령
- 장애 전후 확인 방법

### Observability 체크리스트

```text
docs/checklists/observability-checklist.md
```

### 공통 장애 Runbook

```text
docs/runbook/common-incident-runbook.md
```

### 장애 증거 자료

```text
docs/evidence/observability/
```

추천 파일:

```text
docs/evidence/observability/
├── before-target-health.png
├── after-target-unhealthy.png
├── recovered-target-health.png
├── ec2-metrics.png
├── alb-metrics.png
├── docker-running.log
├── docker-stopped.log
├── docker-recovered.log
└── incident-result.md
```

### Resource Handoff

```text
docs/resource-handoff.md
```

## 9.2 Optional 산출물

```text
docs/optional/cloudwatch-dashboard.md
docs/optional/cloudwatch-alarm-sns.md
docs/optional/cloudwatch-agent.md
docs/optional/log-metric-filter.md
```

### Optional 증거 자료

```text
docs/evidence/optional/
```

---

## 10. 장애 기록 템플릿

```markdown
# 장애 기록

## 1. 장애 개요

- 장애 이름:
- 발생 일시:
- 복구 일시:
- 총 장애 시간:
- 담당자:

## 2. 장애 시나리오

- 발생시킨 장애:
- 변경한 설정:
- 예상 결과:

## 3. 사용자 증상

- ALB DNS 접속:
- `/health` 응답:
- Main Page:
- API 응답:

## 4. Target Group

- 장애 전 Target 상태:
- 장애 후 Target 상태:
- Target Health Reason:
- HealthyHostCount:
- UnHealthyHostCount:

## 5. EC2

- Instance 상태:
- Status Check:
- CPUUtilization:
- NetworkIn:
- NetworkOut:

## 6. Docker / Application

- `docker compose ps` 결과:
- `docker compose logs minipep` 결과:
- `/health` 결과:
- 확인한 오류 메시지:

## 7. Root Cause

-

## 8. Resolution

-

## 9. Recovery Validation

- Target Healthy:
- ALB `/health` HTTP 200:
- Main Page 정상:
- API 정상:
- Application Log 정상:

## 10. Evidence

- 장애 전 캡처:
- 장애 중 캡처:
- 복구 후 캡처:
- 관련 로그:
```

---

## 11. 매일 진행 기록 템플릿

```markdown
# Day N Observability / Platform 진행 기록

## 오늘 목표

-
-
-

## 완료한 작업

-
-
-

## 확인한 AWS 리소스

- EC2:
- ALB:
- Target Group:
- Security Group:

## 검증 명령

```bash
# 실행한 명령을 기록
```

## 확인한 URL

- EC2 내부:
- ALB DNS:
- `/health`:
- `/api/equipment`:
- `/api/jobs`:

## Metric 확인

### EC2

- CPUUtilization:
- NetworkIn:
- NetworkOut:
- StatusCheckFailed:

### ALB

- RequestCount:
- TargetResponseTime:
- ELB 4xx/5xx:
- Target 4xx/5xx:

### Target Group

- HealthyHostCount:
- UnHealthyHostCount:
- Target Health:
- Health Reason:

## Docker / Application Log

- Container 상태:
- 확인한 로그:
- Error 유무:
- 요청 로그 확인:

## 발생한 문제

- 오류 메시지:
- 사용자 증상:
- 추정 원인:
- 확인 순서:
- 해결 방법:
- 결과:

## Resource Handoff

- 리소스 종류:
- 리소스 이름:
- 리소스 ID:
- 연결된 리소스:
- Port:
- Health Check Path:
- 검증 결과:
- Terraform 반영 필요 여부:

## Evidence

- Metric 캡처:
- Target Health 캡처:
- Docker Log:
- Application Log:
- PR 또는 Commit:

## 내일 할 일

-
-
-
```

---

## 12. 2~3분 공유 요약

제가 맡은 파트는 Observability / Platform입니다.

최종 서비스 흐름은 사용자가 Internet-facing ALB의 80번 포트로 접속하고, ALB가 Target Group의 80번 포트를 통해 EC2로 요청을 전달하는 구조입니다.

EC2에서는 Host 80번 포트를 Docker Container의 8000번 포트에 연결하고, Container 내부에서 MiniPEP FastAPI가 실행됩니다.

Must 범위에서는 EC2의 `CPUUtilization`, `NetworkIn`, `NetworkOut`, `StatusCheckFailed`와 ALB의 `RequestCount`, `TargetResponseTime`, ELB 및 Target의 4xx/5xx Metric을 확인합니다.

Target Group에서는 `HealthyHostCount`, `UnHealthyHostCount`, Target Health, Health Reason을 확인합니다.

애플리케이션 로그는 Must에서 CloudWatch Logs로 중앙 수집하지 않고, `docker compose logs minipep`를 이용해 Docker stdout에서 직접 확인합니다.

`/health`, `/api/equipment`, `/api/jobs` 요청이 로그에 나타나는지도 검증합니다.

장애 대응 실습에서는 MiniPEP 컨테이너 중지 또는 잘못된 Health Check Path 중 하나를 이용해 장애 한 건을 재현합니다.

장애가 발생하면 ALB, Target Group, EC2, Security Group, Port, Docker, MiniPEP 순서로 확인하고, Metric과 Target Health, Application Log를 이용해 원인을 파악합니다.

복구 후에는 Target이 다시 Healthy 상태가 되고 ALB DNS의 `/health`가 HTTP 200을 반환하는지 확인합니다.

CloudWatch Dashboard, Alarm + SNS, CloudWatch Agent, CloudWatch Logs 중앙 수집은 Optional로 진행합니다.

최종 산출물은 Observability 체크리스트, 공통 장애 Runbook, Metric 및 Target Health 캡처, Docker/Application Log, 장애 재현 및 복구 기록입니다.

---

## 13. 최종 성공 기준

Observability / Platform 파트는 다음 조건을 모두 만족하면 Must 완료로 판단한다.

1. EC2 기본 Metric을 실제로 확인했다.
2. ALB 기본 Metric을 실제로 확인했다.
3. Target Group이 Healthy 상태이다.
4. EC2 내부 `/health`가 HTTP 200이다.
5. ALB DNS `/health`가 HTTP 200이다.
6. ALB DNS에서 MiniPEP Main Page가 보인다.
7. Docker Container가 정상 실행 중이다.
8. Docker/Application Log를 확인할 수 있다.
9. 주요 API 요청이 Application Log에 표시된다.
10. Observability 체크리스트가 작성되어 있다.
11. 장애 한 건을 실제로 재현했다.
12. Metric 또는 Target Health로 장애를 탐지했다.
13. Runbook에 따라 원인을 확인하고 복구했다.
14. 장애 전후 증거 자료가 저장되어 있다.
15. 복구 후 Target이 다시 Healthy 상태이다.
16. Resource Handoff의 값이 실제 AWS 리소스와 일치한다.

이번 Must 구조는 EC2 한 대를 사용하므로 다음 항목은 성공 기준으로 사용하지 않는다.

- 무중단 배포
- 고가용성 보장
- 자동 장애 복구
- Auto Scaling
- 다중 EC2 Failover

해당 기능은 Optional 확장 범위에서만 다룬다.