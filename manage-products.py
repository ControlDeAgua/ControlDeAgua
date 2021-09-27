"Separate GUI to manage the product info."

import json
from idlelib.textview import view_text
from tkinter import *
from tkinter import messagebox
from tools import panic
from tools.database import get_product_dict
from tools.prefabricated import get_menubutton

class ProductManager:
    """
    Main class for the interface. It doesn't
    manage user information, so the product
    info can be managed by anyone (if they know
    how to do it!)...
    """
    
    def __init__(self, root: Tk) -> None:
        "constructor method."
        self.root = root
        self.product_dict = get_product_dict()
        self.main_menu()
    
    def reload_product_info(self) -> None:
        """
        Open the file stream about product information. Even
        when this stream does not affect the main form
        ('Control de Agua.exe' and its Python format), it is
        reccommended to close that program to use the new
        values.
        
        (In most of the cases, you don't have to run this
        method manually. This is only used to re-force the
        product info).
        """
        try:
            del(self.product_dict)
            self.product_dict = ProductMap()
        except Exception as e:
            panic.panic_msg(e)
    
    def main_menu(self) -> None:
        """
        Main menu with the following options:
        
        - Manage an existent product
        - Delete an existent product
        - Register a new product
        - View the current products
        - Exit
        """
        self.menu_frame = Frame(self.root)
        self.menu_frame.grid()
        # a greetings label
        welcome_l = Label(self.menu_frame, text="""Seleccione una opcion para manejar la
informacion de los productos utilizada
en las operaciones de venta y reporte.""", font=("Calibri", "14", "bold"), bg="white", fg="black").grid(row=0, column=0, sticky="ew")
        # option to manage
        manage = Button(self.menu_frame, text="Manejar un producto que ya existe", fg="black", bg="whitesmoke",
        font=("Calibri", "14", "bold"), command=lambda: self.move_to_option("home", "manage")).grid(row=1, column=0, sticky="ew")
        # option to delete
        delete = Button(self.menu_frame, text="Eliminar un producto de la lista", fg="black", bg="whitesmoke",
        font=("Calibri", "14", "bold"), command=lambda: self.move_to_option("home", "delete")).grid(row=2, column=0, sticky="ew")
        # option to create
        create = Button(self.menu_frame, text="Agregar un producto a la lista", fg="black", bg="whitesmoke",
        font=("Calibri", "14", "bold"), command=lambda: self.move_to_option("home", "create")).grid(row=3, column=0, sticky="ew")
        # option to show
        show = Button(self.menu_frame, text="Ver la lista de productos", fg="black", bg="whitesmoke",
        font=("Calibri", "14", "bold"), command=lambda: self.move_to_option("home", "show")).grid(row=4, column=0, sticky="ew")
        # option to exit
        exit = Button(self.menu_frame, text="Salir", fg="white", bg="red",
        font=("Calibri", "14", "bold"), command=self.root.quit).grid(row=5, column=0, sticky="ew")
    
    def manage(self) -> None:
        "manage a product."
        self.manage_frame = Frame(self.root)
        self.manage_frame.grid()
        self.manage_selection = IntVar()
        self.manage_new_value = DoubleVar()
        self.manage_options = self.product_dir.get_list()
        # add a manage_product function
        def manage_product():
            try:
                target, value = self.product_dict.product_index[self.manage_selection.get()], self.manage_new_value.get()
                self.product_dict.products[target] = value
                with open("C:/Program Files/Control de Agua/tools/products.json", "w") as f:
                    f.write(json.dump(self.product_dict.products))
            except Exception as e:
                messagebox.showerror("Error", f"""{type(e).__name__}: {str(e)}

Verifique sus entradas e intente de nuevo.""")
                self.move_to_option("manage", "RETRY")
            self.finish_message("manage")
            self.move_to_option("manage", "home")
        # add abels and menubuttons
        l = Label(self.manage_frame, text="1. Elija un producto:", bg="whitesmoke", fg="black",
        font=("Calibri", "13", "bold")).grid(row=0, column=0, sticky="ew")
        opts = get_menubutton(self.manage_frame,
                              self.manage_options,
                              self.manage_selection,
                              row=0,
                              column=1)
        l2 = Label(self.manage_frame, text="2. Introduzca un valor para reemplazar (pesos mexicanos):", bg="whitesmoke",
        fg="black", font=("Calibri", "13", "bold")).grid(row=1, column=0, sticky="ew")
        new_value = Entry(self.manage_frame, textvariable=self.manage_new_value, width=40).grid(row=1, column=1, sticky="ew")
        cancel = Button(self.manage_frame, text="Cancelar", bg="red", fg="whitesmoke",
        command=lambda:self.move_to_option("manage", "home")).grid(row=2, column=0, sticky="ew")
        move_it = Button(self.manage_frame, text="Modificar", bg="cyan",  # i decided to use cyan instead of green!
        fg="whitesmoke", command=manage_product).grid(row=2, column=1, sticky="ew")
    
    def delete(self) -> None:
        "interface to delete an item."
        self.delete_frame = Frame(self.root)

    def loop(self) -> None:
        "run self.root.mainloop() from the class."
        self.root.mainloop()
    
    def finish_message(self, event: str) -> None:
        "message shown each time we complete an operation here. Ain't so hard."
        messagebox.showinfo("Proceso completado sin errores", f"""El proceso se ha completado con exito.
Recuerde cerrar la aplicacion de registro/configuracion y volverla a abrir
para poder ver los cambios realizados.

(Proceso: {event})""")
    
    def move_to_option(self, origin: str, dest: str) -> None:
        "Move between frames."
        result = (origin, dest)
        # redirect
        if result == ("home", "show"):
            # an easy one: just show the product list
            text = ""
            for k, v in self.product_dict.products.values():
                text += f"{'='*60}\n- Producto: {k}\n- Valor monetario: ${v[0]}\n- Valor en la cuenta del odometro: {v[1]}\n"
            view_text("Lista de productos registrados", text)
            del(text)
            return None
        elif result == ("home", "manage"):
            self.menu_frame.grid_remove()
            self.manage()
        elif result == ("manage", "home"):
            self.manage_frame.grid_remove()
            self.main_menu()
        elif result == ("manage", "RETRY"):
            # retry the "manage" operations
            self.reload_product_info()
            self.manage()
        elif result == ("home", "delete"):
            self.menu_frame.grid_remove()
            self.delete()
        elif result == ("delete", "home"):
            self.delete_frame.grid_remove()
            self.main_menu()
        else:
            # no results? you should say it
            messagebox.showwarning("NotImplemented Error", f"""La opcion del menu no fue identificada: {result}.
Comuniquese con el desarrollador para manejar esta incompatibilidad.""")
        # always reload the info, to avoid mistakes
        self.reload_product_info()

if __name__ == "__main__":
    # main level execution
    gui = ProductManager(Tk())
    gui.loop()
