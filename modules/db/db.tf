module db {
  source  = "terraform-aws-modules/rds/aws"
  version = "1.22.0"
  identifier = "${var.identifier}"

  engine = "mysql"
  engine_version = "5.7.19"
  instance_class = "db.t2.large"
  allocated_storage = 5

  name = "${var.name}"
  username = "user"
  password = "YourPwdShouldBeLongAndSecure!"
  port = "3306"


  vpc_security_group_ids = "${var.vpc_sg_id}"

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window = "03:00-06:00"

  tags = {
    Owner = "user"
    Environment = "${var.env}"
  }

  # DB subnet group
  subnet_ids = "${var.vpc_subnets}"

  # DB parameter group
  family = "mysql5.7"

  # DB option group
  major_engine_version = "5.7"

  # Snapshot name upon DB deletion
  final_snapshot_identifier = "${var.name}"

  # Database Deletion Protection
  deletion_protection = true

  parameters = [
    {
      name = "character_set_client"
      value = "utf8"
    },
    {
      name = "character_set_server"
      value = "utf8"
    }
  ]
}