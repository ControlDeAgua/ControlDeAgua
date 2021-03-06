"""
Bienvenido a la configuracion de la aplicacion.
Aqui, puede ver la informacion de usuarios, y ver
las ventas desde diferentes formatos.
"""

import json
from tkinter import *
from tkinter import messagebox
from idlelib.textview import view_text
from os import startfile
from tools.pathfinders import identify_dir, find_our_file
from tools.database import *
from tools.datetimes import compare_dates
from tools.panic import panic_msg
from tools.prefabricated import get_menubutton
from tools.windowmanager import *
from tools.users import check, get_admin_pwd

# annotation stuff
from typing import Callable, Optional

DB, CUR = getDatabase(find_our_file("db/WaterDB.sqlite"))

class GUI:
    """
    GUI class for this feature.
    """

    def __init__(self, root: Tk) -> None:
        "constructor method."
        # handle the root internally
        self.root = root
        windowTitle(self.root, "App de configuracion")
        # generate the menu directly
        if get_admin_pwd() is not None:
            # there is an admin password, ask for it
            self.ensureAdmin(next_page=lambda: self.go("get-in"))
        else:
            # just advice of the vulnerability and go ahead
            messagebox.showwarning("Advertencia: Cuenta de Administrador desprotegida", """La cuenta del administrador no tiene
actualmente una clave de acceso. Esto puede ser riesgoso,
pues cualquier usuario podra ingresar a las opciones
y privilegios del administrador.""")
            self.go("get-in-directly")

    def ensureAdmin(self, next_page: Optional[Callable] = None) -> Optional[bool]:
        "get sure the admin is here..."
        self.adminport = Frame(self.root)
        self.adminport.grid()
        entry_var = StringVar()
        # we need a door helper
        def submit():
            if len(entry_var.get().strip()) < 1:
                messagebox.showerror("Error", "Contraseña vacia.")
            if check(entry_var):
                # go to the next place
                if next_page is not None:
                    # it is a function, go there
                    next_page()
                else:
                    # just get back
                    return True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return False
        # create the widgets
        door_l = Label(self.adminport, text="Ingrese contraseña del administrador del programa:",
        font=("Calibri", "14", "bold")).grid(row=0, column=0, sticky="ew")
        door_e = Entry(self.adminport, textvariable=entry_var, width=40,
        show="*", font=("Calibri", "14", "normal")).grid(row=0, column=1, sticky="ew")
        skip = Button(self.adminport, text="Cancelar y salir", command=self.root.quit, bg="red",
        fg="white", font=("Calibri", "14", "bold")).grid(row=1, column=0, sticky="ew")
        submit = Button(self.adminport, text="Ingresar", command=submit, bg="green",
        fg="white", font=("Calibri", "14", "bold")).grid(row=1, column=1, sticky="ew")

    def showUsers(self) -> None:
        "show the users"
        user_map = {}
        try:
            with open(find_our_file("tools/users.json"), "r") as f:
                user_map = json.loads(f.read())
        except Exception as e:
            if len(open(find_our_file("tools/users.json"), "r").read().strip()) < 1:
                open(find_our_file("tools/users.json"), "w").write("{}")
                panic_msg(e)
            else:
                messagebox.showwarning("?", f"error: {str(e)}")
        s = ""
        for k, v in user_map.items():
            s += f"- {k}: {v}\n"
        view_text(self.root, "Usuarios y contraseñas registradas", s)

    def notDefined(self, arg: str) -> None:
        "default for not-implemented or not-defined features."
        messagebox.showinfo(str(NotImplemented), f"Funcion/elemento sin definir: <{arg}>")

    def menu(self) -> None:
        "generate the menu gui."
        # use a frame to pack all the menu stuff
        self.welcome = Frame(self.root)
        self.welcome.grid()
        # use __doc__ for the description
        descr = Label(self.welcome, text=__doc__, bg="white", fg="black",
        font=("Calibri", "14", "normal")).grid(row=0, column=0, sticky="ew")
        # user registry function
        new_usr = Button(self.welcome, text="Nuevo usuario", bg="whitesmoke", fg="black", font=("Calibri", "14", "bold"),
        command=lambda: self.go("home -> register")).grid(row=1, column=0, sticky="ew")
        # remove a user
        del_usr = Button(self.welcome, text="Eliminar usuario", bg="whitesmoke", fg="black", font=("Calibri", "14", "bold"),
        command=lambda: self.go("home -> del_user")).grid(row=2, column=0, sticky="ew")
        # view the registered users
        view_usrs = Button(self.welcome, text="Ver lista de usuarios", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: self.go("view users")).grid(row=3, column=0, sticky="ew")
        # view a report
        view_report = Button(self.welcome, text="Ver registro de ventas", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: self.go("view registry")).grid(row=4, column=0, sticky="ew")
        # docs button
        view_docs = Button(self.welcome, text="Ver el instructivo en linea", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: startfile("https://controldeagua.github.io/ControlDeAgua-docs")).grid(row=5, column=0, sticky="ew")
        # manage the product info
        manage_product = Button(self.welcome, text="Manejar la informacion de producto", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: self.go("manage product info")).grid(row=6, column=0, sticky="ew")
        # exit button
        get_out = Button(self.welcome, text="Salir de la pagina", bg="red", fg="white",
        font=("Calibri", "14", "bold"), command=self.root.quit).grid(row=7, column=0, sticky="ew")

    def del_user_internal(self) -> None:
        "internal deletion for the selected user (self.del_name)"
        if not messagebox.askyesno("¿Proceder?", """¿En verdad desea proceder con esta accion?
(Una vez realizada la accion, ya no se podra acceder con esa cuenta,
pero los registros a su nombre no se eliminan)"""):
            return None
        try:
            selected_usr = self.del_name.get().strip()
            if len(selected_usr) < 1: raise ValueError('Expected non-empty strings, got ""')
            # update
            to_save = {}
            with open(find_our_file("tools/users.json"), "r") as f:
                f_parsed = json.loads(f.read())
                if selected_usr not in f_parsed: raise KeyError("El usuario no existe")
                for k, v in f_parsed.items():
                    if k == selected_usr:
                        # don't save that user
                        continue
                    to_save[k] = v
            with open(find_our_file("tools/users.json"), "w") as wf:
                wf.write(json.dumps(to_save))
        except Exception as e:
            messagebox.showerror("Error al registrar", f"""Ha sucedido un error al retirar al usuario. Puede que
haya dejado la entrada totalmente vacia o haya agregado algun caracter no
permitido. Verifique e intente de nuevo.

(Error: '{str(e)}')""")
            if len(open(find_our_file("tools/users.json"), "r").read().strip()) < 1:
                # probably, we couldn't write inside the file. So, we are going to push a panic message
                open(find_our_file("tools/users.json"), "w").write("{}")
                panic_msg(e)
            return None
        # success message
        messagebox.showinfo("Eliminacion completada", f"""Se ha eliminado con exito al usuario
'{selected_usr}' del registro de usuarios.""")
        self.go("del_user -> home")


    def del_user_page(self) -> None:
        "remove a user from the list."
        self.del_page = Frame()
        self.del_page.grid()
        self.del_name = StringVar()
        name_l = Label(self.del_page, text="Introduzca nombre completo (sin acentos):", font=("Calibri", "13", "bold"), bg="whitesmoke",
        fg="black").grid(row=0, column=0, sticky="ew")
        name_e = Entry(self.del_page, width=30, textvariable=self.new_name,
        font=("Calibri", "13", "normal")).grid(row=0, column=1, sticky="ew")
        cancel = Button(self.del_page, text="Cancelar", font=("Calibri", "13", "bold"), bg="gray", fg="white",
        command=lambda: self.go("del_user -> home")).grid(row=1, column=0, sticky="ew")
        go_ahead = Button(self.del_page, text="Eliminar", font=("Calibri", "13", "bold"), bg="red", fg="white",
        command=lambda: self.del_user_internal).grid(row=1, column=1, sticky="ew")

    def reg_page(self) -> None:
        "generate a register page."
        self.regframe = Frame(self.root)
        self.regframe.grid()
        self.new_name = StringVar()
        self.new_pwd = StringVar()
        name_l = Label(self.regframe, text="Introduzca nombre completo (sin acentos):", font=("Calibri", "13", "bold"), bg="whitesmoke",
        fg="black").grid(row=0, column=0, sticky="ew")
        name_e = Entry(self.regframe, width=30, textvariable=self.new_name,
        font=("Calibri", "13", "normal")).grid(row=0, column=1, sticky="ew")
        name_l = Label(self.regframe, text="Introduzca una contraseña para relacionar con la cuenta:",
        font=("Calibri", "13", "bold"), bg="whitesmoke", fg="black").grid(row=1, column=0, sticky="ew")
        name_e = Entry(self.regframe, width=30, textvariable=self.new_pwd,
        font=("Calibri", "13", "normal"), show="*").grid(row=1, column=1, sticky="ew")
        skip = Button(self.regframe, text="Cancelar", font=("Calibri", "13", "bold"), bg="red", fg="white",
        command=lambda: self.go("register -> home")).grid(row=2, column=0, sticky="ew")
        send_b = Button(self.regframe, text="Registrar", font=("Calibri", "13", "bold"), bg="green", fg="white",
        command=self.register_internal).grid(row=2, column=1, sticky="ew")

    def see_registry_internal(self) -> None:
        "Second part of `see_registry`."
        try:
            date_a, date_b = self.date_list[self.di1.get() - 1], self.date_list[self.di2.get() - 1]
            compare_dates(date_a, date_b)
        except (KeyError, NameError, ValueError) as exc:
            messagebox.showerror("Error al mostrar", f"""No se pudo mostrar los datos solicitados. El sistema no pudo hallar
ninguna fecha, o la segunda es mas reciente que la primera (lo cual no es operable).
Verifique e intente de nuevo.

(Error: '{str(exc)}')""")
            return None
        # run directly the SQL command to get the storage
        CUR.execute("SELECT vendor_id, product_id, odometer_read, cost, datetime, noentry_reason FROM Prompt WHERE datetime >= ( ? ) AND datetime <= ( ? )", ( date_a, date_b ))
        finale = CUR.fetchall()
        # analyze and translate
        finale_str = "\n"
        products_operator = {}
        vendors_operator = {}
        final_cost = 0
        initial_odometer = finale[0][2]
        final_odometer = finale[len(finale) - 1][2]
        for v, p, o, c, d, r in finale:
            # translate some IDs
            CUR.execute("SELECT name FROM Vendors WHERE id == ( ? )", ( v, ))
            v = CUR.fetchone()[0]
            CUR.execute("SELECT name FROM Products WHERE id == ( ? )", ( p, ))
            p = CUR.fetchone()[0]
            # map some of the data
            noentry_msg = ""
            if r != "N/A":
                noentry_msg = f"ATENCION: {r}"
            final_cost += int(c)
            products_operator[p] = products_operator.get(p, 0) + 1
            vendors_operator[v] = vendors_operator.get(v, 0) + 1
            # build a string to report
            add_on = "·"*60 + f"{noentry_msg}\n" + f"- Fecha: {d}\n" + f"- Vendedor: {v}\n" + f"- Producto: {p}\n" + f"- Lectura del odometro registrada: {o}\n" + f"- Costo: ${c}\n"
            finale_str += add_on
        intro = f"VENTAS DESDE '{date_a}' HASTA '{date_b}'\n" + "="*60 + "\n- Vendedores: "
        for vendor in vendors_operator.keys():
            if len(vendors_operator.keys()) == 1:
                # only one vendor?
                intro += vendor + f" ({vendors_operator[vendor]})"
                break
            intro += vendor + f" ({vendors_operator[vendor]}), "
        if intro.endswith(", "):
            intro = intro[:len(intro) - 1]
        intro += "\n" + "- Productos vendidos: "
        howmany_sales = 0
        for product in products_operator.keys():
            if len(products_operator.keys()) == 1:
                # only one product?
                intro += product + f"({products_operator[product]})"
            else:
                intro += product + f"({products_operator[product]}), "
            howmany_sales += products_operator[product]
        if intro.endswith(", "):
            intro = intro[:len(intro) - 1]
        intro += "\n" + f"- Cantidad total vendida de productos: {howmany_sales}"
        intro += "\n" + f"- Costo total: {final_cost}\n-Lectura inicial del odometro: {initial_odometer}\n- Lectura final del odometro: {final_odometer}"
        # show the final product
        finale_str = intro + "\n\n" + "*"*60 + finale_str
        view_text(self.root, "Registro de ventas", finale_str)

    def see_registry(self) -> None:
        """
        See the sales registry. This giant function will prompt for an initial date
        and a final date (I mean, a period to search) and then it will return a
        formatted output.
        """
        self.sales_f = Frame(self.root)
        self.sales_f.grid()
        # first date prompt
        first_date_l = Label(self.sales_f, text="Introduzca una fecha inicial para buscar:", bg="whitesmoke", fg="black",
        font=("Calibri", "13", "bold")).grid(row=0, column=0, sticky="ew")
        self.date_list = get_dates("WaterDB.sqlite", True)
        self.di1 = IntVar()
        first_date_m = get_menubutton(self.sales_f, self.date_list, self.di1, 0, 1, "ew")
        # second date
        scnd_date_l = Label(self.sales_f, text="Introduzca una fecha final para buscar:", bg="whitesmoke", fg="black",
        font=("Calibri", "13", "bold")).grid(row=1, column=0, sticky="ew")
        self.di2 = IntVar()
        scnd_date_m = get_menubutton(self.sales_f, self.date_list, self.di2, 1, 1, "ew")
        # buttons to launch
        cancel_b = Button(self.sales_f, text="Cancelar busqueda", bg="red", fg="white", font=("Calibri", "13", "bold"),
        command=lambda: self.go("registry_view -> home")).grid(row=2, column=0, sticky="ew")
        send_b = Button(self.sales_f, text="Buscar", bg="green", fg="white", font=("Calibri", "13", "bold"),
        command=self.see_registry_internal).grid(row=2, column=1, sticky="ew")

    def register_internal(self) -> None:
        "make a database registry for the latest user."
        try:
            new_usr = self.new_name.get().strip()
            new_id = self.new_pwd.get().strip()
            if len(new_usr) < 1: raise ValueError(f'Expected non-empty strings, got ""')
            # update
            to_save = []
            with open(find_our_file("tools/users.json"), "r") as f:
                to_save.append(json.loads(f.read()))
            to_save[0][new_usr.lower()] = new_id
            with open(find_our_file("tools/users.json"), "w") as f:
                f.write(json.dumps(to_save[0]))
                f.close()
        except Exception as e:
            messagebox.showerror("Error al registrar", f"""Ha sucedido un error al registrar al usuario. Puede que
haya dejado la entrada totalmente vacia o haya agregado algun caracter no
permitido. Verifique e intente de nuevo.

(Error: '{str(e)}')""")
            if len(open(find_our_file("tools/users.json"), "r").read().strip()) < 1:
                open(find_our_file("tools/users.json"), "w").write("{}")
                panic_msg(e)
            return None
        # success message
        messagebox.showinfo("Proceso completado", f"""El proceso se ha completado exitosamente. Se le redirigira a la pagina de inicio.

Datos del registro:
- Usuario: {new_usr} ({new_usr.lower()})
- Contraseña: {new_id}""")
        self.go("register -> home")

    def go(self, arg: str) -> None:
        "point to any place in the gui."
        if arg == "home -> register":
            # go to the register page
            self.welcome.grid_remove()
            self.reg_page()
        elif arg == "register -> home":
            # go back to home
            self.regframe.grid_remove()
            self.menu()
        elif arg == "view users":
            self.showUsers()
        elif arg == "get-in":
            self.adminport.grid_remove()
            self.menu()
        elif arg == "get-in-directly":
            # same than "get-in", but overriding
            # the grid_remove (basically because
            # the door is not "activated")
            self.menu()
        elif arg == "view registry":
            self.welcome.grid_remove()
            self.see_registry()
        elif arg == "registry_view -> home":
            self.sales_f.grid_remove()
            self.menu()
        elif arg == "home -> del_user":
            self.welcome.grid_remove()
            self.del_user_page()
        elif arg == "del_user -> home":
            self.del_page.grid_remove()
            self.menu()
        elif arg == "manage product info":
            # this is quite harder than the others. Actually,
            # this command is redirecting to another
            # executable file (or the Python file, if we can).
            # We are not changing anything from the GUI, we are
            # just giving an advice (tkinter.messagebox.showinfo)
            messagebox.showinfo("Aviso", """Se le redirigira a otra
aplicacion para esta funcion. En un momento debe abrirse.""")
            # this names are passed according to setup.py
            # (https://github.com/ControlDeAgua/ControlDeAgua/blob/edaba7bb88b8b41a50b848a97a1486f8d5dc48a1/setup.py#L40-L41)
            names = ("manage-products.py", "Manejar la informacion de producto.exe")
            found_path = identify_dir(names[0], names[1])
            if found_path is not None:
                startfile(found_path)
        else:
            self.notDefined(arg)

# run the main loop
root = Tk()
gui = GUI(root)
root.mainloop()
