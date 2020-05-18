import requests
from requests.auth import HTTPBasicAuth
import base64
import logging
import dino
#requests.packages.urllib3.disable_warnings()
global debug_status
global dnac_token
global dnac_token_lifetime
global dnac_token_expired
##global dnac_savedCreds
global dnac_inventory
#global wifi_inv
global recent_urls
global json_data

dnac_token_expired = True
#dnac_savedCreds = False
debug_status = False




## Common DNAC API URLs to call in functioons


        
def get_dnac_token():
    global dnac_token
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
    except requests.exceptions.ConnectionError:
        print("Some error occured, likely a timeout")
    else:
        data = token.json()
        dnac_token = data["Token"]
        print("\n" \
              "        ##                                                \n" \
              "       ##  Cha-Ching!                                     \n" \
              "      ##     We got the Token!                            \n" \
              " ##  ##                                                   \n" \
              "  ####                                                    \n" \
              "   ##                  ...API Auth-Token that is          \n" \
              "                                                            ")
##        print(dnac_token)
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
    inv_url = "/dna/intent/api/v1/network-device"
    url = "https://" + dino.dnac_connArgs["cluster"] + inv_url
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
              "* DEBUG is Enabled : " + debug_status + "               *\n" \
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
    url = "https://" + dino.dnac_connArgs["cluster"] + sync_url
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
    url = "https://" + dino.dnac_connArgs["cluster"] + ap_WifiInfo_url
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
    


##if __name__ == "__main__":
##    api_main()
#dnac_token = get_dnac_token(dnac_connArgs)
#dnac_inventory = get_dnac_inventory(dnac_token)
