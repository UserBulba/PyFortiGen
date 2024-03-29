'''Settings file'''
# settings.py

# Network prefix to validate.
PREFIX = "10.128.0.0/9"

# Network mask for vLans.
MASK = "255.255.255.0"

# Aggregated mask.
AGGREGATED_MASK = "28"

# Hostname pattern.
PATTERN = (r'\b([R]{1})(-[A-Z]{2})([0-9]{5})\b')

# Golden image file name in conf directory.
# GOLDEN_IMAGE_FILE = "golden_config_fgt_system.conf"

# Output config file name.
CONFIG_FILE = "fgt_system.conf"

# FortiGate platform.
PLATFORM = ["40F", "50E"]

# Create path to golden image base on realpath location.
# current_dir = (os.path.dirname(os.path.realpath(__file__)))
# golden_image_path = os.path.join(current_dir, "conf", GOLDEN_IMAGE_FILE)

# GOLDEN_IMAGE_PATH = golden_image_path

# Values in config file to replace.
DEVICE_NAME = "R-DUMMY"
FORTILINK = "FORTILINK"
COUNTER = "COUNTER"
FORTILINK_GATEWAY = "FORTILINK_GATEWAY"
FORTILINK_DHCP_START = "FORTILINK_DHCP_START"
FORTILINK_DHCP_STOP = "FORTILINK_DHCP_STOP"
FORTILINK_DHCP_START_VALUE = 2
FORTILINK_DHCP_STOP_VALUE = 254

# GUI settings
COLOR = "white"
MESSAGE = "Choose the FortiGate platform"
