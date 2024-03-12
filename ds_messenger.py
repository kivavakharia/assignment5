"""
ds_messenger.py

"""

# Kiva Vakharia
# kvakhari@uci.edu
# 23234227

import socket
from ds_protocol import *


class FailedInteraction(Exception):
    """FailedInteraction is raised when a client-server operation
    fails to occur."""


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
		
    def send(self, message:str, recipient:str) -> bool:
       # must return true if message successfully sent, false if send failed.
        port = 3021

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.dsuserver, port))
        
            if not sock:
                return False

            try:
                msg = DirectMessage()
                msg_resp = send_message(message, msg.username, msg.timestamp, self.timestamp)




                return True

            except FailedInteraction as e:
                print(f"ERROR: {e}. \nFailed to interact with server.")
                return False
        

		
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        pass
 
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        pass