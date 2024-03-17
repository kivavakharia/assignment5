"""
ds_messenger.py

"""

# Kiva Vakharia
# kvakhari@uci.edu
# 23234227

import socket
import time
import json
from ds_protocol import format_join, format_send, format_unread, format_all


class FailedInteraction(Exception):
    """FailedInteraction is raised when a client-server operation
    fails to occur."""


class DirectMessage:
    def __init__(self, sender=None, message=None, timestamp=None):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.sock = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password


    def send(self, message:str, recipient:str) -> bool:
        """Send a message to a user on the DSU server."""
        # must return true if message successfully sent, false if send failed.

        if not self.token:
            self._login_user()
        if not self.token:
            return False

        send_msg = format_send(message, recipient, str(time.time()), self.token)
        resp = self._command_to_server(send_msg)
        print(resp)
        return resp and resp.get('response', {}).get('type') == 'ok'

    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        if not self.token:
            self._login_user()
        if not self.token:
            return []

        see_unread = format_unread(self.token)
        resp = self._command_to_server(see_unread)
        if resp and resp.get('response', {}).get('type') == 'ok':
            unread_messages = resp['response'].get('messages', [])
            return [DirectMessage(m['from'], m['message'], m['timestamp']) for m in unread_messages]
        return []


    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        self._socket_create()
        if not self.token:
            self._login_user()
        if not self.token:
            return []

        see_all = format_all(self.token)
        resp = self._command_to_server(see_all)
        if resp and resp.get('response', {}).get('type') == 'ok':
            all_messages = resp['response'].get('messages', [])
            print("all messages: ", all_messages)
            return [DirectMessage(m['from'], m['message'], m['timestamp']) for m in all_messages]
        return []


    def _socket_create(self):
        """Create and return a socket connecting to the DSU server."""
        try:
            port = 3021
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, port))
            self.sock = sock
            return sock

        except Exception as e:
            print(f"Could not connect to server: {e}")


    def _login_user(self):
        """Log the user into the DSU server."""
        self._socket_create()
        join_cmd = format_join(self.username, self.password)
        resp = self._command_to_server(join_cmd)
        print(f"Login response: {resp}")

        if resp and resp.get('response', {}).get('type') == 'ok':
            self.token = resp['response']['token']

        else:
            raise FailedInteraction("Failed to log in.")


    def _command_to_server(self, cmd):
        """Send a command to the DSU server."""
        try:
            snd = self.sock.makefile('w')
            recv = self.sock.makefile('r')

            snd.write(cmd + '\r\n')
            snd.flush()

            resp = recv.readline()
            return json.loads(resp)

        except Exception:
            print("ERROR: Failed to send ", {cmd})
            return None


    def close_sock(self):
        """Closes the current open socket."""
        if self.sock:
            self.sock.close()
            self.sock = None


# if __name__ == "__main__":
#    messengerA = DirectMessenger(dsuserver="168.235.86.101", username="usernameA", password="passwordA")
#    messengerB = DirectMessenger(dsuserver="168.235.86.101", username="usernameB", password="passwordB")
#    successAtoB = messengerA.send("Hello B!", recipient="usernameB")
#    print("Message sent from A to B:", successAtoB)
#    new_messages_B = messengerB.retrieve_new()
#    print("New messages for B:", new_messages_B)
#    successBtoA = messengerB.send("Hi A", recipient="usernameA")
#    print("Message sent from B to A:", successBtoA)
#    time.sleep(1)  # Wait a bit for the server to process the message
#    new_messages_A = messengerA.retrieve_new()
#    print("New", new_messages_A)
#    all_messages_A = messengerA.retrieve_all()
#    for m in all_messages_A:
#        print(m)
#    print("All messages for A:", all_messages_A)
#    messengerA.close_sock()
#    messengerB.close_sock()

# message format: {'message': 'Hi A, this is B!', 'from': 'usernameB', 'timestamp': '1710359081.003671'}