# Terraform / IaC Must / Optional 정리

담당자: 김태우  
파트: Terraform / IaC

## 1. 이 파트의 역할

수동으로 이해한 AWS 리소스 중 일부를 Terraform으로 정리합니다. 처음부터 모든 것을 자동화하기보다, 구조를 이해한 뒤 코드화할 수 있는 범위를 고릅니다.

## 2. Must 범위

- Terraform 기본 구조 이해: provider, resource, variable, output
- AWS provider 설정 방식 이해
- 변수와 output을 왜 분리하는지 설명
- 코드화할 리소스 후보 정리
- `terraform.tfstate`를 커밋하면 안 되는 이유 설명
- 최소 예제 또는 초안 작성

## 3. Optional 범위

- VPC / subnet / security group 일부 코드화
- EC2 또는 ALB 리소스 초안 작성
- module 구조 조사
- remote backend 조사
- formatting, validation 명령어 정리

## 4. Must로 정한 이유

Terraform은 프로젝트의 자동화 방향을 보여주는 파트입니다. 다만 2주 안에 전체 자동화보다 기본 개념과 안전한 파일 관리 기준을 이해하는 것이 우선입니다.

## 5. Optional로 뺀 이유

전체 리소스 자동화는 시간이 많이 걸리고, 수동 구성 이해가 부족한 상태에서 진행하면 디버깅이 어려워질 수 있습니다.

## 6. 다른 파트와 연결되는 부분

- Compute + Network: 코드화할 VPC, subnet, EC2, ALB 후보
- Security + SRE: Security Group, IAM 관련 코드화 주의사항
- Observability / Platform: CloudWatch 리소스 코드화 후보

## 7. 최종 산출물

- Terraform 기본 구조 정리
- 코드화 후보 목록
- 안전한 IaC 파일 관리 기준
