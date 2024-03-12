"""
ds_protocol.py

"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import json
from collections import namedtuple

ResponseTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

# {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

def message_format(entry: str, recipient: str, timestamp: str, token: str = '') -> str:
    """Send a directmessage to another DS user (in the example bellow, ohhimark)"""
    return json.dumps({"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": timestamp}})

# {"token":"user_token", "directmessage": "new"}

def request_unread(token: str = ''):
    """Request unread messages from the DS server."""
    return json.dumps({"token": token, "directmessage": "new"})

# {"token":"user_token", "directmessage": "all"}

def request_all(token: str = ''):
    """Request all messages from the DS server."""
    return json.dumps({"token": token, "directmessage": "all"})


def process_response(json_msg: str):
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
