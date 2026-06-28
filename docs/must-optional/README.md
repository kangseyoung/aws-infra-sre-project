# Must / Optional Guide

이 폴더는 각 파트별로 2주 안에 반드시 해야 할 범위와, 시간이 남으면 도전할 범위를 나누어 정리하는 공간입니다.

범위를 먼저 나누면 프로젝트가 커지는 것을 막고, 마지막에 무엇을 설명해야 하는지 명확해집니다.

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

## Files

| File | Owner / Scope |
| --- | --- |
| `compute-network.md` | 강세영: Compute + Network |
| `observability-platform.md` | 권태욱: Observability / Platform / IaC 보조 / Compute 보조 |
| `terraform-iac.md` | 김태우: Terraform / IaC |
| `security-sre.md` | 박찬혁: Security + SRE 보조 |

## 작성 방법

1. 본인 담당 파일을 엽니다.
2. Must와 Optional을 분리합니다.
3. 왜 Must인지, 왜 Optional인지 이유를 적습니다.
4. 다른 파트와 연결되는 부분을 적습니다.
5. 최종 산출물을 한 줄로 정리합니다.

## Notes

- Must를 너무 크게 잡지 않습니다.
- Optional은 실패해도 괜찮은 범위로 둡니다.
- 공부기록은 복붙보다 본인이 이해한 말로 정리하는 것을 우선합니다.
- AWS Access Key, Secret Key, `.pem` 파일, `.env` 파일, `terraform.tfstate` 파일은 절대 커밋하지 않습니다.

## Commit Message Examples

- `docs: update compute-network must optional`
- `docs: update observability-platform must optional`
- `docs: update terraform-iac must optional`
- `docs: update security-sre must optional`
