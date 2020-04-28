import csv
import netmiko as nm
from netmiko import ConnectHandler
import textfsm
import os
global final_CSVresults
global final_CLIresults
global conn
global connArgs
global connIsAlive
global __name__
global matches
matches = []
connArgs = {}
final_CSVresults = []
final_CLIresults = []
savedCredentials = False
conn = ConnectHandler
connIsAlive = False


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
    global conn
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    print("-------------------------------------------\n" \
          "Now we will connect to  a WLC to pull currently\n" \
          " connected and Registered APs.\n" \
          "-------------------------------------------\n")
    conn = connect()
    return getApCli()
    

def main3():
    """ Validate that we have imported CSV and CLI """
    """ data and do comparison                     """
    print("-------------------------------------------\n" \
          "Now we will compare CSV to CLI for MAC Address\n" \
          " matches and validate it appears correct as expected.\n" \
          "-------------------------------------------\n")
    global final_CSVresults
    global final_CLIresults
    global matches
    global conn
    compare(final_CSVresults, final_CLIresults)
    matches_len = len(matches)
    if matches_len > 0:
          print("-------------------------------------------\n" \
                "Listed below are the matches found between \n" \
                "CSV and CLI. Listed as ...                 \n" \
                " [matched MAC, {Old AP Name, New AP Name}] \n" \
                "-------------------------------------------\n")
          for entry in range(len(matches)):
            print(matches[entry], sep=",")
    else:
        print("No matches were found between the CSV \n" \
              "and CLI results.                      \n")
    choice = int(input("Does this info look correct? 1=Yes | 2=No or Ctrl-C to exit : "))
    if choice == 1:
        create_commands(matches)
    elif choice == 2:
        main()
    

def create_commands(matches):
    """ Here we will pull in the matches from main3 """
    """ and create the commands to rename each AP   """
    """ on the WLC and place them in the list named """
    """ cli_commands to then pass to netmiko.       """
    global conn
    cli_commands = []
    index = 0
    cmd2 = "show ap config general | include ^Cisco AP Name|^MAC Address"
    for entry in range(len(matches)):
        cmd_old_name = matches[index][1].get("Old_Name")
        cmd_new_name = matches[index][1].get("New_Name")
        cmd1 = f"ap name {cmd_old_name} name {cmd_new_name}"
        cli_commands.append(cmd1)
        index = index + 1
    cli_commands.append(cmd2)
    return send_renameCmds(cli_commands)

def compare(final_CSVresults, final_CLIresults):
    """ First we create 2 lists, 1 for matches and 1 for """
    """ no-match. Then create another list with matched  """
    """ MACs with a nested dict with old_name/new_name   """
    """ which will be base for command build.            """
    match = []
    no_match = []
    global matches
    ## Here we check the length of each list and pad the lesser
    ## list with null pad entries to prevent throwing an index
    ## error when looping
    pad = ['null', 'inserted for padding']
    cli_len = len(final_CLIresults)
    csv_len = len(final_CSVresults)
    if cli_len > csv_len:
        diff = cli_len - csv_len
        for x in range(diff):
            final_CSVresults.append(pad)
    elif csv_len > cli_len:
        diff = csv_len - cli_len
        for x in range(diff):
            final_CLIresults.append(pad)
    else:
        print("No Diff, no need to pad")
    ## Here we loop through both lists looking for matching
    ## MACs and add them to lists for matches and no-match
    for x, y in [(x,y) for x in final_CSVresults for y in final_CLIresults]:
        print(x[1], y[1])
        if x[1] == y[1]:
            hit = [x, y]
            print("Match:" + x[1] + " " + y[1])
            match.append(hit)
    ## Here we will loop through matches and create a final
    ## list "matches" that has lists with nested DICTs with
    ## the old_name/new_name key:value pairs
    index = 0
    for item in range(len(match)):
        old_name = match[index][1][0]
        new_name = match[index][0][0]
        mac1 = match[index][0][1]
        mac2 = match[index][1][1]
        if mac1 == mac2:
            mentry = [mac1, {"Old_Name": old_name, "New_Name": new_name}]
            matches.append(mentry)
            index = index + 1
    else:
        print("Done Inserting Matches")
        print(matches, sep="\n")
    

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


def get_conn_args():
    """ Gather connection related Args and pass to Netmiko """
    global connArgs
    global savedCredentials
    print("Lets gather info for the WLC we will connect to....")
    connArgs = {
    "ip": input("Enter IP address of WLC: "),
    "user": input("Enter username-'must have priv15' :"),
    "pass": input("Enter password in cleartext: ")}
    correct = False
    print(connArgs)
    choice = 0
    choice = int(input("Is the above connection info correct? 1=Yes, 2=No  : "))
    while correct == False:
        if choice == 1:
            correct = True
            savedCredentials = True
            return connArgs
        elif choice == 2:
                connArgs = get_conn_args()
        else:
            print("Invalid choice. Please try again or ctrl-c to exit")
            get_connArgs()


def connect():
    global conn
    global connArgs
    global savedCredentials
    global connIsAlive
    attempts = 0
    expPrompt = False
    while connIsAlive is False:
        try:
            connArgs = get_conn_args()
            conn = ConnectHandler(ip=connArgs["ip"], username=connArgs["user"], password=connArgs["pass"], device_type="cisco_ios", session_log="ssh_session_logfile.txt", session_log_file_mode="write", session_log_record_writes="True")
        except nm.NetMikoTimeoutException:
            print("-------------------------------------------\n" \
                  "Error: Timeout Error Occured Attempting to \n" \
                  " Connect. Check IP address and try Again   \n" \
                  "-------------------------------------------\n")
        except nm.NetMikoAuthenticationException:
            print("<--> Auth Error occured <--> Check Username/Password and try again.")
    ##    except:
    ##        print("Unexpected error:", sys.exc_info()[0])
    ##        raise
        else:
            connIsAlive = conn.is_alive()
            if connIsAlive is True:
                print("Connection Successful!")
                getPrompt = conn.find_prompt()
                print("-------------------------------------------\n" \
                      "CONNECTED via SSH- \n" \
                      f"Device returned : {getPrompt}               \n" \
                      "-------------------------------------------\n")
                while expPrompt is False:
                    choice = 0
                    choice = int(input("Is the above CLI prompt the prompt you were\n" \
                                       "expecting from the correct WLC in exec mode? \n" \
                                       "1= Yes | 2=No or Ctrl-C to quit :  "))
                    if choice == 1:
                        conn.disable_paging()
                        expPrompt = True
                        return conn
                    elif choice == 2:
                        savedCredentials = False
                        conn = connect()
            else:
                print("Failure: Unknown Error. Sorry")


def getApCli():
    global conn
    global connIsAlive
    while connIsAlive is False:
        print("SSH Connection to WLC has closed. Reconnecting....")
        conn = connect()
    try:
        cli_output = conn.send_command_timing("show ap config general | include ^Cisco AP Name|^MAC Address", use_textfsm=True, textfsm_template="./templates/cisco_ios_show_ap_template-v2.textfsm")
    except nm.NetMikoTimeoutException:
        print("Timeout Error occured. Timeout waiting for device for an operation to continue.")
##    except:
##        print("Unexpected error:", sys.exc_info()[0])
##        raise
    else:
        parseCLI(cli_output)
        

def send_renameCmds(cli_commands):
    """ Here we send the contents of the cli_commands """
    """ list to the WLC via Netmiko active connection """
    """ If conn is dead, we will open a new one.      """
    global conn
    global connArgs
    global savedCredentials
    is_connActive = False
    is_connActive = conn.is_alive()
    while is_connActive is False:
        print("The SSH session to the WLC has closed. \n")
        if savedCredentials is True:
            print(connArgs)
            print("Reopeneing connection using saved info above...")
            conn = nm.BaseConnection(ip=connArgs["ip"], username=connArgs["user"], password=connArgs["pass"])
            getPrompt = conn.find_prompt()
            is_connActive = conn.is_alive()
        else:
            print("Error")
    conn.send_config_set(config_commands=cli_commands, enter_config_mode=False, cmd_verify=False, exit_config_mode=False)
    conn.disconnect()
    print("-------------------------------------------\n" \
          "Commands sent and logfile is printed below \n" \
          "The logfile is also save locally in the    \n" \
          "current dir as ssh_session_logfile.txt     \n" \
          "-------------------------------------------\n")
    with open("ssh_session_logfile.txt") as log:
        read = log.readlines()
        for line in read:
            print(line)
    close = input("-------------------------------------------\n" \
          "Script Complete. SSH session closed and    \n" \
          "The logfile is also saved locally in the   \n" \
          "current dir as ssh_session_logfile.txt     \n" \
          "---------Press Ctrl-C to Exit--------------\n")

    

def parseCSV(csv_choice):
    import sys
    import json
    with open('./templates/cisco_ap_from_csv_template.textfsm') as template:
        results_template = textfsm.TextFSM(template)
        content2parse = open(csv_choice)
        content = content2parse.read()
        try:
            parsedCSV_results = results_template.ParseText(content)
        except textfsm.TextFSMError:
            err = input("-------------------------------------------\n" \
                  "ERROR: Import error occured while parsing  \n" \
                  "MAC Addresses. Invalid characters were found\n" \
                  "on import(Non-Hex). Check CSV file and try again.\n" \
                  "-------------------------------------------")
        else:
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
        name = str.lower(entry[0])
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
    re_fmt = '[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]\.[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]\.[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]'
#    re_fmt = '^[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\b'
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
            if len(mac) > 12:
                raise ValueError(
                    print(input("-------------------------------------------\n" \
                                "ERROR: Import error occured while parsing  \n" \
                                "MAC Address " + mac + ". More than 12 characters\n" \
                                "are present. Check CSV file and try again. \n" \
                                "-------------------------------------------")))
            else:
                new_mac = mac[:4] + "." + mac[4:8] + "." + mac[8:12]
                print(new_mac)
                if re.match(re_fmt, new_mac):
                    print("Format is now correct...adding to list: " + new_mac)
                    new_entry = [entry[0], new_mac]
                    final_CSVresults.append(new_entry)
                else:
                     print("Unable to normalize MAC Address. Check input and try again")
    print("-------------------------------------------\n" \
          "We located the below entries in the CSV file.\n" \
          "-------------------------------------------\n")
    for row in range(len(final_CSVresults)):
        print(final_CSVresults[row], sep="\n")
    return main2()



if __name__ == "__main__":
    main()
