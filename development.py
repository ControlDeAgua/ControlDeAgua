"""
A developer "fixed" version of the products. This will help
us to modify the database, and then delete it before we upload
it to GitHub.
"""

import argparse
import os
import subprocess

allowed_files = ("water-gui.py", "delete-db.py", "admin-pwd.py", "manage-products.py")


def prepare_and_get_parser():
    """
    Use a CLI to identify the file to run.
    """
    parser = argparse.ArgumentParser(prog="ControlDeAgua[development]")
    parser.add_argument("file", nargs="?", metavar="FILE")
    options = parser.parse_args()
    if options.file not in allowed_files:
        parser.error(f"El archivo '{options.file}' no fue identificado como un archivo de Control de Agua")
    return parser, options.file

def main():
    "Main function."
    parser, file = prepare_and_get_parser()
    if os.path.exists("./db/WaterDB.sqlite"):
        print("Removing the database...")
        os.remove("./db/WaterDB.sqlite")
    try:
        print(f"Running '{file}'. This could take a while.")
        subprocess.run(file, shell=True)
    except Exception as e:
        print(f"{type(e).__name__}: {str(e)}")
    try:
        test_file = "" == open("./db/WaterDB.sqlite", "r").read().strip()
        already_clean = test_file
    except Exception:
        already_clean = False
    if not already_clean:
        try:
            print("Trying to restore the database... ahh...")
            if os.path.exists("./db/WaterDB.sqlite"):
                os.remove("./db/WaterDB.sqlite")
            recovery = open("./db/WaterDB.sqlite", "x")
        except Exception as e:
            parser.error(f"fatal error while cleaning database: {str(e)}")

if __name__ == '__main__':
    main()
