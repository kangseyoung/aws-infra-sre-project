# Security + SRE Checklist

> AWS Infra / SRE 14-Day Project  
> 담당: 박찬혁 · 범위: Day 1~4 · Region: `ap-northeast-2`

## 1. 검수 요약

| 구간 | 검수 대상 | 결과 |
|---|---|---|
| Day 1 | SG, IAM, 민감정보, Runbook 및 MiniPEP 기준 | ✅ 기준 확인 |
| Day 2 | SG Inbound, SSH, IAM Role 및 민감정보 관리 기준 | ✅ 기준 확정 |
| Day 3 | VPC, Public Subnet, IGW, Public Route Table | ✅ 통과 |
| Day 4 | EC2, ALB SG, EC2 SG 및 외부 노출 포트 | ✅ 통과 |

현재까지 확인된 구성은 프로젝트의 Must 아키텍처와 일치한다.

```text
Internet
  → Internet-facing ALB : 80
  → Target Group : 80
  → EC2 Host : 80
  → Docker Container : 8000
  → MiniPEP FastAPI
```

---

## 2. Day 1 - 프로젝트 기준 검토

- [x] 최종 애플리케이션은 MiniPEP FastAPI로 정의되어 있다.
- [x] Health Check 경로는 `/health`이다.
- [x] 정상 Health Check 응답은 `HTTP 200`이다.
- [x] 최종 포트 구조는 `ALB 80 → EC2 Host 80 → Container 8000`이다.
- [x] Nginx는 초기 네트워크 연결 테스트용으로만 사용한다.
- [x] Must 범위에서는 Private Subnet을 제외하고 Public Subnet 2개를 사용한다.
- [x] Must 범위의 EC2는 1대이며, 무중단 또는 고가용성을 보장하는 구조로 표현하지 않는다.

---

## 3. Day 2 - 보안 기준

### Security Group

| 대상 | Inbound | Source | 판정 기준 |
|---|---:|---|---|
| ALB SG | TCP 80 | `0.0.0.0/0` | 인터넷 HTTP 요청 수신 |
| EC2 SG | TCP 22 | 관리자 공인 IP `/32` | SSH 접근 최소화 |
| EC2 SG | TCP 80 | ALB SG | ALB를 통한 요청만 허용 |
| EC2 SG | TCP 8000 | 허용하지 않음 | Container Port 직접 노출 방지 |

- [x] `All traffic`, `All TCP` 등 불필요하게 넓은 규칙을 사용하지 않는다.
- [x] EC2의 80번 포트를 `0.0.0.0/0`에 직접 공개하지 않는다.
- [x] SSH 22번 포트를 `0.0.0.0/0` 또는 넓은 CIDR에 공개하지 않는다.

### IAM

- [x] AWS 콘솔은 Root 사용자가 아닌 IAM 사용자로 접속한다.
- [x] 콘솔 조회만 필요한 경우 Access Key를 발급하거나 저장하지 않는다.
- [x] EC2가 AWS 서비스를 사용할 때는 Access Key 대신 IAM Role을 사용한다.
- [x] 불필요한 관리자 권한을 부여하지 않는다.
- [x] 로그인 URL, 사용자 이름, 비밀번호 및 인증정보를 GitHub에 기록하지 않는다.

### 민감정보

다음 파일과 값은 Git에 커밋하지 않는다.

```text
.env
*.pem
AWS Access Key
AWS Secret Access Key
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfvars
*.db
*.sqlite
*.sqlite3
```

---

## 4. Day 3 - Network Security Review

### 검수 결과

| 대상 | 확인 내용 | 결과 |
|---|---|---|
| VPC | 상태 `Available`, CIDR `10.0.0.0/16`, 프로젝트 전용 VPC | ✅ 정상 |
| Public Subnet A | CIDR `10.0.1.0/24`, AZ `ap-northeast-2a` | ✅ 정상 |
| Public Subnet B | CIDR `10.0.2.0/24`, AZ `ap-northeast-2c` | ✅ 정상 |
| CIDR/AZ | CIDR 중복 없음, 서로 다른 AZ 사용 | ✅ 정상 |
| Internet Gateway | 프로젝트 VPC에 `Attached` | ✅ 정상 |
| Public Route Table | Public Subnet 2개 명시적 연결 | ✅ 정상 |
| Local Route | `10.0.0.0/16 → local` | ✅ 정상 |
| Internet Route | `0.0.0.0/0 → IGW` | ✅ 정상 |

### 참고 사항

- Public Subnet의 Public IPv4 자동 할당은 비활성화되어 있다.
- Day 4 EC2에는 Public IPv4가 별도로 할당된 것을 확인했다.
- 설정 변경 없이 AWS 콘솔에서 조회 방식으로만 검수했다.

**Day 3 판정: ✅ Network Security Review 통과**

---

## 5. Day 4 - EC2 / Security Group Review

### EC2

- [x] 프로젝트 EC2가 생성되어 있다.
- [x] 인스턴스 상태는 `Running`이다.
- [x] 상태 검사는 `3/3 통과`이다.
- [x] 인스턴스 유형은 `t3.micro`이다.
- [x] EC2는 `ap-northeast-2a`에 배치되어 있다.
- [x] Public IPv4가 할당되어 있다.
- [x] 프로젝트 EC2 SG가 연결되어 있다.
- [x] Default SG가 EC2에 추가 적용되지 않았다.

### ALB Security Group

| 유형 | 프로토콜 | 포트 | Source | 결과 |
|---|---|---:|---|---|
| HTTP | TCP | 80 | `0.0.0.0/0` | ✅ 정상 |

- [x] Internet-facing ALB가 외부 HTTP 요청을 받을 수 있다.
- [x] 불필요한 Inbound Rule이 없다.

### EC2 Security Group

| 유형 | 프로토콜 | 포트 | Source | 결과 |
|---|---|---:|---|---|
| SSH | TCP | 22 | 관리자 공인 IP `/32` | ✅ 정상 |
| HTTP | TCP | 80 | 프로젝트 ALB SG | ✅ 정상 |

- [x] SSH 접근이 단일 관리자 IP로 제한되어 있다.
- [x] EC2의 HTTP 80번은 ALB SG에서 오는 요청만 허용한다.
- [x] EC2의 HTTP 80번이 인터넷에 직접 공개되지 않았다.
- [x] Container Port 8000의 Inbound Rule이 없다.
- [x] `All traffic` 또는 사용 목적이 없는 포트가 열려 있지 않다.

**Day 4 판정: ✅ EC2 / SG Security Review 통과**

---

## 6. 증빙 캡처 목록

원본 캡처에는 AWS 계정 ID, 리소스 ID, EC2 Public IP 및 관리자 공인 IP가 포함될 수 있다. 공개 저장소에는 원본을 그대로 커밋하지 않고, 필요한 경우 민감·식별 값을 마스킹한 사본만 사용한다.

| 번호 | 증빙 내용 | 확인 결과 |
|---:|---|---|
| 1 | VPC 목록 | 프로젝트 VPC 및 CIDR 확인 |
| 2 | Subnet 목록 | Public Subnet A/B 및 CIDR 확인 |
| 3 | Public Route Table | Subnet 2개 연결, Local/IGW Route 확인 |
| 4 | Internet Gateway | 프로젝트 VPC 연결 상태 확인 |
| 5 | EC2 Instance | Running, 3/3 Status Check, AZ 확인 |
| 6 | ALB SG Inbound | HTTP 80, `0.0.0.0/0` 확인 |
| 7 | EC2 SG Inbound | SSH `/32`, HTTP Source ALB SG 확인 |

---

## 7. 후속 작업

다음 항목은 MiniPEP 배포 및 ALB/Target Group 구성 이후 검수한다.

- [ ] `EC2 Host 80 → Docker Container 8000` 포트 매핑 확인
- [ ] EC2 내부 `curl -i http://localhost/health`의 `HTTP 200` 확인
- [ ] ALB DNS의 `/health` 응답 확인
- [ ] Target Group의 Target Health가 `Healthy`인지 확인
- [ ] Docker / MiniPEP Application Log 확인
- [ ] `.env`, Access Key 및 SQLite DB의 Git 미포함 확인
- [ ] 공통 장애 대응 Runbook 작성
- [ ] 장애 1개 재현 및 복구 결과 기록

---

## 8. 최종 결론

Day 2~4 범위에서 VPC, Public Subnet, Internet Gateway, Public Route Table, EC2 및 Security Group 구성을 검수했다.

- 네트워크 CIDR과 AZ 구성이 계획과 일치한다.
- Public Subnet A/B에 인터넷 경로가 정상적으로 연결되어 있다.
- ALB SG와 EC2 SG의 역할이 분리되어 있다.
- SSH는 관리자 공인 IP `/32`로 제한되어 있다.
- EC2 앱 포트 80은 ALB SG에서만 접근할 수 있다.
- Container Port 8000 및 불필요한 포트는 외부에 공개되지 않았다.

**종합 판정: ✅ Day 2~4 Security + SRE 검수 통과**
