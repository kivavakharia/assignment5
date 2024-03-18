"""
a5.py

Starting point of the Assignment 5 module.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import tkinter as tk
import tkinter.font as tkFont
import os
import ds_client
import ds_messenger
from ds_messenger import DirectMessenger
from Profile import Profile
from tkinter import ttk, simpledialog


class MainApp():
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.dsuserver = None
        self.contacts = []
        self._draw(self.root)

    def load_user(self):
        self.username = simpledialog.askstring("Input", "Enter your username:")
        self.password = simpledialog.askstring("Input", "Enter your password")
        
        self.user_profile = Profile(username=self.username, password=self.password)
        self.contacts = self.user_profile.get_friends()

        self.messenger.username = self.username
        self.messenger.password = self.password

        ds_client.send('168.235.86.101', 3021, self.username, self.password, '')

        with open("profile.dsu", 'w'):
            path = os.path.abspath("profile.dsu")
            self.user_profile.save_profile(path)

        if True:
            #TODO: if user is valid and matches the password, continue. Else: quit the program.
            pass


    def configure_server(self):
        self.dsuserver = simpledialog.askstring("Input", "Enter Server Address:")
        self.messenger = DirectMessenger(self.dsuserver)
        print(f"Configured Server at {self.dsuserver}.")

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        self.selected = self.contacts[index]

    def quit_app(self, root):
        root.destroy()

    def add_contact(self):
        contact_name = simpledialog.askstring("Input", "Enter Contact Name:")
        self.insert_contact(contact_name)
        self.user_profile.add_friend(contact_name)
        # TODO: get rid of this
        self.user_profile.save_profile("C:\Assignment5\profile.dsu")

    def insert_contact(self, contact: str):
        self.contacts.append(contact)
        id = len(self.contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def left_side(self, root):
        left_frame = tk.Frame(root, width=200, height=400, bg='#FFF1F5', 
                            bd=1, relief="solid")
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        left_title = tk.Frame(left_frame, bg="white", height=25, bd=1, 
                            relief="solid")
        left_title.pack(fill='x', padx=10, pady=5)
        left_title.pack_propagate(False)  # Prevent resizing to fit the label

        label_font = tkFont.Font(family="Georgia", size=12)
        label = tk.Label(left_title, text="CONTACTS", bg="white", font=label_font)
        label.pack()
        left_frame.pack_propagate(False)

        self.posts_tree = ttk.Treeview(left_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        button_font = tkFont.Font(family="Georgia", size=10)
        button = tk.Button(root, text="Add Contact", width=25, font=button_font, 
                        command=self.add_contact)
        button.grid(row=1, column=0, sticky='sw', padx=10, pady=10)

    def right_side(self, root):
        right_frame = tk.Frame(root, width=650, height=400, bg='#FFF1F5')
        right_frame.grid(row=0, column=1, pady=5, sticky='nsew')
        right_frame.grid_propagate(False)

        upper_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=350, bd=1, relief="solid")
        upper_section.pack(fill='both', expand=True, side='top')

        lower_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=50, bd=1, relief="solid")
        lower_section.pack(fill='both', side='bottom')

        entry_font = tkFont.Font(family='Georgia', size=12)
        entry = tk.Entry(lower_section, width=60, font=entry_font)
        entry.grid(row=0, column=0, sticky='ew', padx=20) 

        def send_message():
            message = entry.get()
            try:
                dm = DirectMessenger('168.235.86.101', self.username, self.password)
                dm.send(message, self.selected)
                print(message)
            
            except ds_messenger.FailedInteraction:
                print("dumbo")

        button_font = tkFont.Font(family="Georgia", size=9)
        send_button = tk.Button(lower_section, text="SEND", font=button_font, command=send_message)
        send_button.grid(row=0, column=1, sticky='e', padx=10, pady=10)

        server_button = tk.Button(root, text="Configure Server", font=button_font, command=self.configure_server)
        server_button.grid(row=1, column=1, sticky='se', padx=10, pady=10)

        user_button = tk.Button(root, text="Load User", font=button_font, command=self.load_user)
        user_button.grid(row=1, column=1, sticky='s', padx=10, pady=10)

    def _draw(self, root):
        self.right_side(root)
        self.left_side(root)


def main():
    root = tk.Tk()
    root.title("ICS 32 Distributed Social Messenger")
    root.config(bg="#FFCAD4")
    root.geometry("950x500")
    MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
