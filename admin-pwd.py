"just change the admin password on a command-line interface."

import getpass
from colorama import init, Fore

def main() -> None:
    try:
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
        print(Fore.GREEN+"Listo.", end=" ")
    except KeyboardInterrupt:
        print(Fore.RED+"Error: Operacion interrumpida por el usuario", end=" ")
    except (UnicodeDecodeError, UnicodeEncodeError) as exc:
        print(Fore.RED+f"Error: No se pudo decodificar un caracter ({str(exc)}).", end=" ")
    except OSError:
        print(Fore.RED+f"Error: El sistema rechazo alguna operacion ({str(exc)}).", end=" ")
    except Exception as exc:
        print(Style.BRIGHT+Fore.RED+f"""Error fatal: Hubo un error no esperado. Por favor reportelo a <https://github.com/ControlDeAgua/bug_tracker>.

Error: {type(exc).__name__}: {str(exc)}\n""")
    print("Presione Enter para salir.", end=" ")
    getpass.getpass("")

if __name__ == '__main__':
    main()
