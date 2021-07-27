"""
Anything related to the security door provided to
handle users and accounts.
"""

import json
import hashlib

# stuff for annotations
from typing import Optional
import tkinter

class UserJar:
    """
    Keep the user "jam" on this object "jar"...

    No no, serious now. This class will keep all
    the user data safe and retrive them with simple
    methods.
    """

    def __init__(self, username: str, expected_pwd: str, given_pwd: str, override: bool = False) -> None:
        """
        Constructor method.

        Save the user name ("username") and pass it to
        lowercase.

        The "expected_pwd" and "given_pwd" are only used on
        this method (they won't be saved). Those 2 args are
        used for the door "keys"... The result must be stored
        on "self.safe". Use it as you want.
        """
        # assign the username
        self.legacy_user = username
        self.username = self.legacy_user.lower()

        # test the passwords
        self.safe = True
        if expected_pwd.strip() != given_pwd.strip():
            if not override:
                # you wouldn't mind to raise on console
                raise ValueError(f"Passwords doesn't match: '{expected_pwd.strip()}' and '{given_pwd.strip()}'")
            self.safe = False

    def get(self, original: bool = False) -> None:
        "method overidden from the tkinter Var() instances. This, to avoid big changes to the code."
        if not self.safe:
            # if you overriden the error raising and you don't warn about
            # anything, we are going to return an untrusted user name.
            return "Unverified"
        # if everything is OK, just return the user name
        return self.username if original is not True else self.legacy_user

def get_user_pwd(usr: str) -> str:
    """
    Get the user password.

    The JSON file (users.json) must be like this:

    {
      USERNAME_1: PASSWORD_1,
      USERNAME_2: PASSWORD_2,
      ...
    }
    """
    usr = usr.lower()
    try:
        with open("C:/Program Files/Control de Agua/tools/users.json") as js:
            # the user exists, the value exists too
            return json.loads(js.read())[usr]
    except:
        # use a cryptographic string that (obvoiusly) won't be used on
        # any kind of password!!!
        return hashlib.sha224(b"No one's going to use this password, it must fail when used").hexdigest()

def check(var: UserJar) -> bool:
    "check the admin"
    return open("C:/Program Files/Control De Agua/tools/admin.txt").read().strip() == var.get().strip()

def get_admin_pwd() -> Optional[str]:
    "get the current admin password. If it doesn't exists, just avoid it"
    s = open("C:/Program Files/Control De Agua/tools/admin.txt").read().strip()
    if len(s) < 1:
        return None
    return s
