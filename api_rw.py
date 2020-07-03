import json
import yaml
import os
import sys



def write_yaml(file_name, data):
    """   """
    """   """
    with open(file_name + '.yaml', 'w') as file:
        documents = yaml.dump(data, file)
        print(documents)

def read_yaml(file_name):
    """   """
    """   """
    with open(file_name + '.yaml') as file:
        documents = yaml.full_load(file)
        print(documents)
