# Terraform / IaC

기존 AWS 콘솔 인프라를 Terraform 코드로 관리하기 위한 디렉터리입니다.

## 관리 범위

- VPC
- Public Subnet A/B
- Internet Gateway
- Public Route Table 및 Subnet 연결
- ALB/EC2 Security Group
- EC2
- Application Load Balancer
- Target Group
- HTTP Listener
- Target Group Attachment

## 사전 준비

각 작업자는 프로젝트 AWS 계정에 접근 가능한 개인 AWS CLI 프로필을 준비해야 합니다.

Access Key, Secret Key, SSO 정보, `.pem` 파일은 저장소나 채팅에 공유하지 않습니다.

Git Bash 예시:

```bash
export AWS_PROFILE=<project-aws-profile>
aws sts get-caller-identity --region ap-northeast-2
```

PowerShell 예시:

```powershell
$env:AWS_PROFILE = "<project-aws-profile>"
aws sts get-caller-identity --region ap-northeast-2
```

관리자 SSH CIDR은 Git에 올리지 않고 로컬 `terraform.tfvars`에 설정합니다.

```hcl
admin_ssh_cidr = "x.x.x.x/32"
```

## 실행 방법

Terraform 디렉터리에서 다음 순서로 실행합니다.

### 1. 초기화

```bash
terraform init
```

AWS Provider를 내려받고 Terraform 작업 환경을 초기화합니다. 처음 실행하거나 Provider 설정이 바뀐 경우 실행합니다.

### 2. 코드 형식 정리

```bash
terraform fmt
```

Terraform 파일의 들여쓰기와 형식을 표준 형태로 정리합니다. AWS 리소스는 변경하지 않습니다.

### 3. 문법 및 참조 검사

```bash
terraform validate
```

Terraform 코드의 문법과 리소스 참조가 올바른지 검사합니다. AWS 리소스는 변경하지 않습니다.

### 4. 기존 리소스 import

기존 콘솔 리소스는 새로 생성하지 않고 import 방식으로 Terraform state에 연결합니다.

```bash
terraform import <terraform_resource_address> <aws_resource_id>
```

예시:

```bash
terraform import aws_vpc.main vpc-xxxxxxxxxxxxxxxxx
```

### 5. 실행 계획 확인

```bash
terraform plan
```

코드와 실제 AWS 설정의 차이를 확인합니다. `plan`은 AWS 리소스를 변경하지 않습니다.

## Output

```bash
terraform output
```

다음 값을 제공합니다.

- EC2 Instance ID
- ALB DNS Name
- Target Group ARN
- ALB Security Group ID
- EC2 Security Group ID

## State 및 민감정보 관리

다음 파일과 정보는 커밋하지 않습니다.

- `terraform.tfstate`
- `terraform.tfstate.backup`
- `.terraform/`
- `terraform.tfvars`
- AWS Access Key / Secret Key
- `.pem`, `.env`

현재는 Local State를 사용합니다. Remote Backend는 Optional 범위입니다.

## 제약 사항

`aws_lb_target_group_attachment`는 AWS Provider에서 import를 지원하지 않습니다.
기존 Target 등록은 AWS CLI 또는 콘솔에서 별도로 검증하고, Terraform state 반영을 위한 apply 여부는 팀 합의 후 결정합니다.

## Optional

별도 환경에서 `terraform apply`로 인프라를 재현하고, ALB `/health` HTTP 200 확인 후 `terraform destroy`로 정리하는 작업은 Optional 범위입니다.
