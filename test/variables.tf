variable "countries" {
  type        = map(string)
  description = "Country -> region map"
}

output "org_id" {
  value = var.org_id
  type  = number
}

variable "org_policies" {
  type        = any
  default     = []
  description = "Org policies for organization"
  # Validation will be performed in the org-policy module.
}