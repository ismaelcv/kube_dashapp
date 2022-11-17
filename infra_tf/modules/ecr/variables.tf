variable "image_mutability" {
  description = "Provide image mutability"
  type        = string
  default     = "MUTABLE"
}


variable "encrypt_type" {
  description = "Provide type of encryption here"
  type        = string
  default     = "AES256"
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
