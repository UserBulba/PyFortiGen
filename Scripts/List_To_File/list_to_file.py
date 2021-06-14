'''List PDF in PATH to file'''
import os
PATH = r'C:\Users\piokmi\OTCF S.A\Admin - FortiNet\Licensing\FortiCare - 3Nodes\FC-50E-3Y\FC-10-W502R-311-02-36_18078920'  # pylint: disable=line-too-long

files = os.listdir(PATH)
myfile = open('C:\\Temp\\License-3Y.txt', 'w+')
for f in files:
    ext = os.path.splitext(f)
    if (ext[1]) == ".pdf":

        myfile.write(ext[0] + "\n")
myfile.close()
