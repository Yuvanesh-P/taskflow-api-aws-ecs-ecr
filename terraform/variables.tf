variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "taskflow-api"
}

variable "container_port" {
  description = "FastAPI container port"
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "Fargate CPU units"
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Fargate memory in MiB"
  type        = number
  default     = 512
}

variable "github_owner" {
  description = "GitHub username or organization"
  type        = string
  default     = "Yuvanesh-P"
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "taskflow-api-aws-ecs-ecr"
}

variable "github_branch" {
  description = "GitHub deployment branch"
  type        = string
  default     = "main"
}