#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator for the GUI prompt. It also creates the WaterDB.sqlite if it
doesn't exists.

Dirtly built by Diego Ramirez <dr01191115@gmail> (@DiddiLeija on GitHub)
"""

# add some std vars
__author__ = "Diego Ramirez <dr01191115@gmail>"
__version__ = "1.0.1"
__license__ = "MIT"

# import the std libraries:
import os
import sys

# libraries that uses "from package/module import names":
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from os import startfile

# annotation stuff
from typing import Optional

# try to add the PIL 3rth-party module
try:
    from PIL import ImageTk
except ImportError:
    sys.exit("you need the pillow module to continue")

# import my loveful toolkit (I made it by myself!)
from tools.database import (getDatabase,
                            deleteDatabase,
                            ensureDatabase,
                            buildInstertionCommand,
                            get_product_dict,
                            ProductMap)
from tools.windowmanager import *
from tools.users import UserJar, get_user_pwd
from tools.pathfinders import find_our_file
from tools.prefabricated import *

# set some file variables
FILE = find_our_file("db/WaterDB.sqlite", True)

# get sure that the database is correctly generated
ensureDatabase(FILE)
DATABASE, CURSOR = getDatabase(FILE)

# genereate the GUI declarations
class WaterGUI:
    """
    After we defined the database stuff, we can build
    the GUI class. It will contain the tkinter widgets
    and will coordinate them.
    """

    def __init__(self, tk_root: Optional[Tk] = None) -> None:
        "define the Tk root and go to the menu building."
        if tk_root is not None:
            self.root = tk_root
        else:
            self.root = Tk()
        windowTitle(self.root, "Control de Agua", True)
        self.door()

    def door(self) -> None:
        "user door."
        self.door_page = Frame(self.root)
        setSize(self.root, 632, 115)
        self.door_page.grid()
        usr_var = StringVar()
        pwd_var = StringVar()
        actual_odometer = DoubleVar()
        # define a check passer
        def check_user():
            try:
                self.actual_odometer_read = actual_odometer.get()
            except Exception as exc:
                messagebox.showerror("Error: Lectura no reconocida", f"""La lectura del odometro no fue reconocida correctamente.
Verifique e intente de nuevo.

(Mensaje de error: '{str(exc)}')
(Tipo de error: '{type(exc).__name__}')""")
                self.goto("log-retry")
            self.vendor = UserJar(usr_var.get(),
                                  pwd_var.get(),
                                  get_user_pwd(usr_var.get()),
                                  True)
            if not self.vendor.safe:
                messagebox.showerror("Error: datos incorrectos", """Alguno de los datos introducidos fue incorrecto.
Verifique el usuario o la contraseña e intente de nuevo.""")
                self.goto("log-retry")
            else:
                self.goto("door_to_home")
        # user prompt
        usr_l = Label(self.door_page, text="- Introduzca nombre completo", fg="black", bg="whitesmoke",
        font=("Calibri", "12", "bold")).grid(row=0, column=0, sticky="ew")
        usr_prompt = Entry(self.door_page, width=40, font=("Calibri", "12", "normal"),
        textvariable=usr_var).grid(row=0, column=1, sticky="ew")
        # password prompt
        pwd_l = Label(self.door_page, text="- Introduzca contraseña", fg="black", bg="whitesmoke",
        font=("Calibri", "12", "bold")).grid(row=1, column=0, sticky="ew")
        pwd_prompt = Entry(self.door_page, width=40, font=("Calibri", "12", "normal"),
        textvariable=pwd_var, show="*").grid(row=1, column=1, sticky="ew")
        # initial odometer read
        odometer_l = Label(self.door_page, text="- Introduzca la lectura actual del ododmetro", fg="black", bg="whitesmoke",
        font=("Calibri", "12", "bold")).grid(row=2, column=0, sticky="ew")
        odometer_prompt = Entry(self.door_page, width=40, font=("Calibri", "12", "normal"), textvariable=actual_odometer).grid(row=2, column=1, sticky="ew")
        # check the stored data
        check = Button(self.door_page, text="Ingresar ahora", bg="green", fg="white", font=("Calibri", "14", "bold"),
        command=check_user).grid(row=3, column=0, sticky="ew")
        skip_all = Button(self.door_page, text="Cancelar y salir", bg="red", fg="white",
        font=("Calibri", "14", "bold"), command=self.root.quit).grid(row=3, column=1, sticky="ew")

    def home_menu(self) -> None:
        "generate the welcome menu."
        # add an image logo
        if os.path.exists(find_our_file("img/home.jpg")):
            img_file = ImageTk.PhotoImage(file=find_our_file("img/home.jpg"))
            setSize(self.root, 678, 430) # WARNING: take a look for this when inserting a new image!
        else:
            # there is no home image! use a weird supply image
            img_file = ImageTk.PhotoImage(file=find_our_file("img/home-supply.jpg"))
            setSize(self.root, 752, 615)
        self.home = Frame(self.root)
        self.home.grid()
        img_label = Label(self.home, image=img_file)
        img_label.grid(row=0, column=0)
        img_label.image = img_file
        # enter a "new", "view database" and "exit" buttons
        addon = Button(self.home, command=lambda:self.goto("register"), text="Nuevo registro",
        bg="whitesmoke", fg="green").grid(row=1, column=0, sticky="ew")
        go_to_file = Button(self.home, command=self.opendb, text="Abrir base de datos (SQLite)",
        bg="whitesmoke", fg="black").grid(row=2, column=0, sticky="ew")
        log_again = Button(self.home, command=lambda: self.goto("log_again"), text="Cerrar sesion",
        bg="#fff999", fg="red").grid(row=3, column=0, sticky="ew")
        usr_name = Label(self.home, text=f"Usuario actual: {self.vendor.get(original=True)}", font=("Calibri", "12", "italic"),
        bg="white", fg="green").grid(row=4, column=0, sticky="ew")

    def register_page(self) -> None:
        "prompt to enter new things."
        self.rpage = Frame(self.root)
        self.rpage.grid()
        setSize(self.root, 394, 83)
        # data variables to prompt
        self.reading = DoubleVar()
        self.menu_selection = IntVar()
        self.per_unit = ProductMap()
        self.product_index = self.per_unit.get_list()
        self.unit_count = DoubleVar()
        # client prompt
        entry_c = Label(self.rpage, text="1. Producto vendido", bg="whitesmoke", fg="black",
        font=("Calibri", "12", "bold")).grid(row=0, column=0, sticky="ew")
        self.client = get_menubutton(self.rpage,
                                     self.product_index, # use a list shared by all
                                     self.menu_selection,
                                     row=0,
                                     column=1)
        # unit prompt
        entry_u = Label(self.rpage, text="2. Unidades vendidas", bg="whitesmoke", fg="black",
        font=("Calibri", "12", "bold")).grid(row=1, column=0, sticky="ew")
        units_space = Entry(self.rpage, width=40, textvariable=self.unit_count).grid(row=1, column=1, sticky="ew")
        # "check" and "cancel" buttons
        check = Button(self.rpage, text="Entregar ahora", command=self.evaluate, font=("Calibri", "12", "bold"), fg="whitesmoke",
        bg="green").grid(row=2, column=0, sticky="ew")
        cancel = Button(self.rpage, text="Cancelar", command=self.reg_cancel, font=("Calibri", "12", "bold"), fg="whitesmoke",
        bg="red").grid(row=2, column=1, sticky="ew")

    def loop(self) -> None:
        "start looping over the Tk root. Use this when the Tk is not available outside the class."
        self.root.mainloop()

    def analyze_menubutton(self, var: IntVar, menu: Menubutton) -> Optional[str]:
        "fastly analyze the selected IntVar, and return a result"
        # look for a selection
        try:
            index = var.get()
        except Exception as e:
            messagebox.showerror("Parametro inadecuado", f"""En el menu desplegable de opciones, no se ha podido detectar
una seleccion. Verifique e intente de nuevo.
Si le parece haber hallado un error, reportelo a:

    http://github.com/ControlDeAgua/ControlDeAgua/issues/new

(Error: '{str(e)}')""")
            return None

        # return the translated selection
        try:
            return self.product_index[index - 1]
        except Exception as e:
            messagebox.showwarning("Error inesperado", f"""Se ha presentado un error no esperado. Por favor reportelo en
<http://github.com/ControlDeAgua/ControlDeAgua/issues/new>

(Error: '{str(e)}')""")
            return None

    def no_entry(self, p: str, v: str, u: float) -> str:
        "register a sale, but not a monetary entry."
        reason = simpledialog.askstring("Introduzca motivo", "Introduzca un motivo para omitir el ingreso:")
        msg = f"El producto '{p}' (cantidad: {u}) fue tomado por {v}, pero sin ingresos, por la razon: '{reason}'"
        return msg

    def evaluate(self) -> None:
        "get sure everything is all right. After this point is correctly done you will be redirected to self.update_db()"
        # first, extract the string variables
        try:
            vendor = self.vendor.get()
            if len(vendor) < 1:
                messagebox.showerror("Valores de entrada incompletos", """Parece que el programa no ha reconocido alguna entrada de texto.
Revise que los datos introducidos se hallen completos e intente de nuevo.

(Error reportado en consola: 'expected complete strings, but got "" (empty string)')""")
                return None
        except (TclError, ValueError, UnicodeError) as e:
            messagebox.showwarning("Error reportado", f"""Parece que el programa ha rechazado alguna entrada de texto.
Revise los datos introducidos e intente de nuevo.

(Error reportado en consola: '{str(e)}')""")
            return None
        # get the menu selection
        product = self.analyze_menubutton(self.menu_selection, self.client)
        if product is None:
            # error reported at function, then just skip
            return None
        # then, get the number prompt
        try:
            self.actual_odometer_read += self.per_unit.get_odometer_value(product)
        except Exception as e:
            messagebox.showerror("Error al operar el valor del odometro", f"""Verifique e intente de nuevo.

(Mensaje: {type(e).__name__}: {str(e)})""")
            return None
        try:
            per_unit = self.per_unit.get(product)
            unit_count = self.unit_count.get()
        except (TclError, ValueError) as e:
            messagebox.showwarning("Error reportado", f"""Parece que el programa ha rechazado alguna entrada numerica.
Revise los datos introducidos e intente de nuevo.

(Error reportado en consola: '{str(e)}')""")
            return None
        # done? redirect to self.update_db()
        if messagebox.askyesno("¿Seguir?", """¿Desea seguir con el proceso usando las variables definidas?
(Este proceso no se puede deshacer)"""):
            if not messagebox.askyesno("¿Registrar cobro?", """¿Desea registrar un ingreso al negocio por el producto tomado?

Si no, se le va a redirigir a una pagina para
que explique sus motivos."""):
                reason = self.no_entry(product, vendor, unit_count)
            else:
                reason = "N/A"
            self.update_db(self.actual_odometer_read,
                           product,
                           vendor,
                           per_unit,
                           unit_count,
                           reason)

    def goto(self, target: str) -> None:
        "redirect to any point of the GUI"
        if target == "register":
            self.home.grid_remove()
            self.register_page()
        elif target == "go_home":
            self.rpage.grid_remove()
            self.home_menu()
        elif target == "door_to_home":
            self.door_page.grid_remove()
            self.home_menu()
        elif target == "log_again":
            self.home.grid_remove()
            self.door()
        elif target == "log-retry":
            self.door_page.grid_remove()
            self.door()

    def reg_cancel(self) -> None:
        "cancel the registry, go back to the home page."
        if messagebox.askyesno("¿Cancelar?", """¿Desea cancelar el registro?
(Esto no se puede deshacer)"""):
            self.goto("go_home")

    def update_db(self,             # this class
                  reading: float,   # water reading
                  client: str,      # client name
                  vendor: str,      # vendor name
                  per_unit: float,  # cost per unit
                  units: float,     # units
                  reason: str       # why aren't you giving money?
    ) -> None:
        "update the SQLite database and return to the home page."
        # update the SQL
        try:
            buildInstertionCommand(DATABASE, # add the connection object to commit
                                   CURSOR, # add the cursor to extract some stuff and execute
                                   reading,
                                   client,
                                   vendor,
                                   per_unit,
                                   units,
                                   reason)
            # (the function above will format the arguments into a cleaner command,
            # it will run and then save the changes)
        except Exception as e:
            # something crashed, report it and cancel.
            messagebox.showerror("Error fatal al actualizar la base de datos", f"""Los datos no fueron cargados correctamente. Intente
de nuevo o verifique que no haya otros programas trabajando el archivo.

(Error reportado por la base de datos: '{str(e)}')""")
            return None
        # done? go to the last step: going back to the home page
        messagebox.showinfo("Proceso terminado exitosamente", """Los datos han sido devueltos en la base de datos.
Puede generar un nuevo registro o salir desde el menu inicial.""")
        self.goto("go_home")

    def opendb(self):
        "try to open the SQLite. Else, return a Tk error message."
        try:
            startfile(find_our_file("db/WaterDB.sqlite"))
        except OSError as e:
            messagebox.showwarning("Error al abrir archivo", f"""Hubo un error al abrir la base de datos.

(Error reportado en consola: '{str(e)}')""")

# build a main() for the __main__ level
def main() -> None:
    "just run the GUI infrastructure."
    root = Tk()
    gui = WaterGUI(root)
    gui.loop()

# __main__ level execution
if __name__ == '__main__':
    main()
