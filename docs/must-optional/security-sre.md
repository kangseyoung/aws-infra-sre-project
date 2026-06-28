# Security + SRE Must / Optional 정리

담당자: 박찬혁  
파트: Security + SRE 보조

## 1. 이 파트의 역할

프로젝트에서 필요한 최소 보안 설정과 장애 대응 관점을 정리합니다. Security Group, IAM, secret handling, incident response 기본 체크리스트를 관리합니다.

## 2. Must 범위

- Security Group inbound/outbound 기본 이해
- 필요한 포트만 여는 이유 설명
- IAM Role과 Access Key 차이 이해
- AWS Access Key, Secret Key, `.pem`, `.env`, `terraform.tfstate` 커밋 금지 기준 정리
- 기본 장애 대응 체크리스트 작성
- 비용 발생 리소스 삭제 주의사항 정리

## 3. Optional 범위

- IAM least privilege 추가 조사
- 보안 점검 체크리스트 고도화
- 장애 시나리오별 runbook 작성
- 비용 알림 또는 예산 설정 조사
- Security Group 변경 이력 정리

## 4. Must로 정한 이유

보안과 장애 대응 기준이 없으면 실습 과정에서 민감정보가 노출되거나 비용 문제가 생길 수 있습니다. 최소한 커밋 금지 파일과 접근 제어 기준은 팀 전체가 공유해야 합니다.

## 5. Optional로 뺀 이유

Least privilege 고도화, 비용 알림, 상세 runbook은 중요하지만 기본 아키텍처를 먼저 완성한 뒤 확장해도 됩니다.

## 6. 다른 파트와 연결되는 부분

- Compute + Network: Security Group 규칙
- Observability / Platform: 장애 확인 순서와 상태 점검
- Terraform / IaC: secret/state 파일 관리, IAM 관련 리소스 주의사항

## 7. 최종 산출물

- 보안 주의사항 문서
- 기본 장애 대응 체크리스트
- 커밋 금지 파일 기준
