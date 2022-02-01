from lark import Token

from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories
import pprint
import yaml
import os
import re
from pathlib import Path
import glob
pp = pprint.PrettyPrinter(indent=4)

class CheckGCPOrgPolicies(BaseResourceCheck):


    def __init__(self):
        name = "Ensure Org policies are not changed"
        id = "CKV_GCP_999"
        supported_resources = [resource_name for resource_name in os.environ['RESOURCES_TO_CHECK'].split(',')]
        test = [3]
        categories = [ CheckCategories.IAM ]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)


    @staticmethod
    def read_yml():
        yml_file_name=os.environ['YML_INPUT_ORG_POLICIES']
        yml_file = Path(yml_file_name)
        if not yml_file.is_file():
            print("ERROR_POLICY: File %s could not be found." % yml_file)
            return None

        with open(yml_file_name, 'r') as stream:
          yml_policies = yaml.safe_load(stream)

        return yml_policies

    def get_current_file_name(self):
        file_name = self.entity_path.split(':')[0]
        return re.sub(r"^\/*", "", file_name)

    @staticmethod
    def check_all_files_exist(yml_policies):
        existing_file_list_in_dir = glob.glob("*")
        file_list_policies = [policies['file_name'] for policies in yml_policies]
        for file_name in file_list_policies:
            if file_name not in existing_file_list_in_dir:
                print("ERROR_POLICY: File name %s could not be found !" % file_name)
                print("ERROR_POLICY: Existing file list in directory: %s" % ", ".join(existing_file_list_in_dir))
                print("ERROR_POLICY: Expected file list from yml file: %s" % ", ".join(file_list_policies))
                return False
            else:
                print("INFO_POLICY: OK file %s exists." % file_name)
        return True

    def get_policy_for_current_file(self, yml_policies):
        current_tf_file_name = self.get_current_file_name()
        for yml_node in yml_policies:
            if current_tf_file_name == yml_node['file_name']:
                return yml_node
        return None
    
    def append_output_yml(self, conf):
        yml_file_name=os.environ['YML_OUTPUT_ORG_POLICIES']
        yml_file = Path(yml_file_name)
        yml_content = None
        if not yml_file.is_file():    
            yml_content =  {'org_policies': []}
            print("DEBUG_POLICY: Creating new data structure to file %s." % yml_file_name)
        else:
            with open(yml_file_name, 'r') as stream:
                yml_content = yaml.safe_load(stream)
            print("DEBUG_POLICY: Read existing data from %s " % yml_file_name)

        file_policies = self.get_policy_for_current_file(yml_content['org_policies'])
        if file_policies is None:
            file_policies = {'file_name': self.get_current_file_name()}
            yml_content['org_policies'].append(file_policies)
            print("DEBUG_POLICY: File %s not found in data structure. Initializing data structure as follows: %s" % (self.get_current_file_name(), pp.pformat(file_policies)))
        

        node_name_exists = True
        index = 0
        base_node_name = "--".join(conf['constraint'])
        while node_name_exists:
            node_name_exists = False
            new_node_name = '%s_%d' % (base_node_name, index)
            for existing_node_name in file_policies.keys():
                if existing_node_name == new_node_name:
                    node_name_exists = True
                    index = index + 1
                    break
        print("DEBUG_POLICY: Using unique name %s for the new node." % new_node_name)

        file_policies[new_node_name] = conf

        #pp.pprint(yml_content)
        with open(yml_file_name, 'w') as stream:
            yaml.dump(yml_content, stream)
        
    def scan_resource_conf(self, conf):
        self.append_output_yml(conf)
        yml_policies = CheckGCPOrgPolicies.read_yml() 

        if yml_policies is None:
            return CheckResult.FAILED

        print("DEBUG_POLICY: Reference policy is %s." % pp.pformat(yml_policies))
        yml_policies = yml_policies['org_policies']
        if not CheckGCPOrgPolicies.check_all_files_exist(yml_policies):
            return CheckResult.FAILED

        current_policies = self.get_policy_for_current_file(yml_policies)

        for policy in current_policies.values():
            if policy == conf:
                print("INFO_POLICY: Policy %s found in file %s" % ("--".join(conf['constraint']), self.get_current_file_name()))
                return CheckResult.PASSED

        print("ERROR_POLICY: Policy could not be found in file %s!" % self.get_current_file_name())
        print("ERROR_POLICY: List of described policies: %s." % pp.pformat(current_policies))
        print("ERROR_POLICY: List of terraform policies: %s." % pp.pformat(conf))
        return CheckResult.FAILED

scanner = CheckGCPOrgPolicies()
