"Prefabicated Tkinter widgets and apps for my projects."

__all__ = ("get_menubutton", "ReasonEntry")

from tkinter import *

# annotation stuff
from typing import List, Optional, Tuple


# Menubutton builder
def get_menubutton(
    root: Frame,
    options: List[str],
    variable: IntVar,
    row: int = 0,
    column: int = 0,
    sticky: str = "ew",
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
        messagebox.showwarning(
            "Advertencia al desarrollador",
            f"""El programa ha lanzado una advertencia. Por favor
reporte esto al desarrollador del producto.

    On 'tools.prefabicated.get_listbox', argument
    'root' is recommended to be an instance of 'tkinter.Frame',
    not 'tkinter.Tk'. When this warning is ignored, many bugs
    might be reported.

    If you are not the developer of this product, please
    report this to the author of the product.

- Test results:
  - 'root' expected class: '_tkinter.Frame' -> 'tkinter.Frame'
  - 'root' real class: {type(root).__name__}""",
        )
    else:
        assert isinstance(root, Frame)
    try:
        assert isinstance(options, list) or isinstance(options, tuple)
    except AssertionError:
        # it might be a dict keys() or values()
        assert isinstance(options, get_type("dict_keys")) or isinstance(
            options, get_type("dict_values")
        )
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
