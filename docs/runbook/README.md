# Runbook

이 폴더는 장애 대응 문서를 모으는 곳입니다.

Runbook은 문제가 생겼을 때 무엇을 먼저 확인할지 정리한 문서입니다. 완벽한 해결책보다, 팀원이 같은 순서로 확인할 수 있는 절차를 남기는 것이 중요합니다.

## 작성할 수 있는 Runbook 예시

- ALB health check failure
- EC2 SSH access failure
- EC2 status check failure
- Application response failure
- CloudWatch alarm 발생
- 예상보다 비용이 많이 발생한 경우

## Runbook 기본 형식

```md
# 장애 상황 이름

## 증상

## 먼저 확인할 것

## 확인 명령어 또는 AWS Console 위치

## 가능한 원인

## 대응 방법

## 재발 방지
```

## Notes

- AWS Access Key, Secret Key, `.pem`, `.env`, `terraform.tfstate`, `.terraform/`은 절대 커밋하지 않습니다.
- 비용이 발생할 수 있는 리소스는 실습 후 반드시 삭제합니다.
- 장애 대응 문서는 복붙보다 본인이 이해한 말로 정리하는 것을 우선합니다.
