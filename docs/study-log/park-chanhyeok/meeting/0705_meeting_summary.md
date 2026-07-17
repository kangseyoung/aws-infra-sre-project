# Security + SRE 보조 Must / Optional 간단 정리

## 역할 목표

이번 프로젝트에서 Security + SRE 보조 역할의 목표는 앱이 AWS에서 안전하게 실행되고, 문제가 생겼을 때 어디를 확인해야 하는지 정리하는 것이다.

기본 구조는 다음과 같다.

```text id="xm1h44"
사용자 → ALB → EC2 → Docker / Nginx / App → CloudWatch
```

중점적으로 볼 내용은 다음과 같다.

* EC2가 외부에 직접 노출되지 않도록 구성되어 있는지 확인
* Security Group이 불필요하게 열려 있지 않은지 확인
* EC2에 Access Key를 저장하지 않고 IAM Role을 사용하는지 확인
* CloudWatch에서 서버 상태와 로그를 확인할 수 있는지 확인
* 장애 발생 시 확인 순서를 문서화

---

# Must

<details>
<summary><strong>1. Security Group 구조 이해</strong></summary>

ALB와 EC2의 Security Group을 분리해서 이해한다.

* ALB는 외부 사용자의 HTTP 요청을 받는다.
* EC2는 외부 전체가 아니라 ALB에서 오는 요청만 받는 것이 좋다.
* SSH 22번 포트는 `0.0.0.0/0`으로 열지 않는다.
* 불필요한 포트는 열지 않는다.

예상 구조:

```text id="t6pyzu"
사용자 → ALB Security Group → EC2 Security Group
```

</details>

---

<details>
<summary><strong>2. IAM Role 이해</strong></summary>

EC2가 CloudWatch 같은 AWS 서비스를 사용할 때 Access Key를 직접 저장하지 않고 IAM Role을 사용하는 이유를 이해한다.

예시:

```text id="g4mv0i"
EC2 → IAM Role → CloudWatch Logs
```

확인할 내용:

* IAM User, Role, Policy 차이
* EC2 Instance Role이 필요한 이유
* EC2 안에 Access Key를 저장하면 안 되는 이유

</details>

---

<details>
<summary><strong>3. 민감정보 관리</strong></summary>

GitHub에 올라가면 안 되는 파일과 정보를 정리한다.

커밋 금지 항목:

```text id="njl3rb"
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

</details>

---

<details>
<summary><strong>4. CloudWatch 기본 이해</strong></summary>

CloudWatch로 서버 상태와 로그를 확인하는 방법을 이해한다.

확인할 지표:

* EC2 CPU 사용률
* EC2 네트워크 사용량
* EC2 상태 검사 실패 여부
* ALB 요청 수
* ALB 5xx 에러
* Target Group unhealthy 여부

확인할 로그 후보:

* Nginx access log
* Nginx error log
* Application log

</details>

---

<details>
<summary><strong>5. 장애 대응 순서 정리</strong></summary>

ALB 주소로 접속이 안 될 때 확인할 순서를 정리한다.

기본 확인 순서:

1. ALB DNS 주소 확인
2. ALB Listener 확인
3. Target Group에서 EC2가 healthy인지 확인
4. EC2가 running 상태인지 확인
5. EC2 Security Group 확인
6. EC2 내부에서 Docker / Nginx / App 실행 상태 확인
7. `curl localhost`로 앱 응답 확인
8. CloudWatch Logs에서 에러 확인

</details>

---

# Optional

<details>
<summary><strong>1. SSM Session Manager 사용</strong></summary>

SSH 대신 SSM Session Manager로 EC2에 접속하는 방식을 공부한다.

목표:

* SSH 22번 포트를 열지 않고 EC2에 접속하기
* `.pem` 키 관리 부담 줄이기

</details>

---

<details>
<summary><strong>2. CloudWatch Agent로 로그 전송</strong></summary>

EC2 내부의 Nginx 로그나 애플리케이션 로그를 CloudWatch Logs로 보내는 방법을 공부한다.

대상 로그:

* Nginx access log
* Nginx error log
* Application log
* Docker container log

</details>

---

<details>
<summary><strong>3. CloudWatch Alarm 만들기</strong></summary>

간단한 장애 감지용 Alarm을 만든다.

Alarm 후보:

* EC2 CPU 사용률 80% 이상
* ALB unhealthy target 발생
* ALB 5xx 에러 발생

</details>

---

<details>
<summary><strong>4. Access Key 유출 대응 정리</strong></summary>

Access Key가 GitHub에 올라갔을 때 어떻게 대응할지 정리한다.

대응 순서:

1. 유출된 Access Key 비활성화
2. Access Key 삭제
3. CloudTrail에서 사용 이력 확인
4. GitHub commit history에서 민감정보 제거
5. `.gitignore`와 팀 규칙 수정

</details>

---

<details>
<summary><strong>5. Terraform 보안 체크</strong></summary>

Terraform 사용 시 민감정보가 GitHub에 올라가지 않도록 확인한다.

확인할 항목:

* `terraform.tfstate`
* `.terraform/`
* `*.tfvars`
* AWS Access Key
* Secret 값

</details>

---

## 최종 목표

Security + SRE 보조 역할의 최종 목표는 다음과 같다.

```text id="k6k4rz"
ALB → EC2 → Docker / Nginx / App 구조에서
보안 설정과 모니터링 흐름을 이해하고,
장애 발생 시 확인 순서를 문서화한다.
```
