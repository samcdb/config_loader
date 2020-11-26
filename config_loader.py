import routeros_api
from config_GUI import Interface
from server import createServer
import socket
import threading
import time
import tkinter as tk
import os
import re
import shutil

PORT = 8000

class WrongIPError(Exception):
    """Raised when IP address is not set to static 192.168.88.(2-254 range)"""
    pass

def getEthernetIP():
    addresses = os.popen('IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
    return re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()

def check_delay(path, file_name):
    print("Checking for file delay")
    with open(path + '\\' + file_name) as rsc_file:
        line_count = 0

        for line in rsc_file:
            line_list = line.split()
            if line_list[0] == '#':
                line_count += 1
                continue
            elif line_list[0] == ':delay' and line_list[1] == '15s;':
                return (True, line_count)
                print("Delay found")
            else:
                return (False, line_count)
                print("No delay found")


def write_delay(path, file_name, delay_pos):
    print("Copying file and writing delay")
    src_file = os.path.join(path, file_name)
    delayed_file = os.path.join(path, file_name[:-4] + "_with_delay.rsc")
    shutil.copy(src_file, delayed_file)
    contents = []

    with open(delayed_file, 'r') as rsc_file:
        contents = rsc_file.readlines()

    contents.insert(delay_pos, ':delay 15s;\n')

    with open(delayed_file, 'w') as rsc_file:
        contents = "".join(contents)
        rsc_file.write(contents)

    return delayed_file.split('\\')[-1]
    
def launchConfig(path, file_name, ip, port=PORT):
    print("path " + path)
    print("file " + file_name)
    delay_check = check_delay(path, file_name)

    if delay_check[0] == False:
        file_name = write_delay(path, file_name, delay_check[1])

    
    # launch web server to host .rsc file
    # use thread so rest of program can continue
    
    server_thread = threading.Thread(target=createServer, args=(path, ip, port))
    server_thread.start()

    reboot = '/system/reboot'
    fetch = '/tool/fetch =url=http://{0}:{1}/{2} =mode=http =dst-path=flash/{2}'.format(ip, port, file_name)
    reset = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/{}'.format(file_name)
    router_count = 0

    while(True):
        try:
            router = routeros_api.Api('192.168.88.1')
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

        except (socket.timeout, routeros_api.CreateSocketError):
            # this isn't clean but it's the only way I can see to allow the program to finish/conclude
            # No routers left => timeout/CreateSocketError => done
            print("No routers left: timing out")
            return
    

def main():
    ip_addr = ""

    try:
        ip_addr = getEthernetIP()
        byte_list = ip_addr.split('.')

        if byte_list[0] != '192' or byte_list[1] != '168' or byte_list[2] != '88' or not 1 < int(byte_list[3]) < 255:
            raise WrongIPError

    except AttributeError:
        ip_addr = "(0) No IP Error!"
        print(ip_addr)
    except WrongIPError:
        ip_addr = "(1) Wrong IP Error!"
        print(ip_addr)
    finally:
        window = tk.Tk()
        Interface(window, ip_addr, launchConfig)
        window.mainloop()

if __name__ == "__main__":
    main()









