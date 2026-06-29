# 2026-06-29 공부기록 - 강세영

## 1. 담당 파트

AWS 인프라 프로젝트에서 **Compute + Network** 파트를 맡았다.

담당 범위는 전체 구조 중 아래 부분이다.

```text
사용자 → ALB → EC2
```

오늘은 실제 구축보다는 AWS 네트워크 기본 개념을 먼저 이해하고, 콘솔에서 VPC / Subnet 쪽을 확인했다.

---

## 2. 오늘 공부한 개념

오늘 공부한 개념은 다음과 같다.

* EC2
* SSH
* Key Pair
* VPC
* Subnet
* Public Subnet / Private Subnet
* Internet Gateway
* Route Table
* Main Route Table
* Explicit Association / Implicit Association
* Security Group
* Public IP / Private IP
* Port 22 / 80 / 443
* ALB
* Target Group
* Health Check
* AWS Region
* Availability Zone
* VPC CIDR / Subnet CIDR

---

## 3. 내가 이해한 내용

EC2는 AWS에서 빌리는 서버 컴퓨터이고, SSH로 접속해서 조작할 수 있다.

SSH 접속에는 Key Pair가 필요하고, SSH는 22번 포트를 사용한다.

VPC는 AWS 안에 만드는 내 프로젝트 전용 네트워크 공간이다.

Subnet은 VPC 안을 나눈 작은 네트워크 구역이다.

Subnet은 반드시 VPC의 CIDR 범위 안에 있어야 한다.

예를 들어 VPC가 아래 범위라면,

```text
10.0.0.0/16
```

Subnet은 아래처럼 만들 수 있다.

```text
10.0.1.0/24
10.0.2.0/24
```

하지만 VPC가 아래 범위라면,

```text
172.31.0.0/16
```

아래 Subnet은 만들 수 없다.

```text
10.0.1.0/24
```

오늘 Subnet을 만들다가 아래 에러를 봤다.

```text
CIDR 주소가 VPC의 CIDR 주소 내에 있지 않습니다.
```

이 에러는 내가 만들려는 Subnet CIDR이 선택한 VPC CIDR 안에 없다는 뜻이다.

또한 Subnet이 Public인지 Private인지는 이름이 아니라 Route Table로 결정된다는 것을 배웠다.

Public Subnet처럼 동작하려면 Route Table에 아래 경로가 있어야 한다.

```text
0.0.0.0/0 → Internet Gateway
```

Route Table은 트래픽이 어디로 갈지 정하는 길 안내표이고, Security Group은 어떤 포트를 열지 정하는 방화벽이다.

```text
Route Table = 길을 정함
Security Group = 문을 열고 닫음
```

Explicit Association은 Subnet에 Route Table을 직접 연결하는 것이고, Implicit Association은 직접 연결하지 않아서 Main Route Table을 자동으로 사용하는 것이다.

```text
Explicit Association = 직접 연결
Implicit Association = 기본값 자동 사용
```

---

## 4. GPT에게 물어본 질문

오늘 물어본 질문은 다음과 같다.

1. 1일차에 뭐부터 해야 하는지
2. 실습 전에 개념부터 공부해야 하는지
3. EC2, SSH, Key Pair가 무엇인지
4. VPC, Subnet, Internet Gateway, Route Table이 무엇인지
5. Security Group이 무엇인지
6. ALB, Target Group, Health Check가 무엇인지
7. Public IP와 Private IP의 차이가 무엇인지
8. 22번, 80번, 443번 포트가 무엇인지
9. 화면에 이미 Subnet이 3개 있는데 이게 뭔지
10. 시드니 리전밖에 안 보이는 이유가 뭔지
11. Subnet 생성 중 CIDR 에러가 왜 뜨는지
12. Explicit Association / Implicit Association이 무엇인지
13. Main Route Table에는 뭐가 들어있는지

---

## 5. 새로 알게 된 점

오늘 새로 알게 된 점은 다음과 같다.

* AWS 리소스는 Region별로 따로 보인다.
* 시드니 리전에서 작업하면 서울 리전 리소스가 보이지 않는다.
* 실습 전에 오른쪽 위 Region을 먼저 확인해야 한다.
* VPC를 만들 때 자동으로 Subnet이 여러 개 생길 수 있다.
* Subnet은 반드시 VPC CIDR 안에 있어야 한다.
* Public Subnet은 이름이 아니라 Route Table 경로로 결정된다.
* `0.0.0.0/0 → Internet Gateway`가 있으면 외부 인터넷으로 나갈 수 있다.
* Main Route Table에는 기본적으로 `VPC CIDR → local` 경로가 있다.
* Route Table을 직접 연결하지 않은 Subnet은 Main Route Table을 자동으로 사용한다.
* 22번 포트는 SSH, 80번 포트는 HTTP, 443번 포트는 HTTPS에 사용된다.
* 22번 포트는 전체 공개하지 말고 내 IP만 열어야 한다.

---

## 6. Must / Optional 후보

### Must 후보

오늘 기준으로 앞으로 반드시 해야 할 것은 다음과 같다.

* 서울 리전인지 확인하기
* 사용할 VPC CIDR 확인하기
* Subnet CIDR이 VPC CIDR 안에 있는지 확인하기
* Internet Gateway 만들고 VPC에 연결하기
* Public Route Table 만들기
* `0.0.0.0/0 → Internet Gateway` 경로 추가하기
* Public Route Table을 Public Subnet에 직접 연결하기
* Security Group에서 22번 포트는 내 IP만 허용하기
* EC2 생성하기
* SSH 접속 성공하기

### Optional 후보

시간이 남으면 할 것은 다음과 같다.

* Nginx 설치하기
* Docker 설치하기
* Docker로 Nginx 실행하기
* ALB 만들기
* Target Group 만들기
* Health Check 확인하기

---

## 7. 아직 헷갈리는 부분

아직 헷갈리는 부분은 다음과 같다.

* `/16`, `/24` 같은 CIDR 계산이 아직 익숙하지 않다.
* VPC를 만들 때 자동으로 생긴 Subnet과 내가 직접 만든 Subnet의 차이가 헷갈린다.
* Main Route Table과 내가 만든 Route Table을 콘솔에서 구분하는 연습이 더 필요하다.
* Public Subnet과 Private Subnet을 실제로 어떻게 나누는지 더 실습해야 한다.
* EC2를 Public Subnet에 둘지 Private Subnet에 둘지 아직 완전히 감이 잡히지는 않았다.

---

## 8. 내일 할 일

내일 할 일은 다음과 같다.

1. AWS 콘솔에서 Region을 서울로 맞춘다.
2. VPC CIDR을 확인한다.
3. Subnet CIDR이 VPC CIDR 안에 들어가게 만든다.
4. Internet Gateway를 만든다.
5. Route Table에 `0.0.0.0/0 → Internet Gateway`를 추가한다.
6. Route Table을 Public Subnet에 연결한다.
7. EC2용 Security Group을 만든다.
8. 22번 포트는 내 IP만 허용한다.
9. EC2를 만든다.
10. SSH 접속을 성공시킨다.

내일 목표는 아래 흐름을 성공시키는 것이다.

```text
내 노트북 → SSH → EC2
```

---

## 9. 참고한 자료

* AWS 콘솔 VPC 화면
* AWS 콘솔 Subnet 생성 화면
* GPT 개념 설명
* GPT 확인 문제
* AWS SAA 교재 VPC / Region / Availability Zone 설명

---

## 오늘 메타인지 테스트 결과

오늘 개념 확인 문제를 풀었다.

```text
기본 개념 문제: 10/10
ALB / Target Group / Health Check 문제: 3/3
Public IP / Private IP / Security Group 문제: 4/4
포트 문제: 4/4
```

문제는 모두 맞혔지만, 실제 콘솔에서 CIDR과 Route Table을 연결하는 부분은 아직 더 연습이 필요하다.

---

## 오늘 실제로 한 실습

오늘 실제로 한 실습은 다음과 같다.

* AWS 콘솔에 들어갔다.
* VPC / Subnet 화면을 확인했다.
* 이미 Subnet이 여러 개 있는 것을 확인했다.
* Region이 시드니로 되어 있어서 서울 리소스가 안 보일 수 있다는 것을 알았다.
* Subnet을 만들다가 CIDR 관련 에러를 확인했다.
* VPC CIDR과 Subnet CIDR이 맞지 않으면 Subnet을 만들 수 없다는 것을 이해했다.
* Route Table, Main Route Table, Association 개념을 확인했다.

아직 EC2 생성과 SSH 접속까지는 진행하지 않았다.

---
