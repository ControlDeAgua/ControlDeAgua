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
    sys.exit("""This file was intended for win32 implementations of Python.
By now, we are not supporting any other implementation. If
you really need another implementation, please contact the
developers of this tool.""")
if sys.version_info < (3, 7, 0):
    sys.exit("""We don't support Python 3.6 (or older).
Please try to use a newer version.""")

# now, import the libraries...
import shutil
import os
import subprocess
from typing import Optional


# and start to build (or re-build) a ControlDeAgua distribution
def main() -> None:
    "main function."
    try:
        print("Installing requirements...")
        subprocess.run(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as exc:
        print(f"Could not install dependecies due to a {type(exc).__name__}: {str(exc)}")
        print("Some dependencies may not be installed.")
    if os.path.exists("./build"):
        # there is a previous installation, remove it
        print("\nTrying to remove the previous installation... please wait...")
        shutil.rmtree("build")
        print("Removed any previous executable!")

    print(f"\nUsing cx_Freeze to build now... this could take a while...\n")
    subprocess.run(["setup.py", "build"], shell=True)

if __name__ == "__main__":
    try:
        main() # this could fail at any time, so get ready
        sys.exit(0)
    except Exception as exc:
        sys.exit(f"FATAL: Got error while building: {str(exc)}")
