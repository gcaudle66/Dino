import dnac_api
import os
import ap_rename20
global dnac_savedCreds
global dnac_connArgs
global wifi_inv
global DEBUGstatus
global test_mode
global session_data
global apRename_run
apRename_run = False
test_mode = False
DEBUGstatus = False
dnac_savedCreds = False
##dnac_savedCreds = False
##dnac_connArgs = {"cluster": "sandboxdnac2.cisco.com",
##                 "username": "devnetuser",
##                "password": "Cisco123!"}
dnac_connArgs = {}
session_data = []
sandboxdnac2 = "sandboxdnac2.cisco.com"
# Version and Author Info
__version__ = "2.0"
__author__ = "Garrett Caudle | gcaudle66@gmail.com"

class Dino_NetUtil:
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


def dinoValueError(location):
    print("\n\n")
    print(f"|  ERROR                                  \n" \
          "|  E                                      \n" \
          "|  ERROR : Value entered is not a valid value,\n" \
          "|  E           therefore it is invalid!  \n" \
          "|  ERROR                                  \n" \
          "Expecting Value of Type: {} | Please Try Again \n" \
          "Error Details: {}\n\n".format(type(choice), verr))
    return location()


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


def test_config():
    dnac_connArgs = {"cluster": "192.168.20.26",
                 "username": "admin",
                 "password": "C1sco12345"}

def dino_main():
    """
    """
    import logging
    global DEBUGstatus
    global apRename_run
    # logging, debug level, to file {dino.log}
    logging.basicConfig(
        filename='dino.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    apRename_run = False
    choice = 0
    menu_choices = {}
    while True:
        print("*********************************************************")
        print("*                                                       *")
        print("* Dino | Manually Helping You to Automate. v{}         *".format(__version__))
        print("*        Powered by Dino -ConneX-> System               *")
        print("*                                                       *")
        print("*********************************************************")
        print("* Please indicate intent using the options below        *")
        print("* Intent Menu --------                                  *")
        print("*                                                       *")
        print("* [1] Bulk AP Rename for Multi-WLC, DNAC Managed Sites  *")
        print("* [2] Bulk AP Renamer Classic (v1.8) for Direct 1:1 WLC *")
        print("* [3] Interact with DNAC APIs via -ConneX->API Utility   *")
        print("*                                                       *")
        print(f"*                                                       *")
        print("* Control-C to exit                                     *")
        print("*********************************************************")
        try:
            choice = int(input("* Intent Menu Choice [#] :  "))
        except ValueError as verr:
            logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : Value entered is not a valid value,\n" \
                  " E           therefore it is invalid!  \n" \
                  " ERROR                                  \n" \
                  "Expecting Value of Type: {} | Please Try Again \n" \
                  "Error Details: {}\n\n".format(type(choice), verr))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except Exception as exc:
            logging.debug("Exception occured as: " + str(exc))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : An Exception was Thrown!\n" \
                  " E           (which is bad)  \n" \
                  " ERROR                                  \n" \
                  "Arguments Entered: [{}] Please Try Again \n" \
                  "Error Details: {}\n\n".format(exc.args, exc))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        else:
            print("\n\n\n")
            if choice == 1:
                dino1_main()
                break
            elif choice == 2:
                import ap_rename18 as ap18
                ap18.__name__ == "__main__"
                ap18.main()
                break
            elif choice == 3:
                api_main()
                break
            elif choice == 9:
                DEBUGstatus = debugy(True)
                if DEBUGstatus == True:
                    print("DEBUG now enabled to local file dino.log")
                    dino_main()
            else:
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                      " E                                      \n" \
                      " ERROR : Value entered is not a valid value,\n" \
                      " E           therefore it is invalid!  \n" \
                      " ERROR                                  \n" \
                      "Value Entered: [{}] Does not exist. Please Try Again \n".format(choice))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                dino_main()
                break


def dino1_main():
    """
    """
    print("\n\n\n")
    while True:
        print("*********************************************************")
        print("* Dino | AP Rename Utility                              *")
        print("*********************************************************")
        print("*                                                       *")
        print("* Import CSV - Ensure CSV file to import is placed in   *")
        print("*              current DIR and proceed.                 *")
        print("*                                                       *")
        print("*        [1] Yes | [2] No or Control-C to exit          *")
        print("*********************************************************")
        cont = False
        choice = 0
        try:
            choice = int(input("* Are you ready to proceed? : "))
        except ValueError as verr:
            #logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : Value entered is not a valid value,\n" \
                  " E           therefore it is invalid!  \n" \
                  " ERROR                                  \n" \
                  "Expecting Value of Type: {} | Please Try Again \n" \
                  "Error Details: {}\n\n".format(type(choice), verr))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except Exception as exc:
            #logging.debug("Exception occured as: " + str(exc))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : An Exception was Thrown!\n" \
                  " E           (which is bad)  \n" \
                  " ERROR                                  \n" \
                  "Arguments Entered: [{}] Please Try Again \n" \
                  "Error Details: {}\n\n".format(exc.args, exc))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        else:
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
                break
            elif choice == 2:
                dino_main()
                break
            else:
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                      " E                                      \n" \
                      " ERROR : Value entered is not a valid value,\n" \
                      " E           therefore it is invalid!  \n" \
                      " ERROR                                  \n" \
                      "Value Entered: [{}] Does not exist. Please Try Again \n".format(choice))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                dino1_main()
                break
                exit()


def dino1_connex(matches):
    """
    """
    if len(ap_rename20.matches) == 0:
        print("*********************************************************")
        print("* Dino | ConneX ERROR                                   *")
        print("*********************************************************")
        print("*                                                       *")
        print("*             Houston, we have a problem!               *")
        print("* Dino is unable to find any matches between the CSV    *")
        print("* file that was imported and the APs that were listed   *")
        print("* in the inventory pulled from DNA Center.              *")
        print("*                                                       *")
        print(f"* Could be our issue...could be yours!                  *")
        print("* Press Enter key to return to Main Menu                *")
        print("*                                                       *")
        err = input("*********************************************************")
        quit()
    split_conns = ap_rename20.connex_split()
    ## Lets do a sanity check and make sure that length split_conns == matches
    lenMatch = False
    if (ap_rename20.entries == len(ap_rename20.matches)) and (len(ap_rename20.matches) > 0):
        lenMatch = True
    else:
        print("*********************************************************")
        print("* Dino | ConneX ERROR                                   *")
        print("*********************************************************")
        print("*                                                       *")
        print("* Houston, we have a problem!                           *")
        print("* For some reason, the # of matches found               *")
        print("* between the CSV and API do not match after parsing.   *")
        print("* ERROR is unrecoverable! Quit and Relaunch program.    *")
        print(f"*    Found: {entries} vs. {len(ap_rename20.matches)}      *")
        print("* Press Enter key to quit program.                   *")
        print("*                                                       *")
        err = input("*********************************************************")
        quit()
    while lenMatch:
        print("\n\n\n")
        print("*********************************************************")
        print("* Dino | AP Rename Utility                              *")
        print("*********************************************************")
        print("* SSH ConneX - Analysis of CSV and API data             *")
        print("*********************************************************\n")
        print("*                                                       *")
        print(f"* Matches found : {ap_rename20.entries}                         ")
        print(f"* Number of WLCs to connect to : {len(split_conns)} ")
        print("*                                                       *")
        print("*********************ATTENTION***************************")
        print(" Now we will start connecting to WLCs and making magic   \n"
              " happen. The script ASSUMES the same username/password   \n"
              " combo can be used across all WLCs in this process. If   \n"
              " this is not the case, the script will fail as DINO is   \n"
              " not setup to handle item-by-item authentication. Not    \n"
              " that it cannot do it, it has the power, thats just to   \n"
              " much typing and hassle for my creator to deal with.     \n"
              " With that said...                                       \n"
              "  -If WLCs share login info, Press [Enter] to continue   \n"
              "  -If not, exit script and resolve or run script per WLC \n")
        print("*********************************************************")
        print("*                 Are you ready?? :                     *")
        cont = input("      [Enter] to continue or [Ctrl-C] to exit            ")
        print("\n\n")
        print("Hold on tight! If my calculations are correct, \n"
              "when this baby hits 88 miles per hour, \n"
              "you're gonna see some serious...\n\n")
        return dino1_connex_build(split_conns)


def dino1_connex_build(split_conns):
    """
    """
    global session_data
    global apRename_run
    connex_list = ap_rename20.create_connex_list(split_conns)
    ap_rename20.forAPI = True
    connArgs = ap_rename20.get_conn_args()
    print("\n\n")
    while True:
        try:
            conn_report = dino1_connex_handler(connArgs, connex_list)
        except Exception as exc:
            print(exc)
            continue
        else:
            print("*********************************************************")
            print("* Dino | SSH ConneX Completion Report                   *")
            print("*********************************************************")
            for item in conn_report:
                print(item)
            session_data.append
            print("\n")
            choice = input("Press [Enter] to return to API Main Menu\n"
                           "  or Ctrl-C to quit                       ")
            apRename_run = False
            api_main_menu()
            break


def dino1_connex_handler(connArgs, connex_list):
    """
    """
    temp_list = connex_list.copy()
    conn_report = []
    conn_info = []
    conn_cnt = len(connex_list)
    conn_seq = 1
    for item in range(conn_cnt):
        item = temp_list.pop()
        conn_info.clear()
        cnt = len(item)
        cmds_indx = cnt - 1
        conn_info.append(item[0])
        for sub in range(cmds_indx):
            apInfo = item[sub]
            #conn_info.append(apInfo)
        cmds = item[cmds_indx]
        conn_info.insert(2, conn_seq)
        conn_info.insert(1, cmds)
        print("Session {} : ConneX'ing to {}\n".format(conn_seq, conn_info[0]))
        conn_status = ap_rename20.api_connex(connArgs, conn_info)
        print("Session {} : ConneX Status : {}\n\n".format(conn_seq, conn_status))
        status_report = [{"Session": "{}".format(conn_seq), "Host/IP": "{}".format(conn_info[0]), "Result": "{}".format(conn_status)}]
        conn_report.append(status_report)
        conn_seq = conn_seq + 1
    conn_report_sum = "Dino ConneX Completed {} Sessions.".format(conn_cnt)
    return conn_report


def dino2_sync():
    dnac_inv = []
    dnac_inv = dnac_api.gather_inv_devices()
    choice = 0
    index = 0
    print("*********************************************************")
    print("* Dino | DNA-C Device ReSync                            *")
    print("*********************************************************")
    print("*                                                       *")
    print("* Choose a device below to trigger a resync.            *")
    print("*********************************************************\n")
    choices_nums = []
    for item in dnac_inv:
        item = ("Choice #{} : Hostname: {} | Platform: {} |\n| MgmntIP: {}".format(index, item.get("hostname"), item.get("platformId"), item.get("mgmntIP")))
        print(item)
        choices_nums.append(index)
        index = index + 1
    rtrn_choice_num = index + 1
    rtrn_item = ("Choice #{} : Return to API Main Menu ".format(rtrn_choice_num))
    print(rtrn_item)
    print("*********************************************************\n")
    choice = int(input(" Input choice number from above : "))
    dev_uuid = dnac_inv[choice].get("instanceUuid")
    if choice == rtrn_choice_num:
        api_main_menu()
    elif choice in choices_nums:
        while True:
            try:
                sync_response = dnac_api.put_sync_device(dev_uuid)
            except Exception as exc:
                #logging.debug("Exception occured as: " + str(exc))
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                      " E                                      \n" \
                      " ERROR : An Exception was Thrown!\n" \
                      " E           (which is bad)  \n" \
                      " ERROR                                  \n" \
                      "Arguments Entered: [{}] Please Try Again \n" \
                      "Error Details: {}\n\n".format(exc.args, exc))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                continue
            else:
                print("*********************************************************")
                print("* Dino | DNA-C Device ReSync                            *")
                print("*********************************************************")
                print("*                                                       *")
                print("* Device resync was successfully triggered.             *")
                print("*********************************************************\n")
                print(sync_response)
                prompt = input("[Enter] to Return to API Main Menu or [Ctrl-C] to exit\n\n")
                api_main_menu()
    elif choice not in choices_nums:
        print("*********************************************************")
        print("* Dino | ConneX ERROR                                   *")
        print("*********************************************************")
        print("*                                                       *")
        print("* Hmmm...that choice dont't make no sense??!!           *")
        print("* It appears you have entered an invalid choice Number. *")
        print("* Lets drop back and try again.                         *")
        print("*********************************************************")
        cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
        api_main_menu()
    else:
        print("*********************************************************")
        print("* Dino | ConneX ERROR                                   *")
        print("*********************************************************")
        print("*                                                       *")
        print("* Houston, we have a problem!                           *")
        print("* Whatever you just entered, made no sense to us!       *")
        print("* Please try again                                      *")
        print("*********************************************************")
        cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
        api_main_menu()



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
    import getpass
    import time
    global dnac_savedCreds
    global dnac_connArgs
    global test_mode
    while dnac_savedCreds == False:
        print("\n\n\n")
        print("*********************************************************")
        print("* Dino | Cisco DNA Center REST API Connex               *")
        print("*                                                       *")
        print("* Please provide the following data in order to connect *")
        print("*                                                       *")
        print("*********************************************************")
        print("\n")
        dnac_connArgs = {"cluster": input("* DNA-C Hostname/IP : "),
                        "username": input("* Username : "),
                        "password": getpass.win_getpass("* Password : ")}
        print("\n\n")
        while True:
            print("*********************************************************")
            print("*                                                       *")
            print("*  DNA-C Hostname/IP: " + dnac_connArgs["cluster"])
            print("*  Username: " + dnac_connArgs["username"])
            print("*                                                       *")
            print("*        [1] Yes | [2] No or Control-C to exit          *")
            print("*********************************************************")
            choice = 0
            try:
                choice = int(input(" Is the above connection info correct? : "))
            except ValueError as verr:
                #logging.debug("Exception occured as: " + str(verr))
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                      " E                                      \n" \
                      " ERROR : Value entered is not valid,\n" \
                      " E           therefore it is invalid!  \n" \
                      " ERROR                                  \n" \
                      "Expecting Value of Type: {} | Please Try Again \n" \
                      "Error Details: {}\n\n".format(type(choice), verr))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                continue
            except Exception as exc:
                #logging.debug("Exception occured as: " + str(exc))
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                      " E                                      \n" \
                      " ERROR : An Exception was Thrown!\n" \
                      " E           (which is bad)  \n" \
                      " ERROR                                  \n" \
                      "Arguments Entered: [{}] Please Try Again \n" \
                      "Error Details: {}\n\n".format(exc.args, exc))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                continue
            else:
                if choice == 1:
                    dnac_savedCreds = True
                    dnac_connArgs
                    if dnac_connArgs["cluster"] == "127.0.0.1:5000":
                        test_mode = True
                        while True:
                            try:
                                dnac_token = dnac_api.test_get_dnac_token()
                            except KeyError as kerr:
                                print(kerr)
                                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                                pass
                            else:
                                break
                    else:
                        api_getToken()
                        break
                elif choice == 2:
                    dnac_connArgs = {}
                    api_main()
                    break
                else:
                    print("\n\n")
                    print("*********************************************************")
                    print("* Dino | ConneX ERROR                                   *")
                    print("*********************************************************")
                    print(f" ERROR                                  \n" \
                              " E                                      \n" \
                              " ERROR : Value entered is not a valid option,\n" \
                              " E           therefore it is invalid!  \n" \
                              " ERROR                                  \n" \
                              "Value Entered: [{}] Does not exist. Please Try Again \n".format(choice))
                    cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                    continue
        else:
            if choice == 1:
                correct = True
                dnac_savedCreds = True
                dnac_connArgs
                if dnac_connArgs["cluster"] == "127.0.0.1:5000":
                    test_mode = True
                    while True:
                        try:
                            dnac_token = dnac_api.test_get_dnac_token()
                        except KeyError as kerr:
                            print(kerr)
                        else:
                            break
                else:
                    api_getToken()
            elif choice == 2:
                dnac_connArgs = {}
                api_main()
                break

def api_getToken():
    import time
    import requests
    global dnac_connArgs
    print("\n\n\n")
    while True:
        print("*********************************************************")
        print("* Dino | Cisco DNA Center REST API Connex               *")
        print("*                                                       *")
        print("* -Connection info confirmed by user.                   *")
        print("*                                                       *")
        print("* Script will now connect to the DNA Center API         *")
        print("* interface and retreive the Authentication Token       *")
        print("*                                                       *")
        print("*    Press [Enter] to Continue or Control-C to exit     *")
        print("*********************************************************")
        print("\n\n")
        choice = input("")
        try:
            dnac_token = dnac_api.get_dnac_token(dnac_connArgs)
        except ValueError as verr:
            #logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : Value entered is not valid,\n" \
                  " E           therefore it is invalid!  \n" \
                  " ERROR                                  \n" \
                  "Expecting Value of Type: {} | Please Try Again \n" \
                  "Error Details: {}\n\n".format(type(choice), verr))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except Exception as exc:
            #logging.debug("Exception occured as: " + str(exc))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : An Exception was Thrown!\n" \
                  " E           (which is bad)  \n" \
                  " ERROR                                  \n" \
                  "Arguments Entered: [{}] Please Try Again \n" \
                  "Error Details: {}\n\n".format(exc.args, exc))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except requests.exceptions.InvalidURL:
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print("*                                                       *")
            print("* Houston, we have a problem!                           *")
            print("* The URL/IP provided below is invalid. Please re-enter it.*")
            print("*********************************************************")
            print(dnac_connArgs.get("cluster"))
            time.sleep(3)
            dnac_connArgs["cluster"] = input("* DNA-C Hostname/IP : ")
            continue
        else:
            api_main2()
            break


def api_main2():
    """ 
    """
    global test_mode
    choice = 0
    print("\n\n\n")
    print("*********************************************************")
    print("* Dino | Cisco DNA Center REST API Connex               *")
    print("*                                                       *")
    print("* -Success! Script retreived Auth Token from DNAC.      *")
    print("*                                                       *")
    print("* Script will now GET full inventory of devices in      *")
    print("* DNA Center.                                           *")
    print("*                                                       *")
    print("*         [1] Yes | [2] No or Control-C to exit         *")
    print("*********************************************************")
    print("\n\n")
    choice = int(input("* Are you ready to proceed with this step? : "))
    if choice == 1:
        if test_mode == True:
            try:
                print("*********************************************************")
                print("***TEST FUNCTION CALLED** USED ONLY WHEN TESTING        *")
                print("*********************************************************")
                dnac_api.dnac_inventory = dnac_api.test_get_dnac_inventory()
            except Exception as exc:
                print("*********************************************************")
                print("* ERROR IN TEST FUNCTION CALLED** USED ONLY WHEN TESTING*")
                print("*********************************************************")
                print("Something is very bad! Error is :  ")
                print(exc)
            else:
                return api_main_menu()
        elif test_mode == False:
            try:
                dnac_api.dnac_inventory = dnac_api.get_dnac_inventory()
            except Exception:
                print("Something went wonky and an exception got thrown")
                api_main2()
            else:
                print("\n\n")
                print(" -Success! Inventory collected from DNAC. \n" \
                      "  Inventory Item Count: {} \n".format(len(dnac_api.dnac_inventory)))
                return api_main_menu()
    elif choice == 2:
        api_main()


def api_main_menu():
    """
    """
    import json
    from dnac_api import iterate_dnac_inventory
    global test_mode
    global apRename_run
    site_list = dnac_api.dnac_site_list
    menu_apRename = "[0] AP Rename - DNAC->CSV Comparison & Finalize"
    if apRename_run == True:
        label0 = menu_apRename
    else:
        label0 = ""
    choice = 0
    menu_choices = {
        "1": "AP Rename Cont'd - DNAC->CSV Comparison & Finalize", "2": "Resync Device - Force Inventory Resync on Device"}
    while True:
        print("\n\n\n")
        print("*********************************************************")
        print("*                                                       *")
        print("* Dino | -ConneX-> DNA Center API Main Menu             *")
        print("*                                                       *")
        print("*                                                       *")
        print("*********************************************************")
        print("* Interact with APIs via Options Below                   ")
        print("* Intent Menu --------                                  ")
        print("  {}                                                    ".format(label0))
        print("  [1] Browse Collected DNA Center Inventory             ")
        print("  [2] Resync Device - Force Inventory Resync on Device  ")
        print("  [3] Download All Configs from Inventory Locally        ")
        #print("  [4] Add Device Manually                               ")
        #print("  [5] Start a Discovery                                 ")
        print("  [6] Add Site Hierachy                                 ")
        print("  [9] Return to Main Menu                               ")
        print("*********************************************************")
        try:
            choice = int(input("* Intent Menu Choice [#] :  "))
        except ValueError as verr:
            #logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                        \n" \
                  " E                                             \n" \
                  " ERROR : Value entered is not valid,           \n" \
                  " E           therefore it is invalid!          \n" \
                  " ERROR       Give us a number please!          \n" \
                  "Expecting Value of Type: {} | Please Try Again \n" \
                  "Error Details: {}\n\n".format(type(choice), verr))
            cont = input("--> Press [Enter] to Try Again or Ctrl-C to quit   \n")
            continue
        except Exception as exc:
            #logging.debug("Exception occured as: " + str(exc))
            print("\n\n")
            print("*********************************************************")
            print("* Dino | ConneX ERROR                                   *")
            print("*********************************************************")
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : An Exception was Thrown!\n" \
                  " E           (which is bad)  \n" \
                  " ERROR                                  \n" \
                  "Arguments Entered: [{}] Please Try Again \n" \
                  "Error Details: {}\n\n".format(exc.args, exc))
            cont = input("--> Press [Enter] to Try Again or Ctrl-C to quit   \n")
            continue
        else:
            print("\n\n")
            if choice == 0:
                wifi_inv = []
                try:
                    wifi_inv = dnac_api.wifi_inventory(wifi_inv, dnac_connArgs)
                except Exception as exc:
                    print("\n")
                    print("*********************************************************")
                    print("* Dino | Cisco DNA Center REST API Connex               *")
                    print("*********************************************************")
                    print("*                                                       *")
                    print("* Something went wonky and an exception got thrown      *")
                    print("*                                                       *")
                    print("*   Press Enter key to restart program or               *")
                    print("*     Control-C to exit                                 *")
                    print("*********************************************************")
                    print(exc)
                    err = input("*********************************************************")
                    continue
                else:
                    print("\n\n\n")
                    print("*********************************************************\n"
                          "* WiFi Inventory Collection was a Success!              *\n"
                          f"* Total WLCs: [{len(wifi_inv[0])}]                      \n"
                          f"* Total APs: [{len(wifi_inv[1])}]                       \n"
                          "*********************************************************\n")
                    if len(wifi_inv[1]) == 0:
                            print("\n\n\n")
                            print("*********************************************************")
                            print("* Dino | Cisco DNA Center REST API Connex               *")
                            print("*********************************************************")
                            print("*                                                       *")
                            print("*            Houston, we have a problem!                *")
                            print("* No APs we were found in the inventory that Dino       *")
                            print("* pulled from DNA Center. Printing all device \"family\"  *")
                            print("* and \"platformIds\" in the DNAC inventory below.       *")
                            print("* If any APs are in fact in the inventory, capture this *")
                            print("* output and send to dev-team advising them it no worky!*")
                            print("*                                                       *")
                            print("* Dino will now quit to flush any data just in case.    *")
                            print("* Press [Enter] to quit then relaunch Dino.             *")
                            print("*********************************************************")
                            for item in dnac_api.dnac_inventory:
                                print(item.get("family"))
                                print(item.get("platformId"))
                                print("---------------------")
                            err = input("*********************************************************")
                            quit()
                    parsedAPI = ap_rename20.parseAPI(wifi_inv)
                    matches = ap_rename20.api_compare(ap_rename20.final_APIresults)
                    break
                    return dino1_connex(ap_rename20.matches)
            elif choice == 1:
                done = dnac_api.iterate_dnac_inventory()
                api_main_menu()
                break
            elif choice == 2:
                dino2_sync()
                break
            elif choice == 3:
                dnac_inventory = dnac_api.dnac_inventory
                devCnt = len(dnac_inventory)
                print("*********************************************************")
                print("* Dino | ConneX                                         *")
                print("*********************************************************")
                print("Be advised. There are a total of : {} " \
                      "Devices in DNAC inventory you have requested to dump.   \n" \
                      "This could take a considerable amount of time and might \n" \
                      "Fail if devices are not configured correct.             \n" \
                      "Shall we proceed or return to API Main Menu?            ".format(devCnt))
                print("*********************************************************")
                choice = int(input(" [1] Proceed | [2] Return or Control-C to exit : "))
                if choice == 1:
                    results = dnac_api.config_dump(dnac_inventory)
                elif choice == 2:
                    api_main_menu()
                else:
                    print("\n\n")
                    print("*********************************************************")
                    print("* Dino | ConneX ERROR                                   *")
                    print("*********************************************************")
                    print(f" ERROR                                  \n" \
                              " E                                      \n" \
                              " ERROR : Value entered is not a valid option,\n" \
                              " E           therefore it is invalid!  \n" \
                              " ERROR                                  \n" \
                              "Value Entered: [{}] Does not exist. Please Try Again \n".format(choice))
                    cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                    continue
                print(results)
                return api_main_menu()
            elif choice == 4:
                result = add_device()
                print(result)
                cont = input("------- Press [Enter] to return to API Main Menu --------")
                break
            elif choice == 6:
                result = dnac_api.add_site()
                break
            elif choice == 9:
                dino_main()
                break
            else:
                print("\n\n")
                print("*********************************************************")
                print("* Dino | ConneX ERROR                                   *")
                print("*********************************************************")
                print(f" ERROR                                  \n" \
                          " E                                      \n" \
                          " ERROR : Value entered is not a valid option,\n" \
                          " E           therefore it is invalid!  \n" \
                          " ERROR                                  \n" \
                          "Value Entered: [{}] Does not exist. Please Try Again \n".format(choice))
                cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
                continue
##    return wifi_inv


def main3():
    """ Validate that we have imported CSV and CLI    \n""" \
    """ data and do comparison between them based     \n""" \
    """ on MAC addresses. Create commands for         \n""" \
    """ changing names via SSH/CLi on WLC and adding  \n""" \
    """ them to a list. Then present matches to       \n""" \
    """ user and await confirmation b4 sending to WLC   """ 
    print("-------------------------------------------\n"
          "Now we will compare CSV to CLI for MAC Address\n"
          " matches and validate it appears correct as expected.\n"
          "-------------------------------------------\n")
    global final_CSVresults
    global final_CLIresults
    global conn
    ap_rename20.compare(ap_rename20.final_CSVresults, ap_rename20.final_CLIresults)
    ap_rename20.matches_len = len(ap_rename20.matches)
    if ap_rename20.matches_len > 0:
          print("-------------------------------------------\n"
                "Listed below are the matches found between \n"
                "CSV and CLI. Listed as ...                 \n"
                " [matched MAC, {Old AP Name, New AP Name}] \n"
                "-------------------------------------------\n")
          for entry in range(len(ap_rename20.matches)):
            print(ap_rename20.matches[entry], sep=",")
    else:
        print("No matches were found between the CSV \n"
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

class dinoLog:
    def __init__(self, state):
        self.state = status
    def state(status):
        if self.status == True:
            self.__enter__()
        elif self.status == False:
            self.__exit__()
    
    def __enter__():
        import logging
        DEBUGstatus = self.status
        if DEBUGstatus == True:
            logger = logging.basicConfig(filename='dino.log', filemode='w', level=logging.DEBUG)
            import logging
            logging.Logger("log3", level=0)
            logging.error("Fatal__", exc_info=True)
            return self.logger
    def __exit__():
        self.logger.NOTSET()


def debugy(state):
    import logging
    import requests
    global DEBUGstatus
    import logging
    import http.client as http_client
    if state == True:
        DEBUGstatus = True
        http_client.HTTPConnection.debuglevel = 1
        httpclient_logger = logging.getLogger("http.client")
        def httpclient_logging_patch(level=logging.DEBUG):
            """Enable HTTPConnection debug logging to the logging framework"""

            def httpclient_log(*args):
                httpclient_logger.log(level, " ".join(args))

                # mask the print() built-in in the http.client module to use
                # logging instead
                http.client.print = httpclient_log
                # enable debugging
                http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig(filename='dino.log', filemode='w', level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        requests_urllib3_logger = requests.urllib3.add_stderr_logger(level = 1)
        logging.Logger("dinoLog", level=0)
        logging.error("Fatal__error__", exc_info=True)
        logging.exception("Exception_thrown__", exc_info=True)
        return DEBUGstatus


if __name__ == "__main__":
    dino_main()
