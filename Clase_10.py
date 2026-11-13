"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 10: FUNCIONES DEFINIDAS POR EL USUARIO II
Refactor del programa de gestión de productos usando RETURN
===============================================================================

ENUNCIADO:

El día finaliza con otra reunión en la oficina de Mariana. Con su energía
habitual, te felicita por el progreso que estás logrando. "Luis me mostró el
programa de gestión de frutas que desarrollaste, y estoy muy impresionada con
lo bien que aplicaste las funciones para organizar el código. Sin embargo,
quiero proponerte un desafío adicional:

    Tu tarea es modificar el programa que escribiste la clase anterior, para
    que realice las mismas tareas, pero utilizando funciones que devuelvan
    valores cuando sea posible. Recordá que el programa te permitía:

    - Agregar productos: cada producto debe tener un nombre y un precio.
    - Consultar productos: muestra todos los productos en la lista junto con
      sus precios.
    - Eliminar productos: a partir de su nombre.
    - Menú interactivo: debe ofrecer un menú para que se pueda elegir qué
      acción realizar.

===============================================================================
"""


# =============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN (devuelven valores)
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
    Solicita al usuario un nombre de producto no vacío, insistiendo hasta
    que ingrese uno válido.

    Retorna:
        str: nombre del producto (sin espacios extremos).
    """
    while True:
        nombre = input("Nombre del producto: ").strip()
        if nombre == "":
            print("  [ERROR] El nombre no puede estar vacío.")
        else:
            return nombre


def pedir_precio(nombre_producto):
    """
    Solicita al usuario un precio válido para el producto indicado,
    insistiendo hasta que ingrese uno correcto.

    Parámetro:
        nombre_producto (str): nombre a mostrar en el prompt.

    Retorna:
        float: precio ingresado, ya convertido a número decimal.
    """
    while True:
        precio_texto = input(f"Precio de '{nombre_producto}': $").strip()
        if precio_valido(precio_texto):
            return float(precio_texto)
        else:
            print("  [ERROR] Ingresá un número válido (ej: 1500 o 1500.50).")


# =============================================================================
# FUNCIONES DE NEGOCIO (devuelven uno o varios valores)
# =============================================================================

def agregar_producto(lista_productos):
    """
    Agrega un nuevo producto a la lista o actualiza el precio de uno
    existente. Como las listas y los diccionarios son MUTABLES, los cambios
    quedan reflejados en la lista original (paso por referencia, Clase 9).

    Parámetro:
        lista_productos (list): lista de diccionarios con 'nombre' y 'precio'.

    Retorna:
        tuple: (exito (bool), mensaje (str))
            exito -> True si se agregó o actualizó, False si no se modificó.
            mensaje -> texto para mostrar al usuario.
    """
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = pedir_nombre_producto()

    # Buscar si ya existe un producto con el mismo nombre
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            print(f"  [AVISO] Ya existe '{producto['nombre']}' "
                  f"con precio ${producto['precio']:.2f}")
            respuesta = input("  ¿Actualizar su precio? (s/n): ").strip().lower()
            if respuesta != "s":
                return (False, "Producto no modificado.")

            # Actualizamos el valor dentro del diccionario (mutabilidad)
            nuevo_precio = pedir_precio(nombre)
            producto["precio"] = nuevo_precio
            return (True, f"Precio actualizado: '{producto['nombre']}' "
                          f"-> ${nuevo_precio:.2f}")

    # Si no existe: crear el diccionario y agregarlo a la lista
    precio = pedir_precio(nombre)
    nuevo_producto = {"nombre": nombre, "precio": precio}
    lista_productos.append(nuevo_producto)
    return (True, f"Producto agregado: '{nombre}' -> ${precio:.2f}")


def consultar_productos(lista_productos):
    """
    Recorre la lista de productos y devuelve información agregada.
    Ejemplo de 'función que devuelve MÚLTIPLES valores'.

    Parámetro:
        lista_productos (list): lista de diccionarios con 'nombre' y 'precio'.

    Retorna:
        tuple: (cantidad (int), total (float), listado (list de str))
            cantidad -> cuántos productos distintos hay.
            total    -> suma de todos los precios (valor del inventario).
            listado  -> lista de líneas ya formateadas para imprimir.
    """
    cantidad = len(lista_productos)

    # Retorno anticipado: si no hay productos, devolvemos valores neutros
    if cantidad == 0:
        return (0, 0.0, [])

    total = 0
    listado = []
    for i in range(cantidad):
        producto = lista_productos[i]
        total = total + producto["precio"]
        listado.append(f"  {i + 1}. {producto['nombre']} -> "
                       f"${producto['precio']:.2f}")

    return (cantidad, total, listado)


def eliminar_producto(lista_productos):
    """
    Elimina un producto de la lista a partir de su nombre.

    Parámetro:
        lista_productos (list): lista de diccionarios con 'nombre' y 'precio'.

    Retorna:
        tuple: (exito (bool), mensaje (str))
    """
    print("\n--- ELIMINAR PRODUCTO ---")

    if len(lista_productos) == 0:
        return (False, "No hay productos para eliminar.")

    nombre = input("Nombre del producto a eliminar: ").strip()
    if nombre == "":
        return (False, "El nombre no puede estar vacío.")

    # Buscamos primero y eliminamos después (no mutar mientras iteramos)
    for producto in lista_productos:
        if producto["nombre"].lower() == nombre.lower():
            lista_productos.remove(producto)
            return (True, f"Producto eliminado: '{producto['nombre']}' "
                          f"(precio ${producto['precio']:.2f})")

    return (False, f"No se encontró ningún producto con el nombre '{nombre}'.")


# =============================================================================
# FUNCIONES DE INTERFAZ (una sin return, otra con return — comparación)
# =============================================================================

def mostrar_menu():
    """
    Imprime el menú principal.
    Función SIN return: solo produce un efecto (mostrar en pantalla).
    """
    print("\n" + "=" * 45)
    print("   GESTIÓN DE PRODUCTOS - TALENTOLAB")
    print("=" * 45)
    print("  1. Agregar producto")
    print("  2. Consultar productos")
    print("  3. Eliminar producto")
    print("  4. Salir")
    print("=" * 45)


def pedir_opcion():
    """
    Solicita y valida la opción del menú.
    Función CON return: devuelve la opción ya validada para que main() decida
    qué hacer. Esto separa la 'entrada' de la 'decisión'.

    Retorna:
        str: una de las opciones '1', '2', '3' o '4'.
    """
    while True:
        opcion = input("Elegí una opción (1-4): ").strip()
        if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4":
            return opcion
        print("  [ERROR] Opción inválida. Ingresá un número del 1 al 4.")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """
    Coordina el menú principal. Observá que ahora main() casi no imprime:
    recibe los valores devueltos por cada función y decide qué mostrar.
    """
    productos = []  # lista de dicts: {"nombre": ..., "precio": ...}

    while True:
        mostrar_menu()          # efecto: imprime
        opcion = pedir_opcion() # return: devuelve la opción validada

        if opcion == "1":
            exito, mensaje = agregar_producto(productos)
            print(f"  {mensaje}")

        elif opcion == "2":
            cantidad, total, listado = consultar_productos(productos)
            print("\n--- LISTA DE PRODUCTOS ---")
            if cantidad == 0:
                print("  No hay productos registrados todavía.")
            else:
                for linea in listado:
                    print(linea)
                print("-" * 45)
                print(f"  Cantidad de productos: {cantidad}")
                print(f"  Valor total del inventario: ${total:.2f}")

        elif opcion == "3":
            exito, mensaje = eliminar_producto(productos)
            print(f"  {mensaje}")

        elif opcion == "4":
            print("\n¡Hasta luego! Cerrando el programa...")
            break


# =============================================================================
# Punto de entrada
# =============================================================================
main()