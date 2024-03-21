"""
test_ds_messenger.py

Class:
TestDSMessenger: tests server interaction.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import unittest
import random
from string import ascii_letters, digits
from ds_messenger import DirectMessenger


class TestDSMessenger(unittest.TestCase):
    """Tests interaction with the DS Server."""

    def test_send(self):
        """Tests if the send function sends a message to a recipient."""
        user_a = DirectMessenger(dsuserver="168.235.86.101",
                                 username="usernameA", password="passwordA")
        if_send_work = user_a.send("Hello B!", recipient="usernameB")
        assert if_send_work

    def test_retrieve_new(self):
        """Tests if the program can retrieve unread messages."""
        user_a = DirectMessenger(dsuserver="168.235.86.101",
                                 username="usernameA", password="passwordA")
        user_b = DirectMessenger(dsuserver="168.235.86.101",
                                 username="usernameB", password="passwordB")

        msg_chars = random.choices(ascii_letters + digits, k=6)
        msg = ''.join(msg_chars)

        user_a.send(msg, recipient="usernameB")
        new_msg_objs = user_b.retrieve_new()
        unread = []
        for m in new_msg_objs:
            unread.append(m.message)

        assert msg in unread

    def test_retrieve_all(self):
        """Tests if the program can retrieve all messages sent to a profile."""
        user_a = DirectMessenger(dsuserver="168.235.86.101",
                                 username="usernameA", password="passwordA")
        user_b = DirectMessenger(dsuserver="168.235.86.101",
                                 username="usernameB", password="passwordB")

        x = random.choices(ascii_letters + digits, k=6)
        y = random.choices(ascii_letters + digits, k=6)
        msg_1 = ''.join(x)
        msg_2 = ''.join(y)

        user_a.send(msg_1, 'usernameB')
        user_a.send(msg_2, 'usernameB')
        message_objs = user_b.retrieve_all()
        messages = []
        for m in message_objs:
            messages.append(m.message)

        assert all(msg in messages for msg in [msg_1, msg_2])
