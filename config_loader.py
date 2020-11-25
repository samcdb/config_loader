from routeros_api import Api
from config_GUI import Interface
from server import createServer
import threading
import time
import tkinter as tk
import os
import re

PORT = 8000

def getEthernetIP():
    addresses = os.popen('IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
    return re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()

def launchConfig(path, file_name, ip, port=PORT):
    # launch web server to host .rsc file
    # use thread so rest of program can continue
    server_thread = threading.Thread(target=createServer, args=(path, ip, port))
    server_thread.start()

    reboot = '/system/reboot'
    fetch = '/tool/fetch =url=http://{0}:{1}/{2} =mode=http =dst-path=flash/{2}'.format(ip, port, file_name)
    reset = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/config_with_delay.rsc'
    print(fetch)

    while(True):
        try:
            router = Api('192.168.88.1')
            #r = router.talk('/system/identity/print')
            #print(r)
            print('connected')
            # router gets config file from web servers
            router.talk(fetch)
            print("file fetched")
            router.talk(reset)
            print("resetting")
            time.sleep(3)

        except TimeOutError:
            print(timedout)

def main():
    ip_addr = getEthernetIP()
    window = tk.Tk()
    Interface(window, ip_addr, launchConfig)
    window.mainloop()

'''
def main():
    
    reboot = '/system/reboot'
    fetch_file = '/tool/fetch =url=http://192.168.88.254:8000/config_with_delay.rsc =mode=http =dst-path=flash/config_with_delay.rsc'
    reset_config = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/config_with_delay.rsc'  

    while(True):
        try:
            
            #router = Api('192.168.88.1')
            #r = router.talk('/system/identity/print')
            #print(r)
            print('connected')

            # router gets config file from web servers
            #router.talk(fetch_file)
            print("file fetched")
            #router.talk(reset_config)
            print("resetting")
            time.sleep(3)

        except TimeOutError:
            print(timedout)
'''

if __name__ == "__main__":
    main()









