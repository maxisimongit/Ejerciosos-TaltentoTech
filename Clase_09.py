"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 9: FUNCIONES DEFINIDAS POR EL USUARIO
===============================================================================

ENUNCIADO:

Mariana te ha asignado una tarea clave para el proyecto de TalentoLab:
desarrollar un pequeño programa que permita gestionar una lista de productos
utilizando funciones. El objetivo es que la usuaria o usuario pueda agregar,
consultar y eliminar productos, aplicando lo aprendido sobre funciones y listas.
Este ejercicio ayudará a modularizar el código y a practicar la interacción con
el usuario. Así lo comunicó Mariana:

    ¡Hola!
    Tu tarea es crear un programa en Python con las siguientes características:

    - Agregar productos: permite agregar productos a una lista. Cada producto
      debe tener un nombre y un precio.
    - Consultar productos: muestra todos los productos en la lista junto con
      sus precios.
    - Eliminar productos: elimina un producto de la lista a partir de su nombre.
    - Menú interactivo: el programa debe ofrecer un menú para que el usuario o
      usuaria pueda elegir qué acción realizar. Debe incluir una opción para
      salir del programa.

===============================================================================
"""


# =============================================================================
# FUNCIÓN AUXILIAR: validar un precio ingresado como texto
# -----------------------------------------------------------------------------
# Validamos con métodos de cadenas de la Clase 4:
#   1) La cadena no puede estar vacía.
#   2) No puede tener más de un punto decimal.
#   3) Al quitar el punto, todos los caracteres deben ser dígitos.
# Esto rechaza letras, signos negativos, entradas vacías, "1.2.3", etc.
# =============================================================================
def precio_valido(texto):
    """Devuelve True si el texto representa un número positivo válido."""
    if texto == "":
        return False
    if texto.count(".") > 1:
        return False
    if not texto.replace(".", "").isdigit():
        return False
    return True


# =============================================================================
# FUNCIÓN 1: Agregar un producto (nombre + precio) a la lista
# -----------------------------------------------------------------------------
# Recibe 'lista_productos' por parámetro. Como las listas son MUTABLES, los
# cambios realizados dentro de la función (append, modificación de sus dicts)
# se reflejan en la lista original del programa principal (Clase 9: mutabilidad
# y referencia).
# =============================================================================
def agregar_producto(lista_productos):
    print("\n--- AGREGAR PRODUCTO ---")

    # --- Pedir el nombre ---
    nombre = input("Nombre del producto: ").strip()
    if nombre == "":
        print("  [ERROR] El nombre no puede estar vacío.")
        return

    # --- Verificar si ya existe un producto con ese nombre ---
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            print(f"  [AVISO] Ya existe '{producto['nombre']}' "
                  f"con precio ${producto['precio']:.2f}")
            respuesta = input("  ¿Actualizar su precio? (s/n): ").strip().lower()
            if respuesta != "s":
                print("  Producto no modificado.")
                return

            # --- Bucle while para validar el nuevo precio ---
            while True:
                precio_texto = input(f"  Nuevo precio de '{nombre}': $").strip()
                if precio_valido(precio_texto):
                    producto["precio"] = float(precio_texto)
                    print(f"  Precio actualizado: '{nombre}' -> "
                          f"${producto['precio']:.2f}")
                    return
                else:
                    print("  [ERROR] Ingresá un número válido (ej: 1500 o 1500.50).")

    # --- Si no existe, es un producto nuevo: pedir precio con validación ---
    while True:
        precio_texto = input(f"Precio de '{nombre}': $").strip()
        if precio_valido(precio_texto):
            # Cada producto es un diccionario con clave "nombre" y "precio"
            nuevo_producto = {"nombre": nombre, "precio": float(precio_texto)}
            lista_productos.append(nuevo_producto)  # append (Clase 7)
            print(f"  Producto agregado: '{nombre}' -> "
                  f"${nuevo_producto['precio']:.2f}")
            return
        else:
            print("  [ERROR] Ingresá un número válido (ej: 1500 o 1500.50).")


# =============================================================================
# FUNCIÓN 2: Consultar todos los productos de la lista
# =============================================================================
def consultar_productos(lista_productos):
    print("\n--- LISTA DE PRODUCTOS ---")

    # Validación: si la lista está vacía, avisamos y salimos
    if len(lista_productos) == 0:
        print("  No hay productos registrados todavía.")
        return

    # Recorremos con range(len(...)) (Clase 6) para mostrar un número de orden
    for i in range(len(lista_productos)):
        producto = lista_productos[i]
        print(f"  {i + 1}. {producto['nombre']} -> ${producto['precio']:.2f}")

    # Acumulador (Clase 5) para calcular el valor total del inventario
    total_inventario = 0
    for producto in lista_productos:
        total_inventario = total_inventario + producto["precio"]

    print("-" * 45)
    print(f"  Cantidad de productos: {len(lista_productos)}")
    print(f"  Valor total del inventario: ${total_inventario:.2f}")


# =============================================================================
# FUNCIÓN 3: Eliminar un producto de la lista a partir de su nombre
# =============================================================================
def eliminar_producto(lista_productos):
    print("\n--- ELIMINAR PRODUCTO ---")

    if len(lista_productos) == 0:
        print("  No hay productos para eliminar.")
        return

    nombre = input("Nombre del producto a eliminar: ").strip()
    if nombre == "":
        print("  [ERROR] El nombre no puede estar vacío.")
        return

    # Buscamos el producto por nombre y, si lo encontramos, lo eliminamos con
    # el método remove() (Clase 7).
    # Nota: NO modificamos la lista mientras la iteramos con for-in; buscamos
    # primero y eliminamos después (buena práctica de mutabilidad, Clase 9).
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            lista_productos.remove(producto)
            print(f"  Producto eliminado: '{producto['nombre']}' "
                  f"(precio ${producto['precio']:.2f})")
            return

    print(f"  [AVISO] No se encontró ningún producto con el nombre '{nombre}'.")


# =============================================================================
# FUNCIÓN 4: Mostrar el menú principal de opciones
# =============================================================================
def mostrar_menu():
    print("\n" + "=" * 45)
    print("   GESTIÓN DE PRODUCTOS - TALENTOLAB")
    print("=" * 45)
    print("  1. Agregar producto")
    print("  2. Consultar productos")
    print("  3. Eliminar producto")
    print("  4. Salir")
    print("=" * 45)


# =============================================================================
# FUNCIÓN PRINCIPAL: coordina el menú y las operaciones
# =============================================================================
def main():
    # Lista de productos. Cada elemento será un diccionario con nombre y precio.
    # Se pasa por referencia a cada función (Clase 9).
    productos = []

    # Bucle while indeterminado (Clase 5) con break para salir
    while True:
        mostrar_menu()
        opcion = input("Elegí una opción (1-4): ").strip()

        if opcion == "1":
            agregar_producto(productos)
        elif opcion == "2":
            consultar_productos(productos)
        elif opcion == "3":
            eliminar_producto(productos)
        elif opcion == "4":
            print("\n¡Hasta luego! Cerrando el programa...")
            break
        else:
            print("  [ERROR] Opción inválida. Ingresá un número del 1 al 4.")


# =============================================================================
# Punto de entrada del programa
# =============================================================================
main()