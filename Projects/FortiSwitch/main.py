'''FortiSwitch API integrator'''
# main.py

import queue #
import threading #

from python_settings import settings  # Importing configuration file.

import private.read_file as read_file  # Read file.
from fortiswitch import FortiSwitch  # FortiSwitch API.

class Worker(threading.Thread):
    '''Thread'''
    def __init__(self, q, *args, **kwargs):
        self.queue = q
        super().__init__(*args, **kwargs)
    def run(self):
        while True:
            try:
                # work = self.q.get(timeout=3)  # 3s timeout
                print(main(ip_addres=ip, port=tcp_port))
            except queue.Empty:
                return
            # do whatever work you have to do on work
            self.queue.task_done()

def main(ip_addres, port):
    '''Main'''
    forti = FortiSwitch(ip=ip_addres, port=port)
    output = {}

    validator = forti.check_socket()
    if validator:
        output["connectivity"] = True

         # Get FortiSwitch community.
        request = forti.get_forti_community
        if request is None:
            return

        # Remove community getting id from dictionary.
        if "community_id" in request:
            request = forti.delete_forti_community(community_id=request["community_id"])
            output["remove"] = request["status"]

        # Create SNMP community.
        request = forti.create_forti_community()
        output["create"] = request["status"]

        # Fill SysInfo.
        request = forti.put_forti_sysinfo()
        output["sysinfo"] = request["status"]

Switch = read_file.ProcessFile
switch_list = Switch.import_file(settings.PATH)

if switch_list:
    for switch in switch_list:
        ip, tcp_port = switch.split(":")
        forti = FortiSwitch(ip=ip, port=tcp_port)

        # Create list of validated items
        validated_list = []
        validator = forti.check_socket()


    q = queue.Queue()
    for item in validated_list:
        q.put_nowait(item)
    for _ in range(20):
        Worker(q).start()
    q.join()  # blocks until the queue is empty.

    print(main(ip_addres=ip, port=tcp_port))
