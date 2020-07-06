import requests
from requests.auth import HTTPBasicAuth
import base64
import logging
import dino
import time
import json
requests.packages.urllib3.disable_warnings()
global debug_status
global dnac_token
global local_dnac_connArgs
global dnac_token_lifetime
global dnac_token_expired
global dnac_site_list
global dnac_inventory
#global wifi_inv
global recent_urls
global json_data
global DNAC_URL

local_dnac_connArgs = {}
DNAC_URL = ""
dnac_token_expired = True
debug_status = False
dnac_site_list = {}
json_data = []


## Common DNAC API URLs to call in functioons
##class APICall:
##    def __init__(self, name, base_url, api_path, method) 

def get_dnac_token(dnac_connArgs):
    global dnac_token
    global local_dnac_connArgs
    global DNAC_URL
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
    except requests.exceptions.ConnectionError as exc:
        print("*********************************************************");
        print("* Dino | Cisco DNA Center REST API Connex               *");
        print("*********************************************************");
        print("*                                                       *");
        print("* Big E...little e, what begins with E??                *");
        print("* ERROR! Received the below error when attempting the   *");
        print("* connection to DNA Center. Dropping back to resolve... *");
        print("*********************************************************");
        print(exc)
        dino.dnac_savedCreds = False
        cont = input("Press [Enter] to try again or Ctrl-C to quit")
        dino.api_main()
    else:
        DNAC_URL = "https://" + local_dnac_connArgs["cluster"]
        response_code = token.status_code
        print(f"Status Code: {token.status_code}")
        if response_code == 200:
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
        elif response_code == 401:
            print("*********************************************************");
            print("* Dino | Cisco DNA Center REST API Connex               *");
            print("*********************************************************");
            print("*                                                       *");
            print("* Big E...little e, what begins with E?? ERROR!         *");
            print("* Received 401 Unauthorized when attempting the         *");
            print("* connection to DNA Center. Dropping back to resolve... *");
            print("*********************************************************");
            print("\n")
            dino.dnac_savedCreds = False
            cont = input("Press [Enter] to try again or Ctrl-C to quit")
            dino.api_main()
        else:
            print("Failed to retreive token.")
            return response_code




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
    response_code = response.status_code
    print(f"Status Code: {response.status_code}")
    if response_code == 200:
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
    elif response_code == 401:
        print("*********************************************************");
        print("* Dino | Cisco DNA Center REST API Connex               *");
        print("*********************************************************");
        print("*                                                       *");
        print("* Big E...little e, what begins with E?? ERROR!         *");
        print("* Received 401 Unauthorized when attempting the         *");
        print("* connection to DNA Center. Dropping back to resolve... *");
        print("*********************************************************");
        print("\n")
        dino.dnac_savedCreds = False
        cont = input("Press [Enter] to try again or Ctrl-C to quit")
        dino.api_main()
    else:
        print("*********************************************************");
        print("* Dino | Cisco DNA Center REST API Connex               *");
        print("*********************************************************");
        print("*                                                       *");
        print("*            Houston, we have a problem!                *");
        print("* Dino failed to retreive the inventory as expected     *");
        print("* from DNA Center. Response details below.              *");
        print("*********************************************************");
        print("\n")
        dino.dnac_savedCreds = False
        cont = input("Press [Enter] to try again or Ctrl-C to quit")
        print(response)
        print(response.status_code)
        dino.api_main()
        
def iterate_dnac_inventory():
    global dnac_inventory
    exit = False
    entries = len(dnac_inventory)
    print("Total Number of Items in inventory : {}".format(entries))
    cont = input("Press [Enter] to continue or X to exit.")
    if cont == "X":
        done = "done"
        return done
    entry_num = 0
    for x in range(len(dnac_inventory)):
        item = dnac_inventory[x]
        print("Entry {} : \n {}".format(entry_num, item))
        print("---------------------")
        next = input("---Press [Enter] for next entry or type \"x\" [Enter] to Exit---")
        if next == "x":
            dino.api_main_menu()
            break
        entry_num = entry_num + 1
    done = input("*** End of Inventory. Press [Enter] to exit *******")
    return done



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


def get_base(*args):
    """ This function is calling the API at the level """
    """    https://<cluster-ip>/dna/intent/api/v1/    """
    """ ...pass args to this to go to desired level   """
    global dnac_token
    global root_url
    global get_result
    response = requests.get(
        "https://{}/dna/intent/api/v1".format(local_dnac_connArgs["cluster"]) + str(*args),
    headers={
        "X-Auth-Token": "{}".format(dnac_token),
        "Content-type": "application/json",
    },
    verify=False
    )
    res_code = response
    res_json = response.json()
    print(response.status_code)
    response_code = response.status_code
    get_result = res_json()
    return get_result, response, response_code


def get_site():
    import json
    global dnac_token
    global root_url
    global get_result_site
    global dnac_site_list
    site_url = "/site"
    response = requests.get(
        "https://{}/dna/intent/api/v1/site".format(local_dnac_connArgs["cluster"]) + site_url,
    headers={
        "X-Auth-Token": "{}".format(dnac_token),
        "Content-type": "application/json",
    },
    verify=False
    )
    res_json = response.json()
    print(response.status_code)
    response_code = response.status_code
    get_result_site = res_json
    dnac_site_list = res_json
    return dnac_site_list


def full_site_inv(get_result_site):
    """ This functions pulls sites and devices via """
    """ the below api call from the "Global" site  """
    """ so all sites and devices are captured      """
    """ /dna/intent/api/v1/membership/{siteId}     """
    """ g_siteId <--is the global site-id          """
    """      return get results and g_siteId       """
    """      in order to pull inventory from it    """
    """                                            """
    global get_result
    siteIds = {}
    membershipApi = "/membership/"
    g_siteId = ""
##  Loop through and find same values and add to dictionary as key:values
    for x in range(len(get_result_site)):
        sname = get_result_site[x]['name']
        sid = get_result_site[x]['id']
        siteIds[sname] = sid
    g_siteId = siteIds.get('Global', 'Error: Value not found')
    if 'Error' in g_siteId:
        print('Global site id not found. Exiting...')
        raise ValueError
    else:
        print("Global site id found: " + g_siteId + "..continuing")
        apiUrl = (f"/membership/{g_siteId}")
        siteInv = get_base(apiUrl)
        print(siteInv)
    return siteInv              



def post_intent_base(jsonBody, path, headers):
    """ This function is calling the API at the level """
    """    https://<cluster-ip>/dna/intent/api/v1/    """
    """ ...pass args to this to go to desired level   """
    global dnac_token
    global root_url
    global post_result
    payload = jsonBody
    while True:
        try:
            response = requests.post(
            "https://{}/dna/intent/api/v1".format(local_dnac_connArgs["cluster"]) + str(path),
            data=payload,
            headers = headers,
            verify=False
            )
        except requests.exceptions.HTTPError as httperr:
            print(httperr)
        else:
            res_code = response.status_code
            res_json = response.json()
            #requests.Response.raise_for_status(response)
            post_result = ["Response Code: " + str(res_code), res_json]
            print(post_result)
            return post_result, dino.api_main_menu()


#def start_discovery(discoName):
    


def add_device(devName):
    """ Add a device via API. For loop required fields first
    the the rest are optional.
    """
    import json
    headers = {
        "X-Auth-Token": "{}".format(dnac_token),
        "Content-type": "application/json"
        }
    api_path = "/network-device"
    newDevReq = {
        "cliTransport": "string",
        "enablePassword": "string",
        "ipAddress": [
            "string"
            ],
        "password": "string",
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
        "userName": "string"
        }
    for x in newDevReq:
        inputType = newDevReq[x]
        newDevReq[x] = input("Please enter value for  \"{}\" as a {} : ".format(x, inputType))
    devName = json.dumps(newDevReq)
    print(devName)
    return post_intent_base(devName, api_path, headers)


def add_site():
    """
    root    (map, required)
    type    (string, required, enum: area, building, floor)
    site    (map, required)
    area    (map, optional)
    name    (string, required)
    parentName    (string, required)
    building    (map, optional)
    name    (string, required)
    address    (string, optional)
    parentName    (string, required)
    latitude    (number, required)
    longitude    (number, required)
    floor    (map, optional)
    name    (string, required)
    parentName    (string, required)
    rfModel    (string, required, enum: Cubes And Walled Offices, Drywall Office Only, Indoor High Ceiling, Outdoor Open Space)
    width    (number, required)
    length    (number, required)
    height    (number, required)
    """
    api_path = "/site"
    headers = {
        "X-Auth-Token": "{}".format(dnac_token),
        "Content-type": "application/json",
        "__runsync": "true",
        "__runsynctimeout": "30",
        "__persistbapioutput": "true"
        }
    newSiteType = {
    "type": "Type of site (Only 1 can be done at a time): area, building, floor"}
    newSiteConstruct = {
        "site": {
            "area": {
            "name": "string, required",
            "parentName": "string, required"
        },
        "building": {
            "name": "string, required",
            "address": "string, optional",
            "parentName": "string, required",
            "latitude": "number, required",
            "longitude": "number, required"
        },
        "floor": {
            "name": "string, required",
            "parentName": "string, required",
            "rfModel": "string, required, enum: Cubes And Walled Offices, Drywall Office Only, Indoor High Ceiling, Outdoor Open Space",
            "width": "number, required",
            "length": "number, required",
            "height": "number, required"}
        }}
    newSiteType["type"] = input("Please enter value for  \"{}\" : ".format(newSiteType["type"]))
    for x in newSiteConstruct[newSiteType]:
        inputType = newSiteType[x]
        newSiteType[x] = input("Please enter value for  \"{}\" as a {} : ".format(x, inputType))
    newSite = {
        newSiteType}
    addSite = json.dumps(newSite)
    print(devName)
    return post_intent_base(addSite, api_path, headers)


def config_dump(dnac_inventory):
    """
    This script will monitor device configuration changes. It could be executed on demand,
    periodically (every 60 minutes, for example) or continuously.
    It will collect the configuration file for each DNA Center managed device, compare with the existing cached file,
    and detect if any changes.
    When changes detected, identify the last user that configured the device, and create a new ServiceNow incident.
    Automatically roll back all non-compliant configurations, or save new configurations if approved in ServiceNow.
    Device configuration files managemnt using RESTCONF and NETCONF
    Compliance checks at this time:
    - no Access Control Lists changes
    - no logging changes
    - no duplicated IPv4 addresses
    """
    import os
    # Determine number of devices to dump and approve
    devCnt = len(dnac_inventory)

    print('Application config_dump starting...cross your fingers!')
    # create a local directory for all the configuration files
    # check if 'Config_Files' folder exists and create one if it does not

    if not os.path.exists('Config_Files'):
        os.makedirs('Config_Files')

    os.chdir('Config_Files')

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='config_dump_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    while devCnt != 0:

        # get the DNA C auth token
        # ORIGINAL LINE:dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
        global dnac_token

        temp_run_config = 'temp_run_config.txt'

        # get the DNA C managed devices list (excluded wireless, for one location)
        all_devices_info = dnac_inventory#ORIGINAL LINE:dnac_apis.get_all_device_info(dnac_token)
        all_devices_hostnames = []
        for device in all_devices_info:
            print(device['hostname'])
            all_devices_hostnames.append(device['hostname'])
        for device in all_devices_info:
            if device['family'] == 'Switches and Hubs' or device['family'] == 'Routers' or device["family"] == "Wireless Controller":
                all_devices_hostnames.append(device['hostname'])

        # get the config files, compare with existing (if one existing). Save new config if file not existing.
        for device in all_devices_info:
            t = time.localtime()
            deviceId = device["id"]
            tStamp = str("{}{}{}{}{}".format(t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min))
            device_run_config = get_output_command_runner('show running-config', deviceId, dnac_token)
            filename = str(device["hostname"]) + '_' + tStamp + '_run_config.txt'

            f_config = open(filename, 'w')
            f_config.write(device_run_config)
            f_config.seek(0)
            f_config.close()
            print('Device Config Saved : ' + device["hostname"] + ' - as ' + filename)
            devCnt = devCnt - 1
    results = str("Config Dump Complete. Number of Configs Processed: {}".format(len(all_devices_hostnames)))
    return results


def get_output_command_runner(command, deviceId, dnac_jwt_token):
    """
    This function will return the output of the CLI command specified in the {command}, sent to the device with the
    hostname {device}
    :param command: CLI command
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: file with the command output
    """

    # get the DNA C device id
    device_id = deviceId

    # get the DNA C task id that will process the CLI command runner
    payload = {
        "commands": [command],
        "deviceUuids": [device_id],
        "timeout": 0
        }
    url = DNAC_URL + '/api/v1/network-device-poller/cli/read-request'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    task_id = response_json['response']['taskId']
    print(response_json)
    # get task id status
    time.sleep(5)  # wait for a second to receive the file name
    task_result = check_task_id_output(task_id, dnac_jwt_token)
    file_info = json.loads(task_result['progress'])
    file_id = file_info['fileId']

    # get output from file
    time.sleep(2)  # wait for two seconds for the file to be ready
    file_output = get_content_file_id(file_id, dnac_jwt_token)
    command_responses = file_output[0]['commandResponses']
    if command_responses['SUCCESS'] is not {}:
        command_output = command_responses['SUCCESS'][command]
    elif command_responses['FAILURE'] is not {}:
        command_output = command_responses['FAILURE'][command]
    else:
        command_output = command_responses['BLACKLISTED'][command]
    return command_output


def get_content_file_id(file_id, dnac_jwt_token):
    """
    This function will download a file specified by the {file_id}
    :param file_id: file id
    :param dnac_jwt_token: DNA C token
    :return: file
    """
    url = DNAC_URL + '/api/v1/file/' + file_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False, stream=True)
    response_json = response.json()
    return response_json


def get_all_device_info(dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/api/v1/network-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']



def get_device_id_name(device_name, dnac_jwt_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return:
    """
    device_id = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id


def check_task_id_output(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}. Loop one seconds increments until task is completed
    :param task_id: task id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    completed = 'no'
    while completed == 'no':
        try:
            task_response = requests.get(url, headers=header, verify=False)
            task_json = task_response.json()
            task_output = task_json['response']
            completed = 'yes'
        except:
            time.sleep(1)
    return task_output




def check_task_id_status(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}
    :param task_id: task id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    task_response = requests.get(url, headers=header, verify=False)
    task_json = task_response.json()
    task_status = task_json['response']['isError']
    if not task_status:
        task_result = 'SUCCESS'
    else:
        task_result = 'FAILURE'
    return task_result





def enable_req_debug():
    global debug_status
    import logging
    import http.client as http_client
    http_client.HTTPConnectionjson.debuglevel = 1
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

dnac_addSite = {
    "type": "string",
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


dnac_startDiscovery = {
  "cdpLevel": 0,
  "discoveryType": "string",
  "enablePasswordList": [
    "string"
  ],
  "globalCredentialIdList": [
    "string"
  ],
  "httpReadCredential": {
    "comments": "string",
    "credentialType": "GLOBAL",
    "description": "string",
    "id": "string",
    "instanceTenantId": "string",
    "instanceUuid": "string",
    "password": "string",
    "port": 0,
    "secure": True,
    "username": "string"
  },
  "httpWriteCredential": {
    "comments": "string",
    "credentialType": "GLOBAL",
    "description": "string",
    "id": "string",
    "instanceTenantId": "string",
    "instanceUuid": "string",
    "password": "string",
    "port": 0,
    "secure": True,
    "username": "string"
  },
  "ipAddressList": "string",
  "ipFilterList": [
    "string"
  ],
  "lldpLevel": 0,
  "name": "string",
  "netconfPort": "string",
  "noAddNewDevice": True,
  "parentDiscoveryId": "string",
  "passwordList": [
    "string"
  ],
  "preferredMgmtIPMethod": "string",
  "protocolOrder": "string",
  "reDiscovery": True,
  "retry": 0,
  "snmpAuthPassphrase": "string",
  "snmpAuthProtocol": "string",
  "snmpMode": "string",
  "snmpPrivPassphrase": "string",
  "snmpPrivProtocol": "string",
  "snmpROCommunity": "string",
  "snmpROCommunityDesc": "string",
  "snmpRWCommunity": "string",
  "snmpRWCommunityDesc": "string",
  "snmpUserName": "string",
  "snmpVersion": "string",
  "timeout": 0,
  "updateMgmtIp": True,
  "userNameList": [
    "string"
  ]
}

    
### END TESTING FUNCTIONS SECTION

##if __name__ == "__main__":
##    api_main()
#dnac_token = get_dnac_token(dnac_connArgs)
#dnac_inventory = get_dnac_inventory(dnac_token)
