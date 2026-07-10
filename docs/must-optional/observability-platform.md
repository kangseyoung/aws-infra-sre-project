# Observability / Platform Must / Optional 정리

**담당자:** 권태욱
**파트:** Observability / Platform / IaC 보조 / Compute 보조

> 이 문서는 담당자가 직접 Must / Optional 범위를 정리하기 위한 템플릿입니다.
> 아래 내용은 확정된 범위가 아니며, 회의와 학습 내용을 바탕으로 직접 채웁니다.

---

## 1. 이 파트의 역할

### Observability

Observability는 서비스와 인프라가 정상적으로 동작하는지 확인하고, 문제가 발생했을 때 원인을 빠르게 찾을 수 있도록 도와주는 역할입니다.

이 프로젝트에서는 AWS CloudWatch를 중심으로 EC2, ALB, Target Group, Docker, Nginx의 상태를 확인합니다.

단순히 서버가 켜져 있는지 확인하는 것이 아니라, CPU 사용률, 네트워크 사용량, ALB 요청 수, 에러 수, Target Group Health Check, Nginx 로그, Docker 로그 등을 통해 서비스가 실제로 안정적으로 운영 가능한 상태인지 확인합니다.

특히 장애가 발생했을 때 다음과 같은 질문에 답할 수 있어야 합니다.

* 사용자의 요청이 ALB까지 들어오고 있는가?
* ALB가 EC2를 정상 대상으로 인식하고 있는가?
* EC2 인스턴스는 정상적으로 실행 중인가?
* Docker 컨테이너와 Nginx는 정상적으로 동작 중인가?
* 에러 로그는 어디에서 확인할 수 있는가?
* 장애 발생 시 어떤 순서로 확인해야 하는가?

### Platform

Platform은 애플리케이션이 배포되고 실행될 수 있는 공통 기반을 제공하는 역할입니다.

이 프로젝트에서 Platform은 사용자가 서비스에 접근하는 흐름과 애플리케이션이 실행되는 환경을 이해하고 정리하는 역할을 합니다.

기본 서비스 흐름은 다음과 같습니다.

사용자
  ↓
ALB
  ↓
Target Group
  ↓
EC2
  ↓
Docker / Nginx
  
CloudWatch는 ALB, Target Group, EC2, Nginx, Docker 상태를 모니터링
Platform 파트는 Compute, Network, IaC, CI/CD, Observability와 연결되는 중심 역할을 합니다.

즉, 애플리케이션이 어떤 환경에서 실행되고, 배포 후 어떤 항목을 확인해야 하며, 장애가 발생했을 때 어떤 구성 요소부터 점검해야 하는지 정리합니다.

### IaC 보조

IaC 보조는 인프라를 수동으로 생성하는 것이 아니라 코드로 정의하고 관리하는 흐름을 이해하고 돕는 역할입니다.

Terraform 같은 도구를 통해 서버, 네트워크, 보안 그룹, 모니터링 리소스 등이 코드로 관리되는 구조를 파악하고, 필요한 경우 변수 정리, output 추가, 문서화 등을 보조합니다.

### Compute 보조

Compute 보조는 애플리케이션이 실제로 실행되는 환경을 이해하고 정리하는 역할입니다.

VM, 컨테이너, 서버리스 등 어떤 방식으로 서비스가 실행되는지 확인하고, 네트워크 연결, 포트, 로그, 리소스 사용률 등을 Observability와 연결해서 이해합니다.

---

## 2. 초보자가 꼭 알아야 할 핵심 개념

### Observability 핵심 개념

* **Metric:** CPU, Memory, Disk, Network처럼 숫자로 확인할 수 있는 지표
* **Log:** 애플리케이션이나 서버에서 발생한 기록
* **Alert:** 특정 조건이 발생했을 때 알림을 보내는 기능
* **Dashboard:** 여러 지표와 로그 상태를 한눈에 볼 수 있는 화면
* **Health Check:** 
  * 서비스가 정상적으로 응답하는지 확인하는 방법
  * ALB가 Target Group에 등록된 EC2/Nginx가 정상인지 확인하는 데 사용
* **Log Group:** CloudWatch Logs에서 로그를 저장하는 단위


### Platform 핵심 개념

* **배포 환경:** 애플리케이션이 실행되는 공간
* **운영 환경:** 사용자가 실제로 접근하는 서비스 환경
* **공통 인프라:** 여러 서비스가 함께 사용하는 기반 요소
* **CI/CD:** 코드 변경 후 빌드, 테스트, 배포를 자동화하는 흐름
* **ALB:** 외부 사용자의 HTTP 요청을 받아 Target Group으로 전달하는 로드밸런서
* **Target Group:** ALB가 요청을 전달할 대상 EC2 목록
* **운영 체크리스트:** 배포 후 확인해야 할 항목들

---

## 3. Must 범위

<!-- 2주 안에 반드시 구현하거나 이해해야 하는 범위 작성 -->

### Observability Must

* CloudWatch 기본 개념
  Metric
  Log
  Dashboard
  Alarm
  Log Group
  Log Stream

* EC2 기본 지표 확인
  CPUUtilization
  NetworkIn
  NetworkOut
  StatusCheckFailed

* ALB 기본 지표 확인
  RequestCount
  TargetResponseTime
  HTTPCode_ELB_4XX_Count
  HTTPCode_ELB_5XX_Count
  HTTPCode_Target_4XX_Count
  HTTPCode_Target_5XX_Count

* Target Group Health Check 확인
  HealthyHostCount
  UnHealthyHostCount
  Health Check Path
  Target 상태 확인
  Target이 Unhealthy가 되는 원인 정리

* 어떤 로그를 확인해야 하는지 정리
  Nginx access log
  Nginx error log
  Docker container log
  EC2 system log
  CloudWatch Logs에서 확인 가능한 로그

* CloudWatch Logs 확인 범위 정리
  Log Group
  Log Stream
  로그가 정상적으로 수집되고 있는지 확인
  로그가 보이지 않을 때 CloudWatch Agent, 로그 경로, 권한 설정을 확인

* 기본 대시보드에 들어갈 항목 정리
  EC2 CPUUtilization
  EC2 NetworkIn / NetworkOut
  EC2 StatusCheckFailed
  ALB RequestCount
  ALB TargetResponseTime
  ALB 4xx / 5xx Error
  Target Group HealthyHostCount
  Target Group UnHealthyHostCount

* 기본 Alarm 기준 정리
  EC2 CPUUtilization 80% 초과
  EC2 StatusCheckFailed 1 이상
  ALB 5xx Error 증가
  Target 5xx Error 증가
  Target Group UnHealthyHostCount 1 이상
  TargetResponseTime 증가

* 장애 발생 시 먼저 확인할 지표 정리
  ALB RequestCount
  ALB 4xx / 5xx Error
  TargetResponseTime
  HealthyHostCount
  UnHealthyHostCount
  EC2 CPUUtilization
  EC2 StatusCheckFailed
  Nginx access log
  Nginx error log
  Docker logs

* 장애 발생 시 확인 순서 문서화

1. ALB DNS 접속 가능 여부 확인
2. ALB RequestCount 확인
3. ALB 4xx / 5xx 지표 확인
4. Target Group Health Check 확인
5. HealthyHostCount / UnHealthyHostCount 확인
6. EC2 인스턴스 상태 확인
7. EC2 Security Group 확인
8. Docker 컨테이너 실행 상태 확인
9. Nginx 실행 상태 확인
10. Nginx access log / error log 확인


### Platform Must

* Platform이 전체 아키텍처에서 제공하는 역할 정리
  사용자가 서비스에 접근하는 경로 제공
  애플리케이션이 실행되는 환경 제공
  배포 후 상태 확인 기준 제공
  장애 발생 시 확인 순서 제공

* 서비스 요청 흐름 이해

  사용자
    ↓
  ALB
    ↓
  Target Group
    ↓
  EC2
    ↓
  Docker / Nginx
    ↓
  CloudWatch
* ALB / Target Group 구조 이해
  ALB
  Listener
  Target Group
  Health Check
  Security Group
* 애플리케이션 배포 흐름 이해
  코드 변경
  빌드
  배포
  EC2에서 실행
  Docker / Nginx 동작 확인
  CloudWatch로 모니터링
* EC2 기본 운영 이해
  EC2 인스턴스 상태 확인
  Public IP 확인
  SSH 접속 방법 이해
  Security Group Inbound Rule 확인
  Instance Status Check 확인
* Docker / Nginx 기본 운영 이해
  Docker Image
  Docker Container
  Port Mapping
  Nginx 실행 상태
  Nginx access log
  Nginx error log


* 배포 후 확인해야 할 기본 항목 정리

  1. ALB DNS로 접속 가능한가?
  2. ALB Listener가 정상적으로 설정되어 있는가?
  3. Target Group에 EC2가 등록되어 있는가?
  4. Target Group Health Check가 Healthy인가?
  5. EC2 인스턴스가 running 상태인가?
  6. EC2 Security Group에서 필요한 포트가 열려 있는가?
  7. Docker 컨테이너가 실행 중인가?
  8. Nginx가 정상적으로 실행 중인가?
  9. CloudWatch에서 EC2 Metric이 보이는가?
  10. CloudWatch에서 ALB Metric이 보이는가?
  11. CloudWatch Logs에서 로그 확인이 가능한가?
  
* 최종 아키텍처에서 Platform 파트 설명 가능하도록 문서화
  사용자는 ALB DNS로 접속
  ALB는 Target Group으로 요청 전달
  Target Group은 EC2 상태를 Health Check로 확인
  EC2 내부에서 Docker / Nginx 실행
  CloudWatch에서 지표와 로그 확인

---

## 4. Optional 범위

<!-- 시간이 남으면 도전할 범위 작성 -->

### Observability Optional

* 고급 Observability 도구 개념 학습(High Priority)
  OpenTelemetry
  AWS X-Ray
  Prometheus
  Grafana
* SNS 알림 연동
  SNS Topic 생성
  이메일 구독 설정
  CloudWatch Alarm과 SNS 연결
  알림 수신 테스트
* 에러 로그 기반 알림 구성
  Nginx error log 기반 알림
  5xx 로그 기반 알림
  특정 에러 메시지 기반 Metric Filter 구성
* Log Metric Filter 구성
  로그에서 특정 패턴 추출
  에러 발생 횟수를 Metric으로 변환
  변환된 Metric을 Alarm과 연결
* 대시보드 시각화 개선
  EC2 지표 위젯 추가
  ALB 지표 위젯 추가
  Target Group 상태 위젯 추가
  로그 확인 링크 정리
  포트폴리오용 Dashboard 캡처 정리
* 장애 시나리오를 정해서 테스트
  EC2 중지
  Docker 컨테이너 중지
  Nginx 중지
  Security Group 80번 포트 차단
  Health Check Path 오류 설정
  Target Group에서 EC2 제거

* CloudWatch Agent 설정 학습
  EC2 Memory 지표 수집
  EC2 Disk 지표 수집
  Nginx access log / error log 수집
  Docker log 수집 가능 여부 확인
  CloudWatch Logs로 로그 전송 설정

### Platform Optional

* Platform 운영 체크리스트 작성
  배포 전 확인 항목
  배포 후 확인 항목
  장애 발생 시 확인 항목
  복구 후 확인 항목
* 배포 실패 시 확인할 항목 정리
  GitHub Actions 로그
  SSH 접속 여부
  Docker build 실패 여부
  Docker container 실행 여부
  Nginx 설정 오류 여부
  ALB Health Check 상태
* CI/CD와 연결된 자동 배포 흐름까지 정리
  코드 push
  GitHub Actions 실행
  EC2 접속
  Docker image build 또는 pull
  Container restart
  ALB Health Check 확인
  CloudWatch Metric 확인
* Terraform으로 Platform 리소스 관리 학습
  aws_instance
  aws_lb
  aws_lb_target_group
  aws_lb_listener
  aws_security_group
  aws_cloudwatch_dashboard
  aws_cloudwatch_metric_alarm
  variable
  output
* Runbook 문서화
  ALB 502 장애 대응 문서
  ALB 503 장애 대응 문서
  EC2 접속 불가 대응 문서
  Nginx 장애 대응 문서
  CloudWatch Logs 미수집 대응 문서

---

## 5. Must로 정한 이유

<!-- 왜 이 항목들이 꼭 필요한지 작성 -->

최종 아키텍처를 설명할 때 빠지면 안 되는 핵심 내용으로 정했습니다.

Observability는 운영 가능한 서비스를 만들기 위해 반드시 필요합니다. 서비스가 배포되어도 상태를 확인할 수 없다면 장애 대응이 어렵기 때문에 기본 지표, 로그, 대시보드, Health Check, 장애 확인 흐름은 Must로 정했습니다.

Platform은 애플리케이션이 실행되는 기반이기 때문에 전체 구조를 이해하는 데 꼭 필요합니다. 사용자는 EC2에 직접 접근하는 것이 아니라 ALB를 통해 서비스에 접근하고, ALB는 Target Group에 등록된 EC2로 요청을 전달합니다. EC2 내부에서는 Docker / Nginx가 실행되고, CloudWatch에서 상태와 로그를 확인합니다.

이 흐름을 이해하지 못하면 장애 발생 시 어디부터 확인해야 하는지 판단하기 어렵습니다.

---

## 6. Optional로 뺀 이유

<!-- 왜 이 항목들은 후순위로 두는지 작성 -->

Optional 범위는 있으면 좋지만, 프로젝트 전체 완성에 반드시 필요하지는 않은 고도화 항목으로 정했습니다.

CloudWatch Agent, SNS 알림, Metric Filter, 장애 시나리오 테스트, 고급 대시보드 구성은 포트폴리오 완성도를 높여줄 수 있습니다. 하지만 초반 2주 안에 모두 완성하기에는 범위가 넓고, 기본 구조를 이해하지 못한 상태에서 진행하면 오히려 핵심 흐름을 놓칠 수 있습니다.

---

## 7. 다른 파트와 연결되는 부분

<!-- 다른 담당 파트와 연결되는 지점 작성 -->

### Observability 연결

#### Compute와 연결

* 서버 또는 컨테이너의 CPU, Memory, Disk, Network 지표를 수집합니다.
* 애플리케이션 로그와 에러 로그를 확인합니다.

#### Platform과 연결

* 배포된 서비스가 정상적으로 운영되는지 확인합니다.
* 운영 상태를 대시보드로 확인할 수 있게 합니다.

#### Network와 연결

* 외부 요청이 정상적으로 들어오는지 확인합니다.
* 로드밸런서, 보안 그룹, 포트 문제를 확인합니다.

#### IaC와 연결

* 모니터링 리소스와 알림 설정을 코드로 관리할 수 있습니다.

### Platform 연결

#### IaC와 연결

* Platform 구성 요소를 코드로 생성하고 관리합니다.

#### Compute와 연결

* 애플리케이션 실행 환경을 제공합니다.

#### Network와 연결

* 사용자가 서비스에 접근할 수 있는 경로를 제공합니다.

#### CI/CD와 연결

* 코드 변경 사항을 Platform 환경에 배포합니다.

#### Observability와 연결

* 배포 후 서비스 상태를 확인합니다.

---

## 8. GitHub에 남기면 좋은 산출물

<!-- 문서, 다이어그램, 체크리스트, 설정 기록 등 GitHub에 남길 결과물 작성 -->

### 문서 산출물

* `docs/observability.md`

  * 모니터링 대상
  * CloudWatch Metric 정리
  * CloudWatch Logs 확인 방법
  * ALB / Target Group Health Check 확인 방법
  * 장애 시 확인 순서

* `docs/platform.md`

  * Platform 역할
  * 배포 흐름
  * 다른 파트와의 연결
  * EC2 / Docker / Nginx 실행 구조

* `docs/runbook/alb-502.md`

  * 502 Bad Gateway 발생 시 확인 순서
  * Target Group Health Check 확인
  * Nginx 포트 확인
  * Docker 컨테이너 상태 확인

* `docs/runbook/alb-503.md`

  * 503 Service Unavailable
  * 발생 시 확인 순서
  * Healthy Target 존재 여부 확인
  * Target Group 상태 확인

* `docs/runbook/ec2-nginx-down.md`

  * EC2 상태 확인
  * Docker 컨테이너 확인
  * Nginx 상태 확인
  * Nginx log 확인

### 체크리스트 산출물

* `docs/checklists/observability-checklist.md`
* `docs/checklists/platform-checklist.md`

### 포트폴리오용 산출물

* 전체 아키텍처 다이어그램
* 사용자 요청 흐름 다이어그램
* Observability 대시보드 캡처
* CloudWatch Alarm 설정 캡처
* CloudWatch Logs 확인 캡처
* 배포 흐름 다이어그램
* 장애 대응 흐름 정리
* README에 담당 파트 역할 정리

---

## 9. 2~3분 공유 요약

제가 맡은 파트는 Observability / Platform / IaC 보조 / Compute 보조입니다.

먼저 Observability는 서비스와 인프라가 정상적으로 동작하는지 확인하고, 문제가 생겼을 때 원인을 찾기 위한 역할입니다.

이번 프로젝트에서는 CloudWatch를 중심으로 EC2, ALB, Target Group, Docker, Nginx 상태를 확인합니다.

Must 범위로는 EC2의 CPUUtilization, NetworkIn, NetworkOut, StatusCheckFailed 같은 기본 지표와 ALB의 RequestCount, TargetResponseTime, 4xx / 5xx Error, Target Group의 HealthyHostCount와 UnHealthyHostCount를 확인하는 것을 잡았습니다.

또한 Nginx access log, Nginx error log, Docker log, CloudWatch Logs를 통해 장애 원인을 확인하는 방법도 Must로 정했습니다.

Platform은 애플리케이션이 배포되고 실행되는 공통 기반입니다.

이 프로젝트의 기본 흐름은 사용자가 ALB DNS로 접속하고, ALB가 Target Group에 등록된 EC2로 요청을 전달한 뒤, EC2 내부의 Docker / Nginx가 응답하는 구조입니다.

배포 후에는 ALB DNS 접속 가능 여부, Target Group Health Check, EC2 상태, Security Group, Docker 컨테이너 상태, Nginx 상태, CloudWatch 지표와 로그를 확인해야 합니다.

장애가 발생하면 ALB 상태, Target Group Health Check, EC2 상태, Security Group, Docker / Nginx 상태, CloudWatch Logs 순서로 확인합니다.

Optional 범위는 CloudWatch Agent, SNS 알림, Metric Filter, 장애 시나리오 테스트, Dashboard 개선, Runbook 문서화처럼 있으면 좋지만 프로젝트 완성에 필수는 아닌 항목으로 분리했습니다.

최종적으로 GitHub에는 Observability 정리 문서, Platform 역할 문서, 체크리스트, 장애 대응 Runbook, CloudWatch Dashboard 캡처를 남기는 것을 목표로 하겠습니다.
