"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 14: CRUD, TRANSACCIONES Y SQL SEGURO
Sistema de productos con validaciones, confirmación y Colorama
===============================================================================

ENUNCIADO:

La jornada en TalentoLab transcurre con el habitual ritmo de trabajo cuando
Mariana se acerca a tu escritorio con su tablet en la mano.

    "¡Felicitaciones! El cliente ha quedado muy conforme con la primera
    versión del registro de productos. Pudieron cargar información y
    recuperarla sin problemas. Pero ahora nos piden algunas mejoras para
    garantizar que el sistema sea más seguro y fácil de administrar."

Te muestra en pantalla un par de puntos que debemos agregar:

    1. Validación de datos al registrar un producto: Actualmente, el sistema
       permite agregar productos, pero no verifica si los datos ingresados
       son válidos. Es necesario asegurarse de que el nombre del producto no
       esté vacío y que el precio sea un número positivo antes de almacenarlo
       en la base de datos.

    2. Eliminar un producto con confirmación: El cliente quiere evitar
       eliminaciones accidentales. Por lo tanto, al eliminar un producto, el
       sistema debe solicitar una confirmación antes de ejecutar la acción.

Desde su escritorio, Luis se suma a la conversación:

    "Podrías aprovechar Colorama para mejorar la experiencia visual. Por
    ejemplo, podrías resaltar los mensajes de advertencia en rojo, las
    confirmaciones en verde, y la información general en azul. Haría que la
    interfaz sea más clara y atractiva para el usuario."

REQUISITOS ADICIONALES DE LA CLASE 14:
    - Implementar CRUD completo (Create, Read, Update, Delete).
    - Usar placeholders '?' para evitar inyección SQL.
    - Usar transacciones con try/except/rollback.
    - Actualización de datos con UPDATE.

===============================================================================
"""

# =============================================================================
# IMPORTACIÓN DE MÓDULOS
# -----------------------------------------------------------------------------
# - sqlite3  (Clase 13): base de datos.
# - colorama (Clase 11): colores en terminal.
# =============================================================================
import sqlite3
from colorama import init, Fore, Style

# init() de colorama: necesario en Windows, inocuo en Linux/Mac.
init()

# ---- Constantes de color ----
RESET   = Style.RESET_ALL
BRILLO  = Style.BRIGHT
ROJO    = Fore.RED
VERDE   = Fore.GREEN
AMARILLO = Fore.YELLOW
AZUL    = Fore.BLUE
CYAN    = Fore.CYAN
MAGENTA = Fore.MAGENTA


# =============================================================================
# MENSAJES COLOREADOS (helpers simples → evitan repetir RESET por todos lados)
# =============================================================================

def info(mensaje):
    """Mensaje informativo en azul."""
    print(AZUL + mensaje + RESET)


def exito(mensaje):
    """Mensaje de confirmación en verde."""
    print(VERDE + BRILLO + "✓ " + mensaje + RESET)


def error(mensaje):
    """Mensaje de error en rojo."""
    print(ROJO + BRILLO + "[ERROR] " + mensaje + RESET)


def aviso(mensaje):
    """Mensaje de advertencia en amarillo."""
    print(AMARILLO + "[AVISO] " + mensaje + RESET)


# =============================================================================
# BLOQUE 1: CONEXIÓN Y CREACIÓN DE TABLA
# =============================================================================

def conectar_base_datos():
    """
    Abre (o crea) la base 'productos.db'.

    Retorna:
        sqlite3.Connection | None: la conexión, o None si falló.
    """
    try:
        conexion = sqlite3.connect("productos.db")
        return conexion
    except sqlite3.Error as e:
        error(f"No se pudo conectar a la base de datos: {e}")
        return None


def crear_tabla_productos(conexion):
    """
    Crea la tabla 'productos' si no existe.

    Retorna:
        bool: True si la operación tuvo éxito.
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
        conexion.commit()
        return True
    except sqlite3.Error as e:
        error(f"No se pudo crear la tabla: {e}")
        conexion.rollback()
        return False


# =============================================================================
# BLOQUE 2: VALIDACIÓN DE ENTRADA
# =============================================================================

def pedir_nombre():
    """
    Pide un nombre de producto no vacío. Insiste hasta lograrlo.

    Retorna:
        str | None: nombre validado, o None si se interrumpe la entrada.
    """
    while True:
        try:
            nombre = input(CYAN + "Nombre del producto: " + RESET).strip()
        except EOFError:
            error("Entrada interrumpida.")
            return None

        if nombre == "":
            error("El nombre no puede estar vacío.")
        else:
            return nombre


def pedir_precio():
    """
    Pide un precio numérico > 0. Insiste hasta lograrlo.

    Retorna:
        float | None: precio validado, o None si se interrumpe la entrada.
    """
    while True:
        try:
            entrada = input(CYAN + "Precio del producto: $" + RESET).strip()
        except EOFError:
            error("Entrada interrumpida.")
            return None

        # try-except para el casting (validación robusta, Clase 12)
        try:
            precio = float(entrada)
        except ValueError:
            error("Ingresá un número válido (ej: 1500 o 1500.50).")
            continue

        if precio <= 0:
            error("El precio debe ser mayor que cero.")
            continue

        return precio


def pedir_id(mensaje):
    """
    Pide un id numérico entero > 0.

    Parámetro:
        mensaje (str): texto a mostrar en el prompt.

    Retorna:
        int | None: id validado, o None si se interrumpe.
    """
    while True:
        try:
            entrada = input(CYAN + mensaje + RESET).strip()
        except EOFError:
            error("Entrada interrumpida.")
            return None

        try:
            id_producto = int(entrada)
        except ValueError:
            error("El ID debe ser un número entero.")
            continue

        if id_producto <= 0:
            error("El ID debe ser mayor que cero.")
            continue

        return id_producto


def pedir_confirmacion(mensaje):
    """
    Pide una confirmación (s/n) y devuelve True solo si responde 's'.

    Parámetro:
        mensaje (str): pregunta a mostrar.

    Retorna:
        bool: True si el usuario confirma.
    """
    while True:
        try:
            respuesta = input(AMARILLO + mensaje + " (s/n): " + RESET).strip().lower()
        except EOFError:
            error("Entrada interrumpida.")
            return False

        if respuesta == "s":
            return True
        elif respuesta == "n":
            return False
        else:
            error("Respondé 's' para sí, 'n' para no.")


# =============================================================================
# BLOQUE 3: CREATE — Insertar un producto (con transacción)
# -----------------------------------------------------------------------------
# - Uso de placeholders '?' → evita inyección SQL (Clase 14).
# - try/except con commit/rollback → transacción segura (Clase 14).
# =============================================================================

def registrar_producto(conexion):
    """Pide nombre y precio validados, e inserta el producto."""
    print(MAGENTA + BRILLO + "\n--- REGISTRAR PRODUCTO ---" + RESET)
    nombre = pedir_nombre()
    if nombre is None:
        return

    precio = pedir_precio()
    if precio is None:
        return

    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
            (nombre, precio)   # parámetros seguros
        )
        conexion.commit()      # confirma la transacción
        exito(f"Producto '{nombre}' registrado por ${precio:.2f}.")
    except sqlite3.Error as e:
        conexion.rollback()    # deshace la transacción si algo falla
        error(f"No se pudo registrar el producto: {e}")


# =============================================================================
# BLOQUE 4: READ — Mostrar todos los productos (SELECT + ORDER BY)
# =============================================================================

def mostrar_productos(conexion):
    """Lista todos los productos con su id, nombre y precio."""
    print(MAGENTA + BRILLO + "\n--- LISTA DE PRODUCTOS ---" + RESET)
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
        productos = cursor.fetchall()

        if len(productos) == 0:
            aviso("No hay productos registrados todavía.")
            return

        for producto in productos:
            id_producto, nombre, precio = producto   # desempaquetado de tupla
            print(f"  {id_producto:>3}. {nombre:<15} -> "
                  f"{VERDE}${precio:>10.2f}{RESET}")

        print(AZUL + "-" * 40 + RESET)
        info(f"Total: {len(productos)} producto(s) registrado(s).")

    except sqlite3.Error as e:
        error(f"No se pudo consultar la base: {e}")


# =============================================================================
# BLOQUE 5: UPDATE — Actualizar precio de un producto (con transacción)
# =============================================================================

def actualizar_producto(conexion):
    """Pide id y nuevo precio, y actualiza el registro si existe."""
    print(MAGENTA + BRILLO + "\n--- ACTUALIZAR PRECIO ---" + RESET)

    id_producto = pedir_id("ID del producto a actualizar: ")
    if id_producto is None:
        return

    # Verificamos que exista antes de pedir el precio (mejor UX)
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nombre FROM productos WHERE id = ?",
            (id_producto,)
        )
        fila = cursor.fetchone()
    except sqlite3.Error as e:
        error(f"No se pudo consultar el producto: {e}")
        return

    if fila is None:
        aviso(f"No existe un producto con ID {id_producto}.")
        return

    nombre = fila[0]
    info(f"Producto encontrado: '{nombre}'.")

    nuevo_precio = pedir_precio()
    if nuevo_precio is None:
        return

    try:
        cursor.execute(
            "UPDATE productos SET precio = ? WHERE id = ?",
            (nuevo_precio, id_producto)   # parámetros seguros
        )
        conexion.commit()
        exito(f"Precio de '{nombre}' actualizado a ${nuevo_precio:.2f}.")
    except sqlite3.Error as e:
        conexion.rollback()
        error(f"No se pudo actualizar el producto: {e}")


# =============================================================================
# BLOQUE 6: DELETE — Eliminar un producto con confirmación
# -----------------------------------------------------------------------------
# Doble salvaguarda (requisito 2 del cliente):
#   1) Verificamos que el producto exista antes de preguntar.
#   2) Pedimos confirmación explícita (s/n) antes de borrar.
# =============================================================================

def eliminar_producto(conexion):
    """Pide id, muestra el producto y solicita confirmación antes de borrar."""
    print(MAGENTA + BRILLO + "\n--- ELIMINAR PRODUCTO ---" + RESET)

    id_producto = pedir_id("ID del producto a eliminar: ")
    if id_producto is None:
        return

    # Consultar antes para poder confirmar y mostrar el nombre
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nombre, precio FROM productos WHERE id = ?",
            (id_producto,)
        )
        fila = cursor.fetchone()
    except sqlite3.Error as e:
        error(f"No se pudo consultar el producto: {e}")
        return

    if fila is None:
        aviso(f"No existe un producto con ID {id_producto}.")
        return

    nombre, precio = fila
    print(f"  Producto a eliminar: {BRILLO}{nombre}{RESET} "
          f"(precio ${precio:.2f})")

    # Confirmación obligatoria
    if not pedir_confirmacion("¿Confirmás la eliminación?"):
        aviso("Operación cancelada. El producto NO fue eliminado.")
        return

    # Ejecutar el DELETE solo después de la confirmación
    try:
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        exito(f"Producto '{nombre}' eliminado correctamente.")
    except sqlite3.Error as e:
        conexion.rollback()
        error(f"No se pudo eliminar el producto: {e}")


# =============================================================================
# BLOQUE 7: MENÚ PRINCIPAL
# =============================================================================

def mostrar_menu():
    """Imprime el menú con colores. Función sin return (solo efecto)."""
    print("\n" + MAGENTA + BRILLO + "=" * 48 + RESET)
    print(MAGENTA + BRILLO + "   SISTEMA DE PRODUCTOS - TALENTOLAB" + RESET)
    print(MAGENTA + BRILLO + "=" * 48 + RESET)
    print(AMARILLO + "  1." + RESET + " Registrar producto")
    print(AMARILLO + "  2." + RESET + " Mostrar productos")
    print(AMARILLO + "  3." + RESET + " Actualizar precio")
    print(AMARILLO + "  4." + RESET + " Eliminar producto")
    print(AMARILLO + "  5." + RESET + " Salir")
    print(MAGENTA + BRILLO + "=" * 48 + RESET)


def pedir_opcion():
    """
    Pide una opción válida del menú (1-5).

    Retorna:
        str: opción elegida, o "" si la entrada se interrumpió.
    """
    while True:
        try:
            opcion = input(CYAN + "Elegí una opción (1-5): " + RESET).strip()
        except EOFError:
            error("Entrada interrumpida.")
            return ""

        if opcion in ["1", "2", "3", "4", "5"]:
            return opcion
        error("Opción inválida. Ingresá un número del 1 al 5.")


def main():
    """Orquesta el CRUD completo."""
    conexion = conectar_base_datos()
    if conexion is None:
        return

    if not crear_tabla_productos(conexion):
        conexion.close()
        return

    try:
        while True:
            mostrar_menu()
            opcion = pedir_opcion()

            if opcion == "1":
                registrar_producto(conexion)
            elif opcion == "2":
                mostrar_productos(conexion)
            elif opcion == "3":
                actualizar_producto(conexion)
            elif opcion == "4":
                eliminar_producto(conexion)
            elif opcion == "5":
                info("\nCerrando el sistema... ¡Hasta luego!")
                break
            else:
                # Entrada interrumpida (EOFError en pedir_opcion)
                break
    finally:
        conexion.close()
        info("Conexión con 'productos.db' cerrada correctamente.")


# =============================================================================
# Punto de entrada
# =============================================================================
main()