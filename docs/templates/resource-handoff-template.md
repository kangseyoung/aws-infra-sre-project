# Resource Handoff Template

> **민감정보 기록 금지**
>
> Access Key, Secret Access Key, Session Token, AWS 비밀번호, SSH Private Key, EC2 Private Key 파일 내용, GitHub Token, Database Password 등은 절대 기록하지 않는다.

이 템플릿은 AWS Console에서 생성하거나 확인한 리소스 정보를 Terraform, Observability, Security 담당자에게 전달하기 위해 사용한다.

## 1. 기본 정보

| 항목 | 값 |
| --- | --- |
| 작성자 |  |
| 작성 날짜 | YYYY-MM-DD |
| 담당 파트 |  |
| Region |  |
| Environment |  |

## 2. 리소스 정보

| 항목 | 값 |
| --- | --- |
| Resource Type |  |
| Resource Name |  |
| Resource ID |  |
| VPC ID |  |
| Subnet ID |  |
| Availability Zone |  |
| Availability Zone ID |  |
| CIDR |  |
| Public/Private 여부 |  |
| 연결된 리소스 |  |
| Route Table ID |  |
| Internet Gateway ID |  |
| Security Group ID |  |

## 3. Security Group 규칙

### Inbound 규칙

| Protocol | Port | Source | Description |
| --- | --- | --- | --- |
|  |  |  |  |

### Outbound 규칙

| Protocol | Port | Destination | Description |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. 애플리케이션 및 포트 정보

| 항목 | 값 |
| --- | --- |
| Listener Port |  |
| Target Port |  |
| Host Port |  |
| Container Port |  |
| Health Check Path |  |
| Health Check Success Code |  |
| ALB DNS |  |
| EC2 Public IP |  |

## 5. Terraform 연동 정보

| 항목 | 값 |
| --- | --- |
| Terraform 반영 여부 | Yes / No |
| ManagedBy | console / terraform |

### Terraform Variable로 전달할 값

```text

```

### Terraform Output으로 필요한 값

```text

```

## 6. 검증 정보

### 검증 방법

```text

```

### 검증 결과

```text

```

## 7. 특이사항

-
