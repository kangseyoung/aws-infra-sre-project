# Terraform / IaC Must / Optional 정리

담당자: 김태우  
파트: Terraform / IaC

> 이 문서는 담당자가 직접 Must / Optional 범위를 정리하기 위한 템플릿입니다.  
> 아래 내용은 확정된 범위가 아니며, 회의와 학습 내용을 바탕으로 직접 채웁니다.

## 1. 이 파트의 역할

Terraform / IaC 파트는 프로젝트에서 사용하는 AWS 리소스를 코드로 정의하고 관리하는 역할을 담당한다.

이번 프로젝트에서는 Compute + Network, Observability / Platform, Security + SRE 파트에서 생성한 AWS 리소스와 설정을 전달받아 Terraform으로 코드화하고 관리하는 것을 목표로 한다.

또한 Variable, Output, 디렉터리 구조 등을 정리하여 팀원들이 동일한 Terraform 코드를 기반으로 협업할 수 있는 환경을 제공한다.

## 2. 초보자가 꼭 알아야 할 핵심 개념

### Terraform 핵심 개념

- Infrastructure as Code(IaC)
- Provider
- Resource
- Variable
- Output
- State(terraform.tfstate)
- Terraform 파일 구조(main.tf, variables.tf, outputs.tf 등)
- terraform init
- terraform plan
- terraform apply
- terraform fmt
- terraform validate
- terraform import

### IaC를 사용하는 이유

- 인프라를 코드로 관리할 수 있다.
- 동일한 환경을 반복해서 생성할 수 있다.
- 수작업으로 인한 설정 누락과 실수를 줄일 수 있다.
- 변경 사항을 Git으로 관리할 수 있다.
- 협업 시 동일한 인프라 구성을 쉽게 공유할 수 있다.

## 3. Must 범위

### Terraform 기본 사용법 이해

- Terraform 설치
- Provider
- Resource
- Variable
- Output
- State 기본 개념 이해
- Terraform 기본 명령
  - terraform fmt
  - terraform validate
  - terraform init
  - terraform plan
  - 선택한 방식에 따른 terraform apply 또는 terraform import
    - Day 2에 import/재생성 방식을 정하고 결과를 검증

### Compute + Network 파트 IaC화

Compute + Network 파트에서 생성한 AWS 네트워크 및 컴퓨트 리소스를 Terraform 코드로 재현하거나, 필요 시 terraform import를 고려한다.

예시

- VPC
- Public Subnet
- Internet Gateway
- Route Table
- Security Group
- EC2
- ALB
- Target Group
- ALB Listener
- Target Group Attachment

### Observability / Platform 파트 연계

Observability / Platform 파트에서 필요한 정보를 Output으로 제공하는 것을 Must로 한다.

예시

- EC2 Instance ID
- ALB DNS
- Target Group ARN
- ALB SG ID
- EC2 SG ID

### Security + SRE 파트 연계

Security + SRE 파트에서 사용하는 보안 관련 리소스를 Terraform 코드로 재현하거나, 필요 시 terraform import를 고려한다.

예시

- Security Group
- IAM Role(필요 시)

### 프로젝트 구조 정리

- Terraform 디렉터리 구조
- Variable 관리
- Output 관리
- Terraform 실행 방법(README)
- `.gitignore` 구성
  - terraform.tfstate
  - terraform.tfstate.\*
  - .terraform/
  - \*.tfvars
  - .env
  - AWS Access Key / Secret Key
  - Private Key

## 4. Optional 범위

- Terraform Module 적용
- Remote Backend(S3) 구성
- CloudWatch Dashboard / Alarm 코드화
- SNS 코드화
- Auto Scaling Group 코드화
- Private Subnet / NAT Gateway 코드화
- GitHub Actions를 이용한 `terraform fmt`, `terraform validate` 자동화
- WAF, IAM 정책 등 추가 보안 리소스 코드화

## 5. Must로 정한 이유

이번 프로젝트에서는 Compute + Network, Observability / Platform, Security + SRE 파트에서 생성한 핵심 AWS 리소스와 설정을 Terraform으로 코드화하여 프로젝트 전체가 일관된 환경에서 동작할 수 있도록 하는 것이 중요하다고 판단하였다.

또한 각 파트의 변경 사항을 Terraform 코드에 지속적으로 반영하고, Variable, Output, 프로젝트 구조를 정리하여 팀원들이 동일한 코드를 기반으로 협업할 수 있는 환경을 만드는 것도 Must 범위에 포함하였다.

Terraform 코드뿐만 아니라 디렉터리 구조, 실행 방법, 적용한 AWS 리소스 등을 함께 문서화하여 프로젝트 종료 이후에도 인프라 구성을 쉽게 이해하고 재현할 수 있도록 하는 것도 Must 범위에 포함하였다.

## 6. Optional로 뺀 이유

Module, Remote Backend, Auto Scaling, CloudWatch Dashboard/Alarm, SNS, GitHub Actions 자동화 등의 기능은 실제 운영 환경에서는 중요하지만, 2주 프로젝트 안에 모두 적용하기에는 범위가 넓다.

우선 팀에서 사용하는 핵심 AWS 리소스를 Terraform으로 관리하는 것을 목표로 하고, 시간이 남을 경우 코드 구조 개선과 자동화 요소를 추가하는 것이 적절하다고 판단하였다.

## 7. 다른 파트와 연결되는 부분

### 협업 방식

Terraform은 다른 파트에서 생성한 AWS 리소스와 설정을 코드로 관리하는 역할이므로, 각 파트의 변경 사항을 Terraform 코드에 지속적으로 반영한다.

각 파트는 Resource Handoff 문서를 작성하고, Terraform 담당자는 이를 기반으로 리소스 이름, 목적, 연결 대상, CIDR, Security Group 규칙, 필요한 Output 등의 정보를 취합하여 Terraform 코드를 작성하는 방식으로 진행한다. 변경 사항은 Variable과 Output을 통해 일관성 있게 관리한다.

### Compute + Network

- Compute + Network에서 생성한 AWS 네트워크 및 컴퓨트 리소스를 Terraform 코드로 재현하거나 필요 시 terraform import를 고려한다.
- VPC, Public Subnet, Route Table, Internet Gateway, Security Group, EC2, ALB, Target Group, ALB Listener, Target Group Attachment 등을 관리한다.
- 리소스 이름, CIDR, Security Group 규칙 등을 협의하고 Variable을 활용하여 변경 사항을 쉽고 동일하게 반영할 수 있도록 구성한다.

### Observability / Platform

- EC2 Instance ID, ALB DNS, Target Group ARN, ALB SG ID, EC2 SG ID 등 운영에 필요한 정보를 Output으로 제공한다.
- 시간이 남으면 CloudWatch Dashboard, Alarm, SNS 등의 리소스도 Terraform 코드로 재현하거나 필요 시 import를 고려한다.

### Security + SRE

- Security Group, IAM 등 보안 관련 리소스를 Terraform 코드로 재현하거나 필요 시 terraform import를 고려한다.
- 보안 정책 변경 사항을 Terraform 코드에 반영한다.
- 시간이 남으면 WAF, CloudWatch Alarm 등 운영 및 보안 관련 리소스도 함께 코드화한다.

## 8. GitHub에 남기면 좋은 산출물

### 코드

- Terraform 코드(`infra/`)
- Variable / Output 구성
- `.gitignore` (State 및 민감정보 제외 설정 포함)

### 문서

- Terraform 디렉터리 구조 설명
- Terraform 실행 방법
- Terraform으로 관리하는 AWS 리소스 정리
- Variable / Output 사용 방법
- 파트별 리소스 취합 및 반영 기록

### 포트폴리오

- Terraform으로 생성한 인프라 구조
- Terraform 실행 결과(`terraform plan`, `terraform apply`)
- 프로젝트 아키텍처 다이어그램
- Terraform을 활용한 IaC 구성 설명

## 9. 2~3분 공유 요약

Terraform / IaC 파트는 팀에서 설계한 AWS 인프라를 코드로 관리하는 역할입니다.

이번 프로젝트에서는 Compute + Network, Observability / Platform, Security + SRE 파트에서 생성한 핵심 AWS 리소스와 설정을 Terraform으로 코드화하는 것을 Must 범위로 잡았습니다.

또한 Variable과 Output을 정리하여 팀원들이 동일한 인프라 구성을 함께 관리할 수 있도록 하고, 다른 파트에서 필요한 AWS 리소스 정보를 쉽게 활용할 수 있도록 연결하는 것도 목표입니다.

Terraform은 특정 파트만 담당하는 것이 아니라, 각 파트에서 생성한 AWS 리소스와 설정을 취합하여 일관된 IaC 코드로 관리하는 역할이라고 생각합니다. 따라서 리소스 이름, 네트워크 구성, 보안 정책, 모니터링 대상 등이 변경되면 이를 Terraform 코드에도 함께 반영하며 전체 인프라 구성이 동일하게 유지될 수 있도록 관리하려고 합니다.

또한 Terraform 코드뿐만 아니라 디렉터리 구조, 실행 방법, 적용한 AWS 리소스, Variable 및 Output 구성 등을 문서화하여 팀원들이 쉽게 이해하고 사용할 수 있도록 GitHub에 함께 정리할 계획입니다.

Module, Remote Backend, GitHub Actions 같은 고도화 기능은 시간이 남을 경우 Optional로 진행하려고 합니다.

최종적으로는 Terraform 코드와 문서를 함께 남겨 팀 프로젝트에서 IaC를 활용한 협업 경험과 인프라를 코드로 관리하는 과정을 포트폴리오에서 설명할 수 있도록 하는 것이 목표입니다.
