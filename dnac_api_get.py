import requests
from api_yaml import *
#from api_auth2 import dnac_token
global dnac_cluster
global get_result_device
global root_url # temporary until common vars module below is setup
#from dnac_api import api_vars
requests.packages.urllib3.disable_warnings()

root_url = "https://dnalive.cisco.com"

def get_base(*args):
    """ This function is calling the API at the level """
    """    https://<cluster-ip>/dna/intent/api/v1/    """
    """ ...pass args to this to go to desired level   """
##    global dnac_token
    global root_url
    global get_result
    response = requests.get(
        "{}/dna/intent/api/v1".format(root_url) + str(*args),
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

def get_device(*args):
    global dnac_token
    global root_url
    global get_result_device
    response = requests.get(
        "{}/dna/intent/api/v1/network-device".format(root_url) + str(*args),
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
    get_result_device = res_json['response', 'site']
    return get_result_device, response, response_code

def get_site(*args):
    global dnac_token
    global root_url
    global get_result_site
    response = requests.get(
        "{}/dna/intent/api/v1/site".format(root_url) + str(*args),
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
    return get_result_site, response, response_code

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


if __name__ == "__main__":
    err = input("This is not intended to be called direct. Quitting")
    quit()
##    print("Success loading...")
##    dnac_token = get_token()
##    pass
