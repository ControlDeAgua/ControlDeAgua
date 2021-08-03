"just change the admin password on a command-line interface."

import getpass
from colorama import init, Fore

def main() -> None:
    init(autoreset=True)
    if not len(open("C:/Program Files/Control de Agua/tools/admin.txt").read().strip()) < 1:
        old_pwd = getpass.getpass("Introduzca la clave actual del administrador: ")
        if open("C:/Program Files/Control de Agua/tools/admin.txt").read().strip() != old_pwd.strip():
            print(Fore.RED+"Clave incorrecta. Intente de nuevo.")
            return None
    else:
        print(Fore.YELLOW+"ADVERTENCIA: No hay contraseña previa. Esto no afecta el proceso, solo que no se le va a pedir la contraseña previa.")
    new_pwd = getpass.getpass("Ingrese la nueva clave: ")
    with open("C:/Program Files/Control de Agua/tools/admin.txt", "w") as f:
        f.write(new_pwd.strip())
        f.close()
    print(Fore.GREEN+"Listo. Presione Enter para salir.", end=" ")
    getpass.getpass("")

if __name__ == '__main__':
    main()
