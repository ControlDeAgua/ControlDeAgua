"""
A GUI much more simple than "water-gui.py". It is generated
to delete or seriously handle the SQLite database
named "WaterDB.sqlite", used on "Control de Agua".
"""

import os
from tkinter import *
from tkinter import messagebox
from typing import Optional
from tools import windowmanager
from tools.database import ensureDatabase

PathName = "C:/Program Files/Control de Agua/db/WaterDB.sqlite"

def destroy_database(pathname: str) -> None:
    "if you can, delete the whole database file. If not, show an error message."
    try:
        if not os.path.exists(pathname):
            messagebox.showerror("Error al eliminar", f"""Parece que no se puede eliminar '{pathname}' porque este archivo no existe.
¿No ha eliminado previamente esta base de datos? Verifique o intente de nuevo.""")
            return None
        os.remove(pathname)
        messagebox.showinfo("Proceso terminado", "El proceso ha terminado exitosamente. La base de datos fue eliminada.")
    except Exception as e:
        messagebox.showerror("Error al eliminar", f"""Parece que no se puede eliminar el archivo '{pathname}'.
Verifique que no haya otros programas abriendo este archivo o no se encuentre bajo otros procesos.

(Error reportado '{str(e)}')""")

class Destroyer:
    # this docstring will be used. DON'T TOUCH IT!
    """En este programa usted puede elegir si destruir
la base de datos que se genera en el
ejecutable 'Control de Agua.exe'. Haga clic en
'Eliminar base de datos' para eliminar definitivamente
el archivo generado. Haga clic en 'Salir' para cancelar."""

    def __init__(self, root: Optional[Tk] = None) -> None:
        "generate the interface."
        if not isinstance(root, Tk):
            # generated inside
            self.root = Tk()
        else:
            # generated outside, don't worry
            self.root = root
        windowmanager.windowTitle(self.root, "Opciones para Eliminar la base de datos")
        self.build()

    def loop(self) -> None:
        "use this if the Tk root was generated inside."
        self.root.mainloop()

    def build(self) -> None:
        "create the GUI"
        self.frame = Frame(self.root)
        self.frame.grid()
        # an info label
        destroy_label = Label(self.frame, text=self.__doc__, bg="whitesmoke", fg="black",
        font=("Calibri", "15", "bold")).grid(row=0, column=0, sticky="ew")
        # delete button
        destroy_b = Button(self.frame, text="Eliminar base de datos", bg="red", fg="white", font=("Calibri", "12", "bold"),
        command=self.destroy).grid(row=1, column=0, sticky="ew")
        # "create again" button
        view_b = Button(self.frame, text="Abrir base de datos", bg="gray", fg="white", font=("Calibri", "12", "bold"),
        command=self.gotoDB).grid(row=2, column=0, sticky="ew")
        # skip button
        safe_b = Button(self.frame, text="Salir", bg="gray", fg="white", font=("Calibri", "12", "bold"),
        command=self.root.quit).grid(row=3, column=0, sticky="ew")

    def destroy(self) -> None:
        "just... destroy the whole database! This is a danger zone, ok? be careful"
        if messagebox.askyesno("¿Proceder?", f"¿Eliminar la base de datos?\n(Este proceso no se puede deshacer)"):
            destroy_database(PathName)
        else:
            messagebox.showinfo("Proceso cancelado", "No se ha eliminado el archivo.")

    def gotoDB(self) -> None:
        "go to the database"
        try:
            os.startfile(PathName)
        except:
            messagebox.showerror("No se pudo abrir", "Verifique e intente de nuevo")

if __name__ == '__main__':
    d = Destroyer()
    d.loop()
