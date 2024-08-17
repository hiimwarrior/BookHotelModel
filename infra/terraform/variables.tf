# TODO: Populate after architecture discussion
variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "db_username" {
  description = "The username for the database"
  type        = string
}

variable "db_password" {
  description = "The password for the database"
  type        = string
}
