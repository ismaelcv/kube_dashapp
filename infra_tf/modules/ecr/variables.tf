variable "ecr_name" {
  description = "The name of the ECR registry"
  type        = any
  default     = ["my_pretty_tf_repo","my_second_pretty_tf_repo"]
}

variable "image_mutability" {
  description = "Provide image mutability"
  type        = string
  default     = "IMMUTABLE"
}


variable "encrypt_type" {
  description = "Provide type of encryption here"
  type        = string
  default     = "KMS"
}

variable "tags" {
  description = "The key-value maps for tagging"
  type        = map(string)
  default     = {}
}


variable "application_name" { 
    type = string 
    default = "dashapptf"
    }

