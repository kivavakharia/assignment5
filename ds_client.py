"""
ds_client.py

Connects and posts to a DSU server.

Functions:
- send: sends a post to a DSU server.
- cmd: initializes socket.
- join_cmd: formats the join command to send.
- post_cmd: formats the post command to send.
- bio_cmd: formats the bio command to send.
"""

# Kiva Vakharia
# kvakhari@uci.edu
# 23234227

import socket
import json
import time
from ds_protocol import format_join, post_format, bio_format


class FailedInteraction(Exception):
    """FailedInteraction is raised when a client-server operation
    fails to occur."""


def send(server: str, port: int, username: str, password: str, message: str,
         bio: str = None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server, port))

        if not sock:
            return False

        try:
            join_resp = join_cmd(sock, username, password)
            join_param = join_resp.get('response', {}).get('type')
            if not join_resp or join_param != 'ok':
                print("Unable to join.")
                raise FailedInteraction

            token = join_resp['response']['token']

            if message:
                post_resp = post_cmd(sock, token, message)
                if not post_resp:
                    print("ERROR: Connection issue or bad response.")
                elif post_resp.get('response', {}).get('type') != 'ok':
                    print("Unable to post message.")
                    print(f"Server message: {post_resp}")
                    raise FailedInteraction

            if bio:
                bio_resp = bio_cmd(sock, token, bio)
                bio_param = bio_resp.get('response', {}).get('type')
                if not bio_resp or bio_param != 'ok':
                    raise FailedInteraction

            return True

        except FailedInteraction as e:
            print(f"ERROR: {e}. \nFailed to interact with server.")
            return False


def cmd(sock, command):
    """Iniitalize socket and send formatted information to the server."""
    try:
        snd = sock.makefile('w')
        recv = sock.makefile('r')

        snd.write(command + '\r\n')
        snd.flush()

        resp = recv.readline()
        return json.loads(resp)

    except Exception:
        print("ERROR: Failed to send ", {command})
        return None


def join_cmd(sock, username, password):
    """Authenticate the user on the server."""
    formatted = format_join(username, password)
    return cmd(sock, formatted)


def post_cmd(sock, token, message):
    """Send a formatted post to the server."""
    formatted = post_format(token, message, str(time.time()))
    return cmd(sock, formatted)


def bio_cmd(sock, token, bio):
    """Send a formatted user's bio to the server."""
    formatted = bio_format(token, bio, str(time.time()))
    return cmd(sock, formatted)
