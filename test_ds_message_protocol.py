"""
test_ds_message_protocol.py

"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import unittest
import ds_protocol


class TestDSMessageProtocol(unittest.TestCase):

    def test_message_format(self):
        token = "user_token"
        entry = "Hello World!"
        recipient = "ohhimark"
        timestamp = "1603167689.3928561"
        resp = ds_protocol.format_send(entry, recipient, timestamp, token)
        exp = '{"token": "user_token", "directmessage": {"entry": "Hello World!", "recipient": "ohhimark", "timestamp": "1603167689.3928561"}}'
        assert resp == exp

    def test_unread_request_format(self):
        token = "user_token"
        resp = ds_protocol.format_unread(token)
        exp = '{"token": "user_token", "directmessage": "new"}'
        assert resp == exp

    def test_all_request_format(self):
        token = "user_token"
        resp = ds_protocol.format_all(token)
        exp = '{"token": "user_token", "directmessage": "all"}'
        assert resp == exp
