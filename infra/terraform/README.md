# Terraform Infrastructure

Terraform configuration for the AWS infrastructure project.

## Management Strategy

The project uses an **Import-first** approach.

Existing AWS resources are kept throughout the project and managed with Terraform by importing them into the Terraform state.

### Must

1. Write Terraform configuration that matches the existing AWS resources.
2. Import the existing resources into the Terraform state.
3. Run `terraform plan` and verify that the result is **No changes**.

### Optional

If time permits, reproduce the same infrastructure in a separate environment using `terraform apply` to verify reproducibility.

## Initial Setup

```bash
terraform init
terraform fmt
terraform validate
```

## Managed Resources

- VPC
- Public Subnet
- Internet Gateway
- Route Table
- Security Group

## Safety Notes

- Do not commit `.terraform/`
- Commit `.terraform.lock.hcl`
- Do not commit `terraform.tfstate`
- Do not commit `terraform.tfvars`
- Do not hardcode AWS credentials
- Prefer environment variables or an AWS profile