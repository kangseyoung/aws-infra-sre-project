# Architecture

이 폴더는 아키텍처 다이어그램과 구조 설명을 모으는 곳입니다.

프로젝트의 목표 흐름은 다음과 같습니다.

```text
사용자 -> ALB -> EC2 -> Docker / Nginx -> CloudWatch
```

## 작성할 내용

- 전체 아키텍처 다이어그램
- 각 구성 요소의 역할
- 사용자 요청이 이동하는 순서
- VPC / subnet / route table 구조
- ALB -> Target Group -> EC2 흐름
- Security Group 연결 관계
- CloudWatch로 확인할 수 있는 상태와 지표
- Must 범위와 Optional 범위가 아키텍처에서 어디에 해당하는지

## Diagram Tips

- 처음에는 손그림이나 간단한 박스 다이어그램도 괜찮습니다.
- 각 화살표가 무엇을 의미하는지 한 줄 설명을 붙입니다.
- 비용이 발생하는 리소스는 다이어그램에 표시합니다.
- 최종 발표에서 설명할 수 있는 수준으로 정리합니다.

## Notes

- AWS Access Key, Secret Key, `.pem`, `.env`, `terraform.tfstate`, `.terraform/`은 절대 커밋하지 않습니다.
- 비용이 발생할 수 있는 리소스는 실습 후 반드시 삭제합니다.
- 다이어그램은 예쁘게 그리는 것보다 흐름을 설명할 수 있는 것이 우선입니다.
