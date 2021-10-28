"Prefabicated Tkinter widgets and apps for my projects."

__all__ = ("get_listbox", "get_menubutton", "ReasonEntry")

from tkinter import *

# annotation stuff
from typing import List, Tuple, Optional

# Listbox builder
def get_listbox(
    root: Frame,
    options: List[str],
    row: int = 0,
    column: int = 0,
    sticky: str = "ew"
) -> Listbox:
    """
    Generate a tkinter.ListBox from a custom
    list / tuple of strings ("options").

    The root object ("root") must be a tkinter.Frame
    that has been set up with the grid() method.

    "row", "column" and "sticky" are just arguments for
    the grid() method applied to the list box object.
    """
    messagebox.showwarning("Advertencia", f"""Se ha detectado el uso obsoleto de un widget. Si no es el creador del
producto, por favor reportelo al desarrollador de inmediato.

(Widget creado: 'tkinter.Listbox')
(Metodo utilizado: 'tools.prefabicated.get_listbox' - mediante 'Control de Agua')
(Tipo de advertencia: Metodo reemplazado)""")
    def get_type(req: str) -> type:
        "function to get a type from undefined classes (I mean, defined on a function - but not imported)."
        if req == "dict_keys":
            # return the dict.keys() type
            return type({"a": 1}.keys())
        elif req == "dict_values":
            # return the dict.values() type
            return type({"b": 1}.values())
        else:
            # return the type of <<None>>
            return type(None)
    # check some of the args (by assertion)
    if isinstance(root, Tk) and not isinstance(root, Frame):
        messagebox.showwarning("Advertencia al desarrollador", f"""El programa ha lanzado una advertencia. Por favor
reporte esto al desarrollador del producto.

    On 'tools.prefabicated.get_listbox', argument
    'root' is recommended to be an instance of 'tkinter.Frame',
    not 'tkinter.Tk'. When this warning is ignored, many bugs
    might be reported.

    If you are not the developer of this product, please
    report this to the author of the product.

- Test results:
  - 'root' expected class: '_tkinter.Frame' -> 'tkinter.Frame'
  - 'root' real class: {root.__class__}""")
    else:
        assert isinstance(root, Frame)
    try:
        assert isinstance(options, list) or isinstance(options, tuple)
    except AssertionError:
        # it might be a dict keys() or values()
        assert isinstance(options, get_type("dict_keys")) or isinstance(options, get_type("dict_values"))
    assert isinstance(row, int)
    assert isinstance(column, int)
    assert isinstance(sticky, str)
    # generate the list box
    index = 1
    lb = Listbox(root)
    # add the options
    for option in options:
        lb.insert(index, option.strip())
        index += 1
    # grid the object
    lb.grid(row=row, column=column, sticky=sticky)
    return lb

#####################################################################################################################

# Menubutton builder
def get_menubutton(
    root: Frame,
    options: List[str],
    variable: IntVar,
    row: int = 0,
    column: int = 0,
    sticky: str = "ew"
) -> Menubutton:
    """
    Generate a tkinter MenuButton. Follow a similar process than
    get_listbox().
    """
    def get_type(req: str) -> type:
        "function to get a type from undefined classes (I mean, defined inside a function but not imported at all)."
        if req == "dict_keys":
            # return the dict.keys() type
            return type({"a": 1}.keys())
        elif req == "dict_values":
            # return the dict.values() type
            return type({"b": 1}.values())
        else:
            # return the type of <<None>>
            return type(None)
    # check some of the args (by assertion)
    if isinstance(root, Tk) and not isinstance(root, Frame):
        messagebox.showwarning("Advertencia al desarrollador", f"""El programa ha lanzado una advertencia. Por favor
reporte esto al desarrollador del producto.

    On 'tools.prefabicated.get_listbox', argument
    'root' is recommended to be an instance of 'tkinter.Frame',
    not 'tkinter.Tk'. When this warning is ignored, many bugs
    might be reported.

    If you are not the developer of this product, please
    report this to the author of the product.

- Test results:
  - 'root' expected class: '_tkinter.Frame' -> 'tkinter.Frame'
  - 'root' real class: {type(root).__name__}""")
    else:
        assert isinstance(root, Frame)
    try:
        assert isinstance(options, list) or isinstance(options, tuple)
    except AssertionError:
        # it might be a dict keys() or values()
        assert isinstance(options, get_type("dict_keys")) or isinstance(options, get_type("dict_values"))
    assert isinstance(row, int)
    assert isinstance(column, int)
    assert isinstance(sticky, str)

    # generate the menu button using a menu widget
    index = 1
    mb = Menubutton(root, text="Seleccione una opcion")
    mn = Menu(mb, tearoff=0)
    
    # add the options to the Menu widget
    for option in options:
        mn.add_radiobutton(label=option.strip(), variable=variable, value=index)
        index += 1
    
    # grid the Menubutton
    mb["menu"] = mn
    mb.grid(row=row, column=column, sticky=sticky)
    return mb

#####################################################################################################################

# GUI for explaining a "no-monetary sale"
class ReasonEntry:
    "enter a reason to avoid a monetary entry."
    msg = "Introduzca un motivo para no registrar un ingreso con esta venta:"
    completed = False
    
    def __init__(self, root: Optional[Tk] = None) -> None:
        "constructor method."
        if root is None:
            self.root = Tk()
        else:
            self.root = root
        self.root.title(msg)
        self.prepare()
    
    def prepare(self) -> None:
        "prepare the entry."
        self.reason_variable = StringVar()
        frame = Frame(self.root)
        frame.grid()
        # the entry for the reason
        enter_label = Label(frame, text=self.msg, font=("Calibri", "14", "bold"), bg="whitesmoke",
        fg="black").grid(row=0, column=0, sticky="ew")
        enter_entry = Entry(frame, width=40, textvariable=self.reason_variable).grid(row=0, column=1, sticky="ew")
        # and here's the trick: we only want this scheme:
        #
        #         c0           c1
        #    --------------------------
        # r0 | message |     entry
        #    --------------------------
        # r1 |         | button to exit
        #
        # At (r1, c0), it will be a blank space. But how can
        # we do something like that? We are gonna use a Label,
        # with a number of chars equivalent to the length of the
        # "message", and the same font, same colors. Then, we
        # made it look like a blank space!
        blank_space = Label(frame, text="="*len(self.msg), font=("Calibri", "14", "bold"), bg="whitesmoke",
        fg="whitesmoke").grid(row=1, column=0, sticky="ew")
        # and finally, a button to quit
        quit_gui = Button(frame, text="Aceptar", font=("Calibri", "14", "bold"), bg="blue",
        fg="white", command=self.root.quit).grid(row=1, column=1, sticky="ew")
    
    def loop(self) -> None:
        "run self.root.mainloop() from the class."
        self.root.mainloop()
    
    def is_completed(self) -> bool:
        "have we finished?"
        try:
            # if we can generate a frame from here, it means that
            # the user hasn't finished (yet). Return False
            test_frame = Frame(self.root)
            return False
        except Exception as e:
            # we couldn't generate a Frame from the root, because it has been
            # destroyed. That means we have completed!
            return True
    
    def get_msg(self) -> str:
        "Try to return a message."
        try:
            return self.reason_variable.get()
        except Exception as exc:
            messagebox.showwarning("Error al extraer los datos de la entrada", f"""No se pudo extraer la informacion requerida del usuario.
Por favor reporte esto a los desarrolladores del producto,
y agregue estos datos:

- Tipo de error: '{type(exc).__name__}'
- Mensaje de error: '{str(exc)}'""")
            return f"Error particular con la herramienta: {str(exc)}"
