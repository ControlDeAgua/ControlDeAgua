"Separate GUI to manage the product info."

import json
from tkinter import *
from tkinter import messagebox
from tools.database import get_product_dict

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
    
    def get_product_info(self) -> None:
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
        self.product_dict = get_product_dict()
    
    def main_menu(self) -> None:
        """
        Main menu with the following options:
        
        - Manage an existent product
        - Delete an existent product
        - Register a new product
        - Exit
        """
    
    def loop(self) -> None:
        "run self.root.mainloop() from the class."
        self.root.mainloop()

if __name__ == "__main__":
    # main level execution
    gui = ProductManager(Tk())
    gui.loop()
