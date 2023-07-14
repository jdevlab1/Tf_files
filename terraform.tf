variable "amiid" {
  default = "ami-06a0cd9728546d178"
}

variable "aws_accout_id" {
  default = 255213731871
}

variable "vpc_name" {
  type    = string
  default = "vpc2"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
variable "key_name" {
  default = "terraform.tfstate"
}
variable "region" {
    type = string
  default = "us-east-1"
}
variable "versioning" {
  type    = bool
  default = true
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}


variable "public_subnets" {
  type    = list(string)
  default = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}
variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "nat_gateway" {
  type    = bool
  default = false
}

variable "instance_tenancy" {
  type    = string
  default = "default"
}
