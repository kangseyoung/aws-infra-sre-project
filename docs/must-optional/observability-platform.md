# Observability / Platform Must / Optional 정리

담당자: 권태욱  
파트: Observability / Platform / IaC 보조 / Compute 보조

## 1. 이 파트의 역할

서비스와 인프라 상태를 확인할 수 있도록 기본 모니터링, 로그 확인, 상태 점검 흐름을 정리합니다. Compute와 IaC 파트를 보조하면서 운영 관점의 확인 항목을 만듭니다.

## 2. Must 범위

- CloudWatch 기본 개념 이해
- EC2 상태 확인 방법 정리
- ALB Target Group health check 확인
- 기본 지표 확인: CPU, status check, health status
- 장애 상황에서 먼저 확인할 항목 정리
- 간단한 운영 체크리스트 작성

## 3. Optional 범위

- CloudWatch Alarm 추가
- Dashboard 초안 작성
- 로그 수집 구조 추가 조사
- 장애 시나리오별 타임라인 문서화
- IaC 파트의 output/checklist 보조

## 4. Must로 정한 이유

프로젝트가 단순 생성 실습으로 끝나지 않으려면 상태를 확인하고 문제를 추적하는 방법이 필요합니다. 최소한 EC2, ALB, CloudWatch에서 무엇을 봐야 하는지 설명할 수 있어야 합니다.

## 5. Optional로 뺀 이유

Alarm, Dashboard, 로그 수집 고도화는 시간이 부족하면 전체 아키텍처 완성 이후에 진행해도 됩니다.

## 6. 다른 파트와 연결되는 부분

- Compute + Network: ALB health check, EC2 상태 확인
- Security + SRE: 장애 대응 체크리스트, 보안 설정 확인
- Terraform / IaC: 모니터링 리소스 코드화 후보

## 7. 최종 산출물

- 기본 모니터링 확인 문서
- 장애 시 먼저 볼 항목 체크리스트
- Optional 고도화 후보 정리
