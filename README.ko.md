# AWS 인프라 2주 프로젝트

## 프로젝트 소개
이 레포지토리는 초보자 4~5명이 2주 동안 진행하는 AWS 인프라 중심 팀 프로젝트를 위해 만든 스캐폴딩입니다.  
백엔드 API나 프론트엔드 기능 개발보다, 실제 운영 환경을 닮은 AWS 인프라 구조를 직접 설계하고 구축하며 문서화하는 경험에 초점을 맞춥니다.

기본 요청 흐름은 다음과 같습니다.

`사용자 -> ALB -> EC2 -> Docker + Nginx -> CloudWatch`

즉, 사용자가 접속하는 입구부터 웹 서버가 떠 있는 컴퓨트 계층, 그리고 모니터링 계층까지 하나의 흐름으로 연결해 보는 것이 핵심입니다.

## 왜 이 프로젝트를 하는가
클라우드 학습 초반에는 서비스가 어떻게 뜨는지보다 AWS 리소스가 어떻게 연결되는지를 이해하는 것이 더 중요합니다.  
이 프로젝트는 콘솔에서 직접 리소스를 만들어 보며 VPC, Subnet, Route Table, Security Group, ALB, EC2, CloudWatch 사이의 관계를 체감하도록 설계했습니다.

처음부터 Terraform으로 모든 것을 자동화하지 않는 이유도 분명합니다.

- 먼저 수동 구축으로 구조를 이해한다
- 시행착오와 설정 근거를 문서로 남긴다
- 이후 안정화된 일부 리소스를 Terraform으로 옮긴다

이 순서가 초보자 팀에게 가장 학습 효과가 좋고, 최종 결과물도 포트폴리오로 설명하기 쉬워집니다.

## 아키텍처 개요
이번 프로젝트에서 다루는 주요 범위는 아래와 같습니다.

- AWS VPC
- Public / Private Subnet
- Route Table
- Internet Gateway
- NAT Gateway optional
- EC2
- Docker
- Nginx
- Application Load Balancer
- Target Group
- Security Group
- IAM / IAM Role
- CloudWatch Logs / Metrics / Alarm
- Terraform optional

상세 초안은 다음 문서를 참고합니다.

- [docs/architecture.ko.md](/D:/2026/sre/aws-infra-2week-project/docs/architecture.ko.md)
- [docs/architecture.md](/D:/2026/sre/aws-infra-2week-project/docs/architecture.md)

## 기술 스택
이번 프로젝트는 애플리케이션 기능보다 인프라 구성 요소 이해에 집중합니다.

- 네트워크: VPC, Subnet, Route Table, Internet Gateway, NAT Gateway
- 컴퓨트: EC2
- 런타임: Docker
- 웹 서버: Nginx
- 트래픽 분산: ALB, Target Group
- 보안: Security Group, IAM Role
- 관측성: CloudWatch Logs, Metrics, Alarm
- IaC 초안: Terraform

## 팀 역할
| 이름 | 역할 | 담당 범위 |
| --- | --- | --- |
| 강세영 | Observability / SRE + Network 흐름 정리 | CloudWatch, 모니터링 기준, 알람, 네트워크 흐름 문서화 |
| 권태욱 | Compute / Platform | EC2, Docker, Nginx, ALB 연동, 서버 운영 절차 |
| 김태우 | Terraform / IaC | Terraform 초안 작성, 변수/출력 구조, 수동 구축 내용 일부 코드화 |
| 박찬혁 | Security + Observability 보조 | Security Group, IAM 검토, 모니터링 보조, 체크리스트 검증 |

## 프로젝트 목표
- AWS 인프라 핵심 리소스가 어떻게 연결되는지 이해한다
- 사용자 요청이 ALB를 거쳐 EC2의 Nginx까지 도달하는 흐름을 직접 만든다
- 수동 구축 과정을 기록하고, 운영 문서화 습관을 익힌다
- CloudWatch 기반의 기본 모니터링과 장애 대응 관점을 익힌다
- Terraform을 보조적으로 도입해 IaC 전환의 출발점을 만든다
- 최종적으로 GitHub에 공개 가능한 인프라 포트폴리오 형태로 정리한다

## 레포 구조
```text
aws-infra-2week-project/
├── README.md
├── README.ko.md
├── docs/
├── diagrams/
├── infra/
│   ├── terraform/
│   └── manual-setup/
├── app/
├── runbook/
├── scripts/
└── .gitignore
```

## 2주 진행 로드맵
### 1주차
- Day 1: 킥오프, 역할 분담, 목표 및 아키텍처 합의
- Day 2: VPC, Subnet, Route Table, Internet Gateway 구성
- Day 3: Security Group, IAM Role 정리
- Day 4: EC2 생성, Docker 설치, Nginx 실행
- Day 5: ALB 및 Target Group 연결, 1차 end-to-end 테스트

### 2주차
- Day 6: CloudWatch Logs / Metrics / Alarm 구성
- Day 7: 장애 시나리오 점검 및 Runbook 작성
- Day 8: 비용 확인, 삭제 체크리스트 정리, 문서 보완
- Day 9: Terraform 초안 작성
- Day 10: 최종 리허설, 회고, 발표 자료 정리

## 수동 구축 가이드
`infra/manual-setup/` 폴더에는 실제 콘솔에서 리소스를 만들며 기록할 수 있는 템플릿을 넣었습니다.

권장 순서는 다음과 같습니다.

1. `vpc-setup.md`
2. `security-setup.md`
3. `ec2-setup.md`
4. `alb-setup.md`
5. `cloudwatch-setup.md`

각 문서에는 아래 내용을 남기면 좋습니다.

- 어떤 리소스를 만들었는지
- 왜 그 설정을 선택했는지
- 스크린샷 또는 콘솔 증빙
- 막혔던 지점과 해결 방법
- 나중에 Terraform으로 옮길 후보

## Terraform 계획
이번 프로젝트에서 Terraform은 최종 완성형이 아니라 초안 수준으로 다룹니다.  
핵심은 “먼저 이해하고, 그다음 일부를 코드화한다”는 흐름입니다.

추천 접근 방식:

- `provider.tf`에서 리전과 기본 provider 설정 정리
- `variables.tf`에서 프로젝트명, VPC CIDR, 서브넷 CIDR 등 입력값 관리
- `main.tf`에서 VPC, Subnet, Internet Gateway, Security Group 정도부터 시작
- `outputs.tf`에서 확인이 필요한 주요 값 노출

이 방식이면 Terraform이 부담이 아니라 학습 정리 도구로 작동합니다.

## Observability / SRE 포인트
이번 프로젝트에서 관측성은 단순 옵션이 아니라 결과물의 일부입니다.

최소한 아래 항목은 확인 가능해야 합니다.

- ALB Health Check 상태
- EC2 인스턴스 상태
- Nginx 컨테이너 상태
- CPU 사용량
- 로그 확인 경로
- 알람 조건과 담당자

가능하다면 최종 발표에는 아래 자료도 포함하면 좋습니다.

- CloudWatch 대시보드 캡처
- 알람 기준값 정리
- 장애 대응 예시 타임라인
- 서비스 상태 점검 체크리스트

## 장애 대응 Runbook
`runbook/`에는 장애 대응 문서 템플릿을 넣었습니다.

예시 시나리오:

- ALB 헬스체크 실패
- EC2 SSH 접속 실패
- Nginx 다운
- 비용 급증 및 정리 필요

실제 프로젝트 중에 한 번이라도 장애를 재현해 보고, 해당 문서에 확인 순서와 해결 과정을 채워 넣는 것을 권장합니다.

## 비용 관리
학습용 프로젝트라도 비용 통제는 반드시 포함되어야 합니다.  
특히 ALB, NAT Gateway, EBS, Elastic IP는 생각보다 비용 인지 포인트가 되기 쉽습니다.

권장 원칙:

- 가능하면 작은 사양의 EC2 사용
- NAT Gateway는 필요할 때만 사용
- 불필요한 ALB, 볼륨, 스냅샷, EIP 즉시 정리
- 매일 리소스 현황 확인
- 종료 전 `runbook/cost-cleanup.md` 체크리스트 수행

## 보안 메모
- AWS Access Key, Secret Access Key, `.pem`, `.env`, `terraform.tfstate`, `terraform.tfvars`는 절대 커밋하지 않습니다.
- 자격 증명을 스크립트나 Terraform 파일에 하드코딩하지 않습니다.
- EC2 접근에는 가능하면 IAM Role 기반 접근 방식을 우선합니다.
- Security Group 인바운드는 필요한 포트만 최소 범위로 엽니다.
- 발표 전과 삭제 전, 보안 설정을 한 번 더 점검합니다.

## 회고 포인트
프로젝트 마지막에는 아래 질문을 기준으로 회고를 남기면 좋습니다.

- 어떤 AWS 개념이 가장 선명해졌는가
- 어떤 설정이 가장 헷갈렸는가
- 팀 문서화 방식은 효율적이었는가
- Terraform으로 옮기기 좋은 부분은 어디였는가
- 다음 프로젝트에서는 무엇을 자동화할 것인가

## 비밀 정보 관리
이 레포에는 아래 항목이 절대 올라가면 안 됩니다.

- AWS Access Key
- AWS Secret Access Key
- `.pem` 개인 키 파일
- `.env`
- `terraform.tfstate`
- `terraform.tfvars`

첫 커밋 전과 GitHub push 전에는 반드시 `.gitignore`와 변경 파일을 다시 확인하세요.

