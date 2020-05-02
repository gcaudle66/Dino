import requests
from requests.auth import HTTPBasicAuth
import base64
requests.packages.urllib3.disable_warnings()
global dnac_token 
global dnac_connArgs
global dnav_inventory
global wlc_inv
wlc_inv = []
url = "https://198.18.129.100/dna/intent/api/v1/network-device"
dnac_connArgs = {"cluster": "198.18.129.100",
                 "username": "admin",
                 "password": "C1sco12345"}




def get_dnac_token(dnac_connArgs):
    global dnac_token
    global dnav_inventory
    token = requests.post(
       "https://" + dnac_connArgs["cluster"] + "/dna/system/api/v1/auth/token",
       auth=HTTPBasicAuth(
           username = dnac_connArgs["username"],
           password = dnac_connArgs["password"]
       ),
      headers={'content-type': 'application/json'},
      verify=False,
    )
    data = token.json()
    dnac_token = data["Token"]
    return dnac_token


def get_dnac_inventory(dnac_token):
    import json
    payload = {}
    files = {}
    headers = {
        'X-Auth-Token': dnac_token
        }
    response = requests.request("GET", url, headers=headers, data = payload, files = files, verify=False)
    data = response.text.encode('utf8')
    json_data = json.loads(data)
    dnac_inventory = json_data["response"]
    return dnac_inventory

def locate_wlcs(dnac_inventory):
    global wlc_inv
    temp_inv = dnac_inventory.copy()
    for item in range(len(dnac_inventory)):
        entry = temp_inv.pop()
        wlc = {}
        if entry["family"] == "Wireless Controller":
            wlc["hostname"] = entry["hostname"]
            wlc["mgmntIP"] = entry["managementIpAddress"]
            wlc_inv.append(wlc)
    wlc_found = len(wlc_inv)
    print(f"Located {wlc_found} Wireless LAN Controllers\n" \
          "Registered in DNA Center                     \n")
    return wlc


##def get_token():
##    token = requests.post(
##       "https://" + dnac_cluster + "/dna/system/api/v1/auth/token",
##       auth=HTTPBasicAuth(
##           username=username,
##           password=password
##       ),
##      headers={'content-type': 'application/json'},
##      verify=False,
##    )
##    data = token.json()
##    dnac_token = data["Token"]
##    return dnac_token

dnac_token = get_dnac_token(dnac_connArgs)
dnac_inventory = get_dnac_inventory(dnac_token)
