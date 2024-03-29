"""FortiGate config generator toolkit"""
# forti_gen.py
import argparse
import os
import re
from ipaddress import IPv4Interface, ip_address, ip_network

from python_settings import settings

from backend.forti_preparator import \
    FortiPreparator  # pylint: disable=import-error
from backend.forti_source import FortiSource  # pylint: disable=import-error
from backend.question_box import FortiGUI  # pylint: disable=import-error
from backend.threader import threader  # pylint: disable=import-error

os.environ["SETTINGS_MODULE"] = 'settings'


class FortiGen():
    """FortiGen class"""

    def __init__(self, output, platform):
        """Init class"""
        self.output = output
        self.platform = platform

    def create_config_path(self):
        """Get path to golden image"""

        # Create path to golden image base on realpath location.
        current_dir = (os.path.dirname(os.path.realpath(__file__)))
        golden_image_path = os.path.join(current_dir, "conf", (self.platform + ".conf"))

        return golden_image_path

    def create_config_file(self, device):
        """Create config files"""

        platform = self.create_config_path()

        try:
            with open(os.path.join(platform),'r') as golden_image:

                # Edit alias and hostname.
                edit_content = golden_image.read().replace(settings.DEVICE_NAME, device["hostname"])

                # Create DHCP Scope.
                edit_content = edit_content.replace(settings.FORTILINK_GATEWAY, device["FortiLink"])
                edit_content = edit_content.replace(settings.FORTILINK_DHCP_START,
                                                    str(device["FortiLink"][:-1]) + str(settings.FORTILINK_DHCP_START_VALUE))
                edit_content = edit_content.replace(settings.FORTILINK_DHCP_STOP,
                                                    str(device["FortiLink"][:-1]) + str(settings.FORTILINK_DHCP_STOP_VALUE))

                # Address interface.
                edit_content = edit_content.replace(settings.FORTILINK, (device["FortiLink"] + " " + settings.MASK))
                edit_content = edit_content.replace(settings.COUNTER, (device["Counter"] + " " + settings.MASK))

            with open(os.path.join(self.output, device["hostname"], settings.CONFIG_FILE), "w") as golden_image:
                golden_image.write(edit_content)

                # Output, created info.
                print("{} - created - {}".format(device["hostname"], device["Aggregated"]))

        except Exception as error:
            raise Exception("Cannot read golden image: {}.".format(error)) from None  # noqa: E501

    @staticmethod
    def create_dict(devices_list):
        """Create dict from list"""

        devices_mapped_list = []

        for device in devices_list:
            devices_dict = {}

            try:
                if device[0] and re.search(re.compile(settings.PATTERN), device[0]):
                    devices_dict["hostname"] = device[0]
                else:
                    print("{} - incorrect hostname".format(device[0]))
                    continue

                if device[1] and ip_address(device[1]) in ip_network(settings.PREFIX):
                    devices_dict["Aggregated"] = IPv4Interface(device[1] + "/" + settings.AGGREGATED_MASK).network
                else:
                    print("{} - incorrect IP Addres {}".format(device[0], device[1]))
                    continue

                if device[6] and ip_address(device[6]) in ip_network(settings.PREFIX):
                    devices_dict["Counter"] = device[6]
                else:
                    print("{} - incorrect IP Addres {}".format(device[0], device[6]))
                    continue

                if device[8] and ip_address(device[8]) in ip_network(settings.PREFIX):
                    devices_dict["FortiLink"] = device[8]
                else:
                    print("{} - incorrect IP Addres {}".format(device[0], device[8]))
                    continue

                devices_mapped_list.append(devices_dict)
            except Exception as error:  # pylint: disable=broad-except
                print ("Cannot map device: {}, error message : {}.".format(device, error))  # noqa: E501
                continue

        return devices_mapped_list


def main():
    """Main"""

    # Collect parameters.
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--platform", type=str, choices = settings.PLATFORM,
                        help = "Indicate the model of the device.")

    args = parser.parse_args()
    platform = args.platform

    if not platform:
        get_platform = FortiGUI()
        platform = get_platform.display_choice(settings.MESSAGE, settings.PLATFORM)

    if platform not in settings.PLATFORM:
        print("FortiGate platform not specified")
        return

    # Get source file.
    fortisource = FortiSource()
    source_file = fortisource.read_file()

    if source_file:
        content = fortisource.read_source_file(source_file)
    else:
        return

    # Prepare output.
    fortiprep = FortiPreparator(content)
    output = fortiprep.create_destination_path()

    if output:
        # Initiate FortiGen class.
        fortigen = FortiGen(output, platform)
    else:
        return

    # Map source list to dict.
    device_dict = fortigen.create_dict(content)

    # Start config generator in threads.
    threader(fortigen.create_config_file, device_dict)

if __name__ == "__main__":
    main()
