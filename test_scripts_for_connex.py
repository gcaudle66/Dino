wifi_inv = [
    [
        {'hostname': 'H1-AB07-C9800-2', 'platformId': 'C9800-40-K9', 'mgmntIP': '172.18.149.62', 'location': None, 'instanceUuid': '22c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'},
        {'hostname': 'H1-AB07-C9800-1', 'platformId': 'C9800-40-K9', 'mgmntIP': '172.18.149.61', 'location': None, 'instanceUuid': '11c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'},
        {'hostname': 'C9800-WLC', 'platformId': 'C9800-CL-K9', 'mgmntIP': '198.18.134.100', 'location': None, 'instanceUuid': '7106a31a-3e11-4f3a-be41-115c3b39b9f7'}],
    [
        {'hostname': ' apa453.0edd.8f88', 'platformId': 'C9120AXI-B-K9', 'mgmntIP': '10.110.0.20', 'associatedWlcIp': '172.18.149.62', 'instanceUuid': 'f33c846d-c394-40a9-ac5e-8c5023354c8e', 'ethMacAddress': 'a4:53:0e:dd:8f:88', 'location': None},
        {'hostname': ' apa453.0eb4.b040', 'platformId': 'C9120AXI-B-K9', 'mgmntIP': '10.10.0.108', 'associatedWlcIp': '172.18.149.61', 'instanceUuid': 'f22c846d-c394-40a9-ac5e-8c5023354c8e', 'ethMacAddress': 'a4:53:0e:b4:b0:40', 'location': None},
        {'hostname': ' apa453.0edd.8058', 'platformId': 'C9120AXI-B-K9', 'mgmntIP': '10.10.0.197', 'associatedWlcIp': '172.18.149.61', 'instanceUuid': 'f11c846d-c394-40a9-ac5e-8c5023354c8e', 'ethMacAddress': 'a4:53:0e:dd:80:58', 'location': None},
        {'hostname': 'AP78BC.1ADB.CDCA', 'platformId': 'AIR-AP3802I-B-K9', 'mgmntIP': '172.16.200.100', 'associatedWlcIp': '198.18.134.100', 'instanceUuid': '685951f6-9c53-4237-9054-2d7a90e5b192', 'ethMacAddress': '78:bc:1a:db:cd:ca', 'location': None},
        {'hostname': 'AP78BC.1ADB.CB1C', 'platformId': 'AIR-AP3802I-B-K9', 'mgmntIP': '172.16.100.100', 'associatedWlcIp': '198.18.134.100', 'instanceUuid': '6f133b02-9b32-43f6-9b13-f623d7d075d3', 'ethMacAddress': '78:bc:1a:db:cb:1c', 'location': None}]
    ]
## Then parse it
parsedAPI = ap_rename20.parseAPI(wifi_inv)
### Which returns ap_rename20.final_APIresults
ap_rename20.final_APIresults = [
    ['AP78BC.1ADB.CB1C', '78bc.1adb.cb1c', '198.18.134.100'], ['AP78BC.1ADB.CDCA', '78bc.1adb.cdca', '198.18.134.100'],
    [' apa453.0edd.8058', 'a453.0edd.8058', '172.18.149.61'], [' apa453.0eb4.b040', 'a453.0eb4.b040', '172.18.149.61'],
    [' apa453.0edd.8f88', 'a453.0edd.8f88', '172.18.149.62']]
#### Then generate matches
matches = ap_rename20.api_compare(ap_rename20.final_APIresults)
##### Which returns ap_rename20.matches
ap_rename20.matches = [
    ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}],
    ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}],
    ['a453.0edd.8f88', {'Old_Name': ' apa453.0edd.8f88', 'New_Name': 'ap.blue.milk.2', 'wlc': '172.18.149.62'}],
    ['78bc.1adb.cb1c', {'Old_Name': 'AP78BC.1ADB.CB1C', 'New_Name': 'ap.black.pearl.conf1', 'wlc': '198.18.134.100'}],
    ['78bc.1adb.cdca', {'Old_Name': 'AP78BC.1ADB.CDCA', 'New_Name': 'ap.flying.dutchman.lobby2', 'wlc': '198.18.134.100'}]]
###### Now on to dino1_connex(ap_rename20.matches) for connex work
###### Each function listed below the initial func call is under connex func
######
dino1_connex(ap_rename20.matches)
    ### split_conns func
split_conns = ap_rename20.connex_split()
    ###### Which returns splt_conns
split_conns = [['172.18.149.61',
                ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}],
                ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}]],
               ['172.18.149.62',
                ['a453.0edd.8f88', {'Old_Name': ' apa453.0edd.8f88', 'New_Name': 'ap.blue.milk.2', 'wlc': '172.18.149.62'}]],
               ['198.18.134.100',
                ['78bc.1adb.cb1c', {'Old_Name': 'AP78BC.1ADB.CB1C', 'New_Name': 'ap.black.pearl.conf1', 'wlc': '198.18.134.100'}],
                ['78bc.1adb.cdca', {'Old_Name': 'AP78BC.1ADB.CDCA', 'New_Name': 'ap.flying.dutchman.lobby2', 'wlc': '198.18.134.100'}]]]

    ### create connex_list which creates necessary CLI commands per AP and returns connex_list
connex_list = ap_rename20.create_connex_list(split_conns)
        #### returned connex_list...
connex_list = [['172.18.149.61', ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}], ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}], ['ap name  apa453.0eb4.b040 name ap.padawan.learner1', 'ap name  apa453.0edd.8058 name ap.theseare.notthedroids.youarelooking4', 'show ap config general | include ^Cisco AP Name|^MAC Address']], ['172.18.149.62', ['a453.0edd.8f88', {'Old_Name': ' apa453.0edd.8f88', 'New_Name': 'ap.blue.milk.2', 'wlc': '172.18.149.62'}], ['ap name  apa453.0edd.8f88 name ap.blue.milk.2', 'show ap config general | include ^Cisco AP Name|^MAC Address']], ['198.18.134.100', ['78bc.1adb.cb1c', {'Old_Name': 'AP78BC.1ADB.CB1C', 'New_Name': 'ap.black.pearl.conf1', 'wlc': '198.18.134.100'}], ['78bc.1adb.cdca', {'Old_Name': 'AP78BC.1ADB.CDCA', 'New_Name': 'ap.flying.dutchman.lobby2', 'wlc': '198.18.134.100'}], ['ap name AP78BC.1ADB.CB1C name ap.black.pearl.conf1', 'ap name AP78BC.1ADB.CDCA name ap.flying.dutchman.lobby2', 'show ap config general | include ^Cisco AP Name|^MAC Address']]]


    ### Some minor prep b4
ap_rename20.forAPI = True
connArgs = ap_rename20.get_conn_args()
temp_connex = connex_list.copy()


###############################################################################
#### WORKING LOOP TO ITERATE connex_list
## connex_list used for below example:   connex_list = [['172.18.149.61', ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}], ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}], ['ap name  apa453.0eb4.b040 name ap.padawan.learner1', 'ap name  apa453.0edd.8058 name ap.theseare.notthedroids.youarelooking4', 'show ap config general | include ^Cisco AP Name|^MAC Address']], ['172.18.149.62', ['a453.0edd.8f88', {'Old_Name': ' apa453.0edd.8f88', 'New_Name': 'ap.blue.milk.2', 'wlc': '172.18.149.62'}], ['ap name  apa453.0edd.8f88 name ap.blue.milk.2', 'show ap config general | include ^Cisco AP Name|^MAC Address']], ['198.18.134.100', ['78bc.1adb.cb1c', {'Old_Name': 'AP78BC.1ADB.CB1C', 'New_Name': 'ap.black.pearl.conf1', 'wlc': '198.18.134.100'}], ['78bc.1adb.cdca', {'Old_Name': 'AP78BC.1ADB.CDCA', 'New_Name': 'ap.flying.dutchman.lobby2', 'wlc': '198.18.134.100'}], ['ap name AP78BC.1ADB.CB1C name ap.black.pearl.conf1', 'ap name AP78BC.1ADB.CDCA name ap.flying.dutchman.lobby2', 'show ap config general | include ^Cisco AP Name|^MAC Address']]]

for item in connex_list:
	wlcIP = item[0]
	cnt = len(item)
	cmds = cnt - 1
	for sub in range(cmds):
		print(item[sub])
		print("\n")
	print(f"CLI Commands : \n{item[cmds]}\n")

	
172.18.149.61
['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}]
['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}]
CLI Commands : 
['ap name  apa453.0eb4.b040 name ap.padawan.learner1', 'ap name  apa453.0edd.8058 name ap.theseare.notthedroids.youarelooking4', 'show ap config general | include ^Cisco AP Name|^MAC Address']

172.18.149.62
['a453.0edd.8f88', {'Old_Name': ' apa453.0edd.8f88', 'New_Name': 'ap.blue.milk.2', 'wlc': '172.18.149.62'}]
CLI Commands : 
['ap name  apa453.0edd.8f88 name ap.blue.milk.2', 'show ap config general | include ^Cisco AP Name|^MAC Address']

198.18.134.100
['78bc.1adb.cb1c', {'Old_Name': 'AP78BC.1ADB.CB1C', 'New_Name': 'ap.black.pearl.conf1', 'wlc': '198.18.134.100'}]
['78bc.1adb.cdca', {'Old_Name': 'AP78BC.1ADB.CDCA', 'New_Name': 'ap.flying.dutchman.lobby2', 'wlc': '198.18.134.100'}]
CLI Commands : 
['ap name AP78BC.1ADB.CB1C name ap.black.pearl.conf1', 'ap name AP78BC.1ADB.CDCA name ap.flying.dutchman.lobby2', 'show ap config general | include ^Cisco AP Name|^MAC Address']
########
$$$$ NOW ATTEMPTS TO ITERATE to build conn_info per WLC conn and pass to ap_rename20.api_connect

def dino1_connex_handler(connex_list):
    """
    """
    temp_list = connex_list.copy()
    conn_list = []
    conn_info = []
    conn_cnt = len(connex_list)
    for item in range(conn_cnt):
        item = temp_list.pop()
        conn_info.clear()
        cnt = len(item)
        cmds_indx = cnt - 1
        conn_info.append(item[0])
        for sub in range(cmds_indx):
            apInfo = item[sub]
            conn_info.append(apInfo)
        cmds = item[cmds_indx]
        print(conn_info)
        conn_info.insert(1, cmds)
        conn_list.append(conn_info)
    return conn_list

#######################################################
connex_list2 = [['192.168.20.26', ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}], ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}],
                 ['show version | include ^Cisco IOS XE Software', 'show ap config general | include ^Cisco AP Name|^MAC Address']],
                ['172.18.149.61', ['a453.0eb4.b040', {'Old_Name': ' apa453.0eb4.b040', 'New_Name': 'ap.padawan.learner1', 'wlc': '172.18.149.61'}], ['a453.0edd.8058', {'Old_Name': ' apa453.0edd.8058', 'New_Name': 'ap.theseare.notthedroids.youarelooking4', 'wlc': '172.18.149.61'}],
                 ['show version | include ^Cisco IOS XE Software', 'show ap config general | include ^Cisco AP Name|^MAC Address']]]

def dino1_connex_handler(connex_list):
    """
    """
    temp_list = connex_list.copy()
    conn_list = []
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
        print("Session {} : ConneX'ing to {}".format(conn_seq, conn_info[0]))
        api_connex(conn_info)
        conn_seq = conn_seq + 1
    print("Dino ConneX Completed {} Sessions".format(conn_cnt))



connArgs = {"cluster": "192.168.20.26",
                 "username": "admin",
                 "password": "fsp-WWcs!"}


def api_connex(conn_info):
    import netmiko as nm
    global connArgs
    attempts = 0
    expPrompt = False
    try:
        net_connect = nm.BaseConnection(ip=conn_info[0], username=connArgs["username"], password=connArgs["password"], session_log="ssh_session_logfile{}.txt".format(conn_info[2]), session_log_file_mode="write", session_log_record_writes="True")
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
        connIsAlive = net_connect.is_alive()
        if connIsAlive is True:
            print("*********************************************************");
            print("* Dino | SSH ConneX                                     *");
            print("*********************************************************")
            print("* SSH Connection Successful!                            *")
            getPrompt = net_connect.find_prompt()
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
                net_connect.disable_paging()
                expPrompt = True
                output = net_connect.send_config_set(config_commands=conn_info[1], enter_config_mode=False, cmd_verify=False, exit_config_mode=False)
                print(f"Commands sent to {conn_info[0]}, \n" \
                      f"Output: {output}")
                print("now disconnecting...")
                net_connect.disconnect()
                return
            elif choice == 2:
                print(f"Disconnecting Current SSH Session...") 
                net_connect.disconnect()
                connIsAlive = net_connect.is_alive()
                return conn
        else:
            print("Failure: Unknown Error. Sorry")


#########################################################
#### attempts to loop IN ssh CONNECThANDLER
conn = ConnectHandler(ip=conn_info[0], username=connArgs["user"], password=connArgs["pass"], device_type="cisco_ios", session_log="ssh_session_logfile.txt", session_log_file_mode="write", session_log_record_writes="True")

class ConnexSSH(function):
    def __init__(self, wlcIP, userID, passWD, cliCMDS, connID):
        self.wlcIP = wlcIP
