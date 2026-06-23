# Architecture Draft

## Overview
This project aims to build a simple but production-like AWS infrastructure path for a static web service.
The main flow is:

`Internet User -> ALB -> Target Group -> EC2 -> Docker -> Nginx -> Static Page`

CloudWatch is used to observe logs, metrics, and alarms related to the infrastructure.

## Core Components
### Network
- One VPC as the main network boundary
- Public subnets for internet-facing components such as ALB
- Private subnet optional depending on team scope and time
- Route tables to control internet and internal traffic paths
- Internet Gateway for public internet access
- NAT Gateway optional for private outbound internet access

### Compute
- EC2 as the main compute node
- Docker installed on EC2
- Nginx running as a container
- Static HTML page served through Nginx

### Traffic
- Application Load Balancer as the public entrypoint
- Target Group linked to EC2 instance
- Health checks configured to validate service availability

### Security
- Security Groups separating ALB access and EC2 access
- IAM Role attached to EC2 where needed
- Limited open ports based on actual traffic requirements

### Observability
- CloudWatch metrics for EC2 and ALB
- CloudWatch logs for selected server or application logs
- CloudWatch alarms for basic failure conditions

## Suggested Logical Flow
1. User sends HTTP request to ALB DNS name
2. ALB receives traffic on port 80
3. ALB forwards request to Target Group
4. Target Group routes traffic to EC2 instance
5. EC2 host runs Docker container with Nginx
6. Nginx serves the static test page
7. CloudWatch collects metrics and alarms on unhealthy conditions

## Design Considerations
- Keep the first version simple enough to build manually
- Use NAT Gateway only if the team truly needs a private subnet with outbound access
- Prefer clear documentation over over-engineered architecture
- Treat observability and cleanup planning as part of the architecture

## Optional Extensions
- Private application subnet
- Bastion or SSM-based administration
- HTTPS listener with ACM
- Auto Scaling Group
- Terraform expansion
- Dashboard screenshots in `diagrams/`

