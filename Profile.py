"""
Profile.py

Handles the formatting of post and profile objects in alignment with
the DSU server's protocol.

Classes:
- DSUFileError: raised when there is an error processing a file.
- DSUProfileError: raises when there is an error processing a profile object.
- Post: handles the creation of an individual post.
- Profile: handles the operations of a profile object.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu


import json
import time
from pathlib import Path
from collections import namedtuple



class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to load or save Profile objects to
    file the system.

    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to deserialize a dsu file to a
    Profile object.

    """


class Post(dict):
    """

    The Post class is responsible for working with individual user posts.
    It currently supports two features: A timestamp property that is set
    upon instantiation andwhen the entry object is set and an entry property
    that stores the post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """Set a post's entry."""
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """Get a post's entry."""
        return self._entry

    def set_time(self, time: float):
        """Set the timestamp for a post."""
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        """Get the timestamp of a post."""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32
    DSU server. You will need to use this class to manage the information
    provided by each new user created within your program for a2. Pay close
    attention to the properties and functions in this class as you will need
    to make use of each of them in your program.

    When creating your program you will need to collect user input for
    the properties exposed by this class. A Profile class should ensure
    that a username and password are set, but contains no conventions
    to do so. You should make sure that your code verifies that required
    properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._posts = []
        self.friends = []
        self.all_messages = []

    def add_post(self, post: Post) -> None:
        """

        add_post accepts a Post object as parameter and appends it to the posts
        list. Posts are stored in a list object in the order they are added.
        So if multiple Posts objects are created, but added to the Profile in
        a different order,it is possible for the list to not be sorted by the
        Post.timestamp property. So take caution as to how you implement your
        add_post code.

        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """

        del_post removes a Post at a given index and returns True if successful
        and False if an invalid index was supplied.

        To determine which post to delete you must implement your
        own search operation on the posts returned from the get_posts function
        to find the correct index.

        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """

        get_posts returns the list object containing all posts that have been
        added to the Profile object

        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """

        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w') as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Erros processing DSU file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """

        load_profile will populate the current instance of Profile with data
        stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    for post_obj in obj['_posts']:
                        post = Post(post_obj['entry'], post_obj['timestamp'])
                        self._posts.append(post)
                    self.friends = obj['friends']
                    self.messages = obj['messages']
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()

    def add_friend(self, friend_user: str) -> None:
        """Add a username to the user's list of friends."""
        if not friend_user in self.friends:
            self.friends.append(friend_user)

    def get_friends(self) -> list:
        """Get the user's list of friends."""
        return self.friends

    def add_message(self, messages: list) -> None:
        """Add a message to the DSU profile."""
        for dm in messages:
            format = {'sender': dm.sender, 'message': dm.message, 
                      'timestamp': dm.timestamp, 'if_read': False}
            self.all_messages.append(format)
            

    def get_messages(self) -> dict:
        """Get all the messages sent to the user."""
        return self.all_messages
    
    def mark_read(self, message):
        pass

from ds_messenger import DirectMessage

test_profile = Profile(username="tester_name", password="lmfao")
filepath = r'C:\Assignment5\tester.dsu'
test_profile.add_friend("prabhtaj")
test_profile.add_friend("armanbains")
message = [DirectMessage(sender='aryan_manglm', message='a tester message', timestamp=time.time())]
test_profile.add_message(message)
test_profile.save_profile(filepath)