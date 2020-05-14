import dnac_api
import os
import ap_rename20
global dnac_savedCreds
global dnac_connArgs
global wifi_inv

##dnac_savedCreds = True
dnac_savedCreds = False
##dnac_connArgs = {"cluster": "198.18.129.100",
##                 "username": "admin",
##                "password": "C1sco12345"}
dnac_connArgs = {}

# Version and Author Info
__version__ = "2.0"
__author__ = "Garrett Caudle | gcaudle66@gmail.com"

class Ap_Rename:
    """ This is the AP Rename app (aka AP Renamerer)
    This app is used to bulk rename Access points
    In Cisco 9800 IOS-XE platform wireless LAN
    Controllers. This app is not maintained nor
    Endorsed in any way by Cisco Systems Inc.
    Use of this App is at the users own risk
    """
    def __init__(self, version, author):
        self.version = __version__
        self.author = __author__

class ConnexList(object):
	def __init__(self, match_list):
		self.connexList = match_list
		self.connexArgs = {}
		self.sendCmds = []
	def __enter__(self):
		self.connexList = match_list.copy()
		self.ConnexArgs = self.setConnArgs(self)
		return self.connexList, ConnexArgs
	def setConnArgs(self):
		import getpass
		self.connexArgs = {"ip": self.connexList[0]}
		return self.connexArgs
	def getConnArgs(self):
		self.getConnArgs = print(self.connexArgs)
	def getCmds(self):
		self.sendCmds = ap_rename20.api_create_commands(connexList)
		return self.sendCmds
	def __exit__(self):
		self.connexList.clear()


def config():
    dnac_connArgs = {"cluster": "198.18.129.100",
                 "username": "admin",
                 "password": "C1sco12345"}

def dino_main():
    """
    """
    choice = 0
    print("*********************************************************");
    print("*                                                       *");
    print("* Dino | Network Utility Application                    *");
    print("*                                                       *");
    print("*                                                       *");
    print("*********************************************************");
    print("* Please indicate intent using the options below        *");
    print("* Intent Menu --------                                  *");
    print("*                                                       *");
    print("* [1] AP Rename Utility (DNAC API + SSH to Multi-WLC)   *");
    print("* [2] AP Rename Utility (SSH to Single WLC)             *");
    print("*                                                       *");
    print("*                                                       *");                            
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice = int(input("* Intent Menu Choice [#] :  "))
    if choice == 1:
        dino1_main()
    elif choice == 2:
        dino_main()

def dino1_main():
    """
    """
    print("\n\n\n")
    print("*********************************************************");
    print("* Dino | AP Rename Utility                              *");
    print("*********************************************************");
    print("*                                                       *");
    print("* Import CSV - Ensure CSV file to import is placed in   *");
    print("*              current DIR and proceed.                 *");
    print("*                                                       *");
    print("*                  [1] Yes | [2] No                     *");
    print("*********************************************************");
    cont = False
    choice = 0
    choice = int(input("* Are you ready to proceed? : "))
    if choice == 1:
        cont = True
        cwd = os.getcwd()
        with os.scandir(path=cwd) as it:
            file_list = []
            for entry in it:
                if entry.name.endswith(".csv") and entry.is_file():
                    file_list.append(entry.name)
            file_len = len(file_list)
            ap_rename20.importCSV(file_list)
    elif choice == 2:
        exit()


def dino1_connex(matches):
    """
    """
    split_conns = ap_rename20.connex_split()
    ## Lets do a sanity check and make sure that length split_conns == matches
    lenMatch = False
    if ap_rename20.entries == len(ap_rename20.matches):
        lenMatch = True
    else:
        print("*********************************************************");
        print("* Dino | ConneX ERROR                                   *");
        print("*********************************************************");
        print("*                                                       *");
        print("* Houston, we have a problem!                           *");
        print("* For some unknown reason, the # of matches found       *");
        print("* between the CSV and API do not match after parsing.   *");
        print("* ERROR is unrecoverable! Please report to Dev team.    *");
        print(f"*    Found: {entries} vs. {len(ap_rename20.matches)}      *");
        print("* Press Enter key to restart program.                   *");
        print("*                                                       *");
        err = input("*********************************************************")
        quit()
    while lenMatch:
        print("\n\n\n")
        print("*********************************************************");
        print("* Dino | AP Rename Utility                              *");
        print("*********************************************************");
        print("*                                                       *");
        print("* SSH ConneX - Analysis of CSV and API data             *");
        print("*********************************************************\n");
        print(f"Matches found : {ap_rename20.entries}                         ")
        print(f"Number of WLCs to connect to : {len(split_conns)} ")
        print("*********************ATTENTION***************************");
        print("Now we will start connecting to WLCs and making magic \n" \
              "happen. The script ASSUMES the same username/password \n" \
              "combo can be used across all WLCs in this process. If \n" \
              "this is not the case, the script will fail as DINO is \n" \
              "not setup to handle item-by-item authentication. Not \n" \
              "that it cannot do it, it has the power, thats just to\n" \
              "much typing and hassle for my creator to deal with. \n" \
              "That said...\n" \
              "-If WLCs share login info, Press [Enter] to continue\n" \
              "-If not, exit script and resolve or run script per WLC\n")
        print("*********************************************************");
        cont = input("Shall we? : [Enter] to continue or [Ctrl-C] to exit")
        print("And away we go...")
        connex_list = ap_rename20.create_connex_list(split_conns)
        ap_rename20.forAPI = True
        connArgs = ap_rename20.get_conn_args()
        temp_connex = connex_list.copy()
        for entry in temp_connex:
            length = len(entry)
            cmds = length - 1
            conn = ap_rename20.api_connect(entry)
            if ap_rename20.connIsAlive:
                ap_rename20.send_renameCmds(entry[cmds])




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
##            ap_rename20.importCSV(file_list)
##    elif choice == 2:
##        exit()

def api_main():
    """ Where the magic begins
    Here we begin the process of gathering wireless LAN
    controllers from DNA center in order to locate the
    APs that need to be renamed as requested by the "ap_rename"
    module. This program will...
        --Gather needed info for connection to DNAC (IP, user/pass)
        --Use requests module to make an API POST call to aquire
          AUTH-Token needed to proceed with subsequent calls.
        --If suxcessful acquiring token, program will make API
          call to DNAC and gather entire inventory of "Managed"
          devices, create a local list to hold that inventory and add
          it to it
        --Program will then iterate through this inventory list looking
          for devices with the "Family" value of Wireless Controller
        --If match is found, matches are added to a llocal DICT containing
          the WLC "hostname" and "mgmntIPAddress"
    """
    global dnac_savedCreds
    global dnac_connArgs
    while dnac_savedCreds == False:
        print("\n\n\n")
        print("*********************************************************");
        print("* Dino | Cisco DNA Center REST API Connex               *");
        print("*                                                       *");
        print("* Please provide the following data in order to connect *");
        print("*                                                       *");
        print("* DNAC API IP: Cluster IP address for target DNA Center *");
        print("* Username: [username]                                  *");
        print("* Password: [password]                                  *");
        print("*                                                       *");
        print("*                                                       *");
        print("* Control C to exit                                     *");
        print("*********************************************************");
        dnac_connArgs = {
            "cluster": input("DNAC API IP: "),
            "username": input("Username:"),
            "password": input("Password: ")}
        correct = False
        print("DNAC API IP: " + dnac_connArgs["cluster"] + " | Username: " + dnac_connArgs["username"])
        choice = 0
        choice = int(input("Is the above connection info correct? 1=Yes, 2=No  : "))
        while correct == False:
            if choice == 1:
                correct = True
                dnac_savedCreds = True
                dnac_connArgs
            elif choice == 2:
                main()
                break
    choice2 = 0
    print("\n\n\n")
    print("*********************************************************");
    print("* Dino | Cisco DNA Center REST API Connex               *");
    print("*                                                       *");
    print("* -Success! Connection info confirmed.                  *");
    print("*                                                       *");
    print("* Script will now connect to the DNA Center API         *");
    print("* interface and retreive the Authentication Token       *");
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice2 = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
    if choice2 == 1:
        dnac_token = dnac_api.get_dnac_token()
        return api_main2()
    elif choice2 == 2:
        api_main()


def api_main2():
    """ 
    """
    choice = 0
    print("\n\n\n")
    print("*********************************************************");
    print("* Dino | Cisco DNA Center REST API Connex               *");
    print("*                                                       *");
    print("* -Success! Script retreived Auth Token from DNAC.      *");
    print("*                                                       *");
    print("* Script will now GET full inventory of devices in      *");
    print("* DNA Center.                                           *");
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
    if choice == 1:
        try:
            dnac_api.dnac_inventory = dnac_api.get_dnac_inventory()
        except Exception:
            print("Something went wonky and an exception got thrown")
            api_main2()
        else:
            return api_main_menu()
    elif choice == 2:
        api_main()


def api_main_menu():
    """
    """
    choice = 0
    print("\n\n\n")
    print("*********************************************************");
    print("* Dino | Cisco DNA Center REST API Connex               *");
    print("*                                                       *");
    print("* -Success! Inventory collected from DNAC.              *");
    print("*                                                       *");
    print("*********************************************************");
    print("* Choose next step to continue.          *");
    print("* Intent Menu --------                                  *");
    print("*                                                       *");
    print("* [1] AP Rename - Process DNAC inventory for comparison *");
    print("* [2] DNAC API - Force Inventory Resync All Devices     *");
    print("*                                                       *");
    print("*                                                       *");                            
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice = int(input("* Intent Menu Choice [#] :  "))
    if choice == 1:
        wifi_inv = []
        try:
            wifi_inv = dnac_api.wifi_inventory(wifi_inv, dnac_connArgs)
        except Exception:
            print("Something went wonky and an exception got thrown")
            api_main_menu()
        else:
            print("\n\n\n")
            print("*********************************************************\n" \
                  "* WiFi Inventory Collection was a Success!              *\n" \
                  f"* Total WLCs: {len(wifi_inv[0])}                                    *\n" \
                  f"* Total APs: {len(wifi_inv[1])}                                     *\n" \
                  "*********************************************************\n")
            if len(wifi_inv[1]) == 0:
                    print("\n\n\n")
                    print("*********************************************************");
                    print("* Dino | Cisco DNA Center REST API Connex               *");
                    print("*********************************************************");
                    print("*                                                       *");
                    print("* Houston, we have a problem!                           *");
                    print("* No APs we were found when DNAC was polled.            *");
                    print("*                                                       *");
                    print("* Press Enter key to restart program.                   *");
                    print("*                                                       *");
                    print("* Control C to exit                                     *");
                    print("*********************************************************");
                    err = input("*********************************************************")
                    dino_main()
            parsedAPI = ap_rename20.parseAPI(wifi_inv)
            matches = ap_rename20.api_compare(ap_rename20.final_APIresults)
            return dino1_connex(ap_rename20.matches)
    elif choice == 2:
        dino_main()
    return wifi_inv


def main3():
    """ Validate that we have imported CSV and CLI    \n""" \
    """ data and do comparison between them based     \n""" \
    """ on MAC addresses. Create commands for         \n""" \
    """ changing names via SSH/CLi on WLC and adding  \n""" \
    """ them to a list. Then present matches to       \n""" \
    """ user and await confirmation b4 sending to WLC   """ 
    print("-------------------------------------------\n" \
          "Now we will compare CSV to CLI for MAC Address\n" \
          " matches and validate it appears correct as expected.\n" \
          "-------------------------------------------\n")
    global final_CSVresults
    global final_CLIresults
    global conn
    ap_rename20.compare(ap_rename20.final_CSVresults, ap_rename20.final_CLIresults)
    ap_rename20.matches_len = len(ap_rename20.matches)
    if ap_rename20.matches_len > 0:
          print("-------------------------------------------\n" \
                "Listed below are the matches found between \n" \
                "CSV and CLI. Listed as ...                 \n" \
                " [matched MAC, {Old AP Name, New AP Name}] \n" \
                "-------------------------------------------\n")
          for entry in range(len(ap_rename20.matches)):
            print(ap_rename20.matches[entry], sep=",")
    else:
        print("No matches were found between the CSV \n" \
              "and CLI results.                      \n")
    choice = int(input("Does this info look correct? 1=Yes | 2=No or Ctrl-C to exit : "))
    if choice == 1:
        ap_rename20.create_commands(ap_rename20.matches)
    elif choice == 2:
        savedCredentials = False
        print(f"Disconnecting Current SSH Session...") 
        conn.disconnect()
        connIsAlive = conn.is_alive()
        main()



if __name__ == "__main__":
    dino_main()
