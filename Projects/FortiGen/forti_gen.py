"""FortiGate config generator toolkit"""
import os

from python_settings import settings

from backend.forti_preparator import FortiPreparator
from backend.forti_source import FortiSource
from backend.threader import threader

os.environ["SETTINGS_MODULE"] = 'settings'


class FortiGen():
    """FortiGen class"""

    def __init__(self, output):
        """Init class"""
        self.output = output

    def create_config_file(self, device):
        """Create config files"""
        try:
            with open(os.path.join(settings.GOLDEN_IMAGE_PATH),'r') as golden_image:
                # Edit alias and hostname.
                edit_content = golden_image.read().replace(settings.DEVICE_NAME, device["hostname"])


                # Create DHCP Scope.
                edit_content = edit_content.replace(settings.FORTILINK_GATEWAY, device["FortiLink"])
                edit_content = edit_content.replace(settings.FORTILINK_DHCP_START,
                                                    str(device["FortiLink"][:-1]) + str(settings.FORTILINK_DHCP_START_VALUE))
                edit_content = edit_content.replace(settings.FORTILINK_DHCP_STOP,
                                                    str(device["FortiLink"][:-1]) + str(settings.FORTILINK_DHCP_STOP_VALUE))

                # Address interface.
                edit_content = edit_content.replace(settings.FORTILINK, device["FortiLink"])
                edit_content = edit_content.replace(settings.COUNTER, device["Counter"])



            with open(os.path.join(self.output, device["hostname"], 'fgt_config.conf'), "w") as golden_image:
                golden_image.write(edit_content)

        except Exception as error:
            raise Exception("Cannot read golden image: {}.".format(error)) from None  # noqa: E501

    @staticmethod
    def create_dict(devices_list):
        """Create dict from list"""
        devices_mapped_list = []

        for device in devices_list:
            devices_dict = {}

            try:
                # validate R-PL1234...
                if device[0]:
                    devices_dict["hostname"] = device[0]
                else:
                    continue
                # IP validator by lib.
                if device[6]:
                    devices_dict["Counter"] = device[6]
                else:
                    continue
                # IP validator by lib.
                if device[8]:
                    devices_dict["FortiLink"] = device[8]
                else:
                    continue

                ### MAP OTHER ###
                devices_mapped_list.append(devices_dict)
            except Exception as error:  # pylint: disable=broad-except
                print ("Cannot map device: {}, error message : {}.".format(device, error))  # noqa: E501
                continue

        return devices_mapped_list


def main():
    """Main"""
    #
    fortisource = FortiSource()
    source_file = fortisource.read_file()
    content = fortisource.read_source_file(source_file)

    fortiprep = FortiPreparator(content)
    output = fortiprep.create_destination_path()

    fortigen = FortiGen(output)

    device_dict = fortigen.create_dict(content)

    threader(fortigen.create_config_file, device_dict)

    #for device in device_dict:
    #    fortigen.create_config_file(device)

if __name__ == "__main__":
    main()
