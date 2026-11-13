"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 11: MÓDULOS (colorama + datetime)
===============================================================================

ENUNCIADO:

Cómo es habitual, finalizas el día con una reunión de trabajo en la oficina
de Mariana, que te felicita por tu progreso. "Luis me mostró el programa de
gestión de frutas que desarrollaste, y estoy muy impresionada con lo bien
que aplicaste las funciones para organizar el código. Sin embargo, es hora
de mejorarlo:

    Tu tarea es volver a modificar el programa que escribiste la clase
    anterior, para que realice las mismas tareas, pero que su interacción
    mediante la terminal esté mejorada utilizando Colorama. También sería
    genial si agregas un dato a cada producto que contenga la fecha y hora
    de la compra, usando la librería datetime.

TAREAS:
    - Agregar productos: cada producto tendrá nombre, precio y FECHA/HORA
      de la compra.
    - Consultar productos: muestra todos los productos junto con sus datos.
    - Eliminar productos: a partir de su nombre.
    - Menú interactivo mejorado con colores (colorama) para una mejor UX.

===============================================================================
"""

# =============================================================================
# IMPORTACIÓN DE MÓDULOS ESTÁNDAR / EXTERNOS (Clase 11)
# -----------------------------------------------------------------------------
# - colorama: agrega colores a la salida de la terminal.
# - datetime: proporciona la fecha y hora actual (para la compra).
# Ambas son las librerías sugeridas por la consigna.
# =============================================================================
from colorama import init, Fore, Style
from datetime import datetime

# init() es necesario en Windows para habilitar colores; en Linux/Mac es
# inocuo (no rompe nada). Lo llamamos una sola vez al inicio.
init()

# =============================================================================
# CONSTANTES DE COLOR Y ESTILO (aliases legibles)
# =============================================================================
RESET    = Style.RESET_ALL
BRILLANTE = Style.BRIGHT
ROJO     = Fore.RED
VERDE    = Fore.GREEN
AMARILLO = Fore.YELLOW
CYAN     = Fore.CYAN
MAGENTA  = Fore.MAGENTA
AZUL     = Fore.BLUE


# =============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN (devuelven valores — Clase 10)
# =============================================================================

def precio_valido(texto):
    """
    Verifica si 'texto' representa un precio válido.

    Parámetro:
        texto (str): cadena ingresada por el usuario.

    Retorna:
        bool: True si es un número positivo con a lo sumo un punto decimal.
              False en cualquier otro caso (vacío, con letras, con varios
              puntos, con signos, etc.).
    """
    if texto == "":
        return False
    if texto.count(".") > 1:
        return False
    if not texto.replace(".", "").isdigit():
        return False
    return True


def pedir_nombre_producto():
    """
    Solicita un nombre de producto no vacío, insistiendo hasta que
    el usuario ingrese uno válido.

    Retorna:
        str: nombre del producto (sin espacios extremos).
    """
    while True:
        # El prompt se colorea con cyan para diferenciar la entrada del usuario
        nombre = input(CYAN + "Nombre del producto: " + RESET).strip()
        if nombre == "":
            print(ROJO + "  [ERROR] El nombre no puede estar vacío." + RESET)
        else:
            return nombre


def pedir_precio(nombre_producto):
    """
    Solicita un precio válido para el producto indicado, insistiendo hasta
    que ingrese uno correcto.

    Parámetro:
        nombre_producto (str): nombre a mostrar en el prompt.

    Retorna:
        float: precio ingresado, ya convertido a número decimal.
    """
    while True:
        precio_texto = input(
            CYAN + f"Precio de '{nombre_producto}': $" + RESET
        ).strip()
        if precio_valido(precio_texto):
            return float(precio_texto)
        print(ROJO + "  [ERROR] Ingresá un número válido "
                     "(ej: 1500 o 1500.50)." + RESET)


# =============================================================================
# FUNCIONES DE NEGOCIO (devuelven uno o varios valores — Clase 10)
# =============================================================================

def agregar_producto(lista_productos):
    """
    Agrega un nuevo producto a la lista, o actualiza el precio de uno
    existente. Al crear un producto registra la FECHA Y HORA de compra
    usando datetime.now() (Clase 11).

    Parámetro:
        lista_productos (list): lista de dicts con 'nombre', 'precio' y
                                'fecha_compra'.

    Retorna:
        tuple: (exito (bool), mensaje (str))
    """
    print(MAGENTA + BRILLANTE + "\n--- AGREGAR PRODUCTO ---" + RESET)
    nombre = pedir_nombre_producto()

    # --- ¿Ya existe el producto? ---
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            print(AMARILLO + f"  [AVISO] Ya existe '{producto['nombre']}' "
                             f"con precio ${producto['precio']:.2f}" + RESET)
            print(AZUL + f"  Registrado el: {producto['fecha_compra']}" + RESET)
            respuesta = input(
                AMARILLO + "  ¿Actualizar su precio? (s/n): " + RESET
            ).strip().lower()

            if respuesta != "s":
                return (False, "Producto no modificado.")

            # Actualizamos solo el precio; la fecha de la compra original
            # se conserva (esa compra fue en el pasado).
            nuevo_precio = pedir_precio(nombre)
            producto["precio"] = nuevo_precio
            return (True,
                    f"Precio actualizado: '{producto['nombre']}' -> "
                    f"${nuevo_precio:.2f}")

    # --- Producto nuevo: pedir precio y capturar fecha/hora de compra ---
    precio = pedir_precio(nombre)
    fecha_compra = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    nuevo_producto = {
        "nombre":       nombre,
        "precio":       precio,
        "fecha_compra": fecha_compra,
    }
    lista_productos.append(nuevo_producto)
    return (True,
            f"Producto agregado: '{nombre}' -> ${precio:.2f} "
            f"(el {fecha_compra})")


def consultar_productos(lista_productos):
    """
    Recorre la lista y devuelve información agregada para mostrar en main().
    Ejemplo de función con MÚLTIPLES valores de retorno (Clase 10).

    Parámetro:
        lista_productos (list): lista de dicts con 'nombre', 'precio' y
                                'fecha_compra'.

    Retorna:
        tuple: (cantidad (int), total (float), listado (list de str))
    """
    cantidad = len(lista_productos)

    # Retorno anticipado: sin productos, devolvemos valores neutros
    if cantidad == 0:
        return (0, 0.0, [])

    total = 0
    listado = []
    for i in range(cantidad):
        producto = lista_productos[i]
        total = total + producto["precio"]

        # Armamos la línea completa con colorama: precio verde, fecha azul.
        linea = (
            f"  {i + 1}. {producto['nombre']:<15} -> "
            f"{VERDE}${producto['precio']:>10.2f}{RESET}   "
            f"{AZUL}| Comprado: {producto['fecha_compra']}{RESET}"
        )
        listado.append(linea)

    return (cantidad, total, listado)


def eliminar_producto(lista_productos):
    """
    Elimina un producto de la lista a partir de su nombre.

    Parámetro:
        lista_productos (list): lista de dicts con 'nombre', 'precio' y
                                'fecha_compra'.

    Retorna:
        tuple: (exito (bool), mensaje (str))
    """
    print(MAGENTA + BRILLANTE + "\n--- ELIMINAR PRODUCTO ---" + RESET)

    if len(lista_productos) == 0:
        return (False, "No hay productos para eliminar.")

    nombre = input(CYAN + "Nombre del producto a eliminar: " + RESET).strip()
    if nombre == "":
        return (False, "El nombre no puede estar vacío.")

    # Buscamos primero y eliminamos después (no mutar mientras iteramos)
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            lista_productos.remove(producto)
            return (True,
                    f"Producto eliminado: '{producto['nombre']}' "
                    f"(precio ${producto['precio']:.2f}, "
                    f"comprado el {producto['fecha_compra']})")

    return (False, f"No se encontró ningún producto con el nombre '{nombre}'.")


# =============================================================================
# FUNCIONES DE INTERFAZ (una sin return y otra con return — comparación)
# =============================================================================

def mostrar_menu():
    """
    Imprime el menú principal con colorama.
    Función SIN return: solo produce un efecto visual.
    """
    print("\n" + MAGENTA + BRILLANTE + "=" * 55 + RESET)
    print(MAGENTA + BRILLANTE +
          "        GESTIÓN DE PRODUCTOS - TALENTOLAB" + RESET)
    print(MAGENTA + BRILLANTE + "=" * 55 + RESET)
    print(AMARILLO + "  1." + RESET + " Agregar producto")
    print(AMARILLO + "  2." + RESET + " Consultar productos")
    print(AMARILLO + "  3." + RESET + " Eliminar producto")
    print(AMARILLO + "  4." + RESET + " Salir")
    print(MAGENTA + BRILLANTE + "=" * 55 + RESET)


def pedir_opcion():
    """
    Solicita y valida la opción del menú.
    Función CON return: devuelve la opción ya validada.

    Retorna:
        str: una de las opciones '1', '2', '3' o '4'.
    """
    while True:
        opcion = input(CYAN + "Elegí una opción (1-4): " + RESET).strip()
        if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4":
            return opcion
        print(ROJO + "  [ERROR] Opción inválida. "
                     "Ingresá un número del 1 al 4." + RESET)


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """
    Orquesta el menú. Recibe los valores devueltos por cada función y
    decide qué mostrar usando colorama según el resultado.
    """
    productos = []  # lista de dicts: {"nombre", "precio", "fecha_compra"}

    while True:
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion == "1":
            exito, mensaje = agregar_producto(productos)
            if exito:
                print(VERDE + "  ✓ " + mensaje + RESET)
            else:
                print(AMARILLO + "  ℹ " + mensaje + RESET)

        elif opcion == "2":
            cantidad, total, listado = consultar_productos(productos)
            print(MAGENTA + BRILLANTE +
                  "\n--- LISTA DE PRODUCTOS ---" + RESET)
            if cantidad == 0:
                print(AMARILLO + "  No hay productos registrados todavía."
                      + RESET)
            else:
                for linea in listado:
                    print(linea)
                print(AZUL + "-" * 55 + RESET)
                print(VERDE + f"  Cantidad de productos: {cantidad}" + RESET)
                print(VERDE + f"  Valor total del inventario: "
                              f"${total:.2f}" + RESET)

        elif opcion == "3":
            exito, mensaje = eliminar_producto(productos)
            if exito:
                print(VERDE + "  ✓ " + mensaje + RESET)
            else:
                print(ROJO + "  ✗ " + mensaje + RESET)

        elif opcion == "4":
            print(VERDE + BRILLANTE +
                  "\n¡Hasta luego! Cerrando el programa..." + RESET)
            break


# =============================================================================
# Punto de entrada
# =============================================================================
main()