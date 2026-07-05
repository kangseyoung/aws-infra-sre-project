# Security + SRE Must / Optional 정리

담당자: 박찬혁
파트: Security + SRE 보조

> 이 문서는 담당자가 직접 Must / Optional 범위를 정리하기 위한 템플릿입니다.
> 아래 내용은 확정된 범위가 아니며, 회의와 학습 내용을 바탕으로 직접 채웁니다.

## 1. 이 파트의 역할

Security + SRE 보조 파트는 앱이 AWS 인프라 위에서 안전하게 실행되고, 문제가 생겼을 때 어디를 확인해야 하는지 정리하는 역할을 맡는다.

이번 프로젝트의 기본 아키텍처는 다음과 같다.

```text
사용자 → ALB → EC2 → Docker / Nginx / App → CloudWatch
```

이 구조에서 Security + SRE 보조 파트는 다음 내용을 중점적으로 확인한다.

* 사용자가 EC2에 직접 접근하지 않고 ALB를 통해 접근하도록 구성되어 있는가
* ALB와 EC2의 Security Group이 적절히 분리되어 있는가
* SSH 22번 포트가 불필요하게 전체 공개되어 있지 않은가
* EC2 내부에 Access Key를 직접 저장하지 않고 IAM Role을 사용하는가
* CloudWatch에서 EC2, ALB, 애플리케이션 상태를 확인할 수 있는가
* 장애 발생 시 어떤 순서로 확인해야 하는지 Runbook으로 정리되어 있는가
* `.env`, `.pem`, `terraform.tfstate` 같은 민감정보가 GitHub에 올라가지 않도록 관리되고 있는가

즉, 이 파트는 단순히 “앱이 뜨는지”만 보는 것이 아니라, 앱이 안전하게 접근되고 운영 중 문제를 추적할 수 있는지 확인하는 역할이다.

---

## 2. 초보자가 꼭 알아야 할 핵심 개념

### 1. Security Group

Security Group은 AWS 리소스 앞에 붙는 네트워크 방화벽이다.

이번 프로젝트에서는 주로 ALB와 EC2에 Security Group이 붙는다.

```text
사용자 → ALB Security Group → EC2 Security Group
```

핵심은 다음과 같다.

* Inbound는 외부에서 해당 리소스 안으로 들어오는 트래픽이다.
* Outbound는 해당 리소스에서 외부로 나가는 트래픽이다.
* ALB는 외부 사용자의 HTTP 요청을 받아야 하므로 80번 포트가 열려 있어야 한다.
* EC2는 외부 전체가 아니라 ALB에서 들어오는 요청만 받도록 제한하는 것이 좋다.
* SSH 22번 포트는 `0.0.0.0/0`으로 열지 않는 것이 좋다.

예상 구조:

```text
ALB Security Group
- Inbound: HTTP 80 from 0.0.0.0/0
- Optional: HTTPS 443 from 0.0.0.0/0

EC2 Security Group
- Inbound: HTTP 80 또는 앱 포트 from ALB Security Group
- SSH 22는 필요한 경우 내 IP만 허용
```

---

### 2. IAM User / Role / Policy

IAM은 AWS에서 “누가 어떤 리소스에 어떤 작업을 할 수 있는지”를 제어하는 권한 관리 서비스이다.

이번 프로젝트에서 중요한 개념은 다음과 같다.

* IAM User: 사람이 AWS Console이나 CLI에 접근할 때 사용하는 계정
* IAM Role: EC2 같은 AWS 서비스가 다른 AWS 서비스를 사용할 때 부여받는 역할
* IAM Policy: 어떤 작업을 허용하거나 거부할지 적어둔 권한 문서

이번 프로젝트에서는 EC2가 CloudWatch Logs로 로그를 보내야 할 수 있다.

이때 EC2 내부에 Access Key를 직접 저장하는 방식은 위험하다.

좋은 방식은 다음과 같다.

```text
EC2 → IAM Role → CloudWatch Logs
```

즉, EC2에 IAM Role을 붙여서 필요한 AWS 서비스에 접근하게 하는 것이 좋다.

---

### 3. Access Key 및 민감정보

Access Key는 AWS CLI나 Terraform이 AWS API를 호출할 때 사용할 수 있는 인증 정보이다.

하지만 Access Key가 GitHub에 올라가면 AWS 계정이 외부에 노출될 수 있다.

절대 커밋하면 안 되는 항목은 다음과 같다.

```text
AWS Access Key
AWS Secret Key
.pem
.env
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfvars
```

이 파트에서는 `.gitignore`에 민감 파일이 포함되어 있는지, 코드나 문서에 Access Key가 직접 적혀 있지 않은지 확인해야 한다.

---

### 4. CloudWatch

CloudWatch는 AWS 리소스의 상태와 로그를 확인하는 모니터링 서비스이다.

이번 프로젝트에서는 다음 항목을 확인할 수 있어야 한다.

EC2 지표:

* CPUUtilization
* NetworkIn / NetworkOut
* StatusCheckFailed

ALB 지표:

* RequestCount
* TargetResponseTime
* HTTPCode_Target_5XX_Count
* UnHealthyHostCount

로그 후보:

* Nginx access log
* Nginx error log
* Application log

기본 지표는 어느 정도 자동으로 볼 수 있지만, Nginx 로그나 애플리케이션 로그를 CloudWatch Logs로 보내려면 CloudWatch Agent와 IAM Role 설정이 필요할 수 있다.

---

### 5. Runbook

Runbook은 장애가 발생했을 때 어떤 순서로 확인하고 대응할지 정리한 문서이다.

예를 들어 ALB 주소로 접속이 안 될 때는 다음 순서로 확인할 수 있다.

```text
1. ALB DNS 주소가 맞는지 확인
2. ALB Listener가 80 또는 443으로 열려 있는지 확인
3. Target Group에서 EC2가 healthy 상태인지 확인
4. EC2가 running 상태인지 확인
5. EC2 Security Group이 ALB 요청을 허용하는지 확인
6. EC2 내부에서 Docker / Nginx / App이 실행 중인지 확인
7. EC2 내부에서 curl localhost로 앱 응답 확인
8. CloudWatch Logs에서 에러 확인
```

SRE 관점에서는 앱을 띄우는 것만큼이나, 문제가 생겼을 때 어디를 봐야 하는지 정리하는 것이 중요하다.

---

## 3. Must 범위

2주 안에 반드시 이해하거나 구현해야 하는 범위이다.

### 1. Security Group 기본 구조 이해

ALB와 EC2의 Security Group을 분리해서 이해한다.

목표 구조:

```text
사용자 → ALB Security Group → EC2 Security Group
```

확인할 내용:

* ALB는 외부 사용자의 HTTP 요청을 받을 수 있어야 한다.
* EC2는 외부 전체가 아니라 ALB에서 들어오는 요청만 받는 것이 좋다.
* SSH 22번 포트를 `0.0.0.0/0`으로 열지 않는다.
* 불필요한 포트를 열지 않는다.
* ALB와 EC2의 Inbound / Outbound 방향을 이해한다.

---

### 2. IAM Role 기본 이해

EC2가 AWS 서비스를 사용할 때 Access Key를 EC2 내부에 저장하지 않고 IAM Role을 사용하는 이유를 이해한다.

이번 프로젝트에서 필요한 IAM Role 예시:

```text
EC2 → IAM Role → CloudWatch Logs
```

확인할 내용:

* IAM User, IAM Role, IAM Policy의 차이
* EC2 Instance Role이 필요한 이유
* EC2 내부에 Access Key를 저장하면 안 되는 이유
* CloudWatch Logs 전송을 위해 EC2에 권한이 필요하다는 점

---

### 3. Access Key 및 민감정보 관리

GitHub에 올라가면 안 되는 파일과 정보를 정리한다.

절대 커밋하면 안 되는 항목:

```text
AWS Access Key
AWS Secret Key
.pem
.env
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfvars
```

확인할 내용:

* `.gitignore`에 민감 파일이 포함되어 있는지 확인
* Access Key가 코드나 문서에 직접 적혀 있지 않은지 확인
* 키 유출 시 대응 절차를 간단히 정리
* `.pem`, `.env`, `terraform.tfstate`가 왜 위험한지 이해

---

### 4. CloudWatch 기본 이해

CloudWatch가 서버 상태와 로그를 확인하는 서비스라는 것을 이해한다.

확인할 EC2 지표:

* CPUUtilization
* NetworkIn / NetworkOut
* StatusCheckFailed

확인할 ALB 지표:

* RequestCount
* TargetResponseTime
* HTTPCode_Target_5XX_Count
* UnHealthyHostCount

확인할 로그 후보:

* Nginx access log
* Nginx error log
* Application log

---

### 5. 장애 대응 Runbook 작성

ALB 주소로 접속이 안 될 때 확인할 순서를 문서화한다.

기본 확인 순서:

```text
1. ALB DNS 주소가 맞는지 확인
2. ALB Listener가 80 또는 443으로 열려 있는지 확인
3. Target Group에서 EC2가 healthy 상태인지 확인
4. EC2가 running 상태인지 확인
5. EC2 Security Group이 ALB 요청을 허용하는지 확인
6. EC2 내부에서 Docker / Nginx / App이 실행 중인지 확인
7. EC2 내부에서 curl localhost로 앱 응답 확인
8. CloudWatch Logs에서 에러 확인
```

Runbook 후보:

* ALB 접속 실패 대응 Runbook
* Target Group unhealthy 대응 Runbook
* CloudWatch 로그 미수집 대응 Runbook
* Access Key 유출 대응 Runbook

이 중 최소 1개 이상은 작성하는 것을 Must로 둔다.

---

## 4. Optional 범위

시간이 남으면 도전할 범위이다.

### 1. SSM Session Manager 사용

SSH 키를 직접 사용하는 대신 SSM Session Manager로 EC2에 접속하는 방식을 공부한다.

목표:

```text
SSH 22번 포트를 열지 않고 EC2에 접속하기
```

필요한 내용:

* EC2에 `AmazonSSMManagedInstanceCore` 권한 부여
* SSM Agent 상태 확인
* Session Manager 접속 테스트
* SSH 방식과 SSM 방식의 차이 정리

---

### 2. CloudWatch Agent를 통한 로그 전송

EC2 내부의 Nginx 로그 또는 애플리케이션 로그를 CloudWatch Logs로 전송한다.

대상 로그 후보:

```text
/var/log/nginx/access.log
/var/log/nginx/error.log
Docker container log
Application log
```

확인할 내용:

* CloudWatch Agent 설치 여부
* EC2 IAM Role에 CloudWatch Logs 권한이 있는지 확인
* Log Group / Log Stream이 생성되는지 확인
* 실제 요청 후 access log가 CloudWatch에 들어오는지 확인

---

### 3. CloudWatch Alarm 생성

간단한 장애 감지용 Alarm을 만든다.

Alarm 후보:

* EC2 CPUUtilization > 80%
* ALB UnHealthyHostCount > 0
* ALB HTTPCode_Target_5XX_Count > 0

확인할 내용:

* 어떤 지표를 기준으로 Alarm을 만들지 정하기
* 임계값을 어느 정도로 설정할지 정하기
* Alarm 상태가 OK / ALARM으로 바뀌는지 확인
* 필요하면 SNS 이메일 알림 연결

---

### 4. Access Key 유출 대응 Runbook 작성

Access Key가 GitHub에 올라갔을 때의 대응 순서를 문서화한다.

예상 대응 순서:

```text
1. 유출된 Access Key 비활성화
2. Access Key 삭제
3. 새 Access Key 발급 여부 검토
4. CloudTrail에서 사용 이력 확인
5. GitHub commit history에서 민감정보 제거
6. .gitignore 및 팀 규칙 수정
7. 팀원에게 유출 사실과 재발 방지 방법 공유
```

---

### 5. Terraform 보안 체크

Terraform을 사용할 때 민감정보와 state 파일 관리 방식을 정리한다.

확인할 내용:

* `terraform.tfstate`를 GitHub에 올리지 않는 이유
* `.terraform/` 디렉토리를 커밋하지 않는 이유
* `*.tfvars` 파일 관리 주의점
* Terraform 실행 권한을 과도하게 주지 않는 방법
* Terraform 실행 시 사용하는 AWS Access Key 관리 방식

---

### 6. Security Group 점검 체크리스트 작성

ALB와 EC2의 Security Group 설정을 점검하는 체크리스트를 만든다.

체크 항목:

* ALB Inbound에 HTTP 80이 열려 있는가
* HTTPS를 사용할 경우 443이 열려 있는가
* EC2 Inbound는 ALB Security Group에서 오는 요청만 허용하는가
* SSH 22번 포트가 `0.0.0.0/0`으로 열려 있지 않은가
* 사용하지 않는 포트가 열려 있지 않은가

---

## 5. Must로 정한 이유

Must 항목들은 이번 프로젝트의 기본 아키텍처가 정상적으로 동작하고, 최소한의 보안과 운영 확인이 가능하기 위해 반드시 필요한 내용이다.

### Security Group을 Must로 둔 이유

이번 프로젝트는 사용자가 ALB를 통해 EC2의 앱에 접속하는 구조이다.

이때 Security Group 설정이 잘못되면 다음 문제가 생길 수 있다.

* 사용자가 ALB에 접속하지 못함
* ALB가 EC2에 요청을 전달하지 못함
* EC2가 외부 전체에 직접 노출됨
* SSH 포트가 전체 공개되어 보안 위험이 커짐

따라서 ALB와 EC2의 Security Group 구조는 반드시 이해해야 한다.

---

### IAM Role을 Must로 둔 이유

EC2가 CloudWatch Logs 같은 AWS 서비스를 사용하려면 권한이 필요하다.

이때 EC2 내부에 Access Key를 직접 저장하면 키 유출 위험이 있다.

따라서 EC2에 IAM Role을 붙여 필요한 권한을 부여하는 방식을 이해해야 한다.

---

### 민감정보 관리를 Must로 둔 이유

GitHub에 Access Key, `.pem`, `.env`, `terraform.tfstate` 같은 파일이 올라가면 보안 사고로 이어질 수 있다.

특히 AWS Access Key가 유출되면 외부인이 AWS 리소스를 생성하거나 삭제할 수 있고, 비용 문제가 발생할 수 있다.

따라서 민감정보 관리와 `.gitignore` 확인은 반드시 필요하다.

---

### CloudWatch를 Must로 둔 이유

서비스가 배포된 이후에는 단순히 “페이지가 뜬다”에서 끝나는 것이 아니라, 서버 상태와 로그를 확인할 수 있어야 한다.

CloudWatch를 통해 EC2 상태, ALB 요청 수, 5xx 에러, Target 상태 등을 확인할 수 있다.

운영 관점에서 CloudWatch 기본 이해는 필수이다.

---

### Runbook 작성을 Must로 둔 이유

장애가 발생했을 때 아무 곳이나 확인하면 원인을 찾는 데 시간이 오래 걸린다.

Runbook이 있으면 ALB, Target Group, EC2, Security Group, Docker/Nginx, CloudWatch Logs 순서로 체계적으로 확인할 수 있다.

SRE 관점에서는 장애 대응 흐름을 문서화하는 것이 중요한 산출물이기 때문에 Must에 포함한다.

---

## 6. Optional로 뺀 이유

Optional 항목들은 실무적으로 의미가 크지만, 2주 프로젝트에서 반드시 모두 구현하기에는 시간이 부족할 수 있기 때문에 후순위로 둔다.

### SSM Session Manager를 Optional로 둔 이유

SSM Session Manager는 SSH보다 안전한 EC2 접속 방식이다.

하지만 EC2 IAM Role, SSM Agent, 네트워크 조건 등을 추가로 확인해야 하므로 초반 필수 범위보다는 후순위로 둔다.

기본 구조가 완성된 뒤 시간이 남으면 도전한다.

---

### CloudWatch Agent 로그 전송을 Optional로 둔 이유

CloudWatch 기본 지표는 비교적 쉽게 확인할 수 있지만, Nginx 로그나 애플리케이션 로그를 CloudWatch Logs로 보내려면 Agent 설치와 설정이 필요하다.

구현 시간이 부족할 수 있으므로, 기본 지표 확인을 Must로 두고 로그 전송은 Optional로 둔다.

---

### CloudWatch Alarm을 Optional로 둔 이유

Alarm은 운영 관점에서 중요하지만, 먼저 CloudWatch 지표를 이해하고 확인할 수 있어야 한다.

따라서 지표 확인을 Must로 두고, 알림 설정은 시간이 남으면 진행한다.

---

### Access Key 유출 대응 Runbook을 Optional로 둔 이유

Access Key 유출 대응은 보안 관점에서 중요하지만, 기본 Runbook을 먼저 작성하는 것이 우선이다.

ALB 접속 실패나 Target Group unhealthy 대응 Runbook을 먼저 작성한 뒤, 시간이 남으면 보안 사고 대응 Runbook으로 확장한다.

---

### Terraform 보안 체크를 Optional로 둔 이유

Terraform 보안 체크는 IaC 파트와 밀접하게 연결된다.

하지만 Terraform을 어디까지 사용할지 팀 범위가 확정되어야 구체적으로 정리할 수 있다.

따라서 기본 민감정보 관리와 `.gitignore` 확인을 Must로 두고, Terraform state 관리와 권한 점검은 Optional로 둔다.

---

## 7. 다른 파트와 연결되는 부분

Security + SRE 보조 파트는 다른 파트와 많이 연결된다.

### Compute + Network 파트와 연결

Compute + Network 파트는 VPC, Subnet, ALB, EC2, Security Group 구성을 담당한다.

Security + SRE 보조 파트는 이 설정이 보안상 적절한지 함께 확인한다.

연결 지점:

* ALB Security Group 설정
* EC2 Security Group 설정
* Public Subnet / Private Subnet 구조
* ALB Target Group Health Check
* EC2 접속 방식

확인 질문:

* EC2는 Public Subnet에 둘 예정인가?
* EC2 앱 포트는 몇 번인가?
* ALB Target Group 포트와 Health Check path는 무엇인가?
* SSH는 사용할 것인가, SSM을 사용할 것인가?

---

### Observability / Platform 파트와 연결

Observability 파트는 CloudWatch 지표, 로그, 알림 구성을 담당한다.

Security + SRE 보조 파트는 어떤 로그와 지표를 장애 대응에 사용할지 함께 정리한다.

연결 지점:

* EC2 Metrics
* ALB Metrics
* CloudWatch Logs
* CloudWatch Alarm
* 장애 대응 Runbook

확인 질문:

* CloudWatch에서 어떤 지표를 볼 것인가?
* Nginx 로그를 CloudWatch로 보낼 것인가?
* 애플리케이션 로그는 어디에 남는가?
* Alarm은 어떤 기준으로 만들 것인가?

---

### Terraform / IaC 파트와 연결

Terraform 파트는 AWS 리소스를 코드로 생성하고 관리한다.

Security + SRE 보조 파트는 Terraform 코드와 관련된 민감정보 관리, Security Group, IAM Role 설정을 확인한다.

연결 지점:

* Security Group Terraform 코드
* IAM Role Terraform 코드
* `.tfstate` 관리
* `.tfvars` 관리
* Access Key 관리

확인 질문:

* Terraform으로 어디까지 만들 예정인가?
* `terraform.tfstate`는 GitHub에 올라가지 않도록 되어 있는가?
* `.tfvars`에 민감정보가 들어가는가?
* Terraform 실행 권한은 어떻게 관리할 것인가?

---

### App / Compute 담당과 연결

앱이 어떤 방식으로 실행되는지에 따라 Security Group, Target Group, Health Check, Runbook 내용이 달라진다.

연결 지점:

* 앱 실행 포트
* Dockerfile
* Nginx 사용 여부
* Health Check 경로
* 애플리케이션 로그 위치

확인 질문:

* 앱은 몇 번 포트에서 실행되는가?
* Docker Image는 어디서 가져오는가?
* Nginx는 컨테이너 안에서 사용하는가, EC2에 직접 설치하는가?
* Health Check path는 `/`인가, `/health`인가?
* 앱 로그는 파일로 남는가, Docker logs로 확인하는가?

---

## 8. GitHub에 남기면 좋은 산출물

Security + SRE 보조 파트에서 GitHub에 남기면 좋은 산출물은 다음과 같다.

### 1. Must / Optional 문서

경로 예시:

```text
docs/must-optional/park-chanhyeok.md
```

내용:

* Security + SRE 역할
* Must 범위
* Optional 범위
* Must / Optional로 나눈 이유
* 다른 파트와 연결되는 부분

---

### 2. Security Group 체크리스트

경로 예시:

```text
docs/security/security-group-checklist.md
```

내용:

* ALB Security Group 확인 항목
* EC2 Security Group 확인 항목
* SSH 22번 포트 확인
* 불필요한 포트 확인
* ALB에서 EC2로만 접근하도록 제한되어 있는지 확인

---

### 3. IAM Role 정리 문서

경로 예시:

```text
docs/security/iam-role-summary.md
```

내용:

* IAM User / Role / Policy 차이
* EC2 Instance Role이 필요한 이유
* EC2에 Access Key를 저장하면 안 되는 이유
* EC2 → CloudWatch Logs 권한 흐름

---

### 4. 민감정보 관리 체크리스트

경로 예시:

```text
docs/security/secret-management-checklist.md
```

내용:

* GitHub에 올리면 안 되는 파일 목록
* `.gitignore` 확인 항목
* Access Key 유출 위험
* `.pem`, `.env`, `terraform.tfstate` 관리 주의점

---

### 5. 장애 대응 Runbook

경로 예시:

```text
docs/runbook/alb-ec2-troubleshooting.md
```

내용:

* ALB 주소로 접속 안 될 때 확인 순서
* Target Group unhealthy일 때 확인 순서
* EC2 내부에서 Docker / Nginx / App 상태 확인
* CloudWatch Logs 확인 방법

---

### 6. CloudWatch 확인 문서

경로 예시:

```text
docs/observability/cloudwatch-basic-check.md
```

내용:

* EC2에서 확인할 지표
* ALB에서 확인할 지표
* 확인할 로그 후보
* 장애 대응에서 어떤 지표를 볼지 정리

---

## 9. 2~3분 공유 요약

다음 회의에서 팀원들에게 2~3분 정도로 공유할 내용은 다음과 같다.

이번 Security + SRE 보조 파트의 목표는 앱을 EC2에 올리는 것에서 끝내지 않고, 안전하게 접근되도록 설정하고 문제가 생겼을 때 확인 순서를 정리하는 것이다.

우리 프로젝트의 기본 구조는 다음과 같다.

```text
사용자 → ALB → EC2 → Docker / Nginx / App → CloudWatch
```

이 구조에서 Security 관점으로는 ALB와 EC2의 Security Group을 분리해서 봐야 한다. 사용자는 ALB에만 접근하고, EC2는 가능하면 ALB에서 들어오는 요청만 받도록 하는 것이 좋다. 또한 SSH 22번 포트는 `0.0.0.0/0`으로 열지 않는 것이 좋다.

IAM 관점에서는 EC2가 CloudWatch 같은 AWS 서비스를 사용할 때 Access Key를 EC2 내부에 저장하지 않고 IAM Role을 사용하는 이유를 이해해야 한다. EC2 내부에 Access Key를 저장하면 키 유출 위험이 있기 때문에, EC2 Instance Role을 사용하는 방식이 더 안전하다.

민감정보 관리도 Must로 두었다. AWS Access Key, Secret Key, `.pem`, `.env`, `terraform.tfstate`, `.terraform/`, `*.tfvars` 같은 파일은 GitHub에 올라가면 안 된다. `.gitignore`에 포함되어 있는지 확인할 필요가 있다.

SRE 관점에서는 CloudWatch에서 EC2와 ALB의 기본 지표를 확인할 수 있어야 한다. 예를 들어 EC2 CPU 사용률, 상태 검사 실패 여부, ALB 요청 수, 5xx 에러, unhealthy target 여부 등을 확인한다.

마지막으로 Runbook 작성을 Must로 넣었다. ALB 주소로 접속이 안 될 때 ALB DNS, Listener, Target Group health check, EC2 상태, Security Group, Docker/Nginx/App 실행 상태, CloudWatch Logs 순서로 확인할 수 있도록 문서화하는 것이 목표이다.

Optional로는 SSM Session Manager 사용, CloudWatch Agent 로그 전송, CloudWatch Alarm, Access Key 유출 대응 Runbook, Terraform 보안 체크를 넣었다. 이 항목들은 실무적으로 중요하지만 2주 안에 모두 구현하기에는 시간이 부족할 수 있어서 기본 구조가 완성된 뒤 도전하는 범위로 두었다.
