import csv
from jinja2 import Environment, FileSystemLoader
ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template("ap_name.j2")

ap_import = {}

ap_rename_dict = {
	"cur_name": "FUBAR.AP.NewName",
	"new_name": "AP7069.5AEB.E424"
}

with open('name.csv', 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
