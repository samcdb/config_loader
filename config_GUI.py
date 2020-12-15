import tkinter as tk
from os import listdir
from os.path import isfile, join

class Interface:
    def __init__(self, window, ip, launch_func):
        # state variable - if false then nothing runs
        self.run = True

        self.launch_func = launch_func
        self.ip = ip
        self.path = ""

        # dynamic checkbox info
        self.frames = []
        self.file_checkboxes = []
        self.checkbox_info = {}

        # window
        self.window = window
        self.window.title("Config Loader " + self.ip)

        # Frames (in positional order)
        self.window_frm = tk.Frame(master=window, pady=10, padx=20)
        self.error_frm = tk.Frame(master=self.window_frm)
        self.dir_frm = tk.Frame(master=self.window_frm)
        self.open_frm = tk.Frame(master=self.window_frm, pady=10)
        self.detail_frm = tk.Frame(master=self.window_frm)
        self.launch_frm = tk.Frame(master=self.window_frm)

        # directory/path entry
        self.dir_ent = tk.Entry(master=self.dir_frm, width=40)
        self.dir_ent.insert(0, "Enter path to .rsc file")
        self.dir_ent.bind("<FocusIn>", lambda args: self.dir_ent.delete('0', 'end'))
        self.dir_ent.bind("<Return>", lambda event: self.enter(event))

        # buttons (launch_btn packed later)
        self.open_btn = tk.Button(master=self.open_frm, text="Open", command=self.draw)
        self.launch_btn = tk.Button(self.launch_frm, text="Launch", command=self.launch)

        # text
        self.error_txt = tk.StringVar()
        self.error_txt.set(self.ip_check())
        self.detail_txt = tk.StringVar()
        self.detail_txt.set("")

        # labels
        self.detail_lbl = tk.Label(master=self.detail_frm, textvariable=self.detail_txt, fg="blue")
        self.error_lbl = tk.Label(master=self.error_frm, textvariable=self.error_txt, fg="red")

        # pack components
        self.error_lbl.pack()
        self.dir_ent.pack(padx=40, pady=5)
        self.open_btn.pack()

        # pack frames
        self.window_frm.pack()
        self.error_frm.pack()
        self.dir_frm.pack()
        self.open_frm.pack(pady=5)
        
    # dynamically draws checkboxes for all .rsc files
    def draw(self):
        self.detail_txt.set("")
        if self.run == False:
            return

        try:
            # clear old frames
            for frame in self.frames:
                frame.pack_forget()

            # clear old text and frame/checkbox lists
            self.error_txt.set("")
            self.frames.clear()
            self.file_checkboxes.clear()
            self.checkbox_info.clear()

            # get rsc files from path
            self.path = self.dir_ent.get()
            files = [f for f in listdir(self.path) if isfile(join(self.path, f)) and f[-4:] == '.rsc']

            # make checkboxes for .rsc files
            for f in files:
                self.checkbox_info[f] = tk.IntVar()
                self.frames.append(tk.Frame(self.window_frm))
                self.file_checkboxes.append(tk.Checkbutton(
                        master=self.frames[-1], text = f, variable=self.checkbox_info[f], 
                        onvalue = 1, offvalue = 0, height=1, 
                        width = 20, anchor="w"
                        )
                )

                self.frames[-1].pack(side="top")
                self.file_checkboxes[-1].pack()
            
            # dynamically pack checkboxes
            self.launch_frm.pack(side="bottom")
            self.launch_btn.pack()
            self.detail_frm.pack(side="bottom")
            self.detail_lbl.pack()

        except:
            self.error_txt.set("Invalid path")
        

    # launches whichever function is passed into Interface __init__()
    def launch(self):
        self.detail_txt.set("")
        if self.run == False:
            return

        target_file = ""
        check_count = 0
        
        for file in self.checkbox_info:
            if self.checkbox_info[file].get() == 1:
                check_count += 1
                target_file = file
                if(check_count > 1):
                    self.detail_txt.set("Only one file must be selected")
                    return

        if check_count < 1:
            self.detail_txt.set("Please select a file")
            return

        # stop all GUI inputs while function runs
        self.run = False
        # ensure text is set to "Running..."
        self.detail_txt.set("Running...")
        self.window.update_idletasks()

        result_msg = self.launch_func(self.path, target_file, self.ip) 
        self.detail_txt.set(result_msg) 

        self.window.update_idletasks()
        self.run = True

    # wanted to make multi line lambda (couldn't)
    # get path when enter is pressed
    def enter(self, event):
        if self.run == False:
            return

        if event == "":
            return

        self.path = event
        self.draw()

    # check for IP errors
    def ip_check(self):
        if self.ip[:3] == "(1)":
            self.run = False
            return "Error: No IP - Check connection and restart Config Loader"
        elif self.ip[:3] == "(2)":
            self.run = False
            return "Error: Wrong IP - Ensure IP address is 192.168.88.(2-254) then restart Config Loader"
        else:
            return ""