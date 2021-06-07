"""FortiGate config generator toolkit"""
import os
import shutil
import tkinter
from pathlib import Path
from threading import Thread
from tkinter import filedialog

from backend.fortisource import FortiSource


class FortiGen():
    """FortiSource class"""

    def __init__(self, source):
        """Init class"""
        self.source = source
        self.device_list = []
        self.directory_path = "Empty"

    def __create_folder(self, host):
        """Create folders for devices configuration"""
        try:
            device_path = os.path.join(self.directory_path, host)
            device_path = Path(device_path)
            if device_path.exists() and device_path.is_dir():
                try:
                    shutil.rmtree(device_path)
                    Path(device_path).mkdir(parents=True, exist_ok=True)

                except OSError as error:
                    raise Exception("Paths cannot be created: {}.".format(error)) from None  # noqa: E501

            else:
                Path(device_path).mkdir(parents=True, exist_ok=True)

        except Exception as error:
            raise Exception("Paths cannot be created: {}.".format(error)) from None  # noqa: E501

    def create_destination_path(self):
        """Create destination folders"""
        try:
            root = tkinter.Tk()
            root.withdraw()
            self.directory_path = filedialog.askdirectory()

            for device in self.source:
                self.device_list.append(device[0])
                # Threading?
                self.__create_folder(device[0])

        except Exception as error:
            raise Exception("Paths cannot be created: {}.".format(error)) from None  # noqa: E501

    def create_config_file(self):
        """"""
        try:
            with open(os.path.join(golden_image_path),'r') as golden_image:
                ###
                newText = Config.read().replace('FW502R5618001244', self.Host)
                newText = newText.replace('set timezone 04', 'set timezone ' + self.TimeZone)
                ###
        except Exception as error:
            raise Exception("Cannot read golden image: {}.".format(error)) from None  # noqa: E501


def main():
    """Main"""
    fortisource = FortiSource()
    source_file = fortisource.read_file()
    content = fortisource.read_source_file(source_file)

    fortigen = FortiGen(content)
    fortigen.create_destination_path()

if __name__ == "__main__":
    main()
