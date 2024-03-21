# Kiva Vakharia
# 23234227
# kvakhari@uci.edu


import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.font as tkFont
import os
from ds_messenger import DirectMessenger
from Profile import Profile
from tkinter import ttk, simpledialog, filedialog
from pathlib import Path


class LoginInfo():

    def __init__(self):
        self.server = "168.235.86.101"
        self.username = simpledialog.askstring("USERNAME", "Enter Your Username:")
        self.password = simpledialog.askstring("PASSWORD", "Enter Your Password:")


class MainApp:

    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.contacts = []
        self.dsuserver = None
        self.messenger = None
        self.selected_contact = None
        self.user_profile = None
        self.filepath = None
        self._draw(self.root)

        login = LoginInfo()
        if login.server and login.username and login.password:
            self.load_user(login)
        self.auto_refresh()

    def auto_refresh(self):
        print("Refreshing...")  # Example action
        if self.selected_contact is not None:
            self.get_message_history()
        self.root.after(5000, self.auto_refresh)

    def load_user(self, login):
        """Load a user profile onto the GUI."""
        profile_file = f"{login.username}.dsu"
        profile_dir = os.getcwd()
        self.filepath = os.path.join(profile_dir, profile_file)

        if os.path.exists(self.filepath):
            self.user_profile = Profile()
            self.user_profile.load_profile(self.filepath)
            self.load_contacts()
        else:
            Path(self.filepath).touch()
            self.user_profile = Profile(dsuserver=login.server, username=login.username, password=login.password)
            self.user_profile.save_profile(self.filepath)

        self.username = login.username
        self.password = login.password
        self.contacts = self.user_profile.get_friends()

    def new_server(self):
        self.dsuserver = simpledialog.askstring("Input", "Enter Server Address:")
        self.configure_server()

    def configure_server(self):
        """Connect to the DSU Server and instantiate DirectMessenger."""
        self.user_profile.dsuserver = self.dsuserver
        self.messenger = DirectMessenger(self.dsuserver, self.username, self.password)
        print(f"Configured Server at {self.dsuserver}.")

    def node_select(self, event):
        """Handles contact selection."""
        selected_id = self.posts_tree.selection()[0]  # This is the item ID, not an index
        self.selected_contact = self.posts_tree.item(selected_id, 'text')
        self.get_message_history()

    def get_message_history(self):
        """Displays old and new messages in different colors."""
        self.message_display.config(state='normal')
        self.message_display.delete('1.0', tk.END)

        # Check and display received messages
        if self.messenger:
            messages = self.messenger.retrieve_all()
            for m in messages:
                if m.sender == self.selected_contact and not any(d['message'] == m.message for d in self.user_profile.received):
                    self.user_profile.add_received_message([m])
            self.user_profile.save_profile(self.filepath)
            for m in messages:
                if m.sender == self.selected_contact:
                    display_text = f"From {m.sender}: {m.message}\n"
                    self.message_display.insert(tk.END, display_text, 'received')

        # Display messages from the profile (assuming no messenger or offline)
        else:
            received_messages = self.user_profile.received
            for m in received_messages:
                if m['sender'] == self.selected_contact:
                    display_text = f"From {m['sender']}: {m['message']}\n"
                    self.message_display.insert(tk.END, display_text, 'received')

        # Display sent messages
        sent_messages = self.user_profile.sent
        for m in sent_messages:
            if m['recipient'] == self.selected_contact:
                display_text = f"To {m['recipient']}: {m['message']}\n"
                self.message_display.insert(tk.END, display_text, 'sent')

        self.message_display.config(state='disabled')

    def insert_contact(self, contact: str):
        self.contacts.append(contact)
        id = len(self.contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def add_contact(self):
        contact_name = simpledialog.askstring("Input", "Enter Contact Name:")
        self.insert_contact(contact_name)
        self.user_profile.add_friend(contact_name)
        self.user_profile.save_profile(self.filepath)
    
    def load_contacts(self):
        """Loads and displays the user's friends list in the UI."""
        for i in self.posts_tree.get_children():
            self.posts_tree.delete(i)
        for friend in self.user_profile.friends:
            self.posts_tree.insert('', 'end', text=friend)

    def left_side(self, root):
        """Create the left side of the GUI."""
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
        """Create the right side of the GUI."""
        right_frame = tk.Frame(root, width=650, height=400, bg='#FFF1F5')
        right_frame.grid(row=0, column=1, pady=5, sticky='nsew')
        right_frame.grid_propagate(False)

        self.upper_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=350, bd=1, relief="solid")
        self.upper_section.pack(fill='both', expand=True, side='top')

        self.message_display = st.ScrolledText(self.upper_section, wrap=tk.WORD, width=80, height=20)
        self.message_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.message_display.config(state='disabled')

        self.message_display.tag_configure('sent', foreground='black')
        self.message_display.tag_configure('received', foreground='blue')

        lower_section = tk.Frame(right_frame, bg='#FFF1F5', width=650, height=50, bd=1, relief="solid")
        lower_section.pack(fill='both', side='bottom')

        entry_font = tkFont.Font(family='Georgia', size=12)
        entry = tk.Entry(lower_section, width=60, font=entry_font)
        entry.grid(row=0, column=0, sticky='ew', padx=20) 

        def send_message():
            message = entry.get()
            recipient = self.selected_contact
            self.messenger.send(message, recipient)
            self.user_profile.add_sent_message(message, recipient)
            self.user_profile.save_profile(self.filepath)
            entry.delete(0, 'end')

        button_font = tkFont.Font(family="Georgia", size=9)
        send_button = tk.Button(lower_section, text="SEND", font=button_font, command=send_message)
        send_button.grid(row=0, column=1, sticky='e', padx=10, pady=10)

        server_button = tk.Button(root, text="Connect to Server", font=button_font, command=self.new_server)
        server_button.grid(row=1, column=1, sticky='se', padx=10, pady=10)

        quit_button = tk.Button(root, text="QUIT PROGRAM", font=button_font, command=self.quit_application)
        quit_button.grid(row=2, column=1, sticky='se', padx=10, pady=10)

        user_button = tk.Button(root, text="Load User", font=button_font, command=self.load_user)
        user_button.grid(row=1, column=1, sticky='s', padx=10, pady=10)
    
    def _draw(self, root):
        self.right_side(root)
        self.left_side(root)

    def quit_application(self):
        """Quits the application."""
        self.root.destroy()
