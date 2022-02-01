#!/bin/bash
#/opt/homebrew/bin/checkov

custom_policy_name=checkcov-orgpolicies
terraform_package=test
export YML_INPUT_ORG_POLICIES=org_policies_reference.yaml
export YML_OUTPUT_ORG_POLICIES=generated_org_policies_reference.yaml
export LOG_LEVEL=WARNING
# Following must be a CSV list
export RESOURCES_TO_CHECK='google_organization_policy,google_folder_organization_policy'
force_update_org_policies=0
usage() { echo "Usage: $0 [-c <custom_policy_name:default = $custom_policy_name>] [-f to initialize yaml: will always return an error]  [-d for debug] [-i <input_yml_file:default = $YML_INPUT_ORG_POLICIES>] [-o <output_yml_file:default = $YML_OUTPUT_ORG_POLICIES>] [-r <list of resources to be checked: default = $RESOURCES_TO_CHECK>] [-t <terraform directory: default = $terraform_package>]" 1>&2; exit 1; }

while getopts fhdc:t:i:o: flag
do
    case "${flag}" in
        d) export LOG_LEVEL=DEBUG;;
        c) custom_policy_name=${OPTARG};;
        t) terraform_package=${OPTARG};;
        i) export YML_INPUT_ORG_POLICIES=${OPTARG};;
        o) export YML_OUTPUT_ORG_POLICIES=${OPTARG};;
        r) export RESOURCES_TO_CHECK=${OPTARG};;
        f) force_update_org_policies=1;;
        h) usage;;
        *) usage;;
    esac
done
pushd $terraform_package
rm -f $YML_OUTPUT_ORG_POLICIES
checkov -d . --external-checks-dir $custom_policy_name
popd
if (( $force_update_org_policies > 0 )); then
  cp $terraform_package/$YML_OUTPUT_ORG_POLICIES $terraform_package/$YML_INPUT_ORG_POLICIES
  echo "WARNING: Copied $terraform_package/$YML_OUTPUT_ORG_POLICIES to $terraform_package/$YML_INPUT_ORG_POLICIES"
  echo "WARNING: Do not use the option -f in a CI/CD pipeline: it does not verify anything"
  echo "WARNING: This script is failing on purpose"
  exit 1
fi
python3 diffyml.py $terraform_package/$YML_INPUT_ORG_POLICIES $terraform_package/$YML_OUTPUT_ORG_POLICIES 