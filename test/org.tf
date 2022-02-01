

resource "google_organization_policy" "disableSerialPortAccess" {
  org_id     = var.org_id
  constraint = "compute.disableSerialPortAccess"

  boolean_policy {
    enforced = true
  }
}

resource "google_organization_policy" "trustedImageProjects" {
  org_id     = var.org_id
  constraint = "compute.trustedImageProjects"

  boolean_policy {
    enforced = true
  }
}