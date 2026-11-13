"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 13: MÓDULO SQLITE3
Base de datos 'productos.db' + tabla 'productos'
===============================================================================

ENUNCIADO:

Al finalizar el día, Diego se acerca con una solicitud concreta:

    "Mariana ha hablado con el cliente, y tienen una tarea específica que
    quieren resolver ya mismo. Nos pidieron que hagamos una prueba con el
    sistema SQLite. Necesitamos algo básico pero funcional: registrar
    productos con su nombre y precio, y luego mostrarlos en pantalla para
    asegurarnos de que el registro funciona correctamente. ¿Te animás a
    encargarte de esta parte? Es clave para que avancemos hacia la solución
    más completa."

Necesitarás:
    1. Crear una base de datos SQLite llamada 'productos.db'.
    2. Definir una tabla llamada 'productos' con los campos:
         - id     (clave primaria autoincremental)
         - nombre (texto, no nulo)
         - precio (real, no nulo)
    3. Diseñar un programa que permita:
         - Registrar un producto ingresando su nombre y precio.
         - Mostrar todos los productos almacenados en la base de datos.

Validaciones básicas:
    - El nombre no puede estar vacío.
    - El precio debe ser un número mayor que cero.

===============================================================================
"""

# =============================================================================
# IMPORTACIÓN DEL MÓDULO ESTÁNDAR SQLITE3 (Clase 13)
# =============================================================================
import sqlite3


# =============================================================================
# BLOQUE 1: CONEXIÓN A LA BASE DE DATOS
# -----------------------------------------------------------------------------
# sqlite3.connect("productos.db") abre la base si existe o la crea si no.
# try-except (Clase 12) captura errores de conexión.
# =============================================================================

def conectar_base_datos():
    """
    Establece la conexión con 'productos.db'.

    Retorna:
        sqlite3.Connection: objeto conexión listo para usar, o
        None si hubo un error.
    """
    try:
        conexion = sqlite3.connect("productos.db")
        return conexion
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo conectar a la base de datos: {error}")
        return None


# =============================================================================
# BLOQUE 2: CREACIÓN DE LA TABLA
# -----------------------------------------------------------------------------
# CREATE TABLE IF NOT EXISTS evita el error si ya existe.
# Tipos SQLite:
#   INTEGER PRIMARY KEY AUTOINCREMENT -> id autoincremental
#   TEXT    NOT NULL                  -> nombre
#   REAL    NOT NULL                  -> precio
# =============================================================================

def crear_tabla_productos(conexion):
    """
    Crea la tabla 'productos' si todavía no existe.

    Parámetro:
        conexion (sqlite3.Connection): conexión activa a la base.

    Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT    NOT NULL,
                precio REAL    NOT NULL
            )
        """)
        conexion.commit()   # confirma los cambios en disco
        return True
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo crear la tabla: {error}")
        return False


# =============================================================================
# BLOQUE 3: VALIDACIÓN DE ENTRADA DEL USUARIO
# -----------------------------------------------------------------------------
# - Nombre: while + if para rechazar cadenas vacías, try-except para EOFError.
# - Precio: try-except con ValueError para casting (Clase 12) + check > 0.
# =============================================================================

def pedir_nombre():
    """
    Solicita el nombre del producto, insistiendo hasta que sea válido.

    Retorna:
        str: nombre válido (sin espacios extremos), o None si se interrumpe.
    """
    while True:
        try:
            nombre = input("Nombre del producto: ").strip()
        except EOFError:
            print("\n[ERROR] Entrada interrumpida.")
            return None

        if nombre == "":
            print("[ERROR] El nombre no puede estar vacío.")
        else:
            return nombre


def pedir_precio():
    """
    Solicita el precio del producto. Acepta solo números > 0.

    Retorna:
        float: precio válido, o None si se interrumpe.
    """
    while True:
        try:
            entrada = input("Precio del producto: $").strip()
        except EOFError:
            print("\n[ERROR] Entrada interrumpida.")
            return None

        # try-except para el casting: si no es número, no explota
        try:
            precio = float(entrada)
        except ValueError:
            print("[ERROR] Ingresá un número válido (ej: 1500 o 1500.50).")
            continue

        if precio <= 0:
            print("[ERROR] El precio debe ser mayor que cero.")
            continue

        return precio


# =============================================================================
# BLOQUE 4: REGISTRAR UN PRODUCTO (INSERT)
# -----------------------------------------------------------------------------
# Se usan placeholders '?' para evitar inyección SQL y errores de formato.
# Los valores se pasan como tupla → (nombre, precio).
# =============================================================================

def registrar_producto(conexion):
    """
    Pide nombre y precio, los valida y los inserta en la tabla 'productos'.

    Parámetro:
        conexion (sqlite3.Connection): conexión activa a la base.
    """
    print("\n--- REGISTRAR PRODUCTO ---")
    nombre = pedir_nombre()
    if nombre is None:
        return

    precio = pedir_precio()
    if precio is None:
        return

    try:
        cursor = conexion.cursor()
        # Placeholder '?' → SQLite se encarga del escapado seguro
        cursor.execute(
            "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
            (nombre, precio)
        )
        conexion.commit()   # confirmamos la inserción
        print(f"[OK] Producto '{nombre}' registrado por ${precio:.2f}.")
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo registrar el producto: {error}")


# =============================================================================
# BLOQUE 5: MOSTRAR TODOS LOS PRODUCTOS (SELECT + ORDER BY)
# -----------------------------------------------------------------------------
# ORDER BY id ordena los resultados por id ascendente.
# fetchall() trae todas las filas como una lista de tuplas.
# =============================================================================

def mostrar_productos(conexion):
    """
    Consulta todos los productos de la base y los imprime en pantalla.

    Parámetro:
        conexion (sqlite3.Connection): conexión activa a la base.
    """
    print("\n--- LISTA DE PRODUCTOS ---")
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
        productos = cursor.fetchall()

        if len(productos) == 0:
            print("  No hay productos registrados todavía.")
            return

        # Desempaquetamos cada fila (tupla) en tres variables (Clases 7 y 8)
        for producto in productos:
            id_producto, nombre, precio = producto
            print(f"  {id_producto:>3}. {nombre:<15} -> ${precio:>10.2f}")

        print("-" * 40)
        print(f"  Total: {len(productos)} producto(s) registrado(s).")

    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo consultar la base: {error}")


# =============================================================================
# BLOQUE 6: MENÚ PRINCIPAL
# =============================================================================

def mostrar_menu():
    """Muestra las opciones disponibles. Función sin return (solo efecto)."""
    print("\n========================================")
    print("   SISTEMA DE PRODUCTOS - TALENTOLAB")
    print("========================================")
    print("  1. Registrar producto")
    print("  2. Mostrar productos")
    print("  3. Salir")
    print("========================================")


def main():
    """Orquesta el programa: conecta, crea la tabla y ofrece el menú."""
    # --- 1) Conectar a la base de datos ---
    conexion = conectar_base_datos()
    if conexion is None:
        return

    # --- 2) Asegurar que la tabla exista ---
    if not crear_tabla_productos(conexion):
        conexion.close()
        return

    # --- 3) Bucle principal del menú ---
    try:
        while True:
            mostrar_menu()
            opcion = input("Elegí una opción (1-3): ").strip()

            if opcion == "1":
                registrar_producto(conexion)
            elif opcion == "2":
                mostrar_productos(conexion)
            elif opcion == "3":
                print("\nCerrando el sistema... ¡Hasta luego!")
                break
            else:
                print("[ERROR] Opción inválida. Ingresá un número del 1 al 3.")

    finally:
        # Garantizamos el cierre de la conexión (Clase 12: finally)
        conexion.close()
        print("Conexión con 'productos.db' cerrada correctamente.")


# =============================================================================
# Punto de entrada
# =============================================================================
main()