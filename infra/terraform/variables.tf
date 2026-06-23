variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "aws-infra-2week"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_az" {
  description = "Availability Zone for the public subnet"
  type        = string
  default     = "ap-northeast-2a"
}

variable "ssh_allowed_cidrs" {
  description = "CIDR ranges allowed to SSH into EC2"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

