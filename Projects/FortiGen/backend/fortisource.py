"""FortiGate config generator toolkit"""
import csv
import tkinter
from tkinter import filedialog


class FortiSource():
    """FortiSource class"""

    def __init__(self):
        """Init class"""

    @staticmethod
    def read_file():
        """Read path to source file"""
        try:
            root = tkinter.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()

        except Exception as error:
            raise Exception("Cannot open source file: {}.".format(error)) from None  # noqa: E501

        return file_path

    @staticmethod
    def read_source_file(path):
        """Get device with parameters"""
        try:
            with open(path, 'r') as file:
                datareader = csv.reader(file, delimiter=',')
                dev_list = []
                for index, row in enumerate(datareader):
                    if index == 0:
                        continue

                    dev_list.append(row)

        except Exception as error:
            raise Exception("Cannot read value from source file: {}.".format(error)) from None  # noqa: E501

        return dev_list

def main():
    """Main"""
    device = FortiSource()
    file = device.read_file()
    print(device.read_source_file(file))


if __name__ == "__main__":
    main()
