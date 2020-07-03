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
    try:
        dnac_inventory = json_data["response"]
    except KeyError:
        print("Received an error in response. Possible expired DNAC token")
    else:
        return dnac_inventory, dump
    finally:
        dump = []
        dump.append(data)
        dump.append(json_data)
        dump.append(response)
        dump.append(headers)

