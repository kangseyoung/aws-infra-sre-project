# Terraform Draft

This folder contains a starter Terraform draft for the AWS infrastructure project.

## Intent
- Learn AWS resources manually first
- Convert selected resources into Terraform after understanding them
- Keep the first version small and readable

## Suggested First Targets
- VPC
- Public subnet
- Internet Gateway
- Route table
- Security group

## Safety Notes
- Do not commit `terraform.tfstate`
- Do not commit `terraform.tfvars`
- Do not hardcode AWS credentials
- Prefer environment variables or a secure AWS profile

