import tkinter as tk
from os import listdir
from os.path import isfile, join




class Interface:
    def __init__(self, window, ip, launch_func):
        self.launch_func = launch_func

        self.entry_frm = tk.Frame(master=window)
        self.dir_ent = tk.Entry(master=self.entry_frm, width=40)
        self.path_lbl = tk.Label(master=self.entry_frm, text="Path")

        self.dir_ent.insert(0, "Enter path to .rsc file")
        self.dir_ent.bind("<FocusIn>", lambda args: self.dir_ent.delete('0', 'end'))
        self.dir_ent.bind("<Return>", lambda event: self.enter(event))
        

        self.open_btn = tk.Button(
            master=window,
            text="Open",
            command=self.draw
        )

        self.frames = []
        self.file_boxes = []
        self.check_boxes = {}
        self.ip = ip
        self.path = ""

        self.window = window
        self.window.title("Config Loader " + self.ip)
        self.launch_btn = tk.Button(self.window, text="Launch", command=self.launch)

        self.path_lbl.pack()
        self.dir_ent.pack()
        self.entry_frm.pack()
        self.open_btn.pack()

    # dynamically draws checkboxes for all .rsc files
    def draw(self):
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
            self.frames.append(tk.Frame(self.window, borderwidth=1, relief="solid"))
            self.frames[-1].pack(side="top")
            self.file_boxes.append(tk.Checkbutton(master=self.window, text = f, variable=self.check_boxes[f], 
                     onvalue = 1, offvalue = 0, height=1, 
                     width = 20, anchor="w"))

            self.file_boxes[-1].pack()
    

        self.launch_btn.pack(side="bottom")

    # launches whicever function is passed into Interface init
    def launch(self):
        target_file = ""
        check_count = 0
        
        for file in self.check_boxes:
            if self.check_boxes[file].get() == 1:
                check_count += 1
                target_file = file
                if(check_count > 1):
                    print("Please only select 1 file")
                    return

        if check_count < 1:
            print("Please select a file")
            return

        print(file + " " + str(self.check_boxes[file].get()))

        self.launch_func(self.path, target_file, self.ip)
    
    # wanted to make muli line lambda but couldn't
    # gets path when enter is pressed
    def enter(self, event):
        if event == "":
            return

        self.path = event
        self.draw()