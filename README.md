# AWS Infra 2-Week Project

## Project Overview
This repository is a beginner-friendly GitHub scaffold for a 2-week AWS infrastructure project.
The project focuses on designing, building, documenting, and operating a production-like AWS environment rather than building backend or frontend application features.

The baseline user flow is:

`User -> Application Load Balancer -> EC2 -> Docker + Nginx -> CloudWatch`

## Background
This project is designed for a team of 4 to 5 beginners who want hands-on experience with AWS core infrastructure components.
Instead of starting with full Infrastructure as Code on day one, the team first builds key resources manually in AWS, records decisions and steps, and then converts selected parts into Terraform drafts.

## Architecture
Target architecture scope:

- VPC with public and private subnet design
- Route tables and Internet Gateway
- NAT Gateway as an optional cost-sensitive choice
- EC2 instance for web serving
- Docker container runtime on EC2
- Nginx static web server
- Application Load Balancer and Target Group
- Security Groups and IAM Role
- CloudWatch Logs, Metrics, and Alarms

Detailed draft:
- [docs/architecture.md](/D:/2026/sre/aws-infra-2week-project/docs/architecture.md)
- [docs/architecture.ko.md](/D:/2026/sre/aws-infra-2week-project/docs/architecture.ko.md)

## Tech Stack
- AWS VPC
- Public Subnet / Private Subnet
- Route Table
- Internet Gateway
- NAT Gateway (optional)
- EC2
- Docker
- Nginx
- Application Load Balancer
- Target Group
- Security Group
- IAM / IAM Role
- CloudWatch Logs
- CloudWatch Metrics
- CloudWatch Alarm
- Terraform (optional / partial)

## Team Roles
| Member | Primary Role | Scope |
| --- | --- | --- |
| 강세영 | Compute + Network | EC2, ALB, VPC, subnet, route table, traffic flow, network structure documentation |
| 권태욱 | Observability / Platform / IaC Support / Compute Support | CloudWatch, monitoring notes, platform operation notes, IaC support, compute support |
| 김태우 | Terraform / IaC | Terraform structure, provider, variables, outputs, selected resource codification |
| 박찬혁 | Security + SRE Support | Security Group, IAM, secret handling, incident checklist, SRE support |

Role details were updated from the 2026-06-28 kickoff meeting.

## Project Goals
- Understand how AWS networking and compute components connect together
- Build a simple but realistic traffic path from user request to web server
- Practice documenting manual infrastructure setup decisions
- Learn basic observability, alerting, and incident response workflows
- Prepare a small Terraform baseline after manual validation
- Finish with a repository that can be presented as an infrastructure portfolio artifact

## Repository Structure
```text
aws-infra-2week-project/
├── README.md
├── README.ko.md
├── docs/
├── diagrams/
├── infra/
│   ├── terraform/
│   └── manual-setup/
├── app/
├── runbook/
├── scripts/
└── .gitignore
```

## 2-Week Roadmap
### Week 1
- Day 1: Kickoff, role assignment, architecture discussion
- Day 2: VPC, subnet, route table, Internet Gateway setup
- Day 3: Security group and IAM role setup
- Day 4: EC2 provisioning, Docker installation, Nginx container run
- Day 5: ALB and Target Group integration, first end-to-end test

### Week 2
- Day 6: CloudWatch logs, metrics, alarm setup
- Day 7: Failure scenario testing and runbook drafting
- Day 8: Cost review, cleanup planning, documentation refinement
- Day 9: Terraform draft for selected resources
- Day 10: Final review, retrospective, presentation material cleanup

## Manual Setup Guide
Manual setup templates are under [infra/manual-setup](/D:/2026/sre/aws-infra-2week-project/infra/manual-setup).

Recommended order:
1. VPC and subnet setup
2. Security setup
3. EC2 setup
4. ALB setup
5. CloudWatch setup

Each document is meant to capture:
- What was created
- Why the setting was chosen
- Screenshot or console evidence
- Problems encountered
- Follow-up IaC candidates

## Terraform Plan
Terraform is intentionally partial in this project.
The team should not attempt to fully automate everything before understanding the AWS console flow.

Recommended Terraform approach:
- Start with provider, variables, and tagging standards
- Codify VPC, subnet, and security group basics first
- Add EC2 and ALB resources later if the manual setup is stable
- Keep state files local or in a secure remote backend later

Terraform draft files:
- [infra/terraform/provider.tf](/D:/2026/sre/aws-infra-2week-project/infra/terraform/provider.tf)
- [infra/terraform/main.tf](/D:/2026/sre/aws-infra-2week-project/infra/terraform/main.tf)
- [infra/terraform/variables.tf](/D:/2026/sre/aws-infra-2week-project/infra/terraform/variables.tf)
- [infra/terraform/outputs.tf](/D:/2026/sre/aws-infra-2week-project/infra/terraform/outputs.tf)

## Observability / SRE
Minimum observability targets:
- ALB health status
- EC2 instance health
- Nginx container status
- CPU usage
- Basic request and error visibility
- Alarm routing and ownership

Suggested outputs:
- CloudWatch dashboard screenshots
- Alarm threshold notes
- Incident timeline examples
- Simple service health checklist

## Incident Runbook
Runbooks are stored in [runbook](/D:/2026/sre/aws-infra-2week-project/runbook).

Suggested incident scenarios:
- ALB health check failure
- EC2 SSH access failure
- Nginx container down
- Unexpected cost increase

## Cost Management
Because this is a learning project, cost control is part of the deliverable.

Cost controls:
- Prefer minimum-sized EC2 resources where possible
- Use NAT Gateway only if truly needed
- Delete unused Elastic IP, ALB, EBS, and test resources
- Track daily resource inventory during the project
- Perform final cleanup using the checklist in `runbook/cost-cleanup.md`

## Security Notes
- Never commit AWS Access Key, Secret Access Key, `.pem`, `.env`, `terraform.tfstate`, `terraform.tfvars`, or any secret file.
- Do not hardcode credentials in shell scripts, Terraform, or application files.
- Prefer IAM Role attachment over long-term access keys for EC2 access.
- Restrict inbound ports to the minimum required range.
- Review security group rules before demo day and before cleanup.

## Retrospective
At the end of the project, record:
- What the team understood well
- Where setup steps were confusing
- Which resources caused the most operational difficulty
- What should be automated next
- Which documentation helped the most

## Important Secret Handling
This repository must never include:

- AWS Access Key
- AWS Secret Access Key
- `.pem` private keys
- `.env` files
- `terraform.tfstate`
- `terraform.tfvars`

Review `.gitignore` before the first commit and before pushing to GitHub.
