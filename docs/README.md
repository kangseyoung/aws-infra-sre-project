# Project Documentation

이 폴더는 AWS 인프라 2주 프로젝트의 학습 기록, 역할별 범위 정리, 회의록, 런북, 아키텍처 문서를 모으는 공간입니다.

목표는 완벽한 문서를 한 번에 만드는 것이 아니라, 팀원들이 매일 공부한 내용과 결정 사항을 GitHub에 남기면서 프로젝트 이해도를 쌓는 것입니다.

## Folder Structure

```text
docs/
  meeting-notes/      # 회의록
  study-log/          # 개인별 매일 공부기록
  must-optional/      # 파트별 Must / Optional 범위 정리
  runbook/            # 장애 대응 문서
  architecture/       # 아키텍처 다이어그램과 구조 설명
```

## How to Use

- 매일 공부한 내용은 `docs/study-log/{name}/YYYY-MM-DD.md`에 작성합니다.
- 각자 담당 파트의 구현 범위는 `docs/must-optional/`에 정리합니다.
- 회의에서 정한 내용은 `docs/meeting-notes/`에 날짜별로 남깁니다.
- 장애 상황을 테스트하거나 겪으면 `docs/runbook/`에 대응 절차를 정리합니다.
- 아키텍처 다이어그램, 흐름도, 구조 설명은 `docs/architecture/`에 모읍니다.

## Team Roles

| Member | Role |
| --- | --- |
| 강세영 | Compute + Network |
| 권태욱 | Observability / Platform / IaC 보조 / Compute 보조 |
| 김태우 | Terraform / IaC |
| 박찬혁 | Security + SRE 보조 |

## Commit Message Examples

- `chore: add project documentation scaffold`
- `docs: add 2026-06-29 study log - kangseyoung`
- `docs: update compute-network must optional`
- `docs: add kickoff meeting notes`

## Notes

- AWS Access Key, Secret Key, `.pem` 파일, `.env` 파일, `terraform.tfstate` 파일은 절대 커밋하지 않습니다.
- 비용이 발생할 수 있는 리소스는 실습 후 반드시 삭제합니다.
- 공부기록은 복붙보다 본인이 이해한 말로 정리하는 것을 우선합니다.
