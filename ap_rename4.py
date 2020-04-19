import pandas as pd
import numpy as np
import csv
import netmiko as nm
import textfsm
import argparse

##parser = argparse.ArgumentParser(description="Script to change Names of APs on a C9800WLC. Script will " \
##                                 " import CSV file from .current_dir with names and MACs of" \
##                                 " APs and will pull list of current APs on WLC, do a DIFF and compare " \
##                                 " to validate these MACs are present on WLC and if so change the names " \
##                                 " per CSV. Will raise Error if any fault should occur.                 ")

def draw_df(*args):
    data = np.array([['','AP Name','MAC','State'],
                ['Row1',1,2,3],
                ['Row2',4,5,6]])
    print(pd.DataFrame(data=data[1:,1:],
                        index=data[1:,0],
                        columns=data[0,1:]))

## Temp Data to avoid the reconnects
cli_parsed = ([{'ap_name': ': Floor2.AP.C9C0', 'mac_address': ': 683b.7850.d8e0'},
            {'ap_name': ': AP7069.5AEB.E424', 'mac_address': ': 28ac.9ed8.d020'}])

connArgs = {
    "ip": "198.18.134.100",
    "user": "admin",
    "pass": "C1sco12345"}


def connect(connArgs):
    expPrompt = "C9800-WLC#"
    connex = False
    conn = nm.BaseConnection(ip=connArgs["ip"], username=connArgs["user"], password=connArgs["pass"])
    getPrompt = conn.find_prompt()
    print(getPrompt)
    no_paging = conn.disable_paging()
    print("Terminal Width set to :" + no_paging)
    return conn

def getApCli(conn):
    cli_out = conn.send_command("show ap config general | include Cisco AP Name|Identifier", use_textfsm=True, textfsm_template="./templates/cisco_ios_show_ap_template.textfsm")
    return cli_out, conn

def parseCSV():
    with open('./templates/cisco_ap_from_csv_template.textfsm') as template:
        results_template = textfsm.TextFSM(template)
        content2parse = open("pi_name1.csv")
        content = content2parse.read()
        parsedCSV_results = results_template.ParseText(content)
    return parsedCSV_results

def iterateParsedCSV(parsedCSV_results):
    print(len(parsedCSV_results))
    iteratedCSV = []
    index = 0
    for item in parsedCSV_results:
        iteratedCSV.append("Element # {}: {}".format(index,item))
        index = index + 1
    return iteratedCSV
