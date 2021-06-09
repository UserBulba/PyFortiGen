"""FortiGate config generator toolkit"""
# forti_preparator.py

import os
import shutil
import tkinter
from pathlib import Path
from tkinter import filedialog

from backend.threader import threader  # pylint: disable=import-error

class FortiPreparator():
    """FortiPreparator class"""

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

            if not self.directory_path:
                print("Choose a destination path")
                return

            for device in self.source:
                self.device_list.append(device[0])

            threader(self.__create_folder, self.device_list)

        except Exception as error:
            raise Exception("Paths cannot be created: {}.".format(error)) from None  # noqa: E501

        return self.directory_path

def main():
    """Main"""

if __name__ == "__main__":
    main()
