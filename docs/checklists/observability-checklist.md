# Observability / Platform Checklist

**담당자:** 권태욱  
**파트:** Observability / Platform  
**작성 단계:** Day 3 
**상태:** In Progress  
**Region:** `ap-northeast-2`  
**Environment:** `dev`  
**Project:** `aws-infra-sre`

> 이 문서는 AWS 리소스가 생성되는 과정에서 Observability 검증 상태를 누적하여 관리한다.
>
> 각 단계에서는 실제로 전달받거나 확인한 리소스 정보만 체크한다.
> 아직 생성되지 않은 EC2, ALB, Target Group, Docker 관련 항목은 체크하지 않는다.
>
> 최종 애플리케이션은 EC2의 Docker 환경에서 실행되는 MiniPEP FastAPI이다.
> Nginx는 초기 네트워크 연결 테스트에만 사용할 수 있으며 최종 운영 검증 대상에는 포함하지 않는다.

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

| 항목 | 기준 |
| --- | --- |
| Region | `ap-northeast-2` |
| Main Page | `/` |
| Health Check Path | `/health` |
| Expected Response | HTTP 200 |
| ALB Listener Port | `80` |
| Target Group Port | `80` |
| EC2 Host Port | `80` |
| Docker Container Port | `8000` |
| Application Log | Docker stdout |
| Persistence | Local SQLite |
| 초기 연결 테스트 | Nginx |
| 최종 애플리케이션 | MiniPEP FastAPI |

---

## 2. Resource Handoff 확인 항목

Compute + Network 또는 Terraform 담당자로부터 다음 정보를 전달받는다.

### Network

- [x] Region — `ap-northeast-2`
- [x] VPC ID — `vpc-04ac5e34907e1e0e9`
- [x] VPC CIDR — `10.0.0.0/16`
- [x] Public Subnet A ID — `subnet-0da0e473f97b614fa`
- [x] Public Subnet A CIDR — `10.0.1.0/24`
- [x] Public Subnet A Availability Zone — `ap-northeast-2a`
- [x] Public Subnet A Availability Zone ID — `apne2-az1`
- [x] Public Subnet B ID — `subnet-08124f6af7f10cc98`
- [x] Public Subnet B CIDR — `10.0.2.0/24`
- [x] Public Subnet B Availability Zone — `ap-northeast-2c`
- [x] Public Subnet B Availability Zone ID — `apne2-az3`
- [x] Internet Gateway ID — `igw-06e83aa7e2a1cd757`
- [x] Public Route Table ID — `rtb-0ffacb032b9943e43`
- [x] Public Route Table에 `10.0.0.0/16 → local` 경로가 있다.
- [x] Public Route Table에 `0.0.0.0/0 → igw-06e83aa7e2a1cd757` 경로가 있다.
- [x] Public Subnet A가 Public Route Table에 연결되어 있다.
- [x] Public Subnet B가 Public Route Table에 연결되어 있다.

검증 출처:

- `docs/handoff/compute-network-resources.md`

### EC2

- [ ] EC2 Name
- [ ] EC2 Instance ID
- [ ] EC2 Public IP
- [ ] EC2 Security Group ID
- [ ] EC2 Subnet ID
- [ ] EC2 Availability Zone
- [ ] Host Port
- [ ] Docker Container Port
- [ ] Docker Compose Service Name
- [ ] Docker Container Name

### ALB

- [ ] ALB Name
- [ ] ALB ARN
- [ ] ALB DNS
- [ ] ALB Security Group ID
- [ ] Listener Protocol
- [ ] Listener Port

### Target Group

- [ ] Target Group Name
- [ ] Target Group ARN
- [ ] Target Protocol
- [ ] Target Port
- [ ] Registered Target
- [ ] Health Check Protocol
- [ ] Health Check Port
- [ ] Health Check Path
- [ ] Health Check Success Code

### Terraform

- [ ] Terraform 관리 여부
- [ ] `ManagedBy` 값
- [ ] Terraform Resource Address
- [ ] Import 여부
- [ ] 관련 Output 이름

---

## 3. EC2 Metric

### 확인 대상

- [ ] `CPUUtilization`
- [ ] `NetworkIn`
- [ ] `NetworkOut`
- [ ] `StatusCheckFailed`

### Metric 목적

| Metric | 확인 목적 |
| --- | --- |
| `CPUUtilization` | EC2 CPU 사용률 확인 |
| `NetworkIn` | EC2가 수신한 네트워크 데이터 확인 |
| `NetworkOut` | EC2가 송신한 네트워크 데이터 확인 |
| `StatusCheckFailed` | EC2 시스템 또는 인스턴스 상태 검사 실패 확인 |

### 실제 검증 시 확인할 내용

- [ ] 올바른 EC2 Instance ID를 선택했다.
- [ ] Metric 그래프가 정상적으로 표시된다.
- [ ] 조회 기간을 확인했다.
- [ ] Statistic을 확인했다.
- [ ] 정상 상태에서 `StatusCheckFailed`가 0이다.
- [ ] 요청 전후 Metric 변화를 확인했다.
- [ ] 장애 전후 Metric 변화를 확인했다.
- [ ] 관련 화면을 캡처했다.

---

## 4. ALB Metric

### 확인 대상

- [ ] `RequestCount`
- [ ] `TargetResponseTime`
- [ ] `HTTPCode_ELB_4XX_Count`
- [ ] `HTTPCode_ELB_5XX_Count`
- [ ] `HTTPCode_Target_4XX_Count`
- [ ] `HTTPCode_Target_5XX_Count`

### Metric 목적

| Metric | 확인 목적 |
| --- | --- |
| `RequestCount` | ALB가 처리한 요청 수 확인 |
| `TargetResponseTime` | Target이 응답하는 데 걸린 시간 확인 |
| `HTTPCode_ELB_4XX_Count` | ALB에서 생성된 4xx 응답 확인 |
| `HTTPCode_ELB_5XX_Count` | ALB에서 생성된 5xx 응답 확인 |
| `HTTPCode_Target_4XX_Count` | MiniPEP이 반환한 4xx 응답 확인 |
| `HTTPCode_Target_5XX_Count` | MiniPEP이 반환한 5xx 응답 확인 |

### ELB 오류와 Target 오류 구분

- ELB 4xx/5xx는 ALB가 생성한 오류 응답이다.
- Target 4xx/5xx는 MiniPEP 애플리케이션이 생성한 오류 응답이다.

### 실제 검증 시 확인할 내용

- [ ] 올바른 ALB를 선택했다.
- [ ] 테스트 요청 후 `RequestCount`가 증가한다.
- [ ] `TargetResponseTime`이 표시된다.
- [ ] ELB 오류와 Target 오류를 구분할 수 있다.
- [ ] 4xx 또는 5xx 발생 시 원인을 확인할 수 있다.
- [ ] 관련 화면을 캡처했다.

---

## 5. Target Group Metric 및 Health

### 확인 대상

- [ ] `HealthyHostCount`
- [ ] `UnHealthyHostCount`
- [ ] Target Health
- [ ] Target Health Reason

### 설정 기준

| 항목 | 기준 |
| --- | --- |
| Protocol | HTTP |
| Target Port | `80` |
| Health Check Path | `/health` |
| Success Code | `200` |

### 확인 항목

- [ ] EC2가 Target Group에 등록되어 있다.
- [ ] Target Port가 `80`이다.
- [ ] Health Check Protocol이 HTTP이다.
- [ ] Health Check Path가 `/health`이다.
- [ ] Success Code가 `200`이다.
- [ ] Target 상태가 `healthy`이다.
- [ ] Target Health Reason을 확인할 수 있다.
- [ ] `HealthyHostCount`가 정상값이다.
- [ ] `UnHealthyHostCount`가 정상 상태에서 0이다.

### Healthy 조건

```text
EC2 Running
+ ALB SG에서 EC2 SG의 Port 80 접근 가능
+ EC2 Host Port 80 Listening
+ Docker Container Running
+ Host 80 → Container 8000 Port Mapping
+ MiniPEP /health HTTP 200
```

### 주요 Unhealthy 원인

- MiniPEP 컨테이너 중지
- 잘못된 Health Check Path
- 잘못된 Target Port
- EC2 Security Group 오류
- ALB Security Group 오류
- Host 80 → Container 8000 매핑 오류
- `/health`가 HTTP 200을 반환하지 않음
- 잘못된 EC2가 Target으로 등록됨
- 애플리케이션 시작 실패

---

## 6. Docker / Application Log

Must에서는 CloudWatch Logs 중앙 수집을 요구하지 않는다.

MiniPEP의 Docker stdout을 직접 확인한다.

### 컨테이너 상태

```bash
docker compose ps
```

대체 명령:

```bash
docker ps
```

### 전체 로그

```bash
docker compose logs minipep
```

### 최근 로그 100줄

```bash
docker compose logs --tail=100 minipep
```

### 실시간 로그

```bash
docker compose logs -f minipep
```

### 확인 항목

- [ ] MiniPEP 컨테이너가 실행 중이다.
- [ ] 컨테이너가 반복 재시작되지 않는다.
- [ ] 애플리케이션 시작 오류가 없다.
- [ ] `/health` 요청이 로그에 나타난다.
- [ ] `/api/equipment` 요청이 로그에 나타난다.
- [ ] `/api/jobs` 요청이 로그에 나타난다.
- [ ] HTTP Status Code를 확인할 수 있다.
- [ ] Stack Trace 또는 Error Message를 확인할 수 있다.
- [ ] SQLite 경로 또는 권한 오류가 없다.

### Optional 범위

다음 항목은 Must가 아니라 Optional이다.

- [ ] CloudWatch Agent 설치
- [ ] CloudWatch Logs 중앙 수집
- [ ] Log Group 생성
- [ ] Log Stream 생성
- [ ] Memory Metric 수집
- [ ] Disk Metric 수집
- [ ] Log Metric Filter
- [ ] CloudWatch Alarm 및 SNS

---

## 7. EC2 내부 검증

EC2와 MiniPEP 배포 이후 다음 명령을 실행한다.

```bash
curl -i http://localhost/
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
```

### 기대 결과

- [ ] `/`에서 MiniPEP Main Page가 표시된다.
- [ ] `/health`가 HTTP 200을 반환한다.
- [ ] `/api/equipment`가 정상 응답한다.
- [ ] `/api/jobs`가 정상 응답한다.
- [ ] 각 요청이 MiniPEP 로그에 표시된다.

---

## 8. ALB 외부 검증

ALB 생성 이후 다음 명령을 실행한다.

```bash
curl -i http://<ALB-DNS>/
curl -i http://<ALB-DNS>/health
curl -i http://<ALB-DNS>/api/equipment
curl -i http://<ALB-DNS>/api/jobs
```

### 기대 결과

- [ ] ALB DNS에서 MiniPEP Main Page가 표시된다.
- [ ] ALB DNS `/health`가 HTTP 200을 반환한다.
- [ ] Equipment API가 정상 응답한다.
- [ ] Jobs API가 정상 응답한다.
- [ ] 요청 후 `RequestCount`가 증가한다.
- [ ] Target 상태가 Healthy이다.

---

## 9. 장애 발생 시 확인 순서

1. ALB DNS 접속 결과를 확인한다.
2. ALB Listener가 Port 80으로 설정되었는지 확인한다.
3. Listener의 Forwarding Rule을 확인한다.
4. Target Group에 EC2가 등록되었는지 확인한다.
5. Target Health를 확인한다.
6. Target Health Reason을 확인한다.
7. `HealthyHostCount`를 확인한다.
8. `UnHealthyHostCount`를 확인한다.
9. EC2 Instance 상태를 확인한다.
10. EC2 Status Check를 확인한다.
11. ALB Security Group을 확인한다.
12. EC2 Security Group을 확인한다.
13. ALB SG에서 EC2 SG Port 80 접근이 가능한지 확인한다.
14. Target Port가 80인지 확인한다.
15. EC2 Host Port 80이 Listening 상태인지 확인한다.
16. Docker Container 상태를 확인한다.
17. Host 80 → Container 8000 매핑을 확인한다.
18. EC2 내부 `/health`를 확인한다.
19. Docker/Application Log를 확인한다.
20. 원인을 수정한다.
21. Target이 Healthy로 복구되는지 확인한다.
22. ALB `/health`가 다시 HTTP 200인지 확인한다.
23. 장애 원인과 복구 결과를 기록한다.

---

## 10. 증거 자료

추천 저장 경로:

```text
docs/evidence/observability/
```

추천 파일 이름:

```text
ec2-cpu-utilization.png
ec2-network-in-out.png
ec2-status-check-failed.png
alb-request-count.png
alb-target-response-time.png
alb-http-status.png
target-healthy.png
target-unhealthy.png
target-recovered.png
docker-running.log
docker-application.log
health-check-result.txt
```

### 저장할 증거

- [ ] EC2 Metric 캡처
- [ ] ALB Metric 캡처
- [ ] Target Group 설정 캡처
- [ ] Target Healthy 상태 캡처
- [ ] Docker 상태 기록
- [ ] MiniPEP Application Log
- [ ] EC2 내부 `/health` 결과
- [ ] ALB `/health` 결과
- [ ] 장애 전후 증거 자료

---

## 11. Resource Handoff 검증 결과

| 항목 | 값 | 상태 |
| --- | --- | --- |
| Region | `ap-northeast-2` | 확인 |
| VPC ID | `vpc-04ac5e34907e1e0e9` | 확인 |
| VPC CIDR | `10.0.0.0/16` | 확인 |
| Public Subnet A ID | `subnet-0da0e473f97b614fa` | 확인 |
| Public Subnet A CIDR | `10.0.1.0/24` | 확인 |
| Public Subnet A AZ | `ap-northeast-2a` | 확인 |
| Public Subnet B ID | `subnet-08124f6af7f10cc98` | 확인 |
| Public Subnet B CIDR | `10.0.2.0/24` | 확인 |
| Public Subnet B AZ | `ap-northeast-2c` | 확인 |
| Internet Gateway ID | `igw-06e83aa7e2a1cd757` | 확인 |
| Public Route Table ID | `rtb-0ffacb032b9943e43` | 확인 |
| Default Route | `0.0.0.0/0 → igw-06e83aa7e2a1cd757` | 확인 |
| Public Subnet A Association | `rtb-0ffacb032b9943e43` | 확인 |
| Public Subnet B Association | `rtb-0ffacb032b9943e43` | 확인 |
| ALB Security Group ID | TBD | 미생성 |
| EC2 Security Group ID | TBD | 미생성 |
| EC2 Instance ID | TBD | 미생성 |
| EC2 Public IP | TBD | 미생성 |
| ALB ARN | TBD | 미생성 |
| ALB DNS | TBD | 미생성 |
| Target Group ARN | TBD | 미생성 |
| Listener Port | `80` | 기준 확정 |
| Target Port | `80` | 기준 확정 |
| Health Check Path | `/health` | 기준 확정 |
| Success Code | `200` | 기준 확정 |
| Host Port | `80` | 기준 확정 |
| Container Port | `8000` | 기준 확정 |
| Docker Compose Service | `minipep` | 예정 |
| Network Terraform Managed | `No` | `ManagedBy=console` |

### 현재 검증 범위

- Network Resource Handoff는 확인 완료했다.
- VPC, Public Subnet A/B, Internet Gateway, Public Route Table 정보를 확인했다.
- EC2, Security Group, ALB, Target Group은 아직 생성되지 않아 검증하지 않았다.
- Docker와 MiniPEP Application Log는 배포 이후 검증한다.
- CloudWatch EC2 및 ALB Metric은 해당 리소스 생성 이후 검증한다.

---

## 12. Day 2 완료 체크리스트

Day 2에서는 실제 AWS Metric 값이나 Docker 로그를 확인하지 않아도 된다.

오늘은 앞으로 사용할 관측 기준과 검증 방법을 확정한다.

- [x] PR #6의 Region 기준을 확인했다.
- [x] PR #6의 VPC/Subnet CIDR 기준을 확인했다.
- [x] ALB 80 → Target 80 → Host 80 → Container 8000 구조를 확인했다.
- [x] Health Check Path `/health`를 확인했다.
- [x] Success Code `200`을 확인했다.
- [x] EC2 Metric 목록을 확정했다.
- [x] ALB Metric 목록을 확정했다.
- [x] Target Group Metric 목록을 확정했다.
- [x] Target Health 확인 기준을 확정했다.
- [x] Docker Container 상태 확인 명령을 확정했다.
- [x] MiniPEP Application Log 확인 명령을 확정했다.
- [x] EC2 내부 검증 명령을 확정했다.
- [x] ALB 외부 검증 명령을 확정했다.
- [x] Resource Handoff 필수 전달값을 확정했다.
- [x] CloudWatch Agent와 중앙 로그 수집이 Optional임을 확인했다.
- [x] Compute + Network 문서와 기준 충돌이 없는지 확인했다.
- [ ] 팀원에게 Checklist 검토를 요청했다.

---

## 13. Day 2 결과

### 확정된 내용

- Region:
- 포트 구조:
- Health Check Path:
- Success Code:
- EC2 Metric:
- ALB Metric:
- Target Group Metric:
- Docker Log Command:
- Resource Handoff 필수값:

### 미확정 내용

- Terraform import 또는 재생성:
- EC2 Instance ID:
- ALB DNS:
- Target Group ARN:
- Docker Container Name:

### 팀원에게 요청할 내용

- Compute + Network:
- Security + SRE:
- Terraform / IaC:

### 다음 작업

- Day 3 생성 리소스의 Handoff 값 확인
- 새 리소스 ID를 Checklist에 반영
- CloudWatch Metric 위치 사전 학습
- Target Health 확인 방법 사전 학습

---

## 14. Day 3 Network Resource Handoff 검증

### 검증 목적

Compute + Network 담당자가 구성한 Day 3 네트워크 리소스의 전달값이 프로젝트 설계 기준과 일치하는지 확인한다.

Day 3에서는 애플리케이션 통신이 아니라 다음 네트워크 구성과 연결 관계를 확인한다.

```text
VPC
├── Public Subnet A
├── Public Subnet B
├── Internet Gateway
└── Public Route Table
    ├── 10.0.0.0/16 → local
    └── 0.0.0.0/0 → Internet Gateway
```

### 검증 기준 문서

```text
docs/handoff/compute-network-resources.md
```

### 전달받은 네트워크 정보

### 2. network 참고

### 설계 기준 검증

| 검증 항목 | 기대값 | Handoff 확인값 | 결과 |
| --- | --- | --- | --- |
| Region | `ap-northeast-2` | `ap-northeast-2` | PASS |
| VPC CIDR | `10.0.0.0/16` | `10.0.0.0/16` | PASS |
| Public Subnet A CIDR | `10.0.1.0/24` | `10.0.1.0/24` | PASS |
| Public Subnet A AZ | `ap-northeast-2a` | `ap-northeast-2a` | PASS |
| Public Subnet B CIDR | `10.0.2.0/24` | `10.0.2.0/24` | PASS |
| Public Subnet B AZ | `ap-northeast-2c` | `ap-northeast-2c` | PASS |
| 서로 다른 AZ 사용 | Subnet A/B가 다른 AZ | `2a`, `2c` | PASS |
| IGW 연결 대상 | 프로젝트 VPC | `vpc-04ac5e34907e1e0e9` | PASS |
| Local Route | `10.0.0.0/16 → local` | 확인됨 | PASS |
| Default Route | `0.0.0.0/0 → IGW` | `igw-06e83aa7e2a1cd757` | PASS |
| Subnet A Association | Public Route Table 연결 | `rtb-0ffacb032b9943e43` | PASS |
| Subnet B Association | Public Route Table 연결 | `rtb-0ffacb032b9943e43` | PASS |

### Route Table 확인 결과

| Destination | Target |
| --- | --- |
| `10.0.0.0/16` | `local` |
| `0.0.0.0/0` | `igw-06e83aa7e2a1cd757` |

### Subnet Association 확인 결과

| Subnet | Route Table |
| --- | --- |
| `subnet-0da0e473f97b614fa` | `rtb-0ffacb032b9943e43` |
| `subnet-08124f6af7f10cc98` | `rtb-0ffacb032b9943e43` |

### Day 3 완료 체크리스트

- [x] Compute + Network Resource Handoff 문서를 확인했다.
- [x] Region을 확인했다.
- [x] VPC ID를 확인했다.
- [x] VPC CIDR을 확인했다.
- [x] Public Subnet A의 ID, CIDR, AZ를 확인했다.
- [x] Public Subnet B의 ID, CIDR, AZ를 확인했다.
- [x] 두 Public Subnet이 서로 다른 AZ에 있는지 확인했다.
- [x] Internet Gateway ID를 확인했다.
- [x] Public Route Table ID를 확인했다.
- [x] `10.0.0.0/16 → local` 경로를 확인했다.
- [x] `0.0.0.0/0 → Internet Gateway` 경로를 확인했다.
- [x] Public Subnet A의 Route Table 연결을 확인했다.
- [x] Public Subnet B의 Route Table 연결을 확인했다.
- [x] Observability Checklist에 Network Handoff 값을 반영했다.
- [ ] AWS Console에서 Handoff 값과 실제 리소스를 직접 대조했다.
- [ ] Day 3 변경사항에 대한 PR을 생성했다.

### 현재 검증 완료 범위

- VPC
- Public Subnet A
- Public Subnet B
- Internet Gateway
- Public Route Table
- Default Route
- Public Subnet A/B Route Table Association

### 아직 검증하지 않은 항목

다음 리소스는 아직 생성되지 않았으므로 Day 3에서는 검증하지 않는다.

- ALB Security Group
- EC2 Security Group
- EC2 Instance
- EC2 Public IP
- Docker Container
- MiniPEP FastAPI
- Application Load Balancer
- Target Group
- EC2 CloudWatch Metric
- ALB CloudWatch Metric
- Target Health
- Docker/Application Log
- EC2 내부 `/health`
- ALB 외부 `/health`

### 확인 필요 사항

Public Subnet A의 Public IPv4 자동 할당은 현재 비활성화 상태이다.

Day 4 EC2 생성 시 다음 중 하나가 필요하다.

- EC2 생성 과정에서 Public IP 자동 할당 활성화
- Elastic IP 연결
- 별도의 접속 방식 사용

### Day 4 전달 요청

Compute + Network 담당자로부터 다음 값을 전달받는다.

- ALB Security Group ID
- EC2 Security Group ID
- EC2 Instance ID
- EC2 Public IP
- EC2 Subnet ID
- EC2 Availability Zone
- EC2 Status Check 결과
- SSH 또는 EC2 접속 검증 결과
- Host Port
- Docker Container Port

### 검증 결론

Compute + Network Resource Handoff 문서 기준으로 Day 3 네트워크 구성값과 연결 관계가 프로젝트 설계 기준에 일치한다.

현재 결과는 Handoff 문서를 기준으로 검토한 결과이다.


```