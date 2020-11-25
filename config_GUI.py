import tkinter as tk
from os import listdir
from os.path import isfile, join




class Interface:
    def __init__(self, window, ip, launch_func):
        self.launch_func = launch_func

        self.frames = []
        self.file_boxes = []
        self.check_boxes = {}
        self.ip = ip
        self.path = ""

        self.window_frm = tk.Frame(master=window, pady=10, padx=10)
        self.dir_frm = tk.Frame(master=self.window_frm)
        self.dir_ent = tk.Entry(master=self.dir_frm, width=40)

        self.error_txt = tk.StringVar()
        self.error_txt.set("IP Error: Check Network Settings and Restart Config Loader" if ip == "Error" else "")
        self.error_lbl = tk.Label(master=self.window_frm, textvariable=self.error_txt, fg="red")

        self.dir_ent.insert(0, "Enter path to .rsc file")
        self.dir_ent.bind("<FocusIn>", lambda args: self.dir_ent.delete('0', 'end'))
        self.dir_ent.bind("<Return>", lambda event: self.enter(event))
        
        self.open_frm = tk.Frame(master=self.window_frm, pady=10)
        self.open_btn = tk.Button(
            master=self.open_frm,
            text="Open",
            command=self.draw
        )

        self.detail_txt = tk.StringVar()
        self.detail_txt.set("")
        self.detail_frm = tk.Frame(self.window_frm)
        self.detail_lbl = tk.Label(master=self.detail_frm, textvariable=self.detail_txt)

        self.window = window
        self.window.title("Config Loader " + self.ip)

        self.launch_frm = tk.Frame(master=self.window_frm, pady=10)
        self.launch_btn = tk.Button(self.launch_frm, text="Launch", command=self.launch)

        self.window_frm.pack()
        self.error_lbl.pack()
        self.dir_ent.pack(padx=40, pady=5)
        self.dir_frm.pack()
        self.open_frm.pack(pady=5)
        self.open_btn.pack()

    # dynamically draws checkboxes for all .rsc files
    def draw(self):
        try:
            self.error_txt.set("")

            self.path = self.dir_ent.get()
            files = [f for f in listdir(self.path) if isfile(join(self.path, f)) and f[-4:] == '.rsc']
            print(files)

            # clear old frames/checkboxes
            for file, frame in zip(self.file_boxes, self.frames):
                file.pack_forget()
                frame.pack_forget()
            self.frames.clear()
            self.file_boxes.clear()
            self.check_boxes.clear()

            for f in files:
                self.check_boxes[f] = tk.IntVar()
                self.frames.append(tk.Frame(self.window_frm))
                self.frames[-1].pack(side="top")
                self.file_boxes.append(tk.Checkbutton(master=self.frames[-1], text = f, variable=self.check_boxes[f], 
                         onvalue = 1, offvalue = 0, height=1, 
                         width = 20, anchor="w"))

                self.file_boxes[-1].pack()
        
            self.launch_frm.pack(side="bottom")
            self.launch_btn.pack()
            self.detail_frm.pack(side="bottom")
            self.detail_lbl.pack()

        except:
            self.error_txt.set("Invalid path")
        

    # launches whicever function is passed into Interface __init__()
    def launch(self):
        target_file = ""
        check_count = 0
        
        for file in self.check_boxes:
            if self.check_boxes[file].get() == 1:
                check_count += 1
                target_file = file
                if(check_count > 1):
                    self.detail_txt.set("Only one file must be selected")
                    return

        if check_count < 1:
            self.detail_txt.set("Please select a file")
            return

        self.detail_txt.set("Running...")
        self.launch_func(self.path, target_file, self.ip) 
        self.detail_txt.set("Done...")


    # wanted to make muli line lambda 
    # get path when enter is pressed
    def enter(self, event):
        if event == "":
            return

        self.path = event
        self.draw()