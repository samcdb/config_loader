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

    router_count = 0
    while(True):
        try:
            router = Api('192.168.88.1')
            router_count += 1
            print("Router {}".format(router_count))
            print('connected')
            # router gets config file from web servers
            router.talk(fetch)
            print("file fetched")
            # router is reset and then loads new config file
            router.talk(reset)
            print("reset")

            time.sleep(1)

        except:
            return

def main():
    ip_addr = ""

    try:
        ip_addr = getEthernetIP()
        byte_list = ip_addr.split('.')

        #if byte_list[0]


    except:
        ip_addr = "Error"
    finally:
        window = tk.Tk()
        Interface(window, ip_addr, launchConfig)
        window.mainloop()

if __name__ == "__main__":
    main()









