# Security + SRE Must / Optional

* 담당자: 박찬혁
* 파트: Security + SRE 보조

## Must

이번 2주 프로젝트에서 반드시 구현하거나 이해해야 하는 범위입니다.

### 1. Security Group 기본 구조 이해 및 검증

* ALB와 EC2의 Security Group 역할 구분
* ALB는 외부 HTTP 요청을 받을 수 있도록 설정
* EC2 앱 포트 `80`은 ALB Security Group에서 오는 요청만 허용
* SSH 22번 포트가 `0.0.0.0/0`으로 열려 있지 않은지 확인
* 사용하지 않는 포트가 열려 있지 않은지 확인
* 최종 연결 기준은 `ALB:80 -> Target Group:80 -> EC2 Host:80 -> Docker Container:8000`으로 확인

결과물:

* Security Group 점검 체크리스트

### 2. IAM Role 기본 이해

* IAM User, IAM Role, IAM Policy 차이 이해
* EC2가 AWS 서비스를 사용할 때 IAM Role을 사용하는 이유 이해
* EC2 내부에 AWS Access Key를 직접 저장하면 안 되는 이유 이해

결과물:

* EC2 IAM Role 사용 이유 정리

### 3. 민감정보 커밋 방지

다음 파일과 정보가 GitHub에 올라가지 않도록 확인합니다.

* AWS Access Key
* AWS Secret Key
* `.pem`
* `.env`
* `terraform.tfstate`
* `terraform.tfstate.*`
* `.terraform/`
* `*.tfvars`
* SQLite DB 파일

확인할 내용:

* `.gitignore` 설정 확인
* 코드와 문서에 실제 Access Key가 포함되어 있지 않은지 확인

결과물:

* 민감정보 관리 체크리스트

### 4. EC2 내부 로그 확인

CloudWatch Logs 중앙 수집 전에도 EC2 내부에서 기본 로그를 확인할 수 있어야 합니다.

* 실행 중인 Docker 컨테이너 확인
* `docker logs` 확인
* MiniPEP Application Log 확인
* Docker stdout 로그 확인
* EC2 내부에서 `curl -i http://localhost/health` 응답 확인
* `/api/equipment`, `/api/jobs` 요청 로그 확인
* Nginx는 초기 네트워크 연결 테스트용으로만 사용하고, 최종 검증 기준에서는 MiniPEP 로그를 우선 확인

결과물:

* Docker / MiniPEP App 로그 확인 방법 정리

### 5. 기본 장애 대응 Runbook 작성

ALB DNS로 MiniPEP 앱에 접속되지 않을 때의 기본 확인 순서를 작성합니다.

확인 순서:

1. ALB DNS 확인
2. ALB Listener 확인
3. Target Group 연결 확인
4. Target Health 확인
5. EC2 실행 상태 확인
6. Security Group 확인
7. Target Group Port와 앱 포트 확인
8. Health Check Path가 `/health`인지 확인
9. Docker / MiniPEP 앱 실행 상태 확인
10. EC2 내부 `curl -i http://localhost/health` 테스트
11. Docker / MiniPEP Application Log 확인

최종 성공 기준:

* ALB DNS를 통해 MiniPEP 앱이 정상 응답
* `http://ALB-DNS/health` 요청에 `200 OK` 응답
* Target Group 상태가 Healthy

결과물:

* 공통 장애 대응 Runbook 1개

---

## Optional

Must 범위를 완료한 뒤 시간이 남으면 도전하는 범위입니다.

### 1. SSM Session Manager 사용

* SSH 22번 포트를 열지 않고 EC2 접속
* EC2 IAM Role에 SSM 권한 부여
* SSM Agent 상태 확인
* Session Manager 접속 테스트

### 2. CloudWatch Agent 및 CloudWatch Logs 수집

* CloudWatch Agent 설치
* Docker stdout 또는 MiniPEP Application Log 수집
* Log Group / Log Stream 생성 확인
* 실제 로그 수집 확인

### 3. CloudWatch Alarm 및 SNS 연동

* EC2 CPU 사용률 Alarm
* ALB UnHealthyHostCount Alarm
* ALB Target 5XX Alarm
* SNS 이메일 알림 연동
* 실제 알림 수신 테스트

### 4. Access Key 유출 대응 Runbook

* 유출된 Access Key 비활성화 및 삭제
* CloudTrail 사용 이력 확인
* 비정상 리소스 및 비용 확인
* GitHub Commit History에서 민감정보 제거
* 재발 방지 방법 정리

### 5. Terraform 고급 보안 설정

* S3 Remote Backend
* Terraform State 암호화
* State Lock
* Terraform 실행 권한 최소화
* 안전한 AWS 인증 방식 적용

---

## Must로 정한 이유

Security Group, IAM Role, 민감정보 관리, 기본 로그 확인, 장애 대응 Runbook은 최종 아키텍처를 안전하게 구성하고 문제 발생 시 원인을 확인하기 위해 반드시 필요합니다.

특히 Security Group 설정이 잘못되면 ALB와 EC2가 연결되지 않거나 EC2가 외부에 직접 노출될 수 있습니다.

민감정보가 GitHub에 올라가면 보안 사고와 비용 문제가 발생할 수 있기 때문에 기본적인 커밋 방지는 반드시 확인해야 합니다.

또한 서비스 배포 후 문제가 발생했을 때 Docker, MiniPEP App 상태와 로그를 확인하고 정해진 순서대로 대응할 수 있어야 합니다.

---

## Optional로 정한 이유

SSM, CloudWatch Agent, Alarm, SNS, Terraform Remote Backend는 운영과 보안을 고도화하는 데 도움이 됩니다.

하지만 추가 IAM 권한, Agent 설치, 알림 설정, Backend 구성이 필요하기 때문에 2주 안에 반드시 완료해야 하는 핵심 범위에서는 제외했습니다.

Must 범위가 완료된 뒤 시간이 남으면 순서대로 도전합니다.

---

## 다른 파트와 연결되는 부분

* Compute + Network: ALB, EC2, Target Group, Security Group 실제 생성
* Observability / Platform: CloudWatch Metric, Target Health, Docker / MiniPEP App 로그 확인
* Security + SRE: Security Group, IAM, 민감정보 검증, 장애 대응 Runbook 작성
* Terraform / IaC: 생성된 리소스를 전달받아 코드화
* App Contract: 앱 포트, `/health`, Docker 실행 방법, 환경변수, 로그 확인 방법 정리

겹치는 항목은 삭제하지 않고, Security + SRE 파트에서는 보안 검증과 장애 대응 관점으로 정리합니다.

---

## 2~3분 공유 요약

Security + SRE 보조 파트의 Must 범위는 Security Group 안전 설정 검증, IAM Role 기본 이해, 민감정보 커밋 방지, EC2 내부 로그 확인, 기본 장애 대응 Runbook 작성입니다.

Security Group은 사용자가 ALB에만 접근하고 EC2 앱 포트는 ALB Security Group에서 오는 요청만 허용하도록 확인합니다. SSH 22번 포트는 `0.0.0.0/0`으로 열지 않고 사용하지 않는 포트도 닫혀 있는지 점검합니다.

IAM은 EC2 내부에 Access Key를 저장하지 않고 IAM Role을 사용하는 이유를 이해하는 범위로 잡았습니다.

민감정보 관리는 `.env`, `.pem`, `terraform.tfstate`, `.terraform/`, `*.tfvars`, AWS Access Key가 GitHub에 올라가지 않도록 `.gitignore`와 저장소를 확인합니다.

로그는 Must에서 EC2 내부의 `docker logs`와 MiniPEP Application Log를 확인할 수 있는 수준으로 정했습니다. CloudWatch Agent를 설치하고 로그를 CloudWatch Logs로 보내는 것은 Optional입니다.

장애 대응은 ALB, Target Group, EC2, Security Group, 앱 포트, Health Check, Docker, MiniPEP 앱, 로그 순서로 확인하는 공통 Runbook 1개를 작성합니다.

Optional에는 SSM Session Manager, CloudWatch Agent, CloudWatch Alarm과 SNS, Access Key 유출 대응 Runbook, Terraform 고급 보안 설정을 포함했습니다.
