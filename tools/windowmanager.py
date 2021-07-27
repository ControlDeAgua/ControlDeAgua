"""
This file includes the setSize function, useful for defining the size
of a Tk window, and the windowTitle function, to format the Tk window
name.
"""

__all__ = ["setSize", "windowTitle"]

import sys
import tkinter

def setSize(obj: tkinter.Tk, a: int, b: int) -> None:
    "use the 'obj' attributes, and you won't need to import tkinter again!"
    obj.minsize(a, b)
    obj.maxsize(a, b)

def windowTitle(obj: tkinter.Tk, title: str, add_platform: bool = False) -> None:
    "set the Tk window title."
    if add_platform:
        # if add_platform is True, title becomes to f'{title} on {sys.platform}'
        title = f"{title.rstrip()} on {sys.platform}"
    obj.title(title)
