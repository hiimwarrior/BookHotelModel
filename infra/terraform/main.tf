provider "aws" {
  region = var.region
}

# Instancia EC2
resource "aws_instance" "hotel_bookings_instance" {
  ami           = "ami-0a59b2f6d0d4d4f6d"  # Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
  instance_type = "t3.medium"

  tags = {
    Name = "hotel_bookings_instance"
  }
}

# Bucket S3
resource "aws_s3_bucket" "hotel_bookings_bucket" {
  bucket = var.bucket_name
  acl    = "private"
}

# Base de datos RDS
resource "aws_db_instance" "hotel_bookings_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = var.db_instance_class
  db_name              = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  tags = {
    Name = "hotel_bookings_db"
  }
}
