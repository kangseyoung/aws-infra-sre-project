# Day 1 진행 기록 - Security + SRE

## 오늘 목표

- 기존 PR과 문서에서 Security + SRE 기준이 최신 프로젝트 기준과 맞는지 확인한다.
- 최종 앱 기준을 Nginx가 아니라 MiniPEP FastAPI로 통일한다.
- Must와 Optional 범위를 팀 기준에 맞게 다시 정리한다.

## 오늘 바로 확인할 것

### 1. 최종 앱 기준

- [ ] 최종 구조가 `ALB -> EC2 -> Docker -> MiniPEP`로 적혀 있는가?
- [ ] Health Check Path가 `/health`로 적혀 있는가?
- [ ] 성공 기준이 HTTP `200`으로 적혀 있는가?
- [ ] Container Port는 `8000`, EC2 Host Port는 `80`, Target Group Port는 `80`으로 맞는가?
- [ ] Nginx는 초기 연결 테스트용으로만 설명되어 있는가?
- [ ] 최종 로그 기준이 Nginx 로그가 아니라 Docker stdout 또는 MiniPEP Application Log 중심인가?

### 2. Security Group 기준

- [ ] ALB Security Group은 HTTP `80`을 외부에서 받을 수 있는가?
- [ ] EC2 Security Group의 앱 포트 `80`은 ALB Security Group에서 오는 요청만 허용하는가?
- [ ] SSH `22`는 `0.0.0.0/0`이 아니라 내 IP로 제한되어 있는가?
- [ ] 사용하지 않는 포트가 열려 있지 않은가?
- [ ] Security Group 규칙표에 출발지, 포트, 목적이 같이 적혀 있는가?

### 3. IAM / 민감정보 기준

- [ ] EC2 내부에 AWS Access Key를 저장하지 않는다고 명시되어 있는가?
- [ ] 필요한 경우 IAM Role을 사용한다고 적혀 있는가?
- [ ] `.env`, `.pem`, `terraform.tfstate`, `.terraform/`, `*.tfvars`, SQLite DB 파일이 Git에 올라가지 않도록 정리되어 있는가?
- [ ] `.gitignore`에 민감 파일 제외 규칙이 있는가?

### 4. Runbook 기준

- [ ] 장애 확인 순서가 `ALB -> Target Group -> EC2 -> SG -> Port -> Docker -> App` 순서인가?
- [ ] `/health` 실패 시 확인할 항목이 있는가?
- [ ] Docker 컨테이너 상태 확인 명령이 있는가?
- [ ] Application Log 확인 방법이 있는가?
- [ ] Nginx 중심 Runbook은 MiniPEP 기준으로 바꾸거나 테스트용이라고 표시되어 있는가?

### 5. Must / Optional 범위

- [ ] CloudWatch Agent와 CloudWatch Logs 중앙 수집은 Optional로 분리되어 있는가?
- [ ] CloudWatch Alarm과 SNS는 Optional로 분리되어 있는가?
- [ ] Private Subnet, NAT Gateway, SSM, WAF 같은 항목이 Must에 들어가 있지 않은가?
- [ ] Must는 Public Subnet 기반의 단순 구조로 정리되어 있는가?

## 오늘 리뷰 코멘트로 남길 수 있는 문장

```text
최신 프로젝트 기준에서는 최종 시연 대상이 Nginx 정적 페이지가 아니라 MiniPEP FastAPI 앱입니다.
Nginx는 초기 네트워크 연결 테스트용으로만 남기고, 최종 성공 기준은 ALB DNS와 /health HTTP 200,
Docker stdout 또는 MiniPEP Application Log 확인으로 통일하면 좋겠습니다.
```

```text
Security + SRE 기준에서는 EC2 80번 포트가 외부 전체가 아니라 ALB Security Group에서만 접근 가능해야 합니다.
SSH 22번도 0.0.0.0/0이 아니라 작업자 My IP로 제한하는지 확인이 필요합니다.
```

```text
CloudWatch Agent, CloudWatch Logs 중앙 수집, Alarm/SNS는 현재 Must가 아니라 Optional로 보입니다.
Must에서는 AWS 기본 Metric, Target Health, Docker/Application Log 확인까지만 성공 기준으로 두는 게 맞겠습니다.
```

## 오늘 산출물

- [ ] PR Review 기록 또는 수정 요청
- [ ] Security + SRE Must/Optional 수정 확인
- [ ] Runbook 수정 방향 정리
- [ ] 민감정보 제외 기준 확인

## 내일 이어서 할 일

- Day 2에서 ALB SG와 EC2 SG Inbound 규칙표를 작성한다.
- SSH 허용 범위와 IAM Role 사용 기준을 팀과 확정한다.
- Resource Handoff에 Security Group, Port, Health Check Path가 빠지지 않도록 템플릿을 확인한다.
