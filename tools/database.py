"""
Tools for database management.

(specificly made for the project "Control de Agua")
"""

__all__ = ["ensureDatabase", "getDatabase"]

import atexit
import os
import json
import sqlite3
from tkinter import messagebox
from datetime import datetime
from typing import Dict

Prefix = "C:/Program files/Control de Agua/db/"
Container = []


def _destroy_db(path: str, conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    "delete the database, and also close."
    try:
        # try to close the SQL cursor
        cursor.close()
        del(conn)
    except:
        # something happened, just pass
        pass
    atexit.register(lambda: os.remove(_db_route(path, True)))

def _db_route(n: str, prefix: bool = False) -> str:
    "return the route with the selected prefix (or not)."
    if prefix:
        return Prefix + n
    return n


def _db_exists(pathname: str) -> bool:
    "it just returns if the path exists or not."
    return os.path.exists(pathname)


def ensureDatabase(name: str, use_prefix: bool = True) -> None:
    "get sure that the db exists. If not, create one."
    realname = _db_route(name, prefix=use_prefix)
    if not _db_exists(realname):
        # the db does not exists, the tables must be created.
        conn = sqlite3.connect(realname)
        cur = conn.cursor()
        cur.executescript("""
CREATE TABLE Prompt (
    id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    vendor_id    INTEGER,
    product_id   INTEGER,
    water_read   INTEGER,
    cost         INTEGER,
    time         TEXT
);

CREATE TABLE Products (
    id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name     TEXT
);

CREATE TABLE Vendors (
    id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name     TEXT)
""")
        conn.commit()
        cur.close()
        del(cur, conn)
    else:
        # the setup is not needed, just pass
        pass
    # log the database path
    Container.append(realname)


def getDatabase(fname: str, use_prefix: bool = True) -> tuple:
    "obtain the SQL database, and get sure it has the correct setup."
    pathname = _db_route(fname, prefix=use_prefix)
    if pathname not in Container:
        # ensure the database first
        ensureDatabase(fname, use_prefix)
    conn = sqlite3.connect(pathname)
    cur = conn.cursor()
    return conn, cur

def deleteDatabase(p: str, c: sqlite3.Connection, cc: sqlite3.Cursor) -> None:
    "destroy the database (if you can!)"
    c.close()
    _destroy_db(p, c, cc)

def buildInstertionCommand(conn, cur, read: float, client: str, vendor: str, unit_c: float, units: float) -> None:
    "format and test the values to run a clean argument for execute()/executescript()."
    # calculate the cost
    try:
        total_cost = units * unit_c
    except:
        messagebox.showwarning("Error operativo", """Algo ha sucedido al calcular el costo total.
Intente de nuevo o revise esas entradas.""")
    # ensure and select the vendor id
    cur.execute("""INSERT OR IGNORE INTO Vendors (name)
        VALUES ( ? )""", (vendor, )) # add a vendor name if it doesn't exists
    cur.execute('SELECT id FROM Vendors WHERE name = ? ', (vendor, ))
    vendor_id = cur.fetchone()[0]
    # do it with the client, too
    cur.execute("""INSERT OR IGNORE INTO Products (name)
        VALUES ( ? )""", (client, )) # add a client name, if it doesn't exists
    cur.execute('SELECT id FROM Products WHERE name = ? ', (client, ))
    client_id = cur.fetchone()[0]
    # update the selected data
    cur.execute("""INSERT INTO Prompt
        (vendor_id, product_id, water_read, cost, time) VALUES ( ?, ?, ?, ?, ? )""",
        (vendor_id, client_id, read, total_cost, datetime.today().strftime("%B %d, %Y %H:%M:%S")))
    conn.commit()

def get_product_dict() -> Dict[str, float]:
    return json.loads(open("C://Program Files/Control de Agua/tools/products.json").read())

class ProductMap:
    """
    Not a map at all, but it is a ProductMap...

    (Intended for the prefabicated `tools.prefabricated.get_listbox`)
    """

    def __init__(self) -> None:
        self.products = get_product_dict()

    def get(self, arg: str) -> float:
        try:
            return self.products[arg]
        except:
            raise ValueError(f"Argument given by the listbox not found: {arg} (KeyError)")