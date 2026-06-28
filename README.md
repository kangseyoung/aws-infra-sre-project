# AWS Infra 2-Week Project

초보자 4명이 2주 동안 진행하는 AWS 인프라 프로젝트입니다.

이 프로젝트의 목표는 단순히 웹페이지를 띄우는 것이 아니라, AWS 위에서 네트워크, 서버, 보안, 모니터링, 장애 대응 흐름을 직접 구축하고 이해하는 것입니다.

## Project Overview

이번 프로젝트에서는 AWS 핵심 인프라 구성 요소를 직접 만들고, 각 요소가 어떻게 연결되는지 기록합니다.

중요하게 보는 것은 다음과 같습니다.

- 네트워크 흐름 이해
- 서버와 트래픽 처리 구조 이해
- 보안 설정의 이유 이해
- CloudWatch 기반 모니터링 이해
- 장애 상황에서 어디를 확인해야 하는지 정리
- 매일 공부한 내용과 헷갈린 내용을 GitHub에 남기기

## Target Architecture

```text
사용자 -> ALB -> EC2 -> Docker / Nginx -> CloudWatch
```

각 요소의 역할은 다음과 같습니다.

| Component | Role |
| --- | --- |
| 사용자 | 브라우저에서 서비스에 접속하는 사람 |
| ALB | 사용자 요청을 받아 EC2로 전달하는 Load Balancer |
| EC2 | 실제 서버가 실행되는 AWS 가상 서버 |
| Docker / Nginx | EC2 안에서 웹 서버를 실행하는 구성 |
| CloudWatch | 서버 상태, 로그, 지표를 확인하는 AWS 모니터링 서비스 |

## Team Roles

| Member | Role |
| --- | --- |
| 강세영 | Compute + Network |
| 권태욱 | Observability / Platform / IaC 보조 / Compute 보조 |
| 김태우 | Terraform / IaC |
| 박찬혁 | Security + SRE 보조 |

역할은 2026-06-28 kickoff 회의 기준입니다.

## Repository Structure

```text
aws-infra-2week-project/
├── README.md
├── docs/
│   ├── README.md
│   ├── meeting-notes/
│   ├── study-log/
│   ├── must-optional/
│   ├── runbook/
│   └── architecture/
├── templates/
├── infra/
├── app/
├── diagrams/
├── scripts/
└── .gitignore
```

주요 문서 위치:

- `docs/`: 프로젝트 문서 전체 안내
- `docs/study-log/`: 개인별 매일 공부기록
- `docs/must-optional/`: 담당 파트별 Must / Optional 정리
- `docs/runbook/`: 장애 대응 문서
- `docs/architecture/`: 아키텍처 다이어그램과 구조 설명
- `templates/`: 반복해서 사용할 문서 템플릿

## Daily Study Log Rule

각자 매일 공부기록을 올립니다.

경로 예시:

```text
docs/study-log/kangseyoung/2026-06-29.md
```

공부기록은 완벽한 정리본이 아니어도 됩니다. 아래 내용을 남기는 것이 목적입니다.

- 오늘 공부한 개념
- GPT에게 물어본 질문
- 내가 이해한 내용
- 헷갈리는 부분
- 내일 할 일
- 참고한 자료

템플릿:

```text
templates/study-log-template.md
```

## Must / Optional Rule

각자 담당 파트 기준으로 Must / Optional 범위를 정리합니다.

Must:

- 2주 안에 반드시 구현하거나 이해해야 하는 범위
- 최종 아키텍처 완성에 필요한 핵심 요소
- 포트폴리오에서 설명 가능해야 하는 내용

Optional:

- 시간이 남으면 도전할 범위
- 고도화, 자동화, 추가 모니터링, 추가 문서화
- 실패해도 프로젝트 전체 완성에는 영향이 적은 내용

주의할 점:

- 너무 넓게 잡지 않습니다.
- 2주 안에 가능한 범위로 정리합니다.
- 포트폴리오에 남길 수 있는 결과물 중심으로 정리합니다.
- Must / Optional은 처음부터 완벽하지 않아도 됩니다. 공부하면서 계속 수정합니다.

템플릿:

```text
templates/must-optional-template.md
```

## Commit Message Convention

커밋 메시지는 너무 복잡하게 쓰지 않고, 어떤 작업인지 바로 알 수 있게 작성합니다.

규칙:

- `docs:` 문서, 공부기록, 회의록 수정
- `chore:` 폴더 구조, 설정 파일, 템플릿 추가
- `fix:` 잘못된 링크, 오타, 문서 오류 수정
- `feat:` 실제 기능 또는 실습 코드 추가

예시:

```text
docs: add 2026-06-29 study log - kangseyoung
docs: add 2026-06-29 study log - kim-taewoo
docs: update compute-network must optional
docs: update terraform-iac must optional
docs: add kickoff meeting notes
chore: add project documentation scaffold
fix: update broken documentation link
```

## Push Rule

- 공부기록과 문서는 `main`에 직접 push해도 됩니다.
- Terraform 코드나 실제 실습 코드는 가능하면 branch를 따고 PR로 올리는 방식을 권장합니다.
- 초반에는 기록을 남기는 것이 우선이므로 너무 복잡한 Git Flow는 적용하지 않습니다.
- 충돌이 나면 혼자 억지로 해결하지 말고 팀원에게 공유합니다.

## Security Notice

아래 파일과 정보는 절대 커밋하지 않습니다.

- AWS Access Key
- AWS Secret Key
- `.pem`
- `.env`
- `terraform.tfstate`
- `.terraform/`

비용이 발생할 수 있는 AWS 리소스는 실습 후 반드시 삭제합니다.

특히 ALB, NAT Gateway, Elastic IP, EBS volume, 실행 중인 EC2는 실습 후 상태를 확인합니다.
