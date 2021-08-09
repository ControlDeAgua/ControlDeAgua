"""
Manual builder for "Control de Agua"
------------------------------------

This file is a tool for building an
executable distribution that doesn't satisfies
the expected scheme. I mean, the original distribution
with a "build" tree like this:

    + build
    |
    |-+ exe.win32-3.8
    | |
    | |-+ lib
    | | [executable apps?]
    | | python3.dll
    | | python38.dll
    | | vcruntime.dll (the name could vary)

On the above tree, we have a "build" folder generated on
a 32-bit Windows machine, using Python 3.8. This is what
we expected from the beggining. But what may happen if we
are using a 64-bit (or even a 86-bit) machine, or another
Python?

That is where "manual_build.py" starts its job. With Python 3.6+,
this file is running "setup.py build" with the native system info,
completely automated.

(NOTE: In most of the machines, you'll have to give admin permissions
to the file to run it, to avoid perission errors from Windows).
"""

import sys

# check if the system info is supported
if sys.platform != "win32":
    exit_msg = """This file was intended for win32 implementations of Python.
By now, we are not supporting any other implementation. If
you really need another implementation, please contact the
developers of this tool."""
    sys.exit(exit_msg)
if sys.version_info < (3, 6, 0):
    exit_msg = """We don't support Python 3.7- usage.
Please try to use a newer version."""
    sys.exit(exit_msg)

# now, import the libraries...
import shutil
import os
import subprocess
from typing import Optional

try:
    from cx_Freeze import __version__ as cxfreeze_version
except ImportError:
    exit_msg = "Could not find cx_Freeze package, which is required."
    sys.exit(exit_msg)

# and start to remove any older library to re-build

def main() -> None:
    "main function."
    if os.path.exists("build"):
        # there is a previous installation, remove it
        shutil.rmtree("build")

    print(f"Using cx_Freeze (version {cxfreeze_version}) to build now...")
    subprocess.run("setup.py build", shell=True)

if __name__ == "__main__":
    try:
        main() # this could fail at any time, so get ready
    except Exception as exc:
        exit_msg = f"Got error while building: {str(exc)}"
        sys.exit(exit_msg)
