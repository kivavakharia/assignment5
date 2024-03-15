"""
test_ds_messenger.py

"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import unittest
from ds_messenger import DirectMessage, DirectMessenger


class TestDSMessenger(unittest.TestCase):

    def test_send(self):
        A = DirectMessenger(dsuserver="168.235.86.101", username="usernameA", password="passwordA")
        if_send_work = A.send("Hello B!", recipient="usernameB")
        assert if_send_work

    def test_retrieve_new(self):
        A = DirectMessenger(dsuserver="168.235.86.101", username="usernameA", password="passwordA")
        B = DirectMessenger(dsuserver="168.235.86.101", username="usernameB", password="passwordB")
        msg = "Testing New Messages, to UserB"
        A.send(msg, recipient="usernameB")
        new_messages_B = B.retrieve_new()
        assert new_messages_B[0].message == msg

    def test_retrieve_all(self):
        pass
