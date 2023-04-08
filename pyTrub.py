import os.path
import pickle
import socket
import time
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox

import customtkinter as ctk

# Variables
Font_tuple = ("Comic Sans MS", 13, "bold")

required_file_name = ""
downloadingPath = "YOUR STORAGE FILE PATH WHERE THE FILES WILL BE DOWNLOADED || ALSO BE EDITED FROM THE PROGRAMM"
ToUploadPath = ""

host = socket.gethostname()
port = 12345

FileNameList = []

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
# Functions
FileNameList = pickle.loads(client_socket.recv(20886))

class MyWindow:
    def __init__(self, master):
        self.value = None
        self.master = master

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.master.title("P Trub")
        self.master.geometry("600x500")

        self.download_button = ctk.CTkButton(self.master, text="Download", command=self.donwloadAFile_callback,
                                             width=100)
        self.download_button.place(x=25, y=10)

        self.file_name_entry = ctk.CTkEntry(self.master, placeholder_text="Search file")
        self.file_name_entry.place(x=155, y=10)
        self.file_name_entry.bind("<KeyRelease>", lambda event: self.on_change())

        upload_button = ctk.CTkButton(self.master, text="Upload", width=100, command=self.create_Upload_Window)
        upload_button.place(x=325, y=10)

        refresh_button = ctk.CTkButton(self.master, text="Refresh", command=self.refresh, width=100)
        refresh_button.place(x=465, y=10)

        self.listView = tk.Listbox(self.master, background="dark grey", width=68, height=20, font=Font_tuple)
        self.ReClearListView()
        self.listView.place(x=30, y=80)

        main_manu = tk.Menu(self.master)
        main_manu.add_command(label="File",command=self.selectDirectory)
        main_manu.add_command(label="Exit",command=self.master.quit)

        self.master.config(menu=main_manu)
    def refresh(self):
        global FileNameList
        client_socket.send(pickle.dumps(["r"]))
        FileNameList = pickle.loads(client_socket.recv(10248))
        self.ReClearListView()

    def on_change(self):
        inner_value = self.file_name_entry.get()
        i = 0
        self.listView.delete(0, tk.END)
        for x in range(len(FileNameList)):
            if inner_value.lower() in FileNameList[x].lower():
                self.listView.insert(i, FileNameList[x])
    def ReClearListView(self):
        self.listView.delete(0, tk.END)
        for i in range(len(FileNameList)):
            self.listView.insert(i, FileNameList[i])

    def donwloadAFile_callback(self):
        selection = self.listView.curselection()
        if selection:
            index = selection[0]
            self.value = self.listView.get(index)

            browseButton = pickle.dumps(["g", self.value])

            client_socket.send(browseButton)
            self.recv_file()

    def recv_file(self):
        with open(downloadingPath + "/" + self.value, 'ab') as f:
            while True:
                got = pickle.loads(client_socket.recv(4180080))
                if got[0] == '0':
                    break
                else:
                    f.write(got[1])
        flag = messagebox.askyesno("File Downloaded","Do You want To Open File Folder?")

        if flag:
            os.startfile(downloadingPath)

    def create_Upload_Window(self):

        self.App_ = ctk.CTk()
        self.App_.title("Select File")
        self.App_.geometry("400x300")
        self.filePath = ctk.CTkLabel(self.App_, text="File Path")
        self.filePath.place(x=10, y=10)

        browse_button = ctk.CTkButton(self.App_, text="Browse", command=self.browseAFile, width=100)
        browse_button.place(x=10, y=50)

        upload_button = ctk.CTkButton(self.App_, text="Upload", command=self.UploadFile)
        upload_button.place(x=150, y=50)

        self.App_.mainloop()

    def UploadFile(self):
        try:
            with open(ToUploadPath, 'rb') as f:
                client_socket.send(pickle.dumps(["u", os.path.basename(ToUploadPath)]))

                data = f.read(408008)

                while data:
                    client_socket.send(pickle.dumps(['1', data]))
                    data = f.read(408008)
                    time.sleep(0.1)

                client_socket.send(pickle.dumps(['0']))

        except:
            pass
        self.App_.destroy()

    def browseAFile(self):
        global ToUploadPath
        ToUploadPath = tkinter.filedialog.askopenfilename()
        self.filePath.configure(text=ToUploadPath)
    def selectDirectory(self):
        global downloadingPath
        downloadingPath = tkinter.filedialog.askdirectory()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MyWindow(root)
    root.mainloop()

# Initializing
