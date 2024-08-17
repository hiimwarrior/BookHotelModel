# TODO: Populate after architecture discussion
output "instance_id" {
  description = "The ID of the example EC2 instance"
  value       = aws_instance.example.id
}

output "instance_public_ip" {
  description = "The public IP address of the example EC2 instance"
  value       = aws_instance.example.public_ip
}

output "instance_private_ip" {
  description = "The private IP address of the example EC2 instance"
  value       = aws_instance.example.private_ip
}
