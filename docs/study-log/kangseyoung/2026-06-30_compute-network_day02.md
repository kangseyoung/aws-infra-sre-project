
# 2026-06-30 공부기록 - 강세영

## 1. 담당 파트

AWS 인프라 프로젝트에서 Compute + Network 파트를 담당한다.

오늘은 AWS 콘솔에서 VPC 기본 네트워크 구성을 실습했다.

## 2. 오늘 공부한 개념

오늘 공부한 개념은 다음과 같다.

- Public Subnet
- Internet Gateway
- Route Table
- Default Route
- Explicit Association

## 3. 내가 이해한 내용

프로젝트용 VPC의 CIDR은 `10.0.0.0/16`으로 맞췄고, Public Subnet은 아래처럼 나누었다.

- Public Subnet A: `10.0.1.0/24`
- Public Subnet B: `10.0.2.0/24`

그리고 Internet Gateway를 생성해서 VPC에 Attach했다.

Public Route Table을 만든 뒤, 외부 인터넷으로 나가기 위한 경로를 추가했다.

마지막으로 Public Route Table을 Public Subnet에 Explicit Association으로 연결했다.

## 4. GPT에게 물어본 질문

* AWS 콘솔에서 Region을 먼저 확인해야 하는 이유
* Internet Gateway가 하는 역할
* Explicit Association이 무엇인지

## 5. 새로 알게 된 점

Subnet을 여러 개 만드는 이유는 나중에 ALB나 고가용성 구성을 위해 여러 AZ에 리소스를 나누기 위해서

## 6. Must / Optional 후보

오늘은 간단 실습 위주라 따로 정리하지 않았다.

## 7. 아직 헷갈리는 부분

* Explicit Association과 Main Route Table의 차이
* CIDR을 직접 나눌 때 계산하는 방법

## 8. 내일 할 일

* 오늘 만든 VPC, Subnet, Internet Gateway, Route Table 구성을 다시 확인하기
* Public Subnet에 EC2를 띄우는 실습 준비하기
* Security Group과 SSH 접속 개념 공부하기
* 계절학기 시험기간이라 시험공부도 병행하기

## 9. 참고한 자료

* AWS Management Console
* GPT 설명
* 팀 프로젝트 실습 가이드
