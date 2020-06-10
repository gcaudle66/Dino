import requests
from requests.auth import HTTPBasicAuth
import base64
import logging
import dino
requests.packages.urllib3.disable_warnings()
global debug_status
global dnac_token
global local_dnac_connArgs
global dnac_token_lifetime
global dnac_token_expired
##global dnac_savedCreds
global dnac_inventory
#global wifi_inv
global recent_urls
global json_data

local_dnac_connArgs = {}
dnac_token_expired = True
#dnac_savedCreds = False
debug_status = False

json_data = []


## Common DNAC API URLs to call in functioons

##def get_dnac_token():
##    import dino
##    global dnac_token
##    global json_data
##    json_data = []
##    try:
##        token = requests.post(
##        "https://" + dino.dnac_connArgs["cluster"] + "/dna/system/api/v1/auth/token",
##        auth=HTTPBasicAuth(
##           username = dino.dnac_connArgs["username"],
##           password = dino.dnac_connArgs["password"]
##        ),
##        headers={'content-type': 'application/json'},
##        verify=False,
##        )
##    except requests.exceptions.ConnectionError:
##        print("Some error occured, likely a timeout")
##    else:
##        data = token.json()
##        json_data.append(data)
##        dnac_token = data["Token"]
##        print("\n" \
##              "        ##                                                \n" \
##              "       ##  Cha-Ching!                                     \n" \
##              "      ##     We got the Token!                            \n" \
##              " ##  ##                                                   \n" \
##              "  ####                                                    \n" \
##              "   ##                  ...API Auth-Token that is          \n" \
##              "                                                            ")
##        return dnac_token
        
def get_dnac_token(dnac_connArgs):
    global dnac_token
    global local_dnac_connArgs
    global json_data
    local_dnac_connArgs = dnac_connArgs.copy()
    json_data = []
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
    else:
        data = token.json()
        json_data.append(data)
        dnac_token = data["Token"]
        print("\n" \
              "        ##                                                \n" \
              "       ##  Cha-Ching!                                     \n" \
              "      ##     We got the Token!                            \n" \
              " ##  ##                                                   \n" \
              "  ####                                                    \n" \
              "   ##                  ...API Auth-Token that is          \n" \
              "                                                            ")
        return dnac_token

def get_device_WifiInfo(dnac_token, ap_uuid):
    import json
    ap_WifiInfo_url = "/dna/intent/api/v1/network-device/" + ap_uuid + "/wireless-info"
    url = "https://" + local_dnac_connArgs["cluster"] + ap_WifiInfo_url
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
    inv_url = "/dna/intent/api/v1/network-device"
    url = "https://" + local_dnac_connArgs["cluster"] + inv_url
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
        print("*********************************************************\n" \
              "* Received an error in response. Possible expired DNAC  *\n" \
              "* token. DEBUG can be enabled to troubleshoot.          *\n" \
              "* DEBUG is Enabled : " + str(debug_status) + "               *\n" \
              "*********************************************************\n") 
    else:
        return dnac_inventory


def gather_inv_devices():
    """
    Here we will grab devices from the inventory with
    a subset of the keys that are relevant for the use
    """
    import json
    temp_inv = dnac_inventory.copy()
    dnac_inv = []
    for item in range(len(dnac_inventory)):
        entry = temp_inv.pop()
        item = {}
        item["family"] = entry["family"]
        item["hostname"] = entry["hostname"]
        item["platformId"] = entry["platformId"]
        item["mgmntIP"] = entry["managementIpAddress"]
        item["location"] = entry["location"]
        item["instanceUuid"] = entry["instanceUuid"]
        dnac_inv.append(item)
    devices_found = len(dnac_inv)
    print(f"Located {devices_found} Devices Registered in DNA Center.\n")
    return dnac_inv


def put_sync_device(body):
    """
    Here we will take the dnac_inv gathered and iterate
    through it for allowing user to choose the device
    """
    import json
    sync_url = "/dna/intent/api/v1/network-device/sync?forceSync=True"
    payload = "[\n    \"" + body + "\"\n]"
    url = "https://" + local_dnac_connArgs["cluster"] + sync_url
    files = {}
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': dnac_token
        }
    response = requests.request("PUT", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    try:
        sync_response = json_data["response"]
    except KeyError:
        print("*********************************************************\n" \
              "* Received an error in response. Possible expired DNAC  *\n" \
              "* token. DEBUG can be enabled to troubleshoot.          *\n" \
              "* DEBUG is Enabled : " + debug_status + "               *\n" \
              "*********************************************************\n") 
    else:
        return sync_response




def wifi_inventory(wifi_inv, dnac_connArgs):
    wlcs = locate_wlcs(dnac_token, dnac_inventory)
    aps = locate_aps(dnac_token, dnac_inventory)
    wifi_inv.insert(0, wlcs)
    wifi_inv.insert(1, aps)
    return wifi_inv

def locate_aps(dnac_token, dnac_inventory):
    from dino import test_mode
    ap_count = 0
    ap_inv = []
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
            if test_mode == True:
                ap["ethMacAddress"] = entry["macAddress"]
            elif test_mode == False:
                ap["ethMacAddress"] = get_ap_ethMac(dnac_token, ap_uuid)
            ap["location"] = entry["location"]
            ap_inv.append(ap)
            ap_count = ap_count + 1
    print(ap_inv)
    ap_found = ap_count
    print(f"Located {ap_found} Access Points\n" \
          "Registered in DNA Center                     \n")
    return ap_inv

def get_ap_ethMac(dnac_token, ap_uuid):
    import json
##    global dnac_token
    ap_WifiInfo_url = "/dna/intent/api/v1/network-device/" + ap_uuid + "/wireless-info"
    url = "https://" + local_dnac_connArgs["cluster"] + ap_WifiInfo_url
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

def locate_wlcs(dnac_token, dnac_inventory):
    wlc_count = 0
    temp_inv = dnac_inventory.copy()
    wlc_inv = []
    for item in range(len(dnac_inventory)):
        entry = temp_inv.pop()
        wlc = {}
        if entry["family"] == "Wireless Controller":
            wlc["hostname"] = entry["hostname"]
            wlc["platformId"] = entry["platformId"]
            wlc["mgmntIP"] = entry["managementIpAddress"]
            wlc["location"] = entry["location"]
            wlc["instanceUuid"] = entry["instanceUuid"]
            wlc_inv.append(wlc)
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
    
### THESE FOLLOWING FUNCTIONS ARE USED ONLY WHEN TESTING
##  SITUATIONS ARE RECOGNIZED
def test_get_dnac_token():
    global dnac_token
    import time
    import requests
    global dnac_connArgs
    while True:
        print("\n\n\n")
        print("*********************************************************")
        print("*     TEST FUNCTION CALLED** USED ONLY WHEN TESTING     *")
        print("*        DETECTED LOOPBACK IP AND TEST API PORT         *")
        print("*********************************************************")
        print("* Dino | Cisco DNA Center REST API Connex               *");
        print("*                                                       *");
        print("* -Connection info confirmed by user.                   *");
        print("*                                                       *");
        print("* Script will now connect to the LOCAL TEST API SERVER  *");
        print("* interface and retreive the TEST Authentication Token  *");
        print("*                                                       *");
        print("*    Press [Enter] to Continue or Control-C to exit     *");
        print("*********************************************************");
        print("\n\n")
        choice = input("")
        print("*********************************************************")
        print("***TEST FUNCTION CALLED** USED ONLY WHEN TESTING        *")
        print("*********************************************************")
        try:
            token = requests.post(
            "https://" + dino.dnac_connArgs["cluster"] + "/dna/system/api/v1/auth/token",
            auth=HTTPBasicAuth(
               username = dino.dnac_connArgs["username"],
               password = dino.dnac_connArgs["password"]
            ),
            headers={'content-type': 'application/json'},
            verify=False,
            )
        except ValueError as verr:
            #logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************");
            print("* Dino | ConneX ERROR                                   *");
            print("*********************************************************");
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : Value entered is not valid,\n" \
                  " E           therefore it is invalid!  \n" \
                  " ERROR                                  \n" \
                  "Expecting Value of Type: {} | Please Try Again \n" \
                  "Error Details: {}\n\n".format(type(choice), verr))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except KeyError as kerr:
            #logging.debug("Exception occured as: " + str(verr))
            print("\n\n")
            print("*********************************************************");
            print("* Dino | ConneX ERROR                                   *");
            print("*********************************************************");
            print(f" ERROR                                  \n" \
                  " E                                      \n" \
                  " ERROR : Key Error has occured\n" \
                  " E           Unrecoverable Error!  \n" \
                  " ERROR                                  \n" \
                  "\n" \
                  "Error Details: {}\n\n".format(kerr))
            cont = input("--> Press [Enter] to Continue or Ctrl-C to quit   \n")
            continue
        except Exception as exc:
            #logging.debug("Exception occured as: " + str(exc))
            print("\n\n")
            print("*********************************************************");
            print("* Dino | ConneX ERROR                                   *");
            print("*********************************************************");
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
            print("*********************************************************");
            print("* Dino | ConneX ERROR                                   *");
            print("*********************************************************");
            print("*                                                       *");
            print("* Houston, we have a problem!                           *");
            print("* The URL/IP provided below is invalid. Please re-enter it.*");                        
            print("*********************************************************")
            print(dnac_connArgs.get("cluster"))
            time.sleep(3)
            dnac_connArgs["cluster"] = input("* DNA-C Hostname/IP : ")
            continue
        else:
            data = token.json()
            dnac_token = data[1]["Token"]
            print("\n" \
                  "        ##                                                \n" \
                  "       ##  Cha-Ching!                                     \n" \
                  "      ##     We got the TEST Token!                            \n" \
                  " ##  ##                                                   \n" \
                  "  ####                                                    \n" \
                  "   ##  TEST FUNCTION CALLED** USED ONLY WHEN TESTING      \n" \
                  "                                                            ")
            print(dnac_token)
            dino.api_main2()
            break

def test_get_dnac_inventory():
    import json
    global dnac_token
    print("*********************************************************")
    print("***TEST FUNCTION CALLED** USED ONLY WHEN TESTING        *")
    print("*********************************************************")
    inv_url = "/dna/intent/api/v1/network-device"
    url = "https://" + dino.dnac_connArgs["cluster"] + inv_url
    payload = {}
    files = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    try:
        dnac_inventory = json_data
    except KeyError:
        print("*********************************************************\n" \
              "* Received an error in response. Possible expired DNAC  *\n" \
              "* token. DEBUG can be enabled to troubleshoot.          *\n" \
              "* DEBUG is Enabled : " + debug_status + "               *\n" \
              "*********************************************************\n") 
    else:
        return dnac_inventory




### DNAC API JSON BODYs for Calls to Modify/PUT Data

dnac_AddDevice = {
    "cliTransport": "string",
    "computeDevice": "boolean",
    "enablePassword": "string",
    "extendedDiscoveryInfo": "string",
    "httpPassword": "string",
    "httpPort": "string",
    "httpSecure": "boolean",
    "httpUserName": "string",
    "ipAddress": [
        "string"
    ],
    "merakiOrgId": [
        "string"
    ],
    "netconfPort": "string",
    "password": "string",
    "serialNumber": "string",
    "snmpAuthPassphrase": "string",
    "snmpAuthProtocol": "string",
    "snmpMode": "string",
    "snmpPrivPassphrase": "string",
    "snmpPrivProtocol": "string",
    "snmpROCommunity": "string",
    "snmpRWCommunity": "string",
    "snmpRetry": "integer",
    "snmpTimeout": "integer",
    "snmpUserName": "string",
    "snmpVersion": "string",
    "type": "string",
    "updateMgmtIPaddressList": [
        {
            "existMgmtIpAddress": "string",
            "newMgmtIpAddress": "string"
        }
    ],
    "userName": "string"}

dnac_AddSite = {
    "type": "area",
    "site": {
        "area": {
            "name": "string",
            "parentName": "string"
        },
        "building": {
            "name": "string",
            "address": "string",
            "parentName": "string",
            "latitude": "number",
            "longitude": "number"
        },
        "floor": {
            "name": "string",
            "parentName": "string",
            "rfModel": "string",
            "width": "number",
            "length": "number",
            "height": "number"
        }
    }
}

    
### END TESTING FUNCTIONS SECTION

##if __name__ == "__main__":
##    api_main()
#dnac_token = get_dnac_token(dnac_connArgs)
#dnac_inventory = get_dnac_inventory(dnac_token)
