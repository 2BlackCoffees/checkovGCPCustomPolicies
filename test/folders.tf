resource "google_folder" "countries" {
  for_each     = var.countries
  display_name = each.key
  parent       = "organizations/${var.org_id}"
}

resource "google_organization_policy" "services_policy" {
  org_id     = "123456789"
  constraint = "serviceuser.services"

  list_policy {
    suggested_value = "compute.googleapis.com"

    deny {
      values = ["cloudresourcemanager.googleapis.com"]
    }
  }
}

resource "google_folder_organization_policy" "serial_port_policy" {
  folder     = "folders/123456789"
  constraint = "compute.disableSerialPortAccess"

  boolean_policy {
    enforced = true
  }
}

