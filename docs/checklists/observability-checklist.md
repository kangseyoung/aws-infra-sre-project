# Observability / Platform Final Checklist

**담당자:** 권태욱  
**파트:** Observability / Platform  
**상태:** Complete  
**최종 업데이트:** `2026-08-05`  
**Region:** `ap-northeast-2`  
**Environment:** `dev`  
**Project:** `aws-infra-sre`

> 이 문서는 AWS Infra / SRE 프로젝트의 최종 Observability 검증 결과를 기록한다.
>
> 검증 범위는 EC2 기본 Metric, ALB Metric, Target Group Health, Docker/Application Log,
> 서비스 연결성, CloudWatch Dashboard, 장애 재현 및 복구, 공통 장애 Runbook이다.
>

---

## 1. 최종 서비스 구조

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

### Application Contract

| 항목 | 최종 기준 |
| --- | --- |
| Main Page | `/` |
| Health Check Path | `/health` |
| Expected Response | HTTP 200 |
| ALB Listener | HTTP `80` |
| Target Group | HTTP `80` |
| EC2 Host Port | `80` |
| Docker Container Port | `8000` |
| Application Log | Docker stdout |
| Persistence | Local SQLite |
| 최종 애플리케이션 | MiniPEP FastAPI |
| 초기 연결 테스트 | Nginx — 최종 검증 대상 아님 |

---

## 2. Resource Handoff 최종 결과

### Network

| 항목 | 값 | 상태 |
| --- | --- | --- |
| Region | `ap-northeast-2` | 확인 |
| VPC ID | `vpc-04ac5e34907e1e0e9` | 확인 |
| VPC CIDR | `10.0.0.0/16` | 확인 |
| Public Subnet A | `subnet-0da0e473f97b614fa` | 확인 |
| Public Subnet A CIDR / AZ | `10.0.1.0/24` / `ap-northeast-2a` | 확인 |
| Public Subnet A AZ ID | `apne2-az1` | 확인 |
| Public Subnet B | `subnet-08124f6af7f10cc98` | 확인 |
| Public Subnet B CIDR / AZ | `10.0.2.0/24` / `ap-northeast-2c` | 확인 |
| Public Subnet B AZ ID | `apne2-az3` | 확인 |
| Internet Gateway | `igw-06e83aa7e2a1cd757` | 확인 |
| Public Route Table | `rtb-0ffacb032b9943e43` | 확인 |
| Local Route | `10.0.0.0/16 → local` | 확인 |
| Default Route | `0.0.0.0/0 → igw-06e83aa7e2a1cd757` | 확인 |
| Subnet Association | Public Subnet A/B → Public Route Table | 확인 |

### EC2 and Docker

| 항목 | 값 | 상태 |
| --- | --- | --- |
| EC2 Name | `aws-infra-sre-dev-app-ec2` | 확인 |
| EC2 Instance ID | `i-07d3895c10c0706be` | 확인 |
| Private IPv4 | `10.0.1.93` | 확인 |
| Public IPv4 | 없음 | 확인 |
| Subnet | `subnet-0da0e473f97b614fa` | 확인 |
| Availability Zone | `ap-northeast-2a` | 확인 |
| Security Group | `sg-03a67f4bd0610147e` | 확인 |
| EC2 Instance Connect Endpoint | `eice-077f856f79efd6170` | 확인 |
| Docker Compose Service | `minipep` | 확인 |
| Container Name | `minipep` | 확인 |
| Docker Image | `app-minipep` | 확인 |
| Port Mapping | Host `80` → Container `8000` | 확인 |
| Restart Policy | `unless-stopped` | 확인 |

### ALB

| 항목 | 값 | 상태 |
| --- | --- | --- |
| ALB Name | `aws-infra-sre-dev-alb` | 확인 |
| ALB ARN | `arn:aws:elasticloadbalancing:ap-northeast-2:712242347430:loadbalancer/app/aws-infra-sre-dev-alb/94494df53e360bab` | 확인 |
| ALB DNS | `aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com` | 확인 |
| Scheme | Internet-facing | 확인 |
| Security Group | `sg-053e06d50216483fe` | 확인 |
| Listener | HTTP `80` | 확인 |
| Default Action | Forward to `aws-infra-sre-dev-app-tg` | 확인 |
| Listener ARN | 최종 문서에 미기록 | 비차단 항목 |

### Target Group

| 항목 | 값 | 상태 |
| --- | --- | --- |
| Target Group Name | `aws-infra-sre-dev-app-tg` | 확인 |
| Target Group ARN | `arn:aws:elasticloadbalancing:ap-northeast-2:712242347430:targetgroup/aws-infra-sre-dev-app-tg/b2ef2cb4d808a127` | 확인 |
| Target Type | Instance | 확인 |
| Protocol / Port | HTTP / `80` | 확인 |
| Registered Target | `i-07d3895c10c0706be` | 확인 |
| Registered Target Count | `1` | 확인 |
| Health Check Protocol / Port | HTTP / `80` | 확인 |
| Health Check Path | `/health` | 확인 |
| Success Code | `200` | 확인 |
| 정상 Target Health | `Healthy` | 확인 |
| 정상 Health Reason | `N/A` — Health Check 통과 | 확인 |

### Terraform 상태

| 항목 | 현재 상태 |
| --- | --- |
| Terraform Managed | `No` |
| ManagedBy | `console` |
| Terraform Resource Address | Terraform 담당 작업에서 기록 |
| Import | 아직 완료되지 않음 |
| 실제 Output | Terraform PR 반영 후 확인 |

> Terraform Import와 Output은 Terraform / IaC 파트의 후속 작업이며,
> Observability Must 완료 여부를 차단하지 않는다.

---

## 3. EC2 Metric 검증

### 확인 Metric

- [x] `CPUUtilization`
- [x] `NetworkIn`
- [x] `NetworkOut`
- [x] `StatusCheckFailed`

### 완료 결과

- [x] 올바른 EC2 Instance ID `i-07d3895c10c0706be`를 선택했다.
- [x] 각 Metric 그래프가 정상적으로 표시되는 것을 확인했다.
- [x] 조회 기간과 Statistic을 확인했다.
- [x] 정상 상태에서 `StatusCheckFailed = 0`을 확인했다.
- [x] 테스트 요청 전후 `NetworkIn`과 `NetworkOut` 변화를 확인했다.
- [x] 장애 전후 관련 Metric 변화를 확인했다.
- [x] 관련 화면을 캡처하고 증거 자료로 저장했다.

---

## 4. ALB Metric 검증

### 확인 Metric

- [x] `RequestCount`
- [x] `TargetResponseTime`
- [x] `HTTPCode_ELB_4XX_Count`
- [x] `HTTPCode_ELB_5XX_Count`
- [x] `HTTPCode_Target_2XX_Count`
- [x] `HTTPCode_Target_4XX_Count`
- [x] `HTTPCode_Target_5XX_Count`

### 완료 결과

- [x] 올바른 ALB `aws-infra-sre-dev-alb`를 선택했다.
- [x] 정상 요청 후 `RequestCount` 증가를 확인했다.
- [x] `TargetResponseTime`이 표시되는 것을 확인했다.
- [x] 정상 요청에 따른 Target 2xx Metric을 확인했다.
- [x] 존재하지 않는 경로 요청에 따른 Target 4xx를 확인했다.
- [x] ELB 오류와 Target 오류의 차이를 구분했다.
- [x] 5xx Metric의 위치와 정상 상태의 값 또는 데이터 유무를 확인했다.
- [x] 장애 전후 ALB Metric 변화를 확인했다.
- [x] 관련 화면을 캡처하고 증거 자료로 저장했다.

> 5xx 응답을 만들기 위해 애플리케이션에 인위적인 내부 오류를 추가하지 않았다.
> Metric 위치와 정상 상태를 확인하고, 컨테이너 중지 장애는 Target Health와 서비스 실패를 중심으로 검증했다.

---

## 5. Target Group Health 및 Metric 검증

### 정상 상태

- [x] EC2 `i-07d3895c10c0706be`가 올바른 Target Group에 등록되어 있다.
- [x] Target Port가 `80`이다.
- [x] Health Check Protocol이 HTTP이다.
- [x] Health Check Path가 `/health`이다.
- [x] Success Code가 `200`이다.
- [x] Target 상태가 `Healthy`이다.
- [x] Target Health Reason 확인 방법을 검증했다.
- [x] 정상 상태에서 `HealthyHostCount = 1`을 확인했다.
- [x] 정상 상태에서 `UnHealthyHostCount = 0`을 확인했다.
- [x] Target Group 설정과 Healthy 상태를 캡처했다.

### 장애 상태 및 복구

- [x] MiniPEP 컨테이너 중지 후 Target이 `Unhealthy`로 변경되는 것을 확인했다.
- [x] 장애 시 `HealthyHostCount` 감소를 확인했다.
- [x] 장애 시 `UnHealthyHostCount` 증가를 확인했다.
- [x] Target Health Reason을 확인했다.
- [x] 컨테이너 복구 후 Target이 다시 `Healthy`로 변경되는 것을 확인했다.
- [x] 복구 후 `HealthyHostCount = 1`을 확인했다.
- [x] 복구 후 `UnHealthyHostCount = 0`을 확인했다.
- [x] 장애·복구 상태를 각각 캡처했다.

---

## 6. Docker / Application Log 검증

### 사용 명령

```bash
docker compose ps
docker compose logs minipep
docker compose logs --tail=100 minipep
docker compose logs -f minipep
```

### 완료 결과

- [x] MiniPEP 컨테이너가 정상적으로 실행 중이다.
- [x] 컨테이너가 반복 재시작되지 않는다.
- [x] Host `80` → Container `8000` 매핑을 확인했다.
- [x] 애플리케이션 시작 오류가 없음을 확인했다.
- [x] `/health` 요청이 로그에 나타나는 것을 확인했다.
- [x] `/api/equipment` 요청이 로그에 나타나는 것을 확인했다.
- [x] `/api/jobs` 요청이 로그에 나타나는 것을 확인했다.
- [x] HTTP Status Code를 로그에서 확인했다.
- [x] Stack Trace 또는 Error Message 확인 방법을 검증했다.
- [x] SQLite 경로 또는 권한 오류가 없음을 확인했다.
- [x] Docker 상태와 Application Log를 증거 자료로 저장했다.

---

## 7. 서비스 연결성 검증

### EC2 내부

```bash
curl -i http://localhost/
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

- [x] `/`에서 MiniPEP Main Page가 표시된다.
- [x] `/health`가 HTTP 200을 반환한다.
- [x] `/health` 응답 본문에서 `{"status":"ok","service":"minipep"}`를 확인했다.
- [x] `/api/equipment`가 정상 응답한다.
- [x] `/api/jobs`가 정상 응답한다.
- [x] 각 요청이 MiniPEP 로그에 표시된다.
- [x] EC2 내부 검증 결과를 저장했다.

### ALB 외부

```bash
curl -i http://aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com/
curl -i http://aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com/health
curl -i http://aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com/api/equipment
curl -i http://aws-infra-sre-dev-alb-891673525.ap-northeast-2.elb.amazonaws.com/api/jobs
```

- [x] ALB DNS에서 MiniPEP Main Page가 표시된다.
- [x] ALB DNS `/health`가 HTTP 200을 반환한다.
- [x] `/health` 응답 본문에서 `{"status":"ok","service":"minipep"}`를 확인했다.
- [x] Equipment API가 정상 응답한다.
- [x] Jobs API가 정상 응답한다.
- [x] 요청 후 `RequestCount` 증가를 확인했다.
- [x] Target가 `Healthy` 상태임을 확인했다.
- [x] ALB 외부 검증 결과를 저장했다.

---

## 8. CloudWatch Dashboard

- [x] EC2, ALB, Target Group 핵심 Metric을 포함한 Dashboard를 생성했다.
- [x] EC2 Metric 위젯이 정상적으로 표시된다.
- [x] ALB Metric 위젯이 정상적으로 표시된다.
- [x] Target Group Metric 위젯이 정상적으로 표시된다.
- [x] 정상 요청 전후 Metric 변화를 Dashboard에서 확인했다.
- [x] 장애 발생 중 Metric 및 Target 상태 변화를 확인했다.
- [x] 복구 후 정상 상태로 돌아오는 것을 확인했다.
- [x] Dashboard 캡처를 저장했다.

### Dashboard 포함 Metric

#### EC2

- `CPUUtilization`
- `NetworkIn`
- `NetworkOut`
- `StatusCheckFailed`

#### ALB

- `RequestCount`
- `TargetResponseTime`
- `HTTPCode_ELB_4XX_Count`
- `HTTPCode_ELB_5XX_Count`
- `HTTPCode_Target_2XX_Count`
- `HTTPCode_Target_4XX_Count`
- `HTTPCode_Target_5XX_Count`

#### Target Group

- `HealthyHostCount`
- `UnHealthyHostCount`

---

## 9. 장애 재현 및 복구 검증

### 장애 시나리오

MiniPEP Docker 컨테이너 중지:

```bash
docker compose stop minipep
```

### 장애 발생 결과

- [x] 장애 발생 시간을 기록했다.
- [x] Docker 컨테이너가 중지된 것을 확인했다.
- [x] EC2 내부 `/health` 요청 실패를 확인했다.
- [x] ALB `/health` 요청 실패를 확인했다.
- [x] Target가 `Unhealthy`로 변경되는 것을 확인했다.
- [x] `HealthyHostCount` 감소를 확인했다.
- [x] `UnHealthyHostCount` 증가를 확인했다.
- [x] 장애 중 Metric 변화를 확인했다.
- [x] Docker/Application Log와 Target Health Reason을 확인했다.
- [x] 장애 상태의 캡처와 명령 결과를 저장했다.

### Root Cause

```text
MiniPEP Docker 컨테이너가 중지되어
EC2 Host Port 80에서 정상 애플리케이션 응답을 제공하지 못했다.
그 결과 ALB Health Check가 실패하고 Target이 Unhealthy 상태로 변경되었다.
```

### 복구

```bash
docker compose start minipep
```

### 복구 결과

- [x] 복구 시간을 기록했다.
- [x] MiniPEP 컨테이너가 Running 상태로 복구되었다.
- [x] EC2 내부 `/health`가 다시 HTTP 200을 반환했다.
- [x] ALB `/health`가 다시 HTTP 200을 반환했다.
- [x] Target가 `Healthy` 상태로 복구되었다.
- [x] `HealthyHostCount = 1`로 복구되었다.
- [x] `UnHealthyHostCount = 0`으로 복구되었다.
- [x] MiniPEP Main Page와 API가 다시 정상 응답했다.
- [x] 복구 후 요청이 Application Log에 표시되는 것을 확인했다.
- [x] 복구 상태의 캡처와 명령 결과를 저장했다.

---

## 10. 증거 자료

저장 경로:

```text
docs/evidence/observability/
```

### 저장 완료 항목

- [x] CloudWatch Dashboard 캡처
- [x] EC2 Metric 캡처
- [x] ALB Metric 캡처
- [x] Target Group 설정 캡처
- [x] Target Healthy 상태 캡처
- [x] Target Unhealthy 상태 캡처
- [x] Target 복구 상태 캡처
- [x] Docker 실행 상태 기록
- [x] MiniPEP Application Log
- [x] EC2 내부 `/health` 결과
- [x] ALB `/health` 정상 결과
- [x] ALB `/health` 장애 결과
- [x] ALB `/health` 복구 결과
- [x] 장애 전후 Metric 및 상태 증거

> 실제 파일명과 링크는 저장소의 `docs/evidence/observability/` 디렉터리를 기준으로 관리한다.

---

## 11. 공통 장애 Runbook

- [x] `docs/runbook/common-incident-runbook.md`를 작성했다.
- [x] 장애 발생 시간과 복구 시간을 기록했다.
- [x] 사용자 증상을 기록했다.
- [x] ALB, Target Group, EC2, Docker 확인 순서를 기록했다.
- [x] 관련 Metric과 Log 확인 방법을 기록했다.
- [x] Root Cause를 기록했다.
- [x] 복구 명령과 복구 검증 절차를 기록했다.
- [x] 재발 방지 또는 후속 확인 항목을 기록했다.
- [x] 증거 자료 경로를 연결했다.
- [x] 실제 장애 재현 결과를 Runbook에 반영했다.

### 표준 확인 순서

1. ALB DNS 응답 확인
2. Listener 및 Forward Action 확인
3. Target 등록 상태 확인
4. Target Health 및 Health Reason 확인
5. `HealthyHostCount`, `UnHealthyHostCount` 확인
6. EC2 상태와 Status Check 확인
7. ALB SG → EC2 SG Port 80 확인
8. EC2 Host Port 80 확인
9. Docker Container 상태 확인
10. Host 80 → Container 8000 매핑 확인
11. EC2 내부 `/health` 확인
12. Docker/Application Log 확인
13. 원인 수정
14. Target Healthy 복구 확인
15. ALB `/health` HTTP 200 확인
16. 장애 원인과 복구 결과 기록

---

## 12. Optional 구현 상태

| 항목 | 상태 |
| --- | --- |
| CloudWatch Dashboard | 완료 |
| CloudWatch Agent | 미진행 |
| CloudWatch Logs 중앙 수집 | 미진행 |
| Log Group / Log Stream | 미진행 |
| Memory / Disk Custom Metric | 미진행 |
| Log Metric Filter | 미진행 |
| CloudWatch Alarm + SNS | 미진행 |

> Optional 미진행 항목은 Observability Must 완료 여부에 영향을 주지 않는다.

---

## 13. 최종 완료 체크리스트

### Resource Handoff

- [x] Network 리소스 값을 확인했다.
- [x] EC2와 Security Group 값을 확인했다.
- [x] ALB와 Target Group 값을 확인했다.
- [x] Docker 서비스와 Port Mapping 값을 확인했다.
- [x] AWS Console과 실제 리소스를 대조했다.

### 정상 상태 Observability

- [x] EC2 기본 Metric을 확인했다.
- [x] ALB 기본 Metric을 확인했다.
- [x] Target Group Metric과 Health를 확인했다.
- [x] Docker/Application Log를 확인했다.
- [x] EC2 내부 연결성을 확인했다.
- [x] ALB 외부 연결성을 확인했다.
- [x] CloudWatch Dashboard를 생성하고 캡처했다.
- [x] 정상 상태 증거 자료를 저장했다.

### 장애 대응

- [x] MiniPEP 컨테이너 중지 장애를 재현했다.
- [x] 장애 상태를 Metric, Target Health, Log로 확인했다.
- [x] 장애 전후 증거 자료를 저장했다.
- [x] 서비스를 복구했다.
- [x] Target Healthy 복구를 확인했다.
- [x] ALB `/health` HTTP 200 복구를 확인했다.
- [x] 공통 장애 Runbook을 작성했다.

### 문서화

- [x] Observability 최종 체크리스트를 완성했다.
- [x] Resource Handoff 값을 반영했다.
- [x] Metric 확인 결과를 기록했다.
- [x] Target Health 확인 결과를 기록했다.
- [x] Docker/Application Log 확인 결과를 기록했다.
- [x] 장애 재현과 복구 결과를 기록했다.
- [x] 증거 자료와 Runbook 경로를 기록했다.

---

## 14. 최종 결론

```text
사용자
→ ALB:80
→ Target Group:80
→ EC2 Host:80
→ Docker Container:8000
→ MiniPEP FastAPI
```

위 요청 흐름이 정상 동작하며 다음을 모두 검증했다.

- MiniPEP 정상 응답
- EC2 및 ALB 기본 Metric
- Target Group Healthy 상태
- Docker/Application Log
- CloudWatch Dashboard
- 장애 발생 탐지
- Target Unhealthy 전환
- 장애 원인 확인
- 서비스 복구
- Target Healthy 복귀
- ALB `/health` HTTP 200 복구
- 증거 자료 저장
- 공통 장애 Runbook 작성

**Observability / Platform Must 범위 완료.**
