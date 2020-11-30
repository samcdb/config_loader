import routeros_api
from config_GUI import Interface
from Server import Server
import socket
import threading
import time
import os
import re
import shutil
import tkinter as tk

# Web server port
PORT = 8000

class WrongIPError(Exception):
    """Raised when IP address is not set to static 192.168.88.(2-254 range)"""
    pass

class RepeatedConnectionError(Exception):
    """Raised when there are multiple (5) consecutive ResetConnectionErrors """
    pass

# use IPCONFIG to get eth0 IP
def getEthernetIP():
    addresses = os.popen('IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
    return re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()

# check if .rsc file has delay at start (needed)
# returns boolean describing if a delay is present and the line number of the delay or the start of the script (lack of delay)
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

# if no delay is present -> copies .rsc file -> renames it -> adds delay -> run
def write_delay(path, file_name, delay_pos):
    print("Copying file and writing delay")
    src_file = os.path.join(path, file_name)
    delayed_file = os.path.join(path, file_name[:-4] + "_WITH_DELAY.rsc") # try to make sure no other files have this name
    print(delayed_file)
    shutil.copy(src_file, delayed_file)
    contents = []

    with open(delayed_file, 'r') as rsc_file:
        contents = rsc_file.readlines()

    contents.insert(delay_pos, ':delay 15s;\n')

    with open(delayed_file, 'w') as rsc_file:
        contents = "".join(contents)
        rsc_file.write(contents)

    return delayed_file.split('\\')[-1]

# config set up function 
def launchConfig(path, file_name, ip, port=PORT):
    run_time = time.time()
    print("path " + path)
    print("file " + file_name)
    delay_present, line = check_delay(path, file_name)

    if not delay_present:
        file_name = write_delay(path, file_name, line)

        
    # launch web server to host .rsc file
    # use thread so rest of program can continue
        
    file_server = Server(path, ip, port)
    file_server.thread_start()

    reboot = '/system/reboot'
    fetch = '/tool/fetch =url=http://{0}:{1}/{2} =mode=http =dst-path=flash/{2}'.format(ip, port, file_name)
    reset = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/{}'.format(file_name)
    router_count = 0
    tries = 0

    try:

        while(True):
            try:
            
                router = routeros_api.Api('192.168.88.1')
                tries = 0
                router_count += 1

                print()
                print("Router {}".format(router_count))
                print('connected')
                # router gets config file from web servers
                router.talk(fetch)
                print("file fetched")
                # router is reset and then loads new config file
                router.talk(reset)
                print("resetting router")
                print()
                print("looking for more routers...")
                print()

                # allow time for router to reset and a new connection to be made
                #time.sleep(1)
                router.close()
                time.sleep(1)

            except ConnectionResetError:
                tries += 1
                print("connection attempts = {}".format(tries))

                if tries == 5:
                    raise RepeatedConnectionError
                    


    except (socket.timeout, routeros_api.CreateSocketError):
        # this isn't clean but it's the only way I can see to allow the program to finish/conclude
        # No routers left => timeout/CreateSocketError => done
        print("Done")
        file_server.shutdown()

    except RepeatedConnectioNError:
            print("ConnectionResetError 5 times")
            print("terminating")

    finally:
        file_server.shutdown()
                
        # if delay copy was made, delete it
        if (not delay_present):
            print("cleaning up")
            os.remove(os.path.join(path, file_name))

        run_time = int(time.time() - run_time)
        print("time taken: {}".format(run_time))
                

        '''
            print("Error")
            file_server.shutdown()
            
            # if delay copy was made, delete it
            if (not delay_present):
                print("cleaning up")
                os.remove(os.path.join(path, file_name))

            print("Router Error")
            return False
        '''
    

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









