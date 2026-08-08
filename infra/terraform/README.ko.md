# Terraform 인프라

AWS 인프라 프로젝트를 위한 Terraform 설정 디렉터리입니다.

## 관리 전략

이 프로젝트는 **Terraform Import 기반 방식**으로 인프라를 관리합니다.

기존 AWS 리소스는 프로젝트 기간 동안 유지하며, Terraform으로 새로 생성하지 않고 **Terraform Import**를 통해 관리합니다.

### Must

1. 기존 AWS 리소스와 동일한 Terraform 코드를 작성합니다.
2. `terraform import`를 통해 Terraform State에 등록합니다.
3. `terraform plan`을 실행하여 최종적으로 **No changes**가 출력되는지 확인합니다.

### Optional

시간이 남는다면 별도 환경에서 `terraform apply`를 사용하여 동일한 인프라가 재현되는지 검증합니다.

## 초기 설정

```bash
terraform init
terraform fmt
terraform validate
```

## 관리 대상 리소스

- VPC
- Public Subnet
- Internet Gateway
- Route Table
- Security Group

## 주의사항

- `.terraform/`는 Git에 커밋하지 않습니다.
- `.terraform.lock.hcl`은 Git에 커밋합니다.
- `terraform.tfstate`는 Git에 커밋하지 않습니다.
- `terraform.tfvars`는 Git에 커밋하지 않습니다.
- AWS Access Key를 코드에 직접 작성하지 않습니다.
- 환경 변수 또는 AWS Profile 사용을 권장합니다.
