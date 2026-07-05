# Compute + Network Must / Optional

Owner: 강세영
Scope: 사용자 -> ALB -> EC2 -> Docker/Nginx -> CloudWatch 중 Compute + Network 중심

## 1. 담당 범위

이번 2주 AWS 인프라 프로젝트에서 Compute + Network 파트를 담당한다.

주요 담당 범위는 다음과 같다.

```text
사용자 -> ALB -> EC2
```

사용자의 요청이 ALB를 거쳐 EC2 서버까지 정상적으로 도착하도록 VPC, Subnet, Route Table, Internet Gateway, Security Group, EC2, Target Group, Health Check를 이해하고 구성하는 것이 목표이다.

Docker/Nginx 실행은 애플리케이션 실행 확인을 위한 최소 수준으로 포함한다.

## 2. 최종 목표 구조

```text
사용자
  ↓
Internet-facing ALB
  ↓
Target Group
  ↓
EC2
  ↓
Docker / Nginx
```

최소 성공 기준은 브라우저에서 ALB DNS 주소로 접속했을 때 EC2에서 실행 중인 Nginx 화면이 정상적으로 보이는 것이다.

## 3. Must 기준

Must는 2주 안에 반드시 구현하거나 이해해야 하는 범위이다.

기준은 다음과 같다.

* 최종 아키텍처 완성에 반드시 필요한 것
* 직접 실습해서 포트폴리오에 설명할 수 있어야 하는 것
* 실패하면 전체 프로젝트 흐름이 끊기는 것

## 4. Must 목록

### 4.1 Region 확인

* 실습 전 AWS Region을 확인한다.
* 기준 Region은 `아시아 태평양(서울) / ap-northeast-2`이다.
* AWS 리소스는 Region별로 따로 존재하므로, 실습 리전이 바뀌면 VPC, Subnet, EC2 등이 다르게 보일 수 있음을 이해한다.

### 4.2 VPC 생성 및 이해

* 프로젝트용 VPC를 직접 생성한다.
* 예시:
  * VPC Name: `project-vpc`
  * CIDR: `10.0.0.0/16`

이해해야 할 내용:

* VPC는 AWS 안에 만드는 프로젝트 전용 네트워크 공간이다.
* VPC CIDR은 이 네트워크에서 사용할 전체 IP 주소 범위이다.
* EC2, ALB, Subnet, Route Table, Security Group은 VPC 안에서 구성된다.

### 4.3 Public Subnet 생성

* Public Subnet을 최소 2개 생성한다.
* 예시:
  * Public Subnet A: `10.0.1.0/24`
  * Public Subnet B: `10.0.2.0/24`

이해해야 할 내용:

* Subnet은 VPC 안을 더 작게 나눈 네트워크 구역이다.
* Subnet CIDR은 반드시 VPC CIDR 안에 포함되어야 한다.
* ALB는 최소 2개 이상의 Availability Zone에 걸친 Subnet이 필요하다.
* Public Subnet인지 여부는 이름이 아니라 Route Table에 의해 결정된다.

### 4.4 Internet Gateway 생성 및 연결

* Internet Gateway를 생성하고 VPC에 Attach한다.
* 예시:
  * Internet Gateway: `project-igw`
  * Attach to: `project-vpc`

이해해야 할 내용:

* Internet Gateway는 VPC가 인터넷과 통신하기 위한 출입문이다.
* Internet Gateway를 만들기만 해서는 인터넷 연결이 완성되지 않는다.
* Route Table에 Internet Gateway로 가는 경로를 추가해야 한다.

### 4.5 Public Route Table 생성 및 연결

* Public Route Table을 생성하고 Public Subnet에 연결한다.
* 예시 Route:
  * `10.0.0.0/16 -> local`
  * `0.0.0.0/0 -> Internet Gateway`

이해해야 할 내용:

* Route Table은 트래픽이 어디로 가야 하는지 정하는 길 안내표이다.
* `local` 경로는 VPC 내부 통신을 의미한다.
* `0.0.0.0/0 -> Internet Gateway` 경로가 있어야 인터넷으로 나갈 수 있다.
* Route Table을 Subnet에 직접 연결하는 것을 Explicit Association이라고 한다.
* 직접 연결하지 않으면 Main Route Table을 자동으로 사용하는데, 이것을 Implicit Association이라고 한다.

### 4.6 Security Group 구성

* ALB용 Security Group과 EC2용 Security Group을 분리해서 만든다.

ALB Security Group:

```text
Inbound
HTTP 80 from 0.0.0.0/0
```

EC2 Security Group:

```text
Inbound
SSH 22 from My IP
HTTP 80 from ALB Security Group
```

이해해야 할 내용:

* Security Group은 EC2나 ALB 앞의 방화벽 역할을 한다.
* Route Table은 길을 정하고, Security Group은 문을 열고 닫는다.
* SSH 22번 포트는 반드시 내 IP만 허용한다.
* EC2의 80번 포트는 최종적으로 ALB Security Group에서만 접근 가능하게 한다.
* 사용자가 EC2에 직접 접근하는 구조가 아니라 ALB를 통해 접근하는 구조로 만든다.

### 4.7 EC2 생성 및 SSH 접속

* Public Subnet에 EC2를 생성하고 SSH 접속을 성공시킨다.
* 예시:
  * EC2 Name: `project-web-ec2`
  * AMI: Ubuntu
  * Instance Type: `t2.micro` 또는 `t3.micro`
  * Subnet: Public Subnet A
  * Public IP: Enable
  * Security Group: EC2 SG

SSH 접속 예시:

```bash
ssh -i <KEY_PAIR_FILE> ubuntu@EC2_PUBLIC_IP
```

이해해야 할 내용:

* EC2는 AWS에서 빌리는 서버 컴퓨터이다.
* Key Pair는 비밀번호 대신 사용하는 접속 열쇠이다.
* Public Subnet에 있고 Public IP가 있어야 외부에서 SSH 접속할 수 있다.
* SSH 접속이 안 될 경우 Security Group, Public IP, Route Table, Key Pair 권한을 확인해야 한다.

### 4.8 Docker 또는 Nginx 실행

* EC2 안에서 Nginx를 실행한다.

최소 방식 1: 직접 Nginx 설치

```bash
sudo apt update
sudo apt install -y nginx
```

최소 방식 2: Docker로 Nginx 실행

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo docker run -d -p 80:80 nginx
```

이해해야 할 내용:

* EC2 안에서 웹 서버가 실행되어야 ALB Health Check가 성공할 수 있다.
* Nginx는 80번 포트로 요청을 받아야 한다.
* 브라우저에서 EC2 Public IP 또는 ALB DNS로 접속했을 때 Nginx 화면이 보여야 한다.

### 4.9 Target Group 생성

* ALB가 요청을 보낼 EC2 목록인 Target Group을 생성한다.
* 예시:
  * Target Type: Instance
  * Protocol: HTTP
  * Port: 80
  * Health Check Path: `/`
  * Target: EC2 instance

이해해야 할 내용:

* Target Group은 ALB가 트래픽을 전달할 대상 목록이다.
* Health Check는 EC2가 정상 응답하는지 확인하는 검사이다.
* Health Check가 unhealthy이면 ALB가 EC2로 트래픽을 보내지 않을 수 있다.

### 4.10 ALB 생성

* Internet-facing ALB를 생성한다.
* 예시:
  * Scheme: Internet-facing
  * Subnets: Public Subnet A, Public Subnet B
  * Security Group: ALB SG
  * Listener: HTTP 80
  * Forward to: Target Group

이해해야 할 내용:

* ALB는 사용자의 HTTP 요청을 받아 EC2로 전달한다.
* ALB는 최소 2개 이상의 Public Subnet에 연결해야 한다.
* 사용자는 EC2 Public IP가 아니라 ALB DNS 주소로 접속하는 것이 목표이다.

### 4.11 최종 연결 확인

최종적으로 아래 흐름을 확인한다.

```text
사용자 브라우저
  ↓
ALB DNS
  ↓
ALB Security Group
  ↓
Target Group
  ↓
EC2 Security Group
  ↓
Docker / Nginx
```

성공 기준:

* ALB DNS 주소로 접속했을 때 Nginx 화면이 보인다.
* Target Group Health Check가 healthy 상태이다.
* EC2 80번 포트는 ALB Security Group에서만 접근 가능하다.
* SSH 22번 포트는 내 IP만 허용되어 있다.

## 5. Optional 기준

Optional은 시간이 남으면 도전할 범위이다.

기준은 다음과 같다.

* 고도화 또는 보안 강화에 해당하는 것
* 실패해도 기본 프로젝트 완성에는 큰 영향이 없는 것
* 포트폴리오에서 추가 설명 요소가 될 수 있는 것

## 6. Optional 목록

### 6.1 Private Subnet 구성

* EC2를 Public Subnet이 아니라 Private Subnet에 배치하는 구조를 도전한다.

예상 구조:

```text
사용자 -> ALB -> Private EC2 -> Docker/Nginx
```

추가로 이해해야 할 내용:

* Private Subnet은 인터넷에서 직접 접근할 수 없다.
* EC2에 직접 SSH 접속하려면 Bastion Host 또는 Session Manager 같은 추가 구성이 필요하다.
* Private Subnet의 EC2가 외부 패키지를 설치하려면 NAT Gateway 또는 다른 대안이 필요하다.

### 6.2 NAT Gateway 구성

* Private Subnet의 EC2가 인터넷으로 나갈 수 있도록 NAT Gateway를 구성한다.

이해해야 할 내용:

* NAT Gateway는 Private Subnet 리소스가 외부 인터넷으로 나갈 수 있게 해준다.
* 외부에서 Private EC2로 직접 들어오는 것은 허용하지 않는다.
* NAT Gateway는 비용이 발생하므로 2주 프로젝트에서는 Optional로 둔다.

### 6.3 Bastion Host 구성

* Private EC2에 접속하기 위한 Bastion Host를 구성한다.

예상 구조:

```text
내 노트북 -> Bastion Host -> Private EC2
```

이해해야 할 내용:

* Bastion Host는 Private Subnet 내부 서버에 접속하기 위한 중간 서버이다.
* SSH 접근 제어와 보안 관리가 중요하다.
* 운영 환경에서는 Bastion보다 Session Manager를 고려할 수도 있다.

### 6.4 HTTPS 적용

* ACM 인증서와 HTTPS Listener를 사용해서 ALB에 HTTPS를 적용한다.

추가 구성:

```text
HTTP 80
HTTPS 443
ACM Certificate
Route 53 도메인 연결
```

이해해야 할 내용:

* HTTPS는 전송 중 데이터 암호화를 위해 사용한다.
* ALB에서 TLS 인증서를 연결할 수 있다.
* 도메인이 필요할 수 있으므로 Optional로 둔다.

### 6.5 Auto Scaling Group 구성

* EC2를 Auto Scaling Group으로 관리하는 구조를 도전한다.

이해해야 할 내용:

* Auto Scaling Group은 EC2 인스턴스 수를 자동으로 조절한다.
* Launch Template이 필요하다.
* ALB Target Group과 연결할 수 있다.
* 2주 프로젝트 기본 구조에서는 EC2 1대로도 충분하므로 Optional로 둔다.

### 6.6 CloudWatch Alarm 연동

* EC2 또는 ALB 지표를 CloudWatch에서 확인하고 Alarm을 설정한다.

예시:

```text
EC2 CPUUtilization
ALB TargetResponseTime
ALB HTTPCode_Target_5XX_Count
```

이해해야 할 내용:

* CloudWatch는 AWS 리소스의 로그와 지표를 확인하는 서비스이다.
* Alarm은 특정 조건이 발생했을 때 알림을 보낼 수 있다.
* Observability 담당자와 협업해서 진행한다.

### 6.7 WAF 적용

* ALB 앞에 AWS WAF를 붙여 기본적인 웹 공격 방어를 실습한다.

이해해야 할 내용:

* WAF는 SQL Injection, XSS 같은 웹 공격을 일부 방어할 수 있다.
* Security 담당자와 협업해서 진행한다.
* 기본 ALB 연결 성공 이후에 도전한다.

### 6.8 Terraform으로 리소스 재구성

* 콘솔로 만든 VPC, Subnet, Route Table, EC2, ALB 구성을 Terraform 코드로 재현한다.

이해해야 할 내용:

* Terraform은 인프라를 코드로 관리하는 IaC 도구이다.
* Terraform 담당자와 협업해서 진행한다.
* 처음부터 Terraform으로만 진행하지 않고, 콘솔로 개념을 먼저 이해한 뒤 코드화한다.

## 7. 이번 2주 프로젝트에서 제외할 것

아래 내용은 이번 2주 안에서는 범위를 넓히지 않기 위해 제외한다.

* Multi Region 구성
* EKS 구성
* ECS/Fargate 전환
* 복잡한 Blue/Green 배포
* 실제 운영 수준의 보안 정책 전체 적용
* 고급 네트워크 구성 Transit Gateway, Direct Connect, VPN
* 대규모 트래픽 테스트

## 8. 회의 공유용 요약

Compute + Network 파트의 Must는 사용자 요청이 ALB를 거쳐 EC2의 Docker/Nginx까지 도달하는 기본 흐름을 완성하는 것이다.

Must 범위는 VPC, Public Subnet 2개, Internet Gateway, Public Route Table, Security Group 분리, EC2 생성, SSH 접속, Nginx 실행, Target Group, ALB, Health Check 성공까지이다.

Optional은 Private Subnet, NAT Gateway, Bastion Host, HTTPS, Auto Scaling Group, CloudWatch Alarm, WAF, Terraform 코드화로 둔다.

2주 안에 반드시 성공시킬 기준은 ALB DNS로 접속했을 때 Nginx 화면이 보이고, Target Group Health Check가 healthy가 되는 것이다.
