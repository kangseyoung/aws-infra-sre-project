# Compute + Network Must / Optional 정리

담당자: 강세영  
파트: Compute + Network

## 1. 이 파트의 역할

사용자 요청이 ALB를 거쳐 EC2까지 도달하는 흐름을 이해하고 구성합니다. VPC, subnet, route table, Security Group, EC2, ALB의 역할을 설명할 수 있어야 합니다.

## 2. Must 범위

- VPC, public/private subnet 구조 이해
- Route table과 Internet Gateway 역할 이해
- EC2 생성과 접속 흐름 이해
- ALB, Target Group, Health Check 기본 흐름 이해
- Security Group에서 필요한 포트만 여는 이유 설명
- 사용자 요청이 ALB에서 EC2까지 가는 흐름 설명

## 3. Optional 범위

- Private subnet 배치 구조 추가 정리
- NAT Gateway 사용 여부와 비용 영향 정리
- ALB health check 실패 시나리오 정리
- 간단한 네트워크 다이어그램 고도화

## 4. Must로 정한 이유

Compute와 Network는 최종 아키텍처의 기본 경로입니다. 이 흐름을 이해하지 못하면 서비스 접근, 보안 그룹, 모니터링, 장애 대응을 설명하기 어렵습니다.

## 5. Optional로 뺀 이유

NAT Gateway, private subnet 고도화, 상세 실패 시나리오는 중요하지만 2주 안에 기본 흐름을 먼저 완성한 뒤 진행해도 됩니다.

## 6. 다른 파트와 연결되는 부분

- Security: Security Group, IAM, inbound/outbound 규칙
- Observability: ALB health check, EC2 상태, CloudWatch 지표
- Terraform / IaC: VPC, subnet, security group, EC2, ALB 리소스 코드화 후보

## 7. 최종 산출물

- 사용자 요청이 ALB를 거쳐 EC2까지 도달하는 구조 설명
- Compute + Network Must / Optional 정리
- 네트워크 흐름 다이어그램 또는 설명 문서
