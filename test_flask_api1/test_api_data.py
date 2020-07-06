## test API Content for API server

companies = [{"id": 1, "name": "C5 Acres Inc."}, {"id": 2, "name": "Dev5 Development LLC"}]
users = [{"id": 1, "name": "Garrett Caudle", "email": "gcaudle66@gmail.com", "company_id": 2}]
#### Test DNAC inventory to pull via API- Inv matches APs and WLCs in AS WLC labs
dnac_inventory = [
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0edd.8058', 'macAddress': 'a4:53:0e:dd:80:58', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.61', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G1', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.10.0.197', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f11c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f11c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0eb4.b040', 'macAddress': 'a4:53:0e:b4:b0:40', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.61', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G2', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.10.0.108', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f22c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f22c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0edd.8f88', 'macAddress': 'a4:53:0e:dd:8f:88', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.62', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G3', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.110.0.20', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f33c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f33c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Wireless Controller', 'hostname': 'H1-AB07-C9800-1', 'macAddress': '00:1e:bd:4e:90:11', 'apManagerInterfaceIp': '', 'associatedWlcIp': '', 'bootDateTime': '2020-05-07 21:25:48', 'collectionStatus': 'Managed', 'upTime': '3:22:23.87', 'softwareType': 'Cisco Controller', 'softwareVersion': '16.12.2s', 'snmpLocation': '', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': '9YLDKDUP011', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': None, 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '172.18.149.61', 'platformId': 'C9800-40-K9', 'reachabilityFailureReason': '', 'reachabilityStatus': 'Reachable', 'series': 'Cisco Catalyst 9800 Wireless Controllers', 'snmpContact': '', 'location': None, 'type': 'Cisco Catalyst 9800-40 Wireless Controller', 'role': 'ACCESS', 'collectionInterval': 'Global Default', 'inventoryStatusDetail': '<status><general code="SUCCESS"/></status>', 'instanceUuid': '11c2efca-57d6-47e7-bcc2-c89f1ccbfa0a', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': '11c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'}, 
{'memorySize': 'NA', 'family': 'Wireless Controller', 'hostname': 'H1-AB07-C9800-2', 'macAddress': '00:1e:bd:4e:90:22', 'apManagerInterfaceIp': '', 'associatedWlcIp': '', 'bootDateTime': '2020-05-07 21:25:48', 'collectionStatus': 'Managed', 'upTime': '3:22:23.87', 'softwareType': 'Cisco Controller', 'softwareVersion': '16.12.2s', 'snmpLocation': '', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': '9YLDKDUP022', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': None, 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '172.18.149.62', 'platformId': 'C9800-40-K9', 'reachabilityFailureReason': '', 'reachabilityStatus': 'Reachable', 'series': 'Cisco Catalyst 9800 Wireless Controllers', 'snmpContact': '', 'location': None, 'type': 'Cisco Catalyst 9800-40 Wireless Controller', 'role': 'ACCESS', 'collectionInterval': 'Global Default', 'inventoryStatusDetail': '<status><general code="SUCCESS"/></status>', 'instanceUuid': '22c2efca-57d6-47e7-bcc2-c89f1ccbfa0a', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': '22c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'}]

dnac_inv = [
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0edd.8058', 'macAddress': 'a4:53:0e:dd:80:58', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.61', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G1', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.10.0.197', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f11c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f11c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0eb4.b040', 'macAddress': 'a4:53:0e:b4:b0:40', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.61', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G2', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.10.0.108', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f22c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f22c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Unified AP', 'hostname': ' apa453.0edd.8f88', 'macAddress': 'a4:53:0e:dd:8f:88', 'apManagerInterfaceIp': '', 'associatedWlcIp': '172.18.149.62', 'bootDateTime': None, 'collectionStatus': 'Managed', 'upTime': '03:20:39.210', 'softwareType': None, 'softwareVersion': '16.12.3.13', 'snmpLocation': 'Global/United States/North Carol', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': 'FCW2325N3G3', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': 'null', 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '10.110.0.20', 'platformId': 'C9120AXI-B-K9', 'reachabilityFailureReason': 'NA', 'reachabilityStatus': 'Reachable', 'series': 'Cisco 9100AXI Series Unified Access Points', 'snmpContact': '', 'location': None, 'type': 'Cisco 9100AXI Unified Access Point', 'role': 'ACCESS', 'collectionInterval': 'NA', 'inventoryStatusDetail': 'NA', 'instanceUuid': 'f33c846d-c394-40a9-ac5e-8c5023354c8e', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': 'f33c846d-c394-40a9-ac5e-8c5023354c8e'}, 
{'memorySize': 'NA', 'family': 'Wireless Controller', 'hostname': 'H1-AB07-C9800-1', 'macAddress': '00:1e:bd:4e:90:11', 'apManagerInterfaceIp': '', 'associatedWlcIp': '', 'bootDateTime': '2020-05-07 21:25:48', 'collectionStatus': 'Managed', 'upTime': '3:22:23.87', 'softwareType': 'Cisco Controller', 'softwareVersion': '16.12.2s', 'snmpLocation': '', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': '9YLDKDUP011', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': None, 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '172.18.149.61', 'platformId': 'C9800-40-K9', 'reachabilityFailureReason': '', 'reachabilityStatus': 'Reachable', 'series': 'Cisco Catalyst 9800 Wireless Controllers', 'snmpContact': '', 'location': None, 'type': 'Cisco Catalyst 9800-40 Wireless Controller', 'role': 'ACCESS', 'collectionInterval': 'Global Default', 'inventoryStatusDetail': '<status><general code="SUCCESS"/></status>', 'instanceUuid': '11c2efca-57d6-47e7-bcc2-c89f1ccbfa0a', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': '11c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'}, 
{'memorySize': 'NA', 'family': 'Wireless Controller', 'hostname': 'H1-AB07-C9800-2', 'macAddress': '00:1e:bd:4e:90:22', 'apManagerInterfaceIp': '', 'associatedWlcIp': '', 'bootDateTime': '2020-05-07 21:25:48', 'collectionStatus': 'Managed', 'upTime': '3:22:23.87', 'softwareType': 'Cisco Controller', 'softwareVersion': '16.12.2s', 'snmpLocation': '', 'tagCount': '0', 'tunnelUdpPort': None, 'waasDeviceMode': None, 'serialNumber': '9YLDKDUP022', 'roleSource': 'AUTO', 'lastUpdateTime': 1588898868771, 'errorCode': None, 'errorDescription': None, 'interfaceCount': '0', 'lastUpdated': '2020-05-08 00:47:48', 'lineCardCount': '0', 'lineCardId': '', 'locationName': None, 'managementIpAddress': '172.18.149.62', 'platformId': 'C9800-40-K9', 'reachabilityFailureReason': '', 'reachabilityStatus': 'Reachable', 'series': 'Cisco Catalyst 9800 Wireless Controllers', 'snmpContact': '', 'location': None, 'type': 'Cisco Catalyst 9800-40 Wireless Controller', 'role': 'ACCESS', 'collectionInterval': 'Global Default', 'inventoryStatusDetail': '<status><general code="SUCCESS"/></status>', 'instanceUuid': '22c2efca-57d6-47e7-bcc2-c89f1ccbfa0a', 'instanceTenantId': '5d8d2b5927a4ee004328f51d', 'id': '22c2efca-57d6-47e7-bcc2-c89f1ccbfa0a'}]


if __name__ == '__main__':
    print("this is a DB and unable to be called direct")
    quit()