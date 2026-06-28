# Must / Optional Guide

이 폴더는 각 파트별로 2주 안에 반드시 해야 할 범위와, 시간이 남으면 도전할 범위를 나누어 정리하는 공간입니다.

처음부터 완벽하게 정할 필요는 없습니다. 공부하면서 계속 수정해도 됩니다.

## Must 기준

Must는 이번 2주 프로젝트에서 반드시 구현하거나 이해해야 하는 범위입니다.

- 2주 안에 반드시 구현하거나 이해해야 하는 범위
- 최종 아키텍처 완성에 필요한 핵심 요소
- 포트폴리오에서 설명 가능해야 하는 내용

## Optional 기준

Optional은 시간이 남으면 도전할 범위입니다.

- 시간이 남으면 도전할 범위
- 고도화, 자동화, 추가 모니터링, 추가 문서화
- 실패해도 프로젝트 전체 완성에는 영향이 적은 내용

## 작성 규칙

- 너무 넓게 잡지 않습니다.
- 2주 안에 가능한 범위로 나눕니다.
- 포트폴리오에 남길 수 있는 결과물 중심으로 정리합니다.
- 다음 회의에서 2~3분 정도로 공유할 수 있게 요약합니다.

## Files

| File | Owner / Scope |
| --- | --- |
| `compute-network.md` | 강세영: Compute + Network |
| `observability-platform.md` | 권태욱: Observability / Platform / IaC 보조 / Compute 보조 |
| `terraform-iac.md` | 김태우: Terraform / IaC |
| `security-sre.md` | 박찬혁: Security + SRE 보조 |

## Templates

- 공통 템플릿: `templates/must-optional-template.md`
- 담당 파트 조사용 GPT 프롬프트: `templates/part-research-prompt.md`

## Commit Message Examples

```text
docs: update compute-network must optional
docs: update observability-platform must optional
docs: update terraform-iac must optional
docs: update security-sre must optional
```

## Notes

- AWS Access Key, Secret Key, `.pem`, `.env`, `terraform.tfstate`, `.terraform/`은 절대 커밋하지 않습니다.
- 공부기록과 파트 정리는 복붙보다 본인이 이해한 말로 정리하는 것을 우선합니다.
