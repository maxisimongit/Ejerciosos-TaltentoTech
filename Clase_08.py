"""
===============================================================================
EJERCICIO PRÁCTICO - CLASE 8: DICCIONARIOS
===============================================================================

ENUNCIADO:

Has aprendido y conocido todo sobre los diccionarios y su enorme importancia
en el mundo de la programación. Mariana te escribió una nota donde te explica
claramente la tarea que debe resolver el programa que deberás escribir el día
de hoy:

    ¡Hola!
    En TalentoLab nos han pedido desarrollar una aplicación que registre
    productos y sus precios utilizando diccionarios. Necesitamos que tu
    programa cumpla con estas instrucciones:

    - Crear un diccionario llamado 'productos' donde las claves sean los
      nombres de los productos y los valores sean sus precios.
    - Permitir agregar productos y sus precios hasta que se decida finalizar.
    - Mostrar el contenido del diccionario después de cada operación.

    Consejo de Luis: Recordá que los diccionarios te permiten acceder a los
    datos rápidamente usando claves y que podés modificar sus valores sin
    problemas. Aprovechá esto para hacer que tu programa sea eficiente y
    fácil de usar.

===============================================================================
"""

# =============================================================================
# PASO 1: Crear el diccionario vacío 'productos'
# -----------------------------------------------------------------------------
# Estructura:  { "nombre_producto" : precio_en_float }
#   - Clave: str   (nombre del producto)
#   - Valor: float (precio del producto)
# =============================================================================
productos = {}

print("=" * 60)
print("     REGISTRO DE PRODUCTOS - TALENTOLAB")
print("=" * 60)
print(" Instrucciones: escribí 'salir' para finalizar el programa.\n")

# =============================================================================
# PASO 2: Bucle principal (while + break) para registrar productos
# =============================================================================
while True:

    # --- 2.1 Pedir el nombre del producto al usuario ---
    # .strip() elimina espacios sobrantes al inicio y al final (Clase 4)
    nombre = input("Nombre del producto: ").strip()

    # Condición de salida: si el usuario escribe "salir" (sin importar
    # mayúsculas/minúsculas), terminamos el bucle con break (Clase 5).
    if nombre.lower() == "salir":
        print("\nCerrando el registro...\n")
        break

    # Validación: el nombre no puede estar vacío
    if nombre == "":
        print("  [ERROR] El nombre no puede estar vacío. Intentá otra vez.\n")
        continue

    # --- 2.2 Si el producto ya existe, preguntar si actualizar su precio ---
    # El operador 'in' devuelve True si la clave existe en el diccionario.
    # Aprovechamos el consejo de Luis: podemos modificar valores fácilmente.
    if nombre in productos:
        print(f"  El producto '{nombre}' ya está registrado "
              f"con un precio de ${productos[nombre]:.2f}")
        respuesta = input("  ¿Querés actualizar su precio? (s/n): ").strip().lower()
        if respuesta != "s":
            print("  Producto no modificado.\n")
            continue

    # --- 2.3 Pedir el precio con validación robusta usando while ---
    # Sin try/except (no visto en el curso). Validamos con métodos de
    # cadenas (Clase 4):
    #   1) La cadena no puede estar vacía.
    #   2) No puede tener más de un punto decimal.
    #   3) Al quitar el punto, todos los caracteres deben ser dígitos.
    # Esto rechaza letras, signos negativos, entradas vacías, etc.
    while True:
        precio_texto = input(f"Precio de '{nombre}': $").strip()

        if precio_texto == "":
            print("  [ERROR] El precio no puede estar vacío.")
        elif precio_texto.count(".") > 1:
            print("  [ERROR] Solo se permite un punto decimal.")
        elif not precio_texto.replace(".", "").isdigit():
            print("  [ERROR] Ingresá un número positivo (ej: 1500 o 1500.50).")
        else:
            # Conversión de str a float (Clase 2)
            precio = float(precio_texto)
            break

    # --- 2.4 Guardar o actualizar el producto en el diccionario ---
    # Si la clave no existe, se crea. Si ya existe, se sobrescribe el valor.
    productos[nombre] = precio

    # --- 2.5 Mostrar el contenido actualizado del diccionario ---
    # Se recorre el diccionario con items() (Clase 8).
    print("\n  --- Contenido actual de 'productos' ---")
    for clave, valor in productos.items():
        print(f"    {clave}: ${valor:.2f}")
    print(f"  Total de productos registrados: {len(productos)}")

    # Acumulador (Clase 5) para calcular el valor total del inventario
    total_inventario = 0
    for valor in productos.values():
        total_inventario = total_inventario + valor
    print(f"  Valor total del inventario: ${total_inventario:.2f}\n")

# =============================================================================
# PASO 3: Resumen final cuando el usuario decide salir
# =============================================================================
print("=" * 60)
print("     RESUMEN FINAL DEL REGISTRO")
print("=" * 60)

if len(productos) == 0:
    print(" No se registró ningún producto.\n")
else:
    for clave, valor in productos.items():
        print(f"    - {clave}: ${valor:.2f}")

    total_final = 0
    for valor in productos.values():
        total_final = total_final + valor

    print("-" * 60)
    print(f"    Cantidad de productos distintos: {len(productos)}")
    print(f"    Valor total del inventario:      ${total_final:.2f}")
    print("=" * 60)