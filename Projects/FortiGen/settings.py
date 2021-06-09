'''Settings file'''
# settings.py

import os

# Golden image file name in conf directory.
GOLDEN_IMAGE_FILE = "golden_config_fgt_system.conf"

# Create path to golden image base on realpath location.
current_dir = (os.path.dirname(os.path.realpath(__file__)))
golden_image_path = os.path.join(current_dir, "conf", GOLDEN_IMAGE_FILE)

GOLDEN_IMAGE_PATH = golden_image_path

# Values in config file to replace.
DEVICE_NAME = "R-DUMMY"
FORTILINK = "FORTILINK"
COUNTER = "COUNTER"
FORTILINK_GATEWAY = "FORTILINK_GATEWAY"
FORTILINK_DHCP_START = "FORTILINK_DHCP_START"
FORTILINK_DHCP_STOP = "FORTILINK_DHCP_STOP"
FORTILINK_DHCP_START_VALUE = 2
FORTILINK_DHCP_STOP_VALUE = 254
