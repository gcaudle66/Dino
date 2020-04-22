import pandas as pd
import numpy as np
import csv
import netmiko as nm
import textfsm
import argparse
import os
global final_CSVresults
global final_CLIresults
global conn
global __name__
final_CSVresults = []
final_CLIresults = []


## Temp Data to avoid the reconnects
#cli_parsed = ([{'ap_name': ': Floor2.AP.C9C0', 'mac_address': ': 683b.7850.d8e0'},
##            {'ap_name': ': AP7069.5AEB.E424', 'mac_address': ': 28ac.9ed8.d020'},
##            {'ap_name': ': AP7069.5AEB.E424', 'mac_address': ': 28ac.9ed8.d020'},
##            {'ap_name': ': AP6C41.0E17.035C', 'mac_address': ': 6c:41:0e:17:03:5c'},
##            {'ap_name': ': AP6C41.1E17.3BCC', 'mac_address': ': 6C410E173BCC'}])
##
###connArgs = {
##    "ip": "198.18.134.100",
##    "user": "admin",
##     "pass": "C1sco12345"}
##
def main():
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    print("-------------------------------------------\n" \
          "<----Welcome to AP Renamerer.---->\n" \
          "-------------------------------------------\n" \
          "In this script we will...\n" \
          "-Scan for CSV files to import.\n" \
          "-Connect to the chosen WLC and gather current registered APs\n" \
          "-We will then parse that data and validate the data imported from\n" \
          " CSV and data imported from WLC matches.\n-Then change the names " \
          " on the WLC.\n"\
          "-------------------------------------------\n" \
          "So first lets get the file to import.....\n" \
          "-!! Make sure any CSV files to import\n" \
          " are placed in the same directory as this\n" \
          " script before continuing !!-\n" \
          "-------------------------------------------\n")
    cont = False
    choice = 0
    choice = int(input("Are you ready to proceed? 1=Yes 2=No or Ctrl-C to quit: "))
    if choice == 1:
        cont = True
        print("-------------------------------------------\n" \
          "Scanning current directory for CSV files...\n" \
          "-------------------------------------------\n")
        cwd = os.getcwd()
        with os.scandir(path=cwd) as it:
            file_list = []
            for entry in it:
                if entry.name.endswith(".csv") and entry.is_file():
                    file_list.append(entry.name)
            file_len = len(file_list)
            print(f"Located {file_len} CSV files.")
            importCSV(file_list)
    elif choice == 2:
        exit()


def main2():
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    print("-------------------------------------------\n" \
          "Now we will connect to  a WLC to pull currently\n" \
          " connected and Registered APs.\n" \
          "-------------------------------------------\n")
    get_conn_args()

def main3():
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    print("-------------------------------------------\n" \
          "Now we will compare CSV to CLI for MAC Address\n" \
          " matches and validate it appears correct as expected.\n" \
          "-------------------------------------------\n")
    global final_CSVresults
    global final_CLIresults
    print(final_CSVresults)
    print(final_CLIresults)
    match = []
    no_match = []
    choice = input("Does this info look correct? :")


def importCSV(file_list):
    """ Choose file to import """
    print("-------------------------------------------\n" \
          "The files found are listed below.          \n" \
          "Please select a number to select the file \n" \
          "to import in.                              \n" \
          "-------------------------------------------\n")
    index = 0
    choice = 0
    choices_list = {}
    for item in range(len(file_list)):
        item = file_list[index]
        print("Choice # {} : {} ".format(index, item))
        choice_entry = choices_list[index] = item
        index = index + 1
    print(choices_list)
    choice = int(input("Please select a file # from the list to import: "))
    csv_choice = choices_list[choice]
    return parseCSV(csv_choice)

##def scan_for_csv():
##    """ Scan current directory for any file ending in csv """
##    print("-------------------------------------------\n" \
##          "Scanning current directory for CSV files...\n" \
##          "-------------------------------------------\n")
##    cwd = os.getcwd()
##    with os.scandir(path=cwd) as it:
##        file_list = []
##        for entry in it:
##            if entry.name.endswith(".csv") and entry.is_file():
##                file_list.append(entry.name)
##    file_len = len(file_list)
##    print(f"Located {file_len} CSV files.")
##    return importCSV(file_list)

def get_conn_args():
    """ Gather connection related Args and pass to Netmiko """
    #parser = argparse.ArgumentParser(description="This parser is to gather connection " \
                                     #"related arguments such as username to build the " \
                                     #" SSH connection to the WLC.                     ")
    #parser.add_argument(divmod
    print("Lets gather info for the WLC we will connect to....")
    connArgs = {
    "ip": input("Enter IP address of WLC: "),
    "user": input("Enter username-'must have priv15' :"),
    "pass": input("Enter password in cleartext: ")}
    correct = False
    print(connArgs)
    choice = 0
    choice = int(input("Is the above connection info correct? 1=Yes, 2=No  :"))
    while correct == False:
        if choice == 1:
            correct = True
            pass
        elif choice == 2:
                get_conn_args()
        else:
            print("Invalid choice. Please try again or ctrl-c to exit")
            get_connArgs()
    return connect(connArgs)        

def connect(connArgs):
    expPrompt = False
    connex = False
    conn = nm.BaseConnection(ip=connArgs["ip"], username=connArgs["user"], password=connArgs["pass"])
    getPrompt = conn.find_prompt()
    print("CONNECTED via SSH- \n" \
          "Device returned :" + getPrompt)
    while expPrompt is False:
        choice = 0
        choice = int(input("Is the above CLI prompt the prompt you were\n" \
                           "expecting from the correct WLC in exec mode? \n" \
                           "1= Yes | 2=No or Ctrl-C to quit :  "))
        if choice == 1:
            no_paging = conn.disable_paging()
            print("Disabling paging and setting Terminal Width: set to :" + no_paging)
            return getApCli(conn)
        elif choice == 2:
            return get_conn_args()

def getApCli(conn):
    alive = conn.is_alive()
    if alive == True:
        cli_output = conn.send_command("show ap config general | include ^Cisco AP Name|^MAC Address", use_textfsm=True, textfsm_template="./templates/cisco_ios_show_ap_template-v2.textfsm")
    return parseCLI(cli_output)

def parseCSV(csv_choice):
    with open('./templates/cisco_ap_from_csv_template.textfsm') as template:
        results_template = textfsm.TextFSM(template)
        content2parse = open(csv_choice)
        content = content2parse.read()
        parsedCSV_results = results_template.ParseText(content)
    return newLower_list(parsedCSV_results)

def parseCLI(cli_output):
    global final_CLIresults
    for item in range(len(cli_output)):
        entry = cli_output.pop()
        name = entry.get("ap_name")
        mac = entry.get("mac_address")
        add = [name, mac]
        final_CLIresults.append(add)
    return main3()

def newLower_list(content):
    """ Converts any MAC address fields to lowercase """
    output = []
    for entry in range(len(content)):
        entry = content.pop()
        name = entry[0]
        mac = str.lower(entry[1])
        new_entry = [name, mac]
        output.append(new_entry)
    return formatMacs(output)

  
def formatMacs(content):
    print("-------------------------------------------\n" \
          "Normalizing MAC Addresses found in CSV     \n" \
          "All MACs will be set to lowercase and then \n" \
          "checked against REGEX to make sute they are\n" \
          "in format xxxx.xxxx.xxxx before proceeding \n" \
          "-------------------------------------------\n")
    import re
    re_fmt = '[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9].[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9].[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]'
    #final_CSVresults = []
    global final_CSVresults
    bad_chars = [":", "."]
    for entry in range(len(content)):
        entry = content.pop()
        if re.match(re_fmt, entry[1]):
            final_CSVresults.append(entry)
        else:
            mac = entry[1]
            print("Incorrect format: " + mac)
            for i in bad_chars:
                mac = mac.replace(i, "")
            print(mac)
            new_mac = mac[:4] + "." + mac[4:8] + "." + mac[8:12]
            print(new_mac)
            if re.match(re_fmt, new_mac):
                print("Format is now correct...adding to list: " + new_mac)
                new_entry = [entry[0], new_mac]
                final_CSVresults.append(new_entry)
            else:
                raise ValueError(
                    print("Unable to normalize MAC Address. Check input and try again"))
    return main2()



if __name__ == "__main__":
    main()
