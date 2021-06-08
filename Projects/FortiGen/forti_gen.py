"""FortiGate config generator toolkit"""
import os

from python_settings import settings

from backend.forti_source import FortiSource

os.environ["SETTINGS_MODULE"] = 'settings'


class FortiGen():
    """FortiGen class"""

    def __init__(self):
        """Init class"""

    def create_config_file(self):
        """Create config files"""
        try:
            with open(os.path.join(settings.GOLDEN_IMAGE_PATH),'r') as golden_image:

                print(golden_image.read())
                ###
                # newText = Config.read().replace('FW502R5618001244', self.Host)
                # newText = newText.replace('set timezone 04', 'set timezone ' + self.TimeZone)
                ###

        except Exception as error:
            raise Exception("Cannot read golden image: {}.".format(error)) from None  # noqa: E501

    @staticmethod
    def create_dict(devices_list):
        """Create dict from list"""
        devices_mapped_list = []
        #print(list)
        for device in devices_list:
            devices_dict = {}

            try:
                devices_dict["hostname"] = device[0]
                devices_mapped_list.append(devices_dict)
            except Exception as error:  # pylint: disable=broad-except
                print ("Cannot map device: {}, error message : {}.".format(device, error))  # noqa: E501
                continue

        print(devices_mapped_list)
        return devices_mapped_list


def main():
    """Main"""
    fortisource = FortiSource()
    source_file = fortisource.read_file()
    content = fortisource.read_source_file(source_file)

    fortigen = FortiGen()
    # fortigen.create_config_file()
    fortigen.create_dict(content)

if __name__ == "__main__":
    main()
