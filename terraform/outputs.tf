output "alb_dns_name" {
  description = "AWS-generated ALB DNS URL (HTTP)"
  value       = "http://${aws_lb.app.dns_name}"
}

output "alb_dns_hostname" {
  description = "ALB DNS hostname"
  value       = aws_lb.app.dns_name
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.app.name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.app.name
}

output "github_actions_role_arn" {
  description = "GitHub Actions IAM role ARN"
  value       = aws_iam_role.github_actions.arn
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}