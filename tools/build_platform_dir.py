# Identify the directory where the executables are stored.

import os
import sys

from typing import Optional


def get_str_python_version() -> str:
    version = sys.version_info
    # equivalent to f"{version.major}.{version.minor}". We
    # decided to use the numeric index to avoid conflicts with
    # a custom tuple.
    return f"{version[0]}.{version[1]}"


def identify_dir(py_name: str, exe_name: str) -> Optional[str]:
    """
    Try to identify the directory where the executables are stored. You should
    pass a `py_name` and an `exe_name` (the Python file and its converted
    executable).
    
    After that, we get all the supported combinations, with Python
    versions:
    
    - 3.6
    - 3.7
    - 3.8
    - 3.9
    - 3.10
    
    and these Windows platforms:
    
    - "win32"
    - "win-amd64"
    
    So, we should get 10 possible paths. Then, we test if `exe_name`
    can be found in one of those directories. If not, we look for
    `py_name` at `C:/Program Files/Control de Agua`.
    
    If none of the paths were found, we raise a GUI error using
    `tkinter.messagebox`. If we found a path, we return it.
    """
    python_versions = [
      (3, 6),
      (3, 7),
      (3, 8),
      (3, 9),
      (3, 10)  # start to consider Python 3.10
    ]
    win_platforms = ["win32", "win-amd64"]
    found_dir = False
    current_path = "C:/Program Files/Control de Agua"
    found_path = ""
    for version in python_versions:
        formatted_version = get_str_python_version(version)
        for platform in win_platforms:
            possible_path = f"{current_path}/build/exe.{platform}-{formatted_version}/{exe_name}"
            if os.path.exists(possible_path):
                found_path = possible_dir
                found_dir = True
                break

    if not found_dir:
        if not os.path.exists(f"{current_path}/{py_name}"):
            messagebox.showerror("Error interno", f"""Error fatal: No se pudo hallar la app: {(py_name, exe_name)}.
Por favor reporte esto en <https://github.com/ControlDeAgua/bug_tracker/issues>""")
            return None
        else:
            found_path = f"{current_path}/{py_name}"
    return found_path
