"""
================================================================================
EJERCICIO PRÁCTICO — Clase N° 7 | Listas y tuplas
================================================================================
Enunciado:
Mariana te ha escrito un correo donde te explica claramente la tarea que
debe resolver el programa a desarrollar:

¡Hola!
En TalentoLab necesitamos llevar un registro ordenado de los nombres de los
nuevos clientes y clientas que se van incorporando. Queremos asegurarnos de
que los datos ingresados sean válidos y estén bien organizados. Tu tarea es
escribir un programa en Python que haga lo siguiente:

    1. Solicite al usuario o usuaria los nombres de los clientes y clientas
       uno por uno y valide que cada nombre no esté vacío. Si se deja el
       campo vacío, mostrale un mensaje de advertencia y volvé a pedir el
       nombre.
    2. Guarde cada nombre válido en una lista, asegurándote de agregarlo con
       el método .append().
    3. Permita que la persona finalice la carga de nombres escribiendo la
       palabra "fin".
    4. Una vez finalizada la carga, ordene alfabéticamente los nombres en la
       lista y muestre la lista ordenada de nombres utilizando un bucle for.

Temas aplicados:
    - Listas y método .append()
    - Método .remove(), .copy(), .sort()
    - Tuplas: creación, acceso, conversión lista <-> tupla
    - Slices y diferencia con el acceso directo
================================================================================
"""

import re  # Para validar el formato del nombre con una expresión regular


# Patrón que permite letras (con o sin acentos), espacios, guiones y apóstrofes.
# Rechaza números y símbolos extraños: refuerza la robustez del programa.
PATRON_NOMBRE_VALIDO = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ'\- ]+$")


# ---------------------------------------------------------------------------
# BLOQUE 1: Carga de nombres con validación
# ---------------------------------------------------------------------------
def solicitar_nombres_clientes() -> list:
    """
    Pide nombres al usuario hasta que escriba 'fin'.
    Valida que no estén vacíos y que solo contengan caracteres razonables.
    Devuelve la lista de nombres válidos ingresados.
    """
    lista_clientes = []

    while True:
        try:
            entrada = input(
                "Ingrese el nombre del cliente ('fin' para terminar): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            # Si el usuario corta la ejecución (Ctrl+C / Ctrl+D) no rompemos el flujo
            print("\n⚠️  Entrada interrumpida. Se cierra la carga.")
            break

        # Condición de salida
        if entrada.lower() == "fin":
            break

        # Validación 1: campo vacío
        if not entrada:
            print("⚠️  El nombre no puede estar vacío. Intente nuevamente.\n")
            continue

        # Validación 2: caracteres inválidos
        if not PATRON_NOMBRE_VALIDO.match(entrada):
            print(
                "⚠️  El nombre solo puede contener letras, espacios, "
                "guiones o apóstrofes. Intente nuevamente.\n"
            )
            continue

        # Nombre válido → se agrega con .append()
        lista_clientes.append(entrada)
        print(f"✔️  Cliente '{entrada}' agregado. Total: {len(lista_clientes)}\n")

    return lista_clientes


# ---------------------------------------------------------------------------
# BLOQUE 2: Ordenar y mostrar la lista con un bucle for
# ---------------------------------------------------------------------------
def mostrar_lista_ordenada(lista_clientes: list) -> None:
    """
    Ordena alfabéticamente (insensible a mayúsculas) e imprime
    cada nombre con un bucle for.
    """
    # key=str.lower hace que 'ana' y 'Ana' se ordenen juntos (mejor UX)
    lista_clientes.sort(key=str.lower)

    print("\n===== CLIENTES ORDENADOS ALFABÉTICAMENTE =====")
    for posicion, nombre in enumerate(lista_clientes, start=1):
        print(f"  {posicion}. {nombre}")


# ---------------------------------------------------------------------------
# BLOQUE 3 (EXTRA DIDÁCTICO): Demostración de conceptos de la clase
# ---------------------------------------------------------------------------
def demostrar_conceptos_de_la_clase(lista_clientes: list) -> None:
    """
    Muestra en consola ejemplos de los conceptos vistos en la clase:
    - Conversión lista <-> tupla
    - Slices
    - Diferencia entre slicing y acceso directo
    - Uso de .remove() y .copy()
    """
    print("\n===== DEMOSTRACIÓN DE CONCEPTOS DE LA CLASE =====")

    # Conversión lista → tupla (las tuplas son inmutables)
    tupla_clientes = tuple(lista_clientes)
    print(f"Lista original : {lista_clientes}   (tipo: {type(lista_clientes).__name__})")
    print(f"Tupla derivada : {tupla_clientes}   (tipo: {type(tupla_clientes).__name__})")

    # Acceso directo vs slicing
    if tupla_clientes:
        print(f"Acceso directo  [0]      -> '{tupla_clientes[0]}'  (un solo elemento)")
    if len(tupla_clientes) >= 2:
        print(f"Slicing         [:2]     -> {tupla_clientes[:2]}   (subtubla)")
        print(f"Slicing         [-2:]    -> {tupla_clientes[-2:]}")
    if len(tupla_clientes) >= 3:
        print(f"Slicing         [1:3]    -> {tupla_clientes[1:3]}")

    # Ejemplo de .remove() trabajando sobre una COPIA para no romper la lista original
    if len(lista_clientes) > 1:
        copia = lista_clientes.copy()
        nombre_eliminado = copia[0]
        copia.remove(nombre_eliminado)
        print(
            f"Ejemplo .remove()  -> se quitó '{nombre_eliminado}' "
            f"de una copia: {copia}"
        )


# ---------------------------------------------------------------------------
# BLOQUE 4: Función principal (punto de entrada)
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 50)
    print(" REGISTRO DE CLIENTES — TalentLab")
    print("=" * 50)

    clientes = solicitar_nombres_clientes()

    if not clientes:
        print("\nNo se ingresaron clientes válidos. Fin del programa.")
        return

    mostrar_lista_ordenada(clientes)
    demostrar_conceptos_de_la_clase(clientes)

    print("\n¡Registro finalizado con éxito! 🎉")


# Guard clause: solo ejecuta si el archivo se corre directamente
if __name__ == "__main__":
    main()