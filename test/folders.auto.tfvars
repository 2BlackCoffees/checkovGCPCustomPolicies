org_id = 1234567890

countries = {
  Georgia = "EU"
  France  = "EU"
  USA     = "NA"
}


org_policies = [
  {
    name    = "compute.skipDefaultNetworkCreation"
    enforce = true
  },
  {
    name     = "compute.trustedImageProjects"
    deny_all = true
  },
  {
    name     = "compute.vmExternalIpAccess"
    deny_all = true
  }
]