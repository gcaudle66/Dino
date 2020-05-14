import csv
import netmiko as nm
from netmiko import ConnectHandler
import textfsm
import os
import dnac_api
global final_CSVresults
global final_CLIresults
global final_APIresults
global conn
global connArgs
global connIsAlive
global matches
global entries
global forAPI
matches = []
entries = 0
connArgs = {}
forAPI = False
final_CSVresults = []
final_CLIresults = []
final_APIresults = []
savedCredentials = False
conn = ConnectHandler
connIsAlive = False

### Version and Author Info
##__version__ = "2.0"
##__author__ = "Garrett Caudle | gcaudle66@gmail.com"
##
##class Ap_Rename:
##    """ This is the AP Rename app (aka AP Renamerer)
##    This app is used to bulk rename Access points
##    In Cisco 9800 IOS-XE platform wireless LAN
##    Controllers. This app is not maintained nor
##    Endorsed in any way by Cisco Systems Inc.
##    Use of this App is at the users own risk
##    """
##    def __init__(self, version, author):
##        self.version = __version__
##        self.author = __author__
##
##def main():
##    """ Initial start of script and disclaimer.       \n""" \
##    """ In this script we will...                     \n""" \
##    """ -Scan for CSV files to import.                \n""" \
##    """ -Connect to the chosen WLC and gather         \n""" \
##    """ current registered APs -We will then parse    \n""" \
##    """ that data and validate the data imported      \n""" \
##    """ from CSV and data imported from WLC           \n""" \
##    """ matches.-Then change the names on the WLC.    """
##    print("-------------------------------------------\n" \
##          "<----Welcome to AP Renamerer.---->\n" \
##          "-------------------------------------------\n" \
##          "In this script we will...\n" \
##          "-Scan for CSV files to import.\n" \
##          "-Connect to the chosen WLC and gather current registered APs\n" \
##          "-We will then parse that data and validate the data imported from\n" \
##          " CSV and data imported from WLC matches.\n-Then change the names " \
##          " on the WLC.\n"\
##          "-------------------------------------------\n" \
##          "-------------------------------------------\n" \
##          "-------------------------------------------\n" \
##          "So first lets get the file to import.....\n" \
##          "-!! Make sure any CSV files to import\n" \
##          " are placed in the same directory as this\n" \
##          " script before continuing !!-\n" \
##          "-------------------------------------------\n")
##    cont = False
##    choice = 0
##    choice = int(input("Are you ready to proceed? 1=Yes 2=No or Ctrl-C to quit: "))
##    if choice == 1:
##        cont = True
##        print("-------------------------------------------\n" \
##          "Scanning current directory for CSV files...\n" \
##          "-------------------------------------------\n")
##        cwd = os.getcwd()
##        with os.scandir(path=cwd) as it:
##            file_list = []
##            for entry in it:
##                if entry.name.endswith(".csv") and entry.is_file():
##                    file_list.append(entry.name)
##            file_len = len(file_list)
##            print(f"Located {file_len} CSV files.")
##            importCSV(file_list)
##    elif choice == 2:
##        exit()
##
##def api_main():
##    """ Where the magic begins
##    Here we begin the process of gathering wireless LAN
##    controllers from DNA center in order to locate the
##    APs that need to be renamed as requested by the "ap_rename"
##    module. This program will...
##        --Gather needed info for connection to DNAC (IP, user/pass)
##        --Use requests module to make an API POST call to aquire
##          AUTH-Token needed to proceed with subsequent calls.
##        --If suxcessful acquiring token, program will make API
##          call to DNAC and gather entire inventory of "Managed"
##          devices, create a local list to hold that inventory and add
##          it to it
##        --Program will then iterate through this inventory list looking
##          for devices with the "Family" value of Wireless Controller
##        --If match is found, matches are added to a llocal DICT containing
##          the WLC "hostname" and "mgmntIPAddress"
##    """
####    global dnac_savedCreds
####    global dnac_connArgs
##    dnac_connArgs = {}
##    dnac_savedCreds = False
##    while dnac_savedCreds == False:
##        print("*********************************************************");
##        print("* Cisco DNA Center REST API Python Utility              *");
##        print("*                                                       *");
##        print("* Please provide the following data in order to connect *");
##        print("*                                                       *");
##        print("* DNAC API IP: Cluster IP address for target DNA Center *");
##        print("* Username: [username]                                  *");
##        print("* Password: [password]                                  *");
##        print("*                                                       *");
##        print("*                                                       *");
##        print("* Control C to exit                                     *");
##        print("*********************************************************");
##        dnac_connArgs = {
##            "cluster": input("DNAC API IP: "),
##            "username": input("Username:"),
##            "password": input("Password: ")}
##        correct = False
##        print("DNAC API IP: " + dnac_connArgs["cluster"] + " | Username: " + dnac_connArgs["username"])
##        choice = 0
##        choice = int(input("Is the above connection info correct? 1=Yes, 2=No  : "))
##        while correct == False:
##            if choice == 1:
##                correct = True
##                dnac_savedCreds = True
##                dnac_connArgs
##            elif choice == 2:
##                main()
##                break
##    choice2 = 0
##    print("*********************************************************");
##    print("* Cisco DNA Center REST API Python Utility              *");
##    print("*                                                       *");
##    print("* User has confirmed connection info. Next step...      *");
##    print("*                                                       *");
##    print("* Script will now connect to the DNA Center API         *");
##    print("* interface and retreive the Authentication Token       *");
##    print("*                                                       *");
##    print("* Control C to exit                                     *");
##    print("*********************************************************");
##    choice2 = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
##    if choice2 == 1:
##        dnac_token = dnac_api.get_dnac_token(dnac_connArgs)
##        return api_main2(dnac_token)
##    elif choice2 == 2:
##        api_main()
##
##
##def api_main2(dnac_token):
##    """ 
##    """
##    choice = 0
##    print("*********************************************************");
##    print("* Cisco DNA Center REST API Python Utility              *");
##    print("*                                                       *");
##    print("* Script retreived Auth Token from API. Next step...    *");
##    print("*                                                       *");
##    print("* Script will now GET full inventory of devices in      *");
##    print("* DNA Center.                                                      *");
##    print("*                                                       *");
##    print("* Control C to exit                                     *");
##    print("*********************************************************");
##    choice = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
##    if choice == 1:
##        try:
##            dnac_inventory = dnac_api.get_dnac_inventory(dnac_token, dnac_connArgs)
##        except Exception:
##            print("Something went wonky and an exception got thrown")
##            api_main2()
##        else:
##            return main_menu(dnac_token, dnac_inventory)
##    elif choice == 2:
##        api_main()
##
##
##def main_menu(dnac_token, dnac_inventory):
##    """
##    """
##    choice = 0
##    print("*********************************************************");
##    print("* Cisco DNA Center REST API Python Utility              *");
##    print("*                                                       *");
##    print("* Success! Inventory was Collected from DNAC API.       *");
##    print("*                                                       *");
##    print("*********************************************************");
##    print("* Now choose what you wanna do with the data!           *");
##    print("* Intent Menu --------                                  *");
##    print("*                                                       *");
##    print("* [1] Wifi Inventory                                    *");
##    print("* [2] Resync All Devices                                *");
##    print("*                                                       *");
##    print("*                                                       *");                            
##    print("*                                                       *");
##    print("* Control C to exit                                     *");
##    print("*********************************************************");
##    choice = int(input("* Intent Menu Choice [#] :  "))
##    if choice == 1:
##        wifi_inv = []
##        try:
##            dnac_api.wifi_inventory(wifi_inv, dnac_token, dnac_connArgs, dnac_inventory)
##        except Exception:
##            print("Something went wonky and an exception got thrown")
##            main_menu()
##        else:
##            print("*********************************************************\n" \
##                  "* WiFi Inventory Collection was a Success!              *\n" \
##                  f"* Total WLCs: {len(wifi_inv[0])}                       *\n" \
##                  f"* Total APs: {len(wifi_inv[1])}                        *\n" \
##                  "*********************************************************\n")
##            return wifi_inv
##    elif choice == 2:
##        main_menu()
##


##def main2():
##    """ Validate that we have imported CSV         \n""" \
##    """ data and now gather info for connecting to \n""" \
##    """ WLC to gather data for comparison with CSV \n"""
##    global conn
##    print("-------------------------------------------\n" \
##          "Now we will connect to  a WLC to pull currently\n" \
##          " connected and Registered APs.\n" \
##          "-------------------------------------------\n")
##    conn = connect()
##    return getApCli()
##    
##
##def main3():
##    """ Validate that we have imported CSV and CLI    \n""" \
##    """ data and do comparison between them based     \n""" \
##    """ on MAC addresses. Create commands for         \n""" \
##    """ changing names via SSH/CLi on WLC and adding  \n""" \
##    """ them to a list. Then present matches to       \n""" \
##    """ user and await confirmation b4 sending to WLC   """ 
##    print("-------------------------------------------\n" \
##          "Now we will compare CSV to CLI for MAC Address\n" \
##          " matches and validate it appears correct as expected.\n" \
##          "-------------------------------------------\n")
##    global final_CSVresults
##    global final_CLIresults
##    global matches
##    global conn
##    compare(final_CSVresults, final_CLIresults)
##    matches_len = len(matches)
##    if matches_len > 0:
##          print("-------------------------------------------\n" \
##                "Listed below are the matches found between \n" \
##                "CSV and CLI. Listed as ...                 \n" \
##                " [matched MAC, {Old AP Name, New AP Name}] \n" \
##                "-------------------------------------------\n")
##          for entry in range(len(matches)):
##            print(matches[entry], sep=",")
##    else:
##        print("No matches were found between the CSV \n" \
##              "and CLI results.                      \n")
##    choice = int(input("Does this info look correct? 1=Yes | 2=No or Ctrl-C to exit : "))
##    if choice == 1:
##        create_commands(matches)
##    elif choice == 2:
##        savedCredentials = False
##        print(f"Disconnecting Current SSH Session...") 
##        conn.disconnect()
##        connIsAlive = conn.is_alive()
##        main()


def connex_split():
    global entries
    entries = 0
    split_conns = []
    split_conns.clear()
    temp_matches = matches.copy()
    counter = len(temp_matches)
    while counter > 0:
        for item in temp_matches:
            wlc = [item[1].get("wlc")]
            if wlc not in split_conns:
                entry = wlc
                split_conns.append(entry)
                counter = counter - 1
            elif wlc in split_conns:
                index = split_conns[:].index(wlc)
                #print(str(index), wlc)
                counter = counter - 1
    counter = len(split_conns)
    for list in split_conns:
            for y in temp_matches:
                #print(y[1].get("wlc"))
                if list[0] == y[1].get("wlc"):
                    #print("match : " + list[0] + y[1].get("wlc"))
                    list.append(y)
                    entries = entries + 1
            counter = counter - 1
    print(entries)
    return split_conns


def create_connex_list(split_conns):
    for entry in split_conns:
        cli_commands = api_create_commands(entry)
        entry.append(cli_commands)
    connex_list = split_conns.copy()
    return connex_list


def api_create_commands(matches):
    """ Here we will pull in the matches from main3 \n""" \
    """ and create the commands to rename each AP   \n""" \
    """ on the WLC and place them in the list named \n""" \
    """ cli_commands to then pass to netmiko.       \n"""
    cli_commands = []
    index = 0
    entries = len(matches)
    temp_matches = matches.copy()
    temp_matches.pop(0)
    cmd2 = "show ap config general | include ^Cisco AP Name|^MAC Address"
    try:
        for entry in temp_matches:
            cmd_old_name = temp_matches[index][1].get("Old_Name")
            cmd_new_name = temp_matches[index][1].get("New_Name")
            cmd1 = f"ap name {cmd_old_name} name {cmd_new_name}"
            cli_commands.append(cmd1)
            index = index + 1
    except TypeError:
        index = index + 1
    except KeyError:
        print("key error")
        print(index)
    except IndexError:
        print("Index error")
        print(index)
    else:
        cli_commands.append(cmd2)
        return cli_commands


def create_commands(matches):
    """ Here we will pull in the matches from main3 \n""" \
    """ and create the commands to rename each AP   \n""" \
    """ on the WLC and place them in the list named \n""" \
    """ cli_commands to then pass to netmiko.       \n"""
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
    """ First we create 2 lists, 1 for matches and 1 for \n""" \
    """ no-match. Then create another list with matched  \n""" \
    """ MACs with a nested dict with old_name/new_name   \n""" \
    """ which will be base for command build.            \n"""
    match = []
    no_match = []
    global matches
##    global final_CSVresults
##    global final_CLIresults
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
  

def api_compare(content):
    """ First we create 2 lists, 1 for matches and 1 for \n""" \
    """ no-match. Then create another list with matched  \n""" \
    """ MACs with a nested dict with old_name/new_name   \n""" \
    """ which will be base for command build.            \n"""
    match = []
    no_match = []
    global matches
    ## Here we check the length of each list and pad the lesser
    ## list with null pad entries to prevent throwing an index
    ## error when looping
    pad = ['null', 'inserted for padding']
    content_len = len(content)
    csv_len = len(final_CSVresults)
    if content_len > csv_len:
        diff = content_len - csv_len
        for x in range(diff):
            final_CSVresults.append(pad)
    elif csv_len > content_len:
        diff = csv_len - content_len
        for x in range(diff):
            content.append(pad)
    else:
        print("No Diff, no need to pad")
    ## Here we loop through both lists looking for matching
    ## MACs and add them to lists for matches and no-match
    for x, y in [(x,y) for x in final_CSVresults for y in content]:
        print(x[1], y[1])
        print(x, y)
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
        wlc = match[index][1][2]
        if mac1 == mac2:
            mentry = [mac1, {"Old_Name": old_name, "New_Name": new_name, "wlc": wlc}]
            matches.append(mentry)
            index = index + 1
    else:
        print("Done Inserting Matches")
        print(matches, sep="\n")
        


def importCSV(file_list):
    """ Choose CSV file to import  that was found in local \n""" \
    """ directory.                                         \n"""
    print("\n\n\n")
    print("*********************************************************");
    print("* Dino | AP Rename                                      *");
    print("*********************************************************\n" \
          f"* [{len(file_list)}] CSV files that were located are listed below      *\n" \
          "* Please select the Choice number of the desired file   *\n" \
          "* to import to begin parsing.                           *\n" \
          "*********************************************************");
    index = 0
    choice = 0
    choices_list = {}
    for item in range(len(file_list)):
        item = file_list[index]
        print("- Choice # [{}] : {} ".format(index, item))
        choice_entry = choices_list[index] = item
        index = index + 1
    print("\n")
    choice = int(input("Please input Choice # from the list to import: "))
    csv_choice = choices_list[choice]
    return parseCSV(csv_choice)


def get_conn_args():
    """ Here we will gather connection arguments that \n""" \
    """ will be used when connecting to WLC.          \n""" \
    """ IP/hostname, Username, Password               \n"""
    import getpass
    global connArgs
    global savedCredentials
    global forAPI
    print("*********************************************************");
    print("* Dino | SSH ConneX                                     *");
    print("*********************************************************");
    print("* Lets gather info for the WLC we will connect to...    *");
    if forAPI == False:
        connArgs = {
            "ip": input("* Enter IP/Hostname of WLC: "),
            "user": input("* Enter username-'must have priv15' :"),
            "pass": getpass.win_getpass("* Enter password: ")}
        correct = False
        print("*********************************************************");
        print("* WLC Hostname/IP: " + connArgs["ip"])                  
        print("* Username: " + connArgs["user"])
        choice = 0
        print("*           [1] Yes | [2] No or Ctrl-C to quit          *");
        print("*********************************************************");
    elif forAPI == True:
        connArgs = {
            "user": input("* Enter username-'must have priv15' :"),
            "pass": getpass.win_getpass("* Enter password: ")}            
        correct = False
        print("*********************************************************");
        print("*")# WLC Hostname/IP: " + connArgs["ip"])                  
        print("* Username: " + connArgs["user"])
        choice = 0
        print("*           [1] Yes | [2] No or Ctrl-C to quit          *");
        print("*********************************************************");
    choice = int(input(" Is the above connection info correct? "))
    while correct == False:
        if choice == 1:
            correct = True
            savedCredentials = True
            return connArgs
        elif choice == 2:
            main2()
            break
        else:
            print("Invalid choice. Please try again or ctrl-c to exit")
            get_connArgs()

def api_connect(conn_info):
    global conn
    global connIsAlive
    global connArgs
    attempts = 0
    expPrompt = False
    while connIsAlive is False:
        try:
            conn = ConnectHandler(ip=conn_info[0], username=connArgs["user"], password=connArgs["pass"], device_type="cisco_ios", session_log="ssh_session_logfile.txt", session_log_file_mode="write", session_log_record_writes="True")
        except nm.NetMikoTimeoutException:
            print("*********************************************************\n" \
                  "* Error: Timeout Error Occured Attempting to            *\n" \
                  "* connect. Check IP/Hostname and try Again              *\n" \
                  "*********************************************************\n")
        except nm.NetMikoAuthenticationException:
            print("*********************************************************\n" \
                  "* Error: Authentication Error Occured.                  *\n" \
                  "* Check Credentials and try Again                       *\n" \
                  "*********************************************************\n")
        else:
            connIsAlive = conn.is_alive()
            if connIsAlive is True:
                print("*********************************************************");
                print("* Dino | SSH ConneX                                     *");
                print("*********************************************************")
                print("* SSH Connection Successful!                            *")
                getPrompt = conn.find_prompt()
                print("* We need to validate if this is the intended device    *")
                print("*                                                       *")
                print(f"* Device CLI prompt : {getPrompt}                     \n")
                print("*                                                       *")
                while expPrompt is False:
                    choice = 0
                    print("*         [1] Yes | [2] No or Ctrl-C to quit            *")
                    print("*********************************************************")
                    choice = int(input(" Is the above CLI prompt the prompt you were           *\n" \
                                       " expecting from the correct WLC in PRIV EXEC mode? : \n"))
                    if choice == 1:
                        conn.disable_paging()
                        expPrompt = True
                        return conn
                    elif choice == 2:
                        print(f"Disconnecting Current SSH Session...") 
                        conn.disconnect()
                        connIsAlive = conn.is_alive()
                        return conn
            else:
                print("Failure: Unknown Error. Sorry")

    
def connect():
    """ Here we will user connArgs gathered from get_conn_args \n""" \
    """ and establish connection to WLC                        \n"""
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
            print("*********************************************************\n" \
                  "* Error: Timeout Error Occured Attempting to            *\n" \
                  "* connect. Check IP/Hostname and try Again              *\n" \
                  "*********************************************************\n")
        except nm.NetMikoAuthenticationException:
            print("*********************************************************\n" \
                  "* Error: Authentication Error Occured.                  *\n" \
                  "* Check Credentials and try Again                       *\n" \
                  "*********************************************************\n")
    ##    except:
    ##        print("Unexpected error:", sys.exc_info()[0])
    ##        raise
        else:
            connIsAlive = conn.is_alive()
            if connIsAlive is True:
                print("*********************************************************");
                print("* Dino | SSH ConneX                                     *");
                print("*********************************************************")
                print("* SSH Connection Successful!                            *")
                getPrompt = conn.find_prompt()
                print("* We need to validate if this is the intended device    *")
                print("*                                                       *")
                print(f"* Device CLI prompt : {getPrompt}                     \n")
                print("*                                                       *")
                while expPrompt is False:
                    choice = 0
                    print("*         [1] Yes | [2] No or Ctrl-C to quit            *")
                    print("*********************************************************")
                    choice = int(input(" Is the above CLI prompt the prompt you were           *\n" \
                                       " expecting from the correct WLC in PRIV EXEC mode? : \n"))
                    if choice == 1:
                        conn.disable_paging()
                        expPrompt = True
                        return conn
                    elif choice == 2:
                        savedCredentials = False
                        print(f"Disconnecting Current SSH Session...") 
                        conn.disconnect()
                        connIsAlive = conn.is_alive()
                        main2()
            else:
                print("Failure: Unknown Error. Sorry")


def getApCli():
    """ Here we will run commands against the WLC to gather \n""" \
    """ necessary data for comparison against CSV           \n"""
    global conn
    global connIsAlive
    while connIsAlive is False:
        print("SSH Connection to WLC has closed. Reconnecting....")
        conn = connect()
    try:
        cli_output = conn.send_command_timing("show ap config general | include ^Cisco AP Name|^MAC Address", use_textfsm=True, textfsm_template="./templates/cisco_ios_show_ap_template-v2.textfsm")
    except nm.NetMikoTimeoutException:
        print("Timeout Error occured. Timeout waiting for device for an operation to continue.")
        main2()
##    except:
##        print("Unexpected error:", sys.exc_info()[0])
##        raise
    else:
        parseCLI(cli_output)
        

def send_renameCmds(cli_commands):
    """ Here we send the contents of the cli_commands \n""" \
    """ list to the WLC via Netmiko active connection \n""" \
    """ If conn is dead, we will open a new one.      \n"""
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
    """ Here we will parse through the CSV that was imported \n""" \
    """ using a TextFSM template that looks for only certain \n""" \
    """ fields in the CSV. These fields are defined in the   \n""" \
    """ below mentioned template variable                    \n"""
    with open('./templates/cisco_ap_from_csv_template-v2.textfsm') as template:
        results_template = textfsm.TextFSM(template)
        content2parse = open(csv_choice)
        content = content2parse.read()
        try:
            parsedCSV_results = results_template.ParseText(content)
        except textfsm.TextFSMError:
            err = input("*********************************************************\n" \
                        "* Houston, we have a problem!                           *\n" \
                  "* ERROR: Import error occured while parsing                   *\n" \
                  "* MAC Addresses. Invalid characters were found                *\n" \
                  "* on import. Check CSV file and try again.                    *\n" \
                  "*********************************************************")
        else:
            return newLower_list(parsedCSV_results)

def parseCLI(cli_output):
    """ Here we will take the CLI gathered data that is    \n""" \
    """ contained in a list, pop off each entry and create \n""" \
    """ a new list so that the format of its list matches  \n""" \
    """ the CSV formatted data list.                       \n"""
    import dino
    global final_CLIresults
    for item in range(len(cli_output)):
        entry = cli_output.pop()
        name = entry.get("ap_name")
        mac = entry.get("mac_address")
        add = [name, mac]
        final_CLIresults.append(add)
    return dino.main3()


def parseAPI(wifi_inv):
    """ Parses through API wifi inventory list seperating
        index[1] which holds the APs, iterating it and
        adding hostname and ethMACAddress to a new list
        to match format of the CSV list for matching
    """
    parsedAPI = []
    index = 0
    temp_inv = wifi_inv
    for item in range(len(temp_inv[1])):
        item = temp_inv[1][index]
        name = item.get("hostname")
        mac = item.get("ethMacAddress")
        wlc = item.get("associatedWlcIp")
        entry = [name, mac, wlc]
        index = index + 1
        parsedAPI.append(entry)
    return api_formatMacs(parsedAPI)

def newLower_list(content):
    """ Converts any MAC address fields to lowercase \n""" \
    """ Converts AP names fields to lowercase        \n"""
    output = []
    for entry in range(len(content)):
        entry = content.pop()
        name = str.lower(entry[0])
        mac = str.lower(entry[1])
        new_entry = [name, mac]
        output.append(new_entry)
    return formatMacs(output)

  
def formatMacs(content):
    """ here is where it gets fun. This function takes data from      \n""" \
    """ the imported CSV list where MAC addresses may not be in       \n""" \
    """ the correct format of xxx.xxx.xxxx and removes any existing   \n""" \
    """ delimeters, checks to make sure there are no more than 12 hex \n""" \
    """ characters, and if no error is present, rebuilds them into    \n""" \
    """ the correct xxxx.xxxx.xxxx format. If any error is raised     \n""" \
    """ during the process, that entry is ignored.                    \n"""
    print("-------------------------------------------\n" \
          "Normalizing MAC Addresses found in CSV     \n" \
          "All MACs will be set to lowercase and then \n" \
          "checked against REGEX to make sute they are\n" \
          "in format xxxx.xxxx.xxxx before proceeding \n" \
          "-------------------------------------------\n")
    import re
    import dino
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
            print(f"Removing seperators: {mac}")
            if len(mac) > 12:
                raise ValueError(
                    print(input("*********************************************************\n" \
                                "* Houston, we have a problem!                           *\n" \
                                "* ERROR: Import error occured while parsing             *\n" \
                                "* MAC Address " + mac + ". More than 12 characters\n" \
                                "* are present. Check CSV file and try again.            *\n" \
                                "*********************************************************\n")))
            else:
                new_mac = mac[:4] + "." + mac[4:8] + "." + mac[8:12]
                print(f"Reformatted: {new_mac}")
                if re.match(re_fmt, new_mac):
                    print("Format is now correct...adding to list: " + new_mac)
                    new_entry = [entry[0], new_mac]
                    final_CSVresults.append(new_entry)
                else:
                     err = input("*********************************************************\n" \
                                 "* Houston, we have a problem!                           *\n" \
                                 "* ERROR: Unable to normalize MAC Address:               *\n" \
                                 f"* {new_mac}                                            *\n" \
                                 "* Possible Non-Hex Character. Ignoring this entry       *\n"
                                 "* Press Enter key to continue                           *\n" \
                                 "*********************************************************")
    print("*********************************************************");
    print("* The following entries were found in the imported CSV  *");
    print("*********************************************************");
    for row in range(len(final_CSVresults)):
        print(final_CSVresults[row], sep="\n")
    return dino.api_main()


def api_formatMacs(content):
    import re
    global final_APIresults
    re_fmt = '[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]\.[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]\.[a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]'
    final_APIresults = []
    bad_chars = [":", "."]
    for entry in range(len(content)):
        entry = content.pop()
        if re.match(re_fmt, entry[1]):
            final_APIresults.append(entry)
        else:
            mac = entry[1]
            print("Incorrect format: " + mac)
            for i in bad_chars:
                mac = mac.replace(i, "")
            print(f"Removing seperators: {mac}")
            if len(mac) > 12:
                raise ValueError(
                    print(input("*********************************************************\n" \
                                "* Houston, we have a problem!                           *\n"
                                "* ERROR: Format error occured while parsing             *\n" \
                                "* MAC Address " + mac + "                               *\n" \
                                "*********************************************************\n")))
            else:
                new_mac = mac[:4] + "." + mac[4:8] + "." + mac[8:12]
                print(f"Reformatted: {new_mac}")
                if re.match(re_fmt, new_mac):
                    print("Format is now correct...adding to list: " + new_mac)
                    new_entry = [entry[0], new_mac, entry[2]]
                    final_APIresults.append(new_entry)
                else:
                     err = input("*********************************************************\n" \
                                 "* Houston, we have a problem!                           *\n" \
                                 "* ERROR: Unable to normalize MAC Address:               *\n" \
                                 f"* {new_mac}                                            *\n" \
                                 "* Possible Non-Hex Character. Ignoring this entry       *\n"
                                 "* Press Enter key to continue                           *\n" \
                                 "*********************************************************")
    print("*********************************************************");
    print("* Formating Complete for the below MAC Entries          *");
    print("*********************************************************");
    for row in range(len(final_APIresults)):
        print(final_APIresults[row], sep="\n")
    return final_APIresults


if __name__ == "__main__":
    """ This script is not intented to run on its own. Please import it. """
    print("This script is not intented to run on its own. Please import it.")
    quit()
