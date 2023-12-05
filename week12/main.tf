terraform {
  cloud {
    organization = "fall2022-adv-scripting"
    workspaces {
      name = "mestin-lab12-startEC2"
    }
  }
}

terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 3.27"
      }
    }
  
    required_version = ">= 0.14.9"
  }
  
  provider "aws" {
    profile = "default"
    region  = "us-east-1"
  }

  data "aws_iam_role" "lab_role" {
    name = "LabRole"
  }

  resource "aws_lambda_function" "start_EC2"{
    filename = "startEC2.zip"
    function_name = "mesfin_function2"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "startEC2.lambda_handler"
}