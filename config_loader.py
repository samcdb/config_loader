from routeros_api import Api
import socket
import asyncio
import time
import tkinter as tk
import os
from os import listdir
from os.path import isfile, join
import re
import http.server
import socketserver

PORT = 8000
 
def getEthernetIP():
    addresses = os.popen('IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
    return re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()

def createServer(path, ip):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=path, **kwargs)


    with socketserver.TCPServer((ip, PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def drawFileBoxes(fileList):
    path = ent_dir.get()
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(files)

    for f in files:
        frm_file = tk.Frame(master=window)
        CheckVar1 = tk.IntVar()
        C1 = tk.Checkbutton(master=frm_file, text = f, variable = CheckVar1, 
                     onvalue = 1, offvalue = 0, height=5, 
                     width = 20
        )


def launchConfig():
    
    ip_addr = getEthernetIP()
    thread.start_new_thread(createServer(rsc_dir, ip_addr))

    reboot = '/system/reboot'
    fetch = '/tool/fetch =url=http://{0}:{1}/{2} =mode=http =dst-path=flash/{2}'.format(ip_addr, PORT, rsc_dir)
    print(fetch)
    reset = '/system/reset-configuration =no-defaults=yes =run-after-reset=flash/config_with_delay.rsc'

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

class App:
    def __init__(self, window):
        self.entry_frm = tk.Frame(master=window)
        self.dir_ent = tk.Entry(master=self.entry_frm, width=40)
        self.path_lbl = tk.Label(master=self.entry_frm, text="Path")

        self.dir_ent.grid(row=0, column=0, sticky="e")
        self.path_lbl.grid(row=0, column=1, sticky="w")

        self.launch_btn = tk.Button(
            master=window,
            text="\N{RIGHTWARDS BLACK ARROW}",
            command=drawFileBoxes
        )
        self.launch_lbl = tk.Label(master=window, text="Launch")

        self.entry_frm.pack()
        self.launch_btn.pack()
        self.launch_lbl.pack()

        self.frames = []
        self.files = []
        self.ip = getEthernetIP()
        self.count = 0

        self.window = window
        self.window.title("Config Loader " + self.ip)
        self.create = tk.Button(self.window, text="Create", command=self.draw)
        self.create.pack(side="bottom")

    def draw(self):
        path = ent_dir.get()
        files = [f for f in listdir(path) if isfile(join(path, f))]

        checkbox = tk.IntVar()
        self.frames.append(tk.Frame(self.window, borderwidth=1, relief="solid"))
        self.frames[self.count].pack(side="top")
        self.files.append(tk.Checkbutton(master=window, text = "Music", variable = checkbox, 
                 onvalue = 1, offvalue = 0, height=2, 
                 width = 20))

        self.files[-1].pack()
        #tk.Button(self.frames[self.count], text="Submit", command=lambda c=self.count: self.submit(c)).pack()
        self.count += 1
    def submit(self, c):
        for i in self.entries[c]:
            print(i.get())

window = tk.Tk()
App(window)
window.mainloop()

#################################################
# label = lbl    entry = ent    button = btn    frame = frm
window = tk.Tk()
window.title("Config Loader " + eth0)
frm_entry = tk.Frame(master=window)

ent_dir = tk.Entry(master=frm_entry, width=40)
lbl_path = tk.Label(master=frm_entry, text="Path")

ent_dir.grid(row=0, column=0, sticky="e")
lbl_path.grid(row=0, column=1, sticky="w")

btn_launch = tk.Button(
    master=window,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=drawFileBoxes
)
lbl_launch = tk.Label(master=window, text="Launch")

frm_entry.grid(row=0, column=0, padx=10)
btn_launch.grid(row=0, column=1, pady=10)
lbl_launch.grid(row=0, column=2, padx=10)

window.mainloop()
################################################



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


if __name__ == "__main__":
    main()



'''






