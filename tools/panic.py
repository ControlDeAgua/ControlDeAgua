"Handle a critical error."

import sys


def panic_msg(exc: Exception) -> None:
    messagebox.showerror("Error fatal", f"""ERROR FATAL: Ha habido un error interno. Por favor
reportelo a los desarrolladores, dando tambien esta
informacion adicional:

Info. adicional:

- Tipo de error: {type(exc).__name__}
- Mensaje de error original: {str(exc)}
- Codigo de salida: 1""")
    messagebox.showwarning("Salida forzada", """Se tiene que forzar la salida. Puede
que se haya perdido informacion importante, o se haya
interrumpido un proceso en curso.""")
    try:
        quit()
    except Exception:
        # force the close, using an exit code 1
        # on sys.exit
        sys.exit(1)
