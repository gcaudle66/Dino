import csv
import json
import yaml
from api_yaml import *
from jinja2 import Environment, FileSystemLoader
ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template("ap_name.j2")

import_ap = {}
ap_dict = {
    "cur_name": "FUBAR.AP.NewName",
    "new_name": "AP7069.5AEB.E424"
}

with open('pi_name1.csv', 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:

    print(import_ap)









