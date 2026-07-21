# Compute + Network Resource Handoff

> **민감정보 기록 금지**
>
> Access Key, Secret Access Key, Session Token, AWS 비밀번호, SSH Private Key, EC2 Private Key 파일 내용, GitHub Token, Database Password 등은 절대 기록하지 않는다.

| 항목 | 값 |
| --- | --- |
| 프로젝트명 | AWS Infra / SRE 14-Day Project |
| 작성일 | 2026-07-16 |
| 작성자 | 강세영 |
| 담당 파트 | Compute + Network |
| Region | ap-northeast-2 |
| Environment | dev |
| Project | aws-infra-sre |

## 1. VPC

| 항목 | 값 |
| --- | --- |
| Resource Type | VPC |
| Resource Name | `aws-infra-sre-dev-vpc` |
| Resource ID | `vpc-04ac5e34907e1e0e9` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| CIDR | `10.0.0.0/16` |
| Region | `ap-northeast-2` |
| Public/Private 여부 | VPC boundary |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-vpc` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `project-network` |
| Must Tag 적용 상태 | 완료 |

검증 결과:

- VPC CIDR이 `10.0.0.0/16`임을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- 기존 Console 리소스이므로 Terraform으로 중복 생성하면 안 된다.
- `terraform import` 또는 재생성 여부는 추후 확정한다.

## 2. Public Subnet A

| 항목 | 값 |
| --- | --- |
| Resource Type | Public Subnet |
| Resource Name | `aws-infra-sre-dev-public-subnet-a` |
| Resource ID | `subnet-0da0e473f97b614fa` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet ID | `subnet-0da0e473f97b614fa` |
| Availability Zone | `ap-northeast-2a` |
| Availability Zone ID | `apne2-az1` |
| CIDR | `10.0.1.0/24` |
| Public/Private 여부 | Public |
| Route Table ID | `rtb-0ffacb032b9943e43` |
| Internet Gateway ID | `igw-06e83aa7e2a1cd757` |
| Public IPv4 자동 할당 | 비활성화 |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-public-subnet-a` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `public-workload` |
| Must Tag 적용 상태 | 완료 |

검증 결과:

- Public Subnet A가 `10.0.1.0/24`이며 `ap-northeast-2a`에 있음을 확인했다.
- Public Subnet A가 Public Route Table과 연결되어 있음을 확인했다.
- 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- Subnet 이름만으로 Public 여부가 결정되지 않는다. Public Route Table 연결과 IGW 경로가 필요하다.
- 기존 Console 리소스이므로 Terraform으로 중복 생성하면 안 된다.

## 3. Public Subnet B

| 항목 | 값 |
| --- | --- |
| Resource Type | Public Subnet |
| Resource Name | `aws-infra-sre-dev-public-subnet-b` |
| Resource ID | `subnet-08124f6af7f10cc98` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet ID | `subnet-08124f6af7f10cc98` |
| Availability Zone | `ap-northeast-2c` |
| Availability Zone ID | `apne2-az3` |
| CIDR | `10.0.2.0/24` |
| Public/Private 여부 | Public |
| Route Table ID | `rtb-0ffacb032b9943e43` |
| Internet Gateway ID | `igw-06e83aa7e2a1cd757` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-public-subnet-b` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `public-workload` |
| Must Tag 적용 상태 | 완료 |

검증 결과:

- Public Subnet B가 `10.0.2.0/24`이며 `ap-northeast-2c`에 있음을 확인했다.
- Public Subnet B가 Public Route Table과 연결되어 있음을 확인했다.
- 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- 기존 Console 리소스이므로 Terraform으로 중복 생성하면 안 된다.

## 4. Internet Gateway

| 항목 | 값 |
| --- | --- |
| Resource Type | Internet Gateway |
| Resource Name | `aws-infra-sre-dev-igw` |
| Resource ID | `igw-06e83aa7e2a1cd757` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Internet Gateway ID | `igw-06e83aa7e2a1cd757` |
| 연결된 리소스 | VPC, Public Route Table default route |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-igw` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `internet-access` |
| Must Tag 적용 상태 | 완료 |

검증 결과:

- Internet Gateway `igw-06e83aa7e2a1cd757`가 VPC `vpc-04ac5e34907e1e0e9`에 연결되어 있으며 Public Route Table의 `0.0.0.0/0` 대상임을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- Console에서 Resource Name `aws-infra-sre-dev-igw`와 Resource ID `igw-06e83aa7e2a1cd757`를 확인했다.

## 5. Public Route Table

| 항목 | 값 |
| --- | --- |
| Resource Type | Route Table |
| Resource Name | `aws-infra-sre-dev-public-rt` |
| 목표 Name | `aws-infra-sre-dev-public-rt` |
| Resource ID | `rtb-0ffacb032b9943e43` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Route Table ID | `rtb-0ffacb032b9943e43` |
| 연결된 리소스 | Public Subnet A, Public Subnet B |
| Internet Gateway ID | `igw-06e83aa7e2a1cd757` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-public-rt` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `public-routing` |
| Must Tag 적용 상태 | 완료 |

확인된 Route:

| Destination | Target |
| --- | --- |
| `10.0.0.0/16` | local |
| `0.0.0.0/0` | `igw-06e83aa7e2a1cd757` |

검증 결과:

- Public Subnet A와 Public Subnet B가 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- Console에서 Resource Name `aws-infra-sre-dev-public-rt`와 Resource ID `rtb-0ffacb032b9943e43`를 확인했다.

## 6. ALB Security Group

| 항목 | 값 |
| --- | --- |
| Resource Type | Security Group |
| Resource Name | `aws-infra-sre-dev-alb-sg` |
| Resource ID | `sg-053e06d50216483fe` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Security Group ID | `sg-053e06d50216483fe` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-alb-sg` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `alb-traffic-control` |
| Must Tag 적용 상태 | 완료 |

Inbound 규칙:

| Protocol | Port | Source | Purpose |
| --- | --- | --- | --- |
| TCP | `80` | `0.0.0.0/0` | 인터넷에서 ALB로 들어오는 HTTP 허용 |

Outbound 규칙:

| Protocol | Port | Destination |
| --- | --- | --- |
| All traffic | All | `0.0.0.0/0` |

검증 결과:

- ALB Security Group `sg-053e06d50216483fe`가 VPC `vpc-04ac5e34907e1e0e9`에 생성되었음을 확인했다.
- TCP 80 inbound가 `0.0.0.0/0`에서 허용됨을 확인했다.
- outbound all traffic이 `0.0.0.0/0` 대상으로 허용됨을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- ALB는 아직 생성되지 않았다.

## 7. EC2 Security Group

| 항목 | 값 |
| --- | --- |
| Resource Type | Security Group |
| Resource Name | `aws-infra-sre-dev-ec2-sg` |
| Resource ID | `sg-03a67f4bd0610147e` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Security Group ID | `sg-03a67f4bd0610147e` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-ec2-sg` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `ec2-traffic-control` |
| Must Tag 적용 상태 | 완료 |

Inbound 규칙:

| Protocol | Port | Source | Purpose |
| --- | --- | --- | --- |
| TCP | `80` | ALB Security Group `sg-053e06d50216483fe` | ALB에서 EC2로 전달되는 HTTP만 허용 |
| TCP | `22` | administrator My IP | 관리자 SSH 접속 |

Outbound 규칙:

| Protocol | Port | Destination |
| --- | --- | --- |
| All traffic | All | `0.0.0.0/0` |

검증 결과:

- EC2 Security Group `sg-03a67f4bd0610147e`가 VPC `vpc-04ac5e34907e1e0e9`에 생성되었음을 확인했다.
- TCP 80 inbound source가 ALB Security Group `sg-053e06d50216483fe`로 제한됨을 확인했다.
- TCP 22 inbound source는 생성 당시 현재 관리자 공인 IP로 제한했다.
- outbound all traffic이 `0.0.0.0/0` 대상으로 허용됨을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- EC2 Port 80을 `0.0.0.0/0`에 직접 개방하지 않는 것을 기본 원칙으로 한다.
- 정확한 SSH CIDR 값은 제공되지 않았으므로 `administrator My IP`로 기록한다.

## 8. EC2

| 항목 | 값 |
| --- | --- |
| Resource Type | EC2 |
| Resource Name | `aws-infra-sre-dev-app-ec2` |
| Resource ID | `i-07d3895c10c0706be` |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet Name | `aws-infra-sre-dev-public-subnet-a` |
| Subnet ID | `subnet-0da0e473f97b614fa` |
| Subnet CIDR | `10.0.1.0/24` |
| Availability Zone | `ap-northeast-2a` |
| Private IPv4 | `10.0.1.93` |
| Current Public IPv4 | `3.39.252.131` |
| AMI | Amazon Linux 2023 |
| Architecture | 64-bit x86 |
| Instance Type | TBD — AWS Console 확인 필요 |
| Key Pair | `aws-infra-sre-dev-ec2-key` |
| Security Group Name | `aws-infra-sre-dev-ec2-sg` |
| Security Group ID | `sg-03a67f4bd0610147e` |
| Host Port | `80` |
| Container Port | `8000` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` |
| Tag: Name | `aws-infra-sre-dev-app-ec2` |
| Tag: Project | `aws-infra-sre` |
| Tag: Environment | `dev` |
| Tag: Owner | `compute-network` |
| Tag: ManagedBy | `console` |
| Tag: Purpose | `minipep-app` |
| Must Tag 적용 상태 | 완료 |

검증 결과:

- EC2 `i-07d3895c10c0706be`가 Public Subnet A에 생성되었음을 확인했다.
- Public IPv4 `3.39.252.131`이 할당되었음을 확인했다.
- Key Pair `aws-infra-sre-dev-ec2-key`를 사용해 SSH 접속에 성공했다.
- SSH 사용자 `ec2-user`로 접속했다.
- Docker 설치가 완료되었다.
- `docker.service` 상태가 enabled 및 active (running)임을 확인했다.
- `ec2-user`를 docker 그룹에 추가했다.
- 재접속 후 sudo 없이 `docker ps` 실행에 성공했다.
- 임시 Nginx 컨테이너 `nginx-test`로 EC2 host port 80 연결을 검증했다.
- `curl -I http://localhost` 결과 `HTTP/1.1 200 OK`와 `Server: nginx/1.31.3`을 확인했다.
- 검증 후 `nginx-test` 컨테이너를 삭제했다.
- 현재 EC2 host port 80은 MiniPEP 컨테이너 배포를 위해 비어 있다.
- MiniPEP FastAPI 배포를 완료했다.
- Docker Compose로 `minipep` 컨테이너를 실행했으며 Host Port `80`에서 Container Port `8000`으로 연결됨을 확인했다.
- `curl -i http://localhost/health` 결과 `HTTP/1.1 200 OK`와 `{"status":"ok","service":"minipep"}` 응답을 확인했다.
- `curl http://localhost/api/equipment`로 Equipment API 정상 응답을 확인했다.
- `curl http://localhost/api/jobs`로 Jobs API 정상 응답을 확인했다.
- `docker compose logs`로 MiniPEP 애플리케이션 시작 로그와 요청 로그를 확인했다.

특이사항:

- Public IPv4는 Elastic IP가 아니므로 인스턴스 중지 후 재시작 시 변경될 수 있다.
- Nginx는 임시 포트 연결 테스트용이며 최종 아키텍처가 아니다.
- 임시 검증 컨테이너는 `nginx:alpine` 이미지, container name `nginx-test`, port mapping `80:80`으로 실행했다.
- 최종 앱은 MiniPEP FastAPI이며 Docker Container Port `8000`으로 실행한다.
- Docker Compose 사용을 위해 EC2에 `git`과 Docker Compose CLI 플러그인을 설치했다.
- `docker compose build` 최초 실행 시 buildx 버전 요구사항으로 실패했으며, Docker Buildx 플러그인을 `v0.25.0`으로 갱신한 뒤 재빌드에 성공했다.

## 9. ALB

| 항목 | 값 |
| --- | --- |
| Resource Type | Application Load Balancer |
| Resource Name | `aws-infra-sre-dev-alb` |
| Resource ID | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet ID | TBD — Day 3 생성 후 기록 |
| Security Group ID | TBD — Day 3 생성 후 기록 |
| Listener Port | `80` |
| ALB DNS | TBD — Day 3 생성 후 기록 |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

검증 결과:

- ALB는 아직 생성되지 않았다.

특이사항:

- Internet-facing ALB로 구성할 예정이다.
- ALB는 Public Subnet A와 Public Subnet B를 사용해야 한다.

## 10. Target Group

| 항목 | 값 |
| --- | --- |
| Resource Type | Target Group |
| Resource Name | `aws-infra-sre-dev-app-tg` |
| Resource ID | TBD — Day 3 생성 후 기록 |
| Target Group ARN | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Target Port | `80` |
| Host Port | `80` |
| Container Port | `8000` |
| Health Check Path | `/health` |
| Health Check Success Code | `200` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

검증 결과:

- Target Group은 아직 생성되지 않았다.

특이사항:

- ALB Listener Port `80`에서 Target Group Port `80`으로 전달한다.
- EC2 Host Port `80`은 Docker Container Port `8000`으로 연결한다.
- 최종 Health Check Path는 `/health`이다.

## Terraform Variable로 전달할 값

- `aws_region = "ap-northeast-2"`
- `project = "aws-infra-sre"`
- `environment = "dev"`
- `vpc_cidr = "10.0.0.0/16"`
- `public_subnet_a_cidr = "10.0.1.0/24"`
- `public_subnet_a_az = "ap-northeast-2a"`
- `public_subnet_b_cidr = "10.0.2.0/24"`
- `public_subnet_b_az = "ap-northeast-2c"`
- `alb_listener_port = 80`
- `target_group_port = 80`
- `ec2_host_port = 80`
- `container_port = 8000`
- `health_check_path = "/health"`
- `health_check_success_code = "200"`
- 각 리소스 이름
- `common_tags`

## Terraform Output으로 필요한 값

- `vpc_id`
- `public_subnet_a_id`
- `public_subnet_b_id`
- `internet_gateway_id`
- `public_route_table_id`
- `alb_security_group_id`
- `ec2_security_group_id`
- `ec2_instance_id`
- `ec2_public_ip`
- `alb_arn`
- `alb_dns_name`
- `target_group_arn`

## 공통 Tag 값

| Key | Value |
| --- | --- |
| Project | `aws-infra-sre` |
| Environment | `dev` |
| Owner | `compute-network` |
| ManagedBy | `console` |

## 기존 리소스 Must Tag 적용 요약

| Resource | Name | Purpose | ManagedBy | 적용 상태 |
| --- | --- | --- | --- | --- |
| VPC | `aws-infra-sre-dev-vpc` | `project-network` | `console` | 완료 |
| Public Subnet A | `aws-infra-sre-dev-public-subnet-a` | `public-workload` | `console` | 완료 |
| Public Subnet B | `aws-infra-sre-dev-public-subnet-b` | `public-workload` | `console` | 완료 |
| Internet Gateway | `aws-infra-sre-dev-igw` | `internet-access` | `console` | 완료 |
| Public Route Table | `aws-infra-sre-dev-public-rt` | `public-routing` | `console` | 완료 |
| ALB Security Group | `aws-infra-sre-dev-alb-sg` | `alb-traffic-control` | `console` | 완료 |
| EC2 Security Group | `aws-infra-sre-dev-ec2-sg` | `ec2-traffic-control` | `console` | 완료 |
| EC2 | `aws-infra-sre-dev-app-ec2` | `minipep-app` | `console` | 완료 |

## 전체 검증 요약

- VPC CIDR이 `10.0.0.0/16`임을 확인했다.
- Public Subnet A가 `10.0.1.0/24`이며 `ap-northeast-2a`에 있음을 확인했다.
- Public Subnet B가 `10.0.2.0/24`이며 `ap-northeast-2c`에 있음을 확인했다.
- Public Subnet A와 Public Subnet B가 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- ALB Security Group `sg-053e06d50216483fe`와 EC2 Security Group `sg-03a67f4bd0610147e`가 생성되었음을 확인했다.
- EC2 `i-07d3895c10c0706be`가 Public Subnet A에 생성되었고 현재 Public IPv4 `3.39.252.131`이 할당되었음을 확인했다.
- SSH, Docker, 임시 Nginx host port 80 검증을 완료했다.
- ALB와 Target Group은 아직 생성되지 않았다.
