'''FortiSwitch API integrator'''
import configparser # Read config file.
import os # Just os module?
import logging # Logging errors.
from pathlib import Path # Create a directory if needed.
import requests # Requests HTTP Library.
import urllib3 # Disable HTTPS warnings.

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

        for item in range(len(loop)):

            com = switch["results"][item]["name"]
            community_id = switch["results"][item]["id"]
            # status = switch["results"][item]["status"]
            # hosts = switch["results"][item]["hosts"]

            if com:
                snmp = "Current SNMP community {0} for {1}".format(com, self.ip_addres)
                # return dictionary with id, status, com, etc...
                return snmp

    def delete_forti_community(self, community_id):
        '''Delete FortiSwitch SNMP community'''

        self.get_forti_request()

        url = "https://{}/api/v2/cmdb/system.snmp/community{}".format(self.ip_addres, community_id)
        try:
            response = self.client.delete(url, cookies = self.apscookie)
        # Add normal exceptions with logging.
        except:
        # Return error code form get_forti_requests.
            response = None
        finally:
            return response

def main(ip_addres):
    '''Main'''
    forti = FortiSwitch(ip=ip_addres)
    request = forti.get_forti_community()
    return request

switch = "10.140.167.2"
print(main(switch))
