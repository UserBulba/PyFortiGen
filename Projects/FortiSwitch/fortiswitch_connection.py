'''Main module'''
# import json
# import cookiejar
import requests
from fortiswitch_methods import fortiswitch_system_snmp

# Disable HTTPS warnings.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SWITCH_IP = r"10.140.167.2"
url_login=f"https://{SWITCH_IP}/logincheck"
client = requests.session()

# Login request
PAYLOAD="username=admin&secretkey=_SWduf8_MUCr"
r = client.post(url_login,data=PAYLOAD,verify=False)

apscookie=r.cookies

for cookie in client.cookies:
    if cookie.name =='ccsrftoken':
        csrftoken=cookie.value[1:-1]

client.headers.update({'X-CSRFTOKEN':csrftoken})
print (csrftoken)

url_cmdb=f"https://{SWITCH_IP}/api/v2/cmdb/system.snmp/community"
r = client.get(url_cmdb, cookies = apscookie)
Switch = r.json()
Loop = Switch["results"]
# print (r.text)
# print (r.json())

print (len(Switch["results"]))
for item in range(len(Loop)):
    # print (item)

    Com = Switch["results"][item]["name"]
    switch_id = Switch["results"][item]["id"]
    Status = Switch["results"][item]["status"]
    Hosts = Switch["results"][item]["hosts"]

    if Com:
        print ("Current SNMP community {0} for {1}".format(Com, SWITCH_IP))
