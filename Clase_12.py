"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 12: PERSISTENCIA DE DATOS
Archivos de texto + manejo de excepciones con try-except
===============================================================================

ENUNCIADO:

Como parte del proyecto de TalentoLab, el cliente necesita un sistema que
permita registrar los datos de los usuarios en un archivo de texto, para que
puedan ser recuperados y utilizados en futuras sesiones. Diego te asignó la
tarea de desarrollar este sistema básico de persistencia de datos, aplicando
todo lo que aprendiste. Tu tarea consiste en:

    1) Creá un programa que permita ingresar los datos de un cliente:
       nombre, apellido y correo electrónico. Usá try-except para manejar
       posibles errores durante la entrada de datos. Por ejemplo:
         - Si el archivo no puede abrirse para escritura.
         - Si los datos ingresados no son válidos (por ejemplo, si el correo
           no contiene una "@" o el nombre está vacío).

    2) Guardá los datos ingresados en un archivo de texto llamado
       'clientes.txt', de forma que cada cliente quede registrado en una
       nueva línea.

    3) Una vez guardados los datos, mostrá un mensaje de confirmación al
       usuario y cerrá el archivo correctamente.

Salida esperada:

    === Registro de Clientes ===
    Ingresá los datos del cliente:
    Nombre: Ana
    Apellido: López
    Correo: ana.lopez@email.com
    Cliente registrado con éxito en clientes.txt

Si ocurre un error, como intentar guardar en un archivo protegido, el
programa debería mostrar un mensaje claro:

    [ERROR] No se pudo guardar la información.

===============================================================================
"""

# =============================================================================
# FUNCIONES DE VALIDACIÓN DE ENTRADA (con while + try-except)
# -----------------------------------------------------------------------------
# Las validaciones lógicas (vacío, sin '@') se resuelven con while + if.
# El try-except se usa para errores técnicos de input: EOFError, que ocurre
# cuando la entrada estándar se cierra inesperadamente (por ejemplo, si se
# interrumpe la lectura en Google Colab).
# =============================================================================

def pedir_nombre():
    """
    Solicita el nombre del cliente. Rechaza cadenas vacías
    y maneja EOFError si la entrada se interrumpe.

    Retorna:
        str: nombre validado, o None si la entrada se interrumpió.
    """
    while True:
        try:
            nombre = input("Nombre: ").strip()
        except EOFError:
            print("\n[ERROR] Entrada interrumpida.")
            return None

        if nombre == "":
            print("[ERROR] El nombre no puede estar vacío. Intentá de nuevo.")
        else:
            return nombre


def pedir_apellido():
    """
    Solicita el apellido del cliente. Rechaza cadenas vacías.

    Retorna:
        str: apellido validado, o None si la entrada se interrumpió.
    """
    while True:
        try:
            apellido = input("Apellido: ").strip()
        except EOFError:
            print("\n[ERROR] Entrada interrumpida.")
            return None

        if apellido == "":
            print("[ERROR] El apellido no puede estar vacío. Intentá de nuevo.")
        else:
            return apellido


def pedir_correo():
    """
    Solicita el correo del cliente. Valida:
        - que no esté vacío,
        - que contenga al menos un carácter '@'.

    Retorna:
        str: correo validado, o None si la entrada se interrumpió.
    """
    while True:
        try:
            correo = input("Correo: ").strip()
        except EOFError:
            print("\n[ERROR] Entrada interrumpida.")
            return None

        if correo == "":
            print("[ERROR] El correo no puede estar vacío.")
        elif "@" not in correo:
            print("[ERROR] El correo debe contener un '@'. Intentá de nuevo.")
        else:
            return correo


# =============================================================================
# FUNCIÓN DE PERSISTENCIA (con try-except-finally)
# -----------------------------------------------------------------------------
# Estrategia:
#   - try: abrir el archivo en modo append ("a") y escribir la línea.
#   - except PermissionError: caso específico (archivo protegido / solo lectura).
#   - except OSError: cualquier otro error de E/S (disco lleno, ruta inválida…).
#   - finally: cerrar SIEMPRE el archivo, exista o no un error.
# Esto cumple el requisito "cerrá el archivo correctamente".
# =============================================================================

def guardar_cliente(nombre, apellido, correo):
    """
    Guarda los datos del cliente en 'clientes.txt'.
    Cada cliente ocupa una línea con formato:
        nombre,apellido,correo

    Parámetros:
        nombre   (str): nombre del cliente.
        apellido (str): apellido del cliente.
        correo   (str): correo electrónico del cliente.

    Retorna:
        bool: True si se guardó correctamente, False si hubo un error.
    """
    archivo = None
    try:
        # Modo "a" (append): agrega al final sin borrar lo anterior.
        # encoding="utf-8" para preservar tildes y caracteres especiales.
        archivo = open("clientes.txt", "a", encoding="utf-8")
        archivo.write(f"{nombre},{apellido},{correo}\n")
        return True

    except PermissionError:
        # Caso típico: archivo con permisos de solo lectura, o bloqueado por
        # otro programa (típico en Windows).
        print("[ERROR] No se pudo guardar la información. "
              "Verificá los permisos del archivo.")
        return False

    except OSError:
        # Cualquier otro error de E/S: disco lleno, ruta inexistente,
        # dispositivo no disponible, etc.
        print("[ERROR] No se pudo guardar la información.")
        return False

    finally:
        # finally se ejecuta SIEMPRE: haya error o no, cerramos el archivo.
        if archivo is not None:
            archivo.close()


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """Coordina el flujo completo del registro de un cliente."""
    print("=== Registro de Clientes ===")
    print("Ingresá los datos del cliente:")

    # --- 1) Solicitar y validar cada dato ---
    nombre = pedir_nombre()
    if nombre is None:
        return   # entrada interrumpida: salimos sin intentar guardar

    apellido = pedir_apellido()
    if apellido is None:
        return

    correo = pedir_correo()
    if correo is None:
        return

    # --- 2) Guardar en el archivo y verificar el resultado ---
    exito = guardar_cliente(nombre, apellido, correo)

    # --- 3) Confirmación al usuario ---
    if exito:
        print(f"Cliente registrado con éxito en clientes.txt")


# =============================================================================
# Punto de entrada
# =============================================================================
main()