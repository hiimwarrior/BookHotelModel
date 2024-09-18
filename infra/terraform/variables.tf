variable "region" {
  description = "AWS region"
  default     = "us-west-2"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "db_instance_class" {
  description = "RDS instance class"
  default     = "db.t3.medium"
}

variable "db_name" {
  description = "RDS database name"
  default     = "hotelbookingsdb"
}
