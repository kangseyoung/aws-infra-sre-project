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
| Resource ID | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet ID | TBD — Day 3 생성 후 기록 |
| Availability Zone | `ap-northeast-2c` |
| Availability Zone ID | TBD — Day 3 생성 후 기록 |
| CIDR | `10.0.2.0/24` |
| Public/Private 여부 | Public 예정 |
| Route Table ID | TBD — Day 3 생성 후 기록 |
| Internet Gateway ID | Verification Needed — AWS Console 확인 필요 |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

검증 결과:

- Public Subnet B는 아직 생성되지 않았다.

특이사항:

- Day 3 생성 후 Subnet ID와 Route Table Association 상태를 기록한다.

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
| 연결된 리소스 | Public Subnet A |
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

- Public Subnet A가 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- Must Tag 적용이 완료되었음을 확인했다.

특이사항:

- Console에서 Resource Name `aws-infra-sre-dev-public-rt`와 Resource ID `rtb-0ffacb032b9943e43`를 확인했다.

## 6. ALB Security Group

| 항목 | 값 |
| --- | --- |
| Resource Type | Security Group |
| Resource Name | `aws-infra-sre-dev-alb-sg` |
| Resource ID | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Security Group ID | TBD — Day 3 생성 후 기록 |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

예정 Inbound 규칙:

| Protocol | Port | Source |
| --- | --- | --- |
| TCP | `80` | `0.0.0.0/0` |

예정 Outbound 규칙:

| Protocol | Port | Destination |
| --- | --- | --- |
| TCP | `80` | EC2 Security Group 방향 통신 허용 예정 |

검증 결과:

- ALB Security Group은 아직 생성되지 않았다.

특이사항:

- Day 3 생성 후 실제 Security Group ID와 규칙을 기록한다.

## 7. EC2 Security Group

| 항목 | 값 |
| --- | --- |
| Resource Type | Security Group |
| Resource Name | `aws-infra-sre-dev-ec2-sg` |
| Resource ID | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Security Group ID | TBD — Day 3 생성 후 기록 |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

예정 Inbound 규칙:

| Protocol | Port | Source |
| --- | --- | --- |
| TCP | `80` | ALB Security Group |

예정 Outbound 규칙:

| Protocol | Port | Destination |
| --- | --- | --- |
| TBD | TBD — Day 3 생성 후 기록 | TBD — Day 3 생성 후 기록 |

검증 결과:

- EC2 Security Group은 아직 생성되지 않았다.

특이사항:

- EC2 Port 80을 `0.0.0.0/0`에 직접 개방하지 않는 것을 기본 원칙으로 한다.
- SSH 규칙은 아직 확정되지 않았으므로 임의로 추가하지 않는다.

## 8. EC2

| 항목 | 값 |
| --- | --- |
| Resource Type | EC2 |
| Resource Name | `aws-infra-sre-dev-app-ec2` |
| Resource ID | TBD — Day 3 생성 후 기록 |
| VPC ID | `vpc-04ac5e34907e1e0e9` |
| Subnet ID | TBD — Day 3 생성 후 기록 |
| Security Group ID | TBD — Day 3 생성 후 기록 |
| EC2 Public IP | TBD — Day 3 생성 후 기록 |
| Host Port | `80` |
| Container Port | `8000` |
| Terraform 반영 여부 | No |
| ManagedBy | `console` 예정 |

검증 결과:

- EC2는 아직 생성되지 않았다.

특이사항:

- Nginx는 초기 연결 테스트용이다.
- 최종 앱은 MiniPEP FastAPI이며 Docker Container Port `8000`으로 실행한다.

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
| Internet Gateway | `aws-infra-sre-dev-igw` | `internet-access` | `console` | 완료 |
| Public Route Table | `aws-infra-sre-dev-public-rt` | `public-routing` | `console` | 완료 |

## 전체 검증 요약

- VPC CIDR이 `10.0.0.0/16`임을 확인했다.
- Public Subnet A가 `10.0.1.0/24`이며 `ap-northeast-2a`에 있음을 확인했다.
- Public Subnet A가 연결된 Route Table에 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 있음을 확인했다.
- Public Subnet B와 이후 리소스는 아직 생성되지 않았다.
