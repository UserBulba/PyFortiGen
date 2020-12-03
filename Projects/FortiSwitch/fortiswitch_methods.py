'''API Methods'''
def fortiswitch_system_snmp(method, cookies):
    '''SNMP...'''
    print(method)

    url_cmdb=f"https://{SWITCH_IP}/api/v2/cmdb/system.snmp/community"
    r = client.get(url_cmdb, cookies = apscookie)
