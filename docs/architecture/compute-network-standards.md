# Compute + Network Standards

## 1. 문서 목적

이 문서는 `AWS Infra / SRE 14-Day Project`의 Day 2 Compute + Network 설계 기준을 정리한다.

목적은 AWS Console에서 이미 확인한 값과 Day 3에 생성할 값을 구분하고, Terraform 담당자가 중복 리소스를 만들지 않도록 필요한 입력값과 출력값을 명확히 전달하는 것이다.

| 항목 | 값 |
| --- | --- |
| 작성일 | 2026-07-16 |
| Environment | dev |
| Project | aws-infra-sre |
| 담당자 | 강세영 |
| 담당 파트 | Compute + Network |
| Region | ap-northeast-2 |

## 2. 최종 서비스 구조

```text
사용자
  -> Internet-facing ALB Port 80
  -> Target Group Port 80
  -> EC2 Host Port 80
  -> Docker Container Port 8000
  -> MiniPEP FastAPI
```

애플리케이션 기준은 다음과 같다.

| 항목 | 값 |
| --- | --- |
| Main Page | `/` |
| Health Check Path | `/health` |
| Expected Health Check Code | `200` |
| Container Port | `8000` |
| EC2 Host Port | `80` |
| Target Group Port | `80` |
| ALB Listener Port | `80` |
| Persistence | Local SQLite |
| 초기 연결 테스트 | Nginx |
| 최종 앱 | MiniPEP FastAPI |

## 3. 네트워크 CIDR

| 항목 | 값 |
| --- | --- |
| VPC Name | `aws-infra-sre-dev-vpc` |
| VPC CIDR | `10.0.0.0/16` |

VPC는 프로젝트 전용 네트워크 범위이다. Subnet CIDR은 반드시 VPC CIDR 안에 포함되어야 한다.

## 4. Public Subnet 구성

| 구분 | Name | CIDR | Availability Zone | Availability Zone ID | 상태 |
| --- | --- | --- | --- | --- | --- |
| Public Subnet A | `aws-infra-sre-dev-public-subnet-a` | `10.0.1.0/24` | `ap-northeast-2a` | `apne2-az1` | 생성됨 |
| Public Subnet B | `aws-infra-sre-dev-public-subnet-b` | `10.0.2.0/24` | `ap-northeast-2c` | TBD — Day 3 생성 후 기록 | Day 3 생성 예정 |

Subnet 이름에 `public`이 들어간다고 해서 자동으로 Public Subnet이 되는 것은 아니다.

Public Subnet으로 동작하려면 연결된 Route Table에 다음 경로가 있어야 한다.

```text
0.0.0.0/0 -> Internet Gateway
```

Public Subnet A는 현재 Public Route Table과 연결되어 있으며, `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로가 확인되었다. Public Subnet B는 아직 생성되지 않았다.

## 5. Day 2 Must 네트워크 범위

Day 2 기준으로 설계에 포함하는 리소스는 다음과 같다.

| 범위 | 포함 여부 |
| --- | --- |
| VPC | Must |
| Public Subnet 2개 | Must |
| Internet Gateway | Must |
| Public Route Table | Must |
| Security Group | Must |
| EC2 | Must |
| ALB | Must |
| Target Group | Must |

이번 범위에서 제외하는 항목은 다음과 같다.

- Private Subnet
- NAT Gateway
- Auto Scaling Group
- WAF
- 기타 복잡한 엔터프라이즈 구조

## 6. Naming Convention

리소스 이름은 다음 규칙을 따른다.

```text
<project>-<environment>-<resource>[-<suffix>]
```

약어는 다음처럼 사용한다.

| 약어 | 의미 |
| --- | --- |
| `igw` | Internet Gateway |
| `rt` | Route Table |
| `sg` | Security Group |
| `tg` | Target Group |
| `app` | MiniPEP Application |

## 7. 리소스 이름 결정표

| Resource Type | Name |
| --- | --- |
| VPC | `aws-infra-sre-dev-vpc` |
| Public Subnet A | `aws-infra-sre-dev-public-subnet-a` |
| Public Subnet B | `aws-infra-sre-dev-public-subnet-b` |
| Internet Gateway | `aws-infra-sre-dev-igw` |
| Public Route Table | `aws-infra-sre-dev-public-rt` |
| ALB Security Group | `aws-infra-sre-dev-alb-sg` |
| EC2 Security Group | `aws-infra-sre-dev-ec2-sg` |
| EC2 | `aws-infra-sre-dev-app-ec2` |
| ALB | `aws-infra-sre-dev-alb` |
| Target Group | `aws-infra-sre-dev-app-tg` |

## 8. Tag 기준

모든 리소스에는 다음 Must Tag를 붙인다.

| Tag Key | 값 |
| --- | --- |
| `Name` | 리소스별 Name |
| `Project` | `aws-infra-sre` |
| `Environment` | `dev` |
| `Owner` | `compute-network` |
| `ManagedBy` | `console` |
| `Purpose` | 리소스 목적 |

Optional Tag는 필요할 때 사용한다.

| Tag Key | 예시 |
| --- | --- |
| `Component` | `network`, `compute`, `load-balancer` |
| `Lifecycle` | `dev`, `temporary`, `persistent` |

기존 Console 리소스의 Must Tag 적용 상태는 다음과 같다.

| Resource | Name | Project | Environment | Owner | ManagedBy | Purpose | 적용 상태 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VPC | `aws-infra-sre-dev-vpc` | `aws-infra-sre` | `dev` | `compute-network` | `console` | `project-network` | 완료 |
| Public Subnet A | `aws-infra-sre-dev-public-subnet-a` | `aws-infra-sre` | `dev` | `compute-network` | `console` | `public-workload` | 완료 |
| Internet Gateway | `aws-infra-sre-dev-igw` | `aws-infra-sre` | `dev` | `compute-network` | `console` | `internet-access` | 완료 |
| Public Route Table | `aws-infra-sre-dev-public-rt` | `aws-infra-sre` | `dev` | `compute-network` | `console` | `public-routing` | 완료 |

## 9. ManagedBy 변경 기준

`ManagedBy`는 실제 관리 주체를 기록한다.

- AWS Console에서 생성했고 아직 Terraform State에서 관리되지 않는 리소스는 `console`로 기록한다.
- Terraform 코드만 작성됐다는 이유로 `terraform`으로 바꾸지 않는다.
- 기존 리소스를 `terraform import`했거나 Terraform으로 재생성하여 실제 State에서 관리하기 시작한 뒤 `terraform`으로 변경한다.

## 10. Security Group 예정 원칙

ALB Security Group 예정 규칙:

| Direction | Rule |
| --- | --- |
| Inbound | TCP 80 from `0.0.0.0/0` |
| Outbound | EC2 Security Group 방향 통신 허용 예정 |

EC2 Security Group 예정 규칙:

| Direction | Rule |
| --- | --- |
| Inbound | TCP 80 from ALB Security Group |
| Outbound | Day 3 생성 시 검토 |

기본 원칙은 EC2 Host Port 80을 `0.0.0.0/0`에 직접 개방하지 않는 것이다. SSH 규칙은 아직 확정되지 않았으므로 임의로 추가하지 않는다.

## 11. Resource Handoff 사용 규칙

Console에서 생성하거나 확인한 리소스는 `docs/handoff/compute-network-resources.md`에 기록한다.

기록 원칙은 다음과 같다.

- 확인된 실제 값만 기록한다.
- 확인되지 않은 값은 `Verification Needed — AWS Console 확인 필요`로 남긴다.
- Day 3 이후 생성할 리소스 ID는 `TBD — Day 3 생성 후 기록`으로 남긴다.
- Access Key, Secret Access Key, Session Token, SSH Private Key 등 민감정보는 기록하지 않는다.
- Terraform 반영 여부와 `ManagedBy` 값을 함께 기록한다.

## 12. Terraform 담당자에게 전달할 Variable

Terraform 코드 작성 시 필요한 입력값은 다음과 같다.

- `aws_region`
- `project`
- `environment`
- `vpc_cidr`
- `public_subnet_a_cidr`
- `public_subnet_a_az`
- `public_subnet_b_cidr`
- `public_subnet_b_az`
- `alb_listener_port`
- `target_group_port`
- `ec2_host_port`
- `container_port`
- `health_check_path`
- `health_check_success_code`
- 각 리소스 이름
- `common_tags`

## 13. Terraform Output으로 필요한 값

Terraform 적용 또는 import 이후 다른 담당자에게 전달해야 하는 출력값은 다음과 같다.

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

## 14. 기존 Console 리소스와 Terraform 중복 생성 주의

현재 일부 리소스는 AWS Console에서 이미 생성되어 있다.

| Resource | 상태 | Terraform 반영 여부 |
| --- | --- | --- |
| VPC | 생성됨 | No |
| Public Subnet A | 생성됨 | No |
| Public Route Table `aws-infra-sre-dev-public-rt` / `rtb-0ffacb032b9943e43` | 생성됨 | No |
| Internet Gateway `aws-infra-sre-dev-igw` / `igw-06e83aa7e2a1cd757` | 연결 확인됨 | No |

Terraform 코드 실행으로 동일한 VPC, Subnet, Route Table 등을 중복 생성하면 안 된다.

기존 리소스에 대해 `terraform import`를 할지, 삭제 후 Terraform으로 재생성할지는 추후 확정한다. 아직 확정되지 않은 처리 방식을 결정된 것처럼 문서화하지 않는다.

## 15. 아직 생성하지 않은 리소스

Day 2 기준 아직 생성되지 않은 리소스는 다음과 같다.

- Public Subnet B
- ALB Security Group
- EC2 Security Group
- EC2
- ALB
- Target Group

## 16. Day 3 생성 예정 리소스

Day 3에는 다음 리소스를 생성하거나 확인할 예정이다.

| Resource | Day 3 작업 |
| --- | --- |
| Public Subnet B | 생성 후 ID 기록 |
| ALB Security Group | 생성 후 Inbound/Outbound 규칙 기록 |
| EC2 Security Group | 생성 후 Inbound/Outbound 규칙 기록 |
| EC2 | 생성 후 Instance ID, Public IP 기록 |
| ALB | 생성 후 ARN, DNS 기록 |
| Target Group | 생성 후 ARN, Health Check 상태 기록 |

## 17. 담당자별 전달 정보

| 담당 파트 | 전달 정보 |
| --- | --- |
| Compute + Network | 실제 리소스 이름, ID, 포트, Health Check Path, 검증 결과 |
| Terraform | 기존 Console 리소스 목록, import 또는 재생성 미확정 상태, Variable, Output |
| Observability | EC2 ID, ALB ARN/DNS, Target Group ARN, Health Check Path, 포트 흐름 |
| Security | ALB/EC2 Security Group 규칙, EC2 직접 개방 금지 원칙, SSH 미확정 상태 |

## 18. Day 2 완료 체크리스트

- [x] VPC CIDR `10.0.0.0/16` 확인
- [x] Public Subnet A CIDR `10.0.1.0/24` 확인
- [x] Public Subnet A AZ `ap-northeast-2a` 확인
- [x] Public Subnet A AZ ID `apne2-az1` 확인
- [x] Public Subnet A의 Public Route Table 연결 확인
- [x] Public Route Table의 `0.0.0.0/0 -> igw-06e83aa7e2a1cd757` 경로 확인
- [x] Naming Convention 정리
- [x] Must Tag와 Optional Tag 정리
- [x] 기존 Console 리소스 Must Tag 적용 완료 확인
- [x] ManagedBy 변경 기준 정리
- [x] Terraform Variable과 Output 정리
- [x] 기존 Console 리소스 중복 생성 주의사항 정리
- [ ] Public Subnet B 생성
- [ ] ALB Security Group 생성
- [ ] EC2 Security Group 생성
- [ ] EC2 생성
- [ ] ALB 생성
- [ ] Target Group 생성
