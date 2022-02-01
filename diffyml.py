# pip install -r requirements.txt
from deepdiff import DeepDiff
import yaml
import os
import sys
from pathlib import Path

def read_yml_file(yml_file_name):

    yml_file = Path(yml_file_name)
    if not yml_file.is_file():
        print("ERROR: File %s could not be found." % yml_file)
        return None
    with open(yml_file_name, 'r') as stream:
      yml_policies = yaml.safe_load(stream)

    return yml_policies    

def print_usage():
      print ('Usage: %s yml_file_1 yml_file_2' % sys.argv[0])

def get_parameters():
    if len(sys.argv) != 3:
        print_usage()
        exit(1)
    return sys.argv[1:]

if __name__ == '__main__':
    filename_in_yml_policies, filename_out_yml_policies = get_parameters()
    in_yml_policies = read_yml_file(filename_in_yml_policies)
    out_yml_policies = read_yml_file(filename_out_yml_policies)

    ddiff = DeepDiff(in_yml_policies, out_yml_policies, ignore_order=True)
    if len(ddiff) > 0:
        print('ERROR: Policies differ: %s' % ddiff, file=sys.stderr)
        exit(1)
    print('OK Described policy and Terraform ones are the same.')
    exit(0)