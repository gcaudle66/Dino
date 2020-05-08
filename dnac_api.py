import requests
from requests.auth import HTTPBasicAuth
import base64
import logging
requests.packages.urllib3.disable_warnings()
global debug_status
global dnac_token
global dnac_token_lifetime
global dnac_token_expired
global dnac_connArgs
global dnac_savedCreds
global dnac_inventory
global wifi_inv
global recent_urls
global json_data

dnac_token_expired = True
dnac_savedCreds = True
debug_status = False



json_data = []

## Common DNAC API URLs to call in functioons
inv_url = "/dna/intent/api/v1/network-device"

dnac_connArgs = {"cluster": "198.18.129.100",
                 "username": "admin",
                 "password": "C1sco12345"}
##dnac_connArgs = {}
## Recent URLs List for storing recent and common API Calls. List of lists with nested DICTs. [[description,{method,url}]
##recent_urls = [["Inventory", {"method": "GET", "url": "/dna/intent/api/v1/network-device"}]
##               ["Token", {"method": "POST", "url": "/dna/system/api/v1/auth/token"}]]

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
        print("*********************************************************");
        print("* Cisco DNA Center REST API Python Utility              *");
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
    print("*********************************************************");
    print("* Cisco DNA Center REST API Python Utility              *");
    print("*                                                       *");
    print("* User has confirmed connection info. Next step...      *");
    print("*                                                       *");
    print("* Script will now connect to the DNA Center API         *");
    print("* interface and retreive the Authentication Token       *");
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice2 = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
    if choice2 == 1:
        dnac_token = get_dnac_token(dnac_connArgs)
        return dnac_token, main2()
    elif choice2 == 2:
        main()

    
def main2():
    """ 
    """
    global dnac_token
    global dnac_inventory
    choice = 0
    global inv_url
    print("*********************************************************");
    print("* Cisco DNA Center REST API Python Utility              *");
    print("*                                                       *");
    print("* Script retreived Auth Token from API. Next step...    *");
    print("*                                                       *");
    print("* Script will now GET full inventory of devices in      *");
    print("* DNA Center.                                                      *");
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice = int(input("* Are you ready to proceed with this step? 1=Yes, 2=No  : "))
    if choice == 1:
        try:
            dnac_inventory = get_dnac_inventory()
        except Exception:
            print("Something went wonky and an exception got thrown")
            main2()
        else:
            return dnac_inventory, main_menu()
    elif choice == 2:
        main()

def main_menu():
    """
    """
    global wifi_inv
    choice = 0
    print("*********************************************************");
    print("* Cisco DNA Center REST API Python Utility              *");
    print("*                                                       *");
    print("* Success! Inventory was Collected from DNAC API.       *");
    print("*                                                       *");
    print("*********************************************************");
    print("* Now choose what you wanna do with the data!           *");
    print("* Intent Menu --------                                  *");
    print("*                                                       *");
    print("* [1] Wifi Inventory                                    *");
    print("* [2] Resync All Devices                                *");
    print("*                                                       *");
    print("*                                                       *");                            
    print("*                                                       *");
    print("* Control C to exit                                     *");
    print("*********************************************************");
    choice = int(input("* Intent Menu Choice [#] :  "))
    if choice == 1:
        wifi_inv = []
        try:
            wifi_inventory(wifi_inv, dnac_inventory)
        except Exception:
            print("Something went wonky and an exception got thrown")
            main_menu()
        else:
            print("*********************************************************\n" \
                  "* WiFi Inventory Collection was a Success!              *\n" \
                  f"* Total WLCs: {len(wifi_inv[0])}                       *\n" \
                  f"* Total APs: {len(wifi_inv[1])}                        *\n" \
                  "*********************************************************\n")
    elif choice == 2:
        main_menu()

        
def get_dnac_token(dnac_connArgs):
    global dnac_token
    try:
        token = requests.post(
        "https://" + dnac_connArgs["cluster"] + "/dna/system/api/v1/auth/token",
        auth=HTTPBasicAuth(
           username = dnac_connArgs["username"],
           password = dnac_connArgs["password"]
        ),
        headers={'content-type': 'application/json'},
        verify=False,
        )
    except requests.exceptions.ConnectionError:
        print("Some error occured, likely a timeout")
        main2()
    else:
        data = token.json()
        dnac_token = data["Token"]
        print("AUTH Token retrieved!")
        print(dnac_token)
        return dnac_token

def get_device_WifiInfo(dnac_token, ap_uuid):
    import json
    ap_WifiInfo_url = "/dna/intent/api/v1/network-device/" + ap_uuid + "/wireless-info"
    url = "https://" + dnac_connArgs["cluster"] + ap_WifiInfo_url
    payload = {}
    files = {}
    headers = {
        'X-Auth-Token': dnac_token
        }
    response = requests.request("GET", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    device_WifiInfo = json_data["response"]
    return device_WifiInfo

def get_dnac_inventory():
    import json
    global dnac_token
    global inv_url
    url = "https://" + dnac_connArgs["cluster"] + inv_url
    payload = {}
    files = {}
    headers = {
        'X-Auth-Token': dnac_token
        }
    response = requests.request("GET", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    try:
        dnac_inventory = json_data["response"]
    except KeyError:
        print("Received an error in response. Possible expired DNAC token.\n" \
              "DEBUG can be enabled to help further troubleshoot.\n" \
              "Current status of DEBUG being Enabled is : " + debug_status + "\n") 
    else:
        return dnac_inventory


def wifi_inventory(wifi_inv, dnac_inventory):
    wlcs = locate_wlcs(dnac_inventory)
    aps = locate_aps(dnac_inventory)
    wifi_inv.append(wlcs)
    wifi_inv.append(aps)
    return wifi_inv

def locate_aps(dnac_inventory):
    ap_count = 0
    ap_inv = {}
    temp_inv = dnac_inventory.copy()
    for item in range(len(dnac_inventory)):
        entry = temp_inv.pop()
        ap = {}
        if entry["family"] == "Unified AP":
            ap["hostname"] = entry["hostname"]
            ap["platformId"] = entry["platformId"]
            ap["mgmntIP"] = entry["managementIpAddress"]
            ap["associatedWlcIp"] = entry["associatedWlcIp"]
            ap["instanceUuid"] = entry["instanceUuid"]
            ap_uuid = entry["instanceUuid"]
            ap["ethMacAddress"] = get_ap_ethMac(ap_uuid)
            ap["location"] = entry["location"]
            ap_inv[ap.get("hostname")] = ap
            ap_count = ap_count + 1
    print(ap_inv)
    ap_found = ap_count
    print(f"Located {ap_found} Access Points\n" \
          "Registered in DNA Center                     \n")
    return ap_inv

def get_ap_ethMac(ap_uuid):
    import json
    global dnac_token
    ap_WifiInfo_url = "/dna/intent/api/v1/network-device/" + ap_uuid + "/wireless-info"
    url = "https://" + dnac_connArgs["cluster"] + ap_WifiInfo_url
    payload = {}
    files = {}
    headers = {
        'X-Auth-Token': dnac_token
        }
    response = requests.request("GET", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    device_WifiInfo = json_data["response"]
    return device_WifiInfo.get("ethMacAddress")

def locate_wlcs(dnac_inventory):
    wlc_count = 0
    temp_inv = dnac_inventory.copy()
    wlc_inv = {}
    for item in range(len(dnac_inventory)):
        entry = temp_inv.pop()
        wlc = {}
        if entry["family"] == "Wireless Controller":
            wlc["hostname"] = entry["hostname"]
            wlc["platformId"] = entry["platformId"]
            wlc["mgmntIP"] = entry["managementIpAddress"]
            wlc["location"] = entry["location"]
            wlc["instanceUuid"] = entry["instanceUuid"]
            wlc_inv[wlc.get("hostname")] = wlc
            wlc_count = wlc_count + 1
    print(wlc_inv)
    wlc_found = len(wlc_inv)
    print(f"Located {wlc_found} Wireless LAN Controllers\n" \
          "Registered in DNA Center                     \n")
    return wlc_inv

def enable_req_debug():
    global debug_status
    import logging
    import http.client as http_client
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
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    requests_urllib3_logger = requests.urllib3.add_stderr_logger(level = 1)
    debug_status = True
    return debug_status
    


if __name__ == "__main__":
    api_main()
#dnac_token = get_dnac_token(dnac_connArgs)
#dnac_inventory = get_dnac_inventory(dnac_token)
