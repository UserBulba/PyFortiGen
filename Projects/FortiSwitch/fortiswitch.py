'''FortiSwitch API integrator'''
import configparser # Read config file.
import os # Just os module?
import logging # Logging errors.
import ast # Use to read list from config file.
from pathlib import Path # Create a directory if needed.
import requests # Requests HTTP Library.
import urllib3 # Disable HTTPS warnings.

##
# Use crypto, key rings.
##

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create logs dir
current_dir = (os.path.dirname(os.path.realpath(__file__)))

# Remove logs dir and try!
##
Path(os.path.join(current_dir, "logs")).mkdir(parents=True, exist_ok=True)
logging_path = os.path.join(current_dir, "logs", "FortiSwitch.log")
##

# DEBUG -> WARNING :
logging.basicConfig(filename=logging_path, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

class FortiSwitch: # pylint: disable=too-few-public-methods
    '''FortiSwitch class'''
    def __init__(self, ip):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + '/conf.ini')
        self.forti_user = config.get("FortiSwitch", "username")
        self.forti_secret = config.get("FortiSwitch", "secretkey")
        self.ip_addres = ip
        self.client = requests.session()
        self.id = 1

    def get_forti_request(self):
        '''Get FortiSwitch api request'''

        # Login request
        url = "https://{}/logincheck".format(self.ip_addres)
        payload = "username={}&secretkey={}".format(self.forti_user, self.forti_secret)
        try:
            response = self.client.post(url, data=payload, verify=False)
        # Add normal exceptions with logging.
        except Exception as error: # pylint: disable=broad-except
            logger.info(error)
        # Return error code form get_forti_requests.
            return None

        self.apscookie = response.cookies

        for cookie in self.client.cookies:
            if cookie.name =='ccsrftoken':
                csrftoken=cookie.value[1:-1]

        self.client.headers.update({'X-CSRFTOKEN':csrftoken})

    @property
    def get_forti_community(self):
        '''Get FortiSwitch SNMP community'''

        self.get_forti_request()

        url = "https://{}/api/v2/cmdb/system.snmp/community".format(self.ip_addres)
        try:
            response = self.client.get(url, cookies = self.apscookie)
        # Add normal exceptions with logging.
        except Exception as error: # pylint: disable=broad-except
            logger.info(error)
        # Return error code form get_forti_requests.
            return None

        switch = response.json()
        loop = switch["results"]
        dictionary = {}

        for item in range(len(loop)):
            try:
                dictionary["community_name"] = switch["results"][item]["name"]
            except Exception as error: # pylint: disable=broad-except
                logger.info(error)

            try:
                dictionary["community_id"] = switch["results"][item]["id"]
            except Exception as error: # pylint: disable=broad-except
                logger.info(error)

        return dictionary

                # status = switch["results"][item]["status"]
                # hosts = switch["results"][item]["hosts"]

            # if community_name:
            #     snmp = "Current SNMP community {0} for {1}".format(community_name, self.ip_addres)
            #     # return dictionary with id, status, com, etc...
            #     return snmp

    def delete_forti_community(self, community_id):
        '''Delete FortiSwitch SNMP community'''

        self.get_forti_request()

        url = "https://{}/api/v2/cmdb/system.snmp/community/{}".format(self.ip_addres, community_id)
        try:
            return self.client.delete(url, cookies = self.apscookie)

        except Exception as error: # pylint: disable=broad-except
            logger.info(error)
            # Return error code form get_forti_requests.
            return None

    def create_forti_community(self):
        '''Create FortiSwitch SNMP community'''

        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + '/conf.ini')
        snmp_community = config.get("SNMP", "community")
        snmp_hosts = ast.literal_eval(config.get("SNMP", "hosts"))

        self.get_forti_request()

        url = "https://{}/api/v2/cmdb/system.snmp/community".format(self.ip_addres)

        payload = {
            "status" : "enable",
            "name" : snmp_community,
            "hosts" : [],
            "id" : self.id
        }

        try:
            for counter, host in enumerate(snmp_hosts, start=1):
                payload["hosts"].append({'ip':host})
                payload["hosts"].append({'id':counter})

        except Exception as error: # pylint: disable=broad-except
            logger.info(error)

        try:
            return self.client.post(url, data=payload, cookies = self.apscookie)

        except Exception as error: # pylint: disable=broad-except
            logger.info(error)
            # Return error code form get_forti_requests.
            return None

def main(ip_addres):
    '''Main'''
    forti = FortiSwitch(ip=ip_addres)

    request = forti.get_forti_community
    print(request)

    # Remove community getting id from dictionary
    if remove_mode and ("community_id" in request):
        request = forti.delete_forti_community(community_id=request["community_id"])
        print(request)

    request = forti.get_forti_community
    print(request)

    return request

remove_mode = True
switch = "10.140.167.2"
print(main(switch))