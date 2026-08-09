variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "aws-infra-sre"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_a_cidr" {
  description = "Public subnet A CIDR block"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_a_az" {
  description = "Public subnet A availability zone"
  type        = string
  default     = "ap-northeast-2a"
}

variable "public_subnet_b_cidr" {
  description = "Public subnet B CIDR block"
  type        = string
  default     = "10.0.2.0/24"
}

variable "public_subnet_b_az" {
  description = "Public subnet B availability zone"
  type        = string
  default     = "ap-northeast-2c"
}

variable "ec2_ami" {
  description = "Existing EC2 AMI ID"
  type        = string
  default     = "ami-08c64967154312fa5"
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ec2_key_name" {
  description = "Existing EC2 key pair name"
  type        = string
  default     = "aws-infra-sre-dev-ec2-key"
}

variable "admin_ssh_cidr" {
  description = "Administrator SSH CIDR"
  type        = string
}

variable "health_check_path" {
  description = "Target group health check path"
  type        = string
  default     = "/health"
}