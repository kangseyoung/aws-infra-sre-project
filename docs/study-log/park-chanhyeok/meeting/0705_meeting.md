# Security + SRE 보조 Must / Optional 정리

## 주요 목표

* 단순히 앱을 EC2에 올리는 것에서 끝나는 것이 아니라, 서비스가 안전하게 접근되도록 보안 설정을 이해하고, 문제가 생겼을 때 어디를 확인해야 하는지 정리한다.
* 이번 프로젝트의 기본 아키텍처는 다음과 같다.

```text
사용자 → ALB → EC2 → Docker / Nginx / App → CloudWatch
```

Security + SRE 관점에서는 다음 내용을 중점적으로 본다.

* 사용자가 EC2에 직접 접근하지 않고 ALB를 통해 접근하도록 구성되어 있는가?
* Security Group이 불필요하게 열려 있지 않은가?
* EC2에 Access Key를 직접 저장하지 않고 IAM Role을 사용하는가?
* CloudWatch에서 EC2, ALB, 애플리케이션 상태를 확인할 수 있는가?
* 장애 발생 시 확인 순서가 문서화되어 있는가?

---

# Must

<details>
<summary><strong>1. Security Group 기본 구조 이해</strong></summary>

ALB와 EC2의 Security Group을 분리해서 이해한다.

### 목표 구조

```text
사용자 → ALB Security Group → EC2 Security Group
```

### 확인할 내용

* ALB는 외부 사용자의 HTTP 요청을 받을 수 있어야 한다.
* EC2는 외부 전체가 아니라 ALB에서 들어오는 요청만 받는 것이 좋다.
* SSH 22번 포트를 `0.0.0.0/0`으로 열지 않는다.
* 불필요한 포트를 열지 않는다.

### 예상 설정

#### ALB Security Group

* Inbound: HTTP 80 from `0.0.0.0/0`
* Optional: HTTPS 443 from `0.0.0.0/0`

#### EC2 Security Group

* Inbound: HTTP 80 또는 앱 포트 from ALB Security Group
* SSH 22는 필요한 경우 내 IP만 허용

</details>

---

<details>
<summary><strong>2. EC2가 AWS 서비스를 사용할 때 IAM Role을 사용하는 이유 이해</strong></summary>

EC2가 AWS 서비스를 사용할 때 Access Key를 EC2 내부에 저장하지 않고 IAM Role을 사용하는 이유를 이해한다.

### 이번 프로젝트에서 필요한 IAM Role 예시

```text
EC2 → IAM Role → CloudWatch Logs
```

### 확인할 내용

* IAM User, IAM Role, IAM Policy의 차이
* EC2 Instance Role이 필요한 이유
* EC2 내부에 Access Key를 저장하면 안 되는 이유
* CloudWatch Logs 전송을 위해 EC2에 권한이 필요하다는 점

</details>

---

<details>
<summary><strong>3. Access Key 및 민감정보 관리</strong></summary>

GitHub에 올라가면 안 되는 파일과 정보를 정리한다.

### 절대 커밋하면 안 되는 항목

* AWS Access Key
* AWS Secret Key
* `.pem`
* `.env`
* `terraform.tfstate`
* `terraform.tfstate.*`
* `.terraform/`
* `*.tfvars`

### 확인할 내용

* `.gitignore`에 민감 파일이 포함되어 있는지 확인
* Access Key가 코드나 문서에 직접 적혀 있지 않은지 확인
* 키 유출 시 대응 절차를 간단히 정리

</details>

---

<details>
<summary><strong>4. CloudWatch 기본 이해</strong></summary>

CloudWatch가 서버 상태와 로그를 확인하는 서비스라는 것을 이해한다.

### EC2에서 확인할 지표

* CPUUtilization
* NetworkIn / NetworkOut
* StatusCheckFailed

### ALB에서 확인할 지표

* RequestCount
* TargetResponseTime
* HTTPCode_Target_5XX_Count
* UnHealthyHostCount

### 확인할 로그 후보

* Nginx access log
* Nginx error log
* Application log

</details>

---

<details>
<summary><strong>5. 장애 대응 Runbook 작성</strong></summary>

ALB 주소로 접속이 안 될 때 확인할 순서를 문서화한다.

### 기본 확인 순서

1. ALB DNS 주소가 맞는지 확인
2. ALB Listener가 80 또는 443으로 열려 있는지 확인
3. Target Group에서 EC2가 healthy 상태인지 확인
4. EC2가 running 상태인지 확인
5. EC2 Security Group이 ALB 요청을 허용하는지 확인
6. EC2 내부에서 Docker / Nginx / App이 실행 중인지 확인
7. EC2 내부에서 `curl localhost`로 앱 응답 확인
8. CloudWatch Logs에서 에러 확인

</details>

---

# Optional

<details>
<summary><strong>1. SSM Session Manager 사용</strong></summary>

SSH 키를 직접 사용하는 대신 SSM Session Manager로 EC2에 접속하는 방식을 공부한다.

### 목표

```text
SSH 22번 포트를 열지 않고 EC2에 접속하기
```

### 필요한 내용

* EC2에 `AmazonSSMManagedInstanceCore` 권한 부여
* SSM Agent 상태 확인
* Session Manager 접속 테스트
* SSH 방식과 SSM 방식의 차이 정리

### 기대 효과

* `.pem` 키 관리 부담 감소
* SSH 22번 포트 노출 감소
* EC2 접속 이력을 AWS에서 더 잘 추적 가능

</details>

---

<details>
<summary><strong>2. CloudWatch Agent를 통한 로그 전송</strong></summary>

EC2 내부의 Nginx 로그 또는 애플리케이션 로그를 CloudWatch Logs로 전송한다.

### 대상 로그 후보

```text
/var/log/nginx/access.log
/var/log/nginx/error.log
Docker container log
Application log
```

### 확인할 내용

* CloudWatch Agent 설치 여부
* EC2 IAM Role에 CloudWatch Logs 권한이 있는지 확인
* Log Group / Log Stream이 생성되는지 확인
* 실제 요청 후 access log가 CloudWatch에 들어오는지 확인

### 기대 효과

* EC2에 직접 접속하지 않아도 로그 확인 가능
* 장애 발생 시 AWS Console에서 로그 기반 원인 분석 가능

</details>

---

<details>
<summary><strong>3. CloudWatch Alarm 생성</strong></summary>

간단한 장애 감지용 Alarm을 만든다.

### Alarm 후보

```text
EC2 CPUUtilization > 80%
ALB UnHealthyHostCount > 0
ALB HTTPCode_Target_5XX_Count > 0
```

### 확인할 내용

* 어떤 지표를 기준으로 Alarm을 만들지 정하기
* 임계값을 어느 정도로 설정할지 정하기
* Alarm 상태가 OK / ALARM으로 바뀌는지 확인
* 필요하면 SNS 이메일 알림 연결

### 기대 효과

* 문제가 생겼을 때 직접 계속 확인하지 않아도 이상 상태를 감지 가능
* SRE 관점에서 모니터링과 알림 구조를 경험할 수 있음

</details>

---

<details>
<summary><strong>4. Access Key 유출 대응 Runbook 작성</strong></summary>

Access Key가 GitHub에 올라갔을 때의 대응 순서를 문서화한다.

### 예상 대응 순서

1. 유출된 Access Key 비활성화
2. Access Key 삭제
3. 새 Access Key 발급 여부 검토
4. CloudTrail에서 사용 이력 확인
5. GitHub commit history에서 민감정보 제거
6. `.gitignore` 및 팀 규칙 수정
7. 팀원에게 유출 사실과 재발 방지 방법 공유

### 확인할 내용

* Access Key가 유출되면 왜 위험한지 정리
* 키 비활성화와 삭제의 차이 이해
* CloudTrail에서 API 호출 이력을 확인하는 방법 조사
* GitHub에 민감정보가 올라갔을 때 단순 삭제만으로는 부족하다는 점 이해

### 기대 효과

* 실제 보안 사고 발생 시 당황하지 않고 대응 가능
* Security 역할의 결과물로 포트폴리오에 남기기 좋음

</details>

---

<details>
<summary><strong>5. Terraform 보안 체크</strong></summary>

Terraform을 사용할 때 민감정보와 state 파일 관리 방식을 정리한다.

### 확인할 내용

* `terraform.tfstate`를 GitHub에 올리지 않는 이유
* `.terraform/` 디렉토리를 커밋하지 않는 이유
* `*.tfvars` 파일 관리 주의점
* Terraform 실행 권한을 과도하게 주지 않는 방법
* Terraform 실행 시 사용하는 AWS Access Key 관리 방식

### 커밋하면 안 되는 Terraform 관련 항목

```text
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfvars
crash.log
override.tf
override.tf.json
```

### 기대 효과

* Terraform 사용 중 민감정보 유출 방지
* 인프라 코드 관리 시 보안상 주의해야 할 부분 이해
* IaC 작업자와 협업할 때 확인해야 할 보안 기준 마련

</details>

---

<details>
<summary><strong>6. Security Group 점검 체크리스트 작성</strong></summary>

ALB와 EC2의 Security Group 설정을 점검하는 체크리스트를 만든다.

### 체크 항목

* ALB Inbound에 HTTP 80이 열려 있는가?
* HTTPS를 사용할 경우 443이 열려 있는가?
* EC2 Inbound는 ALB Security Group에서 오는 요청만 허용하는가?
* SSH 22번 포트가 `0.0.0.0/0`으로 열려 있지 않은가?
* 사용하지 않는 포트가 열려 있지 않은가?
* Outbound 설정이 필요한 범위 내에서 열려 있는가?

### 기대 효과

* 보안 설정을 감으로 확인하지 않고 기준에 따라 확인 가능
* 프로젝트 발표 시 Security 관점의 역할을 명확하게 설명 가능

</details>

---

<details>
<summary><strong>7. Target Group Unhealthy 대응 문서 작성</strong></summary>

ALB Target Group에서 EC2가 unhealthy 상태가 되었을 때 확인할 순서를 정리한다.

### 확인 순서

1. EC2가 running 상태인지 확인
2. EC2 Status Check가 통과했는지 확인
3. Target Group Health Check path가 맞는지 확인
4. Target Group Health Check port가 앱 포트와 맞는지 확인
5. EC2 Security Group이 ALB 요청을 허용하는지 확인
6. EC2 내부에서 Docker / Nginx / App 실행 상태 확인
7. EC2 내부에서 `curl localhost` 또는 `curl localhost:포트`로 응답 확인
8. CloudWatch Logs에서 에러 확인

### 기대 효과

* ALB 연결 장애 발생 시 원인을 빠르게 좁힐 수 있음
* SRE 관점에서 장애 대응 흐름을 문서화할 수 있음

</details>

---

## 최종 목표

이번 프로젝트에서 Security + SRE 보조 역할의 최종 목표는 다음과 같다.

```text
ALB → EC2 → Docker / Nginx / App 구조에서
Security Group, IAM Role, CloudWatch, 장애 대응 흐름을 이해하고
실제 운영 관점에서 확인해야 할 내용을 문서화한다.
```

최종적으로 설명할 수 있어야 하는 내용은 다음과 같다.

* ALB와 EC2 Security Group을 분리하는 이유
* EC2에 Access Key를 저장하지 않고 IAM Role을 붙이는 이유
* CloudWatch에서 어떤 지표와 로그를 확인해야 하는지
* ALB 접속 장애가 발생했을 때 어떤 순서로 확인해야 하는지
* GitHub에 커밋하면 안 되는 민감정보가 무엇인지
