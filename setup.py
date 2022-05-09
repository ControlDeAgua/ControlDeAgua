"""
- setup.py - Python

    ...Setup file for converting dirty Python "eggs" into
    beautiful, huge Executable "dinosaurs"... hahaha...

No, seriously now. This setup() uses the Python cx_Freeze
package to, well, "freeze" the Python scripts (.py) into standalone
executables (.exe).

Also, it changes the script names, so that way you can format a
cleaner executable, adapted to the specified language and client.

This script uses a "Win32GUI" base (from cx_Freeze) to entirely destroy
the console (because the errors will be handled as message boxes!)
"""

import sys

try:
    from cx_Freeze import Executable, setup
except ImportError:
    sys.exit("error: you need the cx_freeze package to run the setup() file")

gui_base = None

if sys.platform == "win32":
    gui_base = "Win32GUI"

exe = [
    Executable("water-gui.py", target_name="Control de Agua.exe", base=gui_base),
    Executable(
        "delete-db.py", target_name="Eliminar archivo SQLite.exe", base=gui_base
    ),
    Executable("config-gui.py", target_name="Configuracion.exe", base=gui_base),
    Executable("admin-pwd.py", target_name="Cambiar clave de administrador.exe"),
    Executable(
        "manage-products.py",
        target_name="Manejar la informacion de producto.exe",
        base=gui_base,
    ),
]

setup(
    name="Control de Agua - MX",
    version="1.0",  # just like a... patch?
    description="""Esta es una aplicacion para manejar
la venta de garrafones en una base de datos
privada mediante una interfaz simple pero
suficiente para la necesidad del usuario.

En el sitio de Configuracion, el administrador del
negocio puede manejar las cuentas de los usuarios.

Desarrollado por Diego Ramirez <dr01191115@gmail.com> (@DiddiLeija en GitHub)""",
    executables=exe,
)
