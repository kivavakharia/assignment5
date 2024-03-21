"""
test_profile.py

Class:
TestProfile: tests new profile methods.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import unittest
import random
from string import ascii_letters, digits
from Profile import Profile


class TestProfile(unittest.TestCase):
    """Tests the profile methods implemented for adding messages and
    friends."""

    def test_add_friend(self):
        """Tests the adding a friend to the profile."""
        profile = Profile()
        name_chars = random.choices(ascii_letters + digits, k=5)
        name = ''.join(name_chars)
        profile.add_friend(name)
        assert name in profile.friends

    def test_get_friends(self):
        """Tests getting a list of a profile's friends."""
        profile = Profile()
        name1_chars = random.choices(ascii_letters + digits, k=5)
        name1 = ''.join(name1_chars)
        name2_chars = random.choices(ascii_letters + digits, k=5)
        name2 = ''.join(name2_chars)

        profile.add_friend(name1)
        profile.add_friend(name2)
        assert profile.get_friends() == profile.friends

    def test_add_sent_message(self):
        """Tests adding a sent message to the profile."""
        profile = Profile()
        exp = {'recipient': 'kiva', 'message': 'hello world'}
        profile.add_sent_message("hello world", "kiva")
        res = profile.sent
        assert exp in res
