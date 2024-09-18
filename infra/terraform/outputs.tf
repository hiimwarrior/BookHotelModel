output "instance_id" {
  value = aws_instance.hotel_bookings_instance.id
}

output "s3_bucket_id" {
  value = aws_s3_bucket.hotel_bookings_bucket.id
}

output "db_instance_endpoint" {
  value = aws_db_instance.hotel_bookings_db.endpoint
}