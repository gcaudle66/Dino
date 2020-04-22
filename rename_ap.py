import pandas as pd
import numpy as np
import csv
import netmiko as nm
import textfsm
import argparse
import os
global final_CSVresults
global final_CLIresults
from ap_rename4 import scan_for_csv

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
        choice = 0
        final_CSVresults = scan_for_csv()
    elif choice == 2:
        exit()

def main2():
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    global final_CSVresults
    global final_CLIresults
    print("-------------------------------------------\n" \
          "Now we will connect to  a WLC to pull currently\n" \
          " connected and Registered APs.\n" \
          "-------------------------------------------\n")
    final_CLIresults = get_conn_args()

def main3(final_CLIresults):
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    global final_CSVresults
    print("-------------------------------------------\n" \
          "Now we will compare CSV to CLI for MAC Address\n" \
          " matches and validate it appears correct as expected.\n" \
          "-------------------------------------------\n")
    print(finalCSV_results)
    print(finalCLI_results)
    match = []
    no_match = []
    choice = input("Does this info look correct? :")

if __name__ == "__main__":
    main()
