"""
ds_protocol.py

Formats commands in order to adhere to the DS Server.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import json
from collections import namedtuple

ResponseTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def format_join(username: str, password: str, token: str = "") -> str:
    """Format the join command to comply with the server."""
    return json.dumps({"join": {"username": username, "password": password,
                                "token": token}})


def post_format(token: str, entry: str, timestamp: str) -> str:
    """Format the post command to comply with the server."""
    return json.dumps({"token": token,
                       "post": {"entry": entry, "timestamp": timestamp}})


def bio_format(token: str, entry: str, timestamp: str) -> str:
    """Format the bio command to comply with the server."""
    return json.dumps({"token": token,
                       "bio": {"entry": entry, "timestamp": timestamp}})


def format_send(entry: str, recipient: str, timestamp: str, token: str = ''):
    """Send a directmessage to another DS user"""
    return json.dumps({"token": token, "directmessage":
                       {"entry": entry, "recipient": recipient,
                        "timestamp": timestamp}})


def format_unread(token: str = ''):
    """Request unread messages from the DS server."""
    return json.dumps({"token": token, "directmessage": "new"})


def format_all(token: str = ''):
    """Request all messages from the DS server."""
    return json.dumps({"token": token, "directmessage": "all"})


def extract_json(json_msg: str):
    """
    Parse a JSON response from the DSP server and convert it to a DataTuple.

    param json_msg: a string holding the message from the data file
    """
    try:
        obj = json.loads(json_msg)
        response_type = obj['response']['type']
        msg = obj['response'].get('message', '')
        token = obj['response'].get('token', '')

    except KeyError:
        print("Unexpected JSON.")
        return ResponseTuple('error', 'Unexpected JSON format', '')

    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return ResponseTuple('error', 'JSON decode error', '')

    return ResponseTuple(response_type, msg, token)
