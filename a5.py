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
import ds_messenger
from ds_messenger import DirectMessenger
from Profile import Profile
from tkinter import ttk, simpledialog, filedialog
from pathlib import Path


class LoginInfo():

    def __init__(self):
        self.server = "168.235.86.101"
        self.username = simpledialog.askstring("USERNAME", "Enter Your Username:")
        self.password = simpledialog.askstring("PASSWORD", "Enter Your Password:")


class MainApp(tk.Tk):

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.username = None
        self.password = None
        self.dsuserver = None
        self.messenger = None
        self.filepath = None
        self.user_profile = None
        self.contacts = []
        self._draw(self.root)

        login = LoginInfo()
        if login.server and login.username and login.password:
            self.load_user(login)
        else:
            self.quit()

    def load_user(self, login):
        profile_file = f"{login.username}.dsu"
        profile_dir = os.getcwd()
        self.filepath = os.path.join(profile_dir, profile_file)

        # Ensure the directory exists
        os.makedirs(profile_dir, exist_ok=True)

        if os.path.exists(self.filepath):
            self.user_profile = Profile()
            self.user_profile.load_profile(self.filepath)
            self.load_contacts()
        else:
            Path(self.filepath).touch()
            self.user_profile = Profile(dsuserver=login.server, username=login.username, password=login.password)
            self.user_profile.save_profile(self.filepath)
        self.messenger = DirectMessenger(dsuserver=login.server, username=login.username, password=login.password)

        self.username = login.username
        self.password = login.password
        self.contacts = self.user_profile.get_friends()

    def switch_user(self):
        """Allows the user to switch to a different user profile."""
        # TODO: change this code.
        new_profile_path = filedialog.askopenfilename(title="Open Profile", filetypes=[("DSU Files", "*.dsu")])
        if new_profile_path:
            new_profile = Profile()
            new_profile.load_profile(new_profile_path)
            self.messenger = DirectMessenger(dsuserver=new_profile.dsuserver, username=new_profile.username, password=new_profile.password)
            self.profile = new_profile
            self.currentFilePath = new_profile_path  # Update the current file path to the new profile
            
            self.load_users()
            self.clear_messages()
            tk.messagebox.showinfo("Switch User", "Switched user successfully.")
        else:
            tk.messagebox.showinfo("Switch User", "User switch cancelled.")

    def configure_server(self):
        self.dsuserver = simpledialog.askstring("Input", "Enter Server Address:")
        self.messenger = DirectMessenger(self.dsuserver)
        print(f"Configured Server at {self.dsuserver}.")

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        self.selected = self.contacts[index]

    def display_messages(self, root):
        if self.messenger:
            all_messages = self.messenger.retrieve_all()
            for m in all_messages:
                text = tk.Text(root, height=5, width=20)
                text.pack(padx=10, pady=10)
                text.insert(tk.END, m.message)
                print(m.message)

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

    def load_contacts(self):
        """Loads and displays the user's friends list in the UI."""
        for i in self.posts_tree.get_children():
            self.posts_tree.delete(i)
        for friend in self.user_profile.friends:
            self.posts_tree.insert('', 'end', text=friend)

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

        self.upper_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=350, bd=1, relief="solid")
        self.upper_section.pack(fill='both', expand=True, side='top')

        lower_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=50, bd=1, relief="solid")
        lower_section.pack(fill='both', side='bottom')

        entry_font = tkFont.Font(family='Georgia', size=12)
        entry = tk.Entry(lower_section, width=60, font=entry_font)
        entry.grid(row=0, column=0, sticky='ew', padx=20) 

        def send_message():
            message = entry.get()
            dm = DirectMessenger('168.235.86.101', self.username, self.password)
            dm.send(message, self.selected)
            print(message)

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
