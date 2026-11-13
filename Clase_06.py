"""
================================================================================
EJERCICIO PRÁCTICO — Clase N° 6 | Bucles for y range()
================================================================================
Enunciado:
Luis está haciendo un excelente trabajo. Al finalizar la jornada, lograste
entender la sintaxis y utilidad de los bucles for, y lo súper útil que son
para recorrer estructuras de datos. Con estas herramientas estás listo para
resolver el pedido de Mariana:

Tu tarea es la siguiente:

Parte 1:
    1. Crear una lista con los nombres de los y las clientes que vamos a
       procesar. Recorrer la lista y mostrar el nombre de cada cliente o
       clienta, junto con su posición en la lista (por ejemplo: Cliente 1,
       Cliente 2, etc.).
    2. Recorrer la lista con un for y mostrar el nombre de cada cliente
       junto con su posición en la lista (por ejemplo: Cliente 1: Ana).
    3. Si encuentras un nombre vacío, mostrar un mensaje de alerta indicando
       que ese dato no es válido.

Ejemplo de salida:
    Cliente 1: Ana
    Cliente 2: Juan
    Cliente 3: [ALERTA] Nombre no válido
    Cliente 4: Marta

Parte 2 (optativa):
    Aplicar el método .capitalize() para que los nombres válidos siempre
    aparezcan en el formato correcto (Primera letra mayúscula, resto
    minúscula), sin importar cómo estén escritos en la lista.

Ejemplo:
    nombre = "mArIa"
    print(nombre.capitalize())   # → "Maria"

Temas aplicados:
    - Bucle for
    - range() en sus variantes: básico, con inicio, con paso, decreciente
      y como herramienta para recorrer listas por índice
    - break y bucles de reintento con input()
    - enumerate() como alternativa más pythonica a range(len(...))
    - Validación de datos del usuario
================================================================================
"""


# Lista de demostración con nombres válidos (en distintas capitalizaciones)
# y también entradas vacías o de solo espacios, para poder mostrar el flujo
# de ALERTA que pide el punto 3 del enunciado.
LISTA_CLIENTES_DEMO = [
    "Ana",
    "jUaN",
    "",           # vacío real
    "Marta",
    "   ",        # solo espacios → también inválido
    "pEdRo",
    "",
]


# ---------------------------------------------------------------------------
# BLOQUE 1: Recorrer y mostrar la lista con for (Parte 1 + Parte 2)
# ---------------------------------------------------------------------------
def procesar_lista_clientes(lista_clientes: list, titulo: str = "") -> None:
    """
    Recorre la lista mostrando la posición y el nombre de cada cliente.
    - Si el nombre está vacío o solo tiene espacios → muestra ALERTA.
    - Si el nombre es válido → lo formatea con .capitalize() (Parte 2).

    Parámetros:
        lista_clientes: lista de strings que puede contener vacíos.
        titulo: texto opcional para encabezar la salida.
    """
    if titulo:
        print(f"\n===== {titulo} =====")

    if not lista_clientes:
        print("(La lista está vacía, no hay nada que mostrar)")
        return

    # ----------------------------------------------------------------------
    # FORMA RECOMENDADA (pythonica): enumerate() devuelve índice + valor
    # en una sola pasada. start=1 hace que la numeración arranque en 1.
    # ----------------------------------------------------------------------
    for posicion, nombre in enumerate(lista_clientes, start=1):
        # Normalizamos: quitamos espacios al inicio/fin
        nombre_limpio = nombre.strip()

        if not nombre_limpio:
            # Punto 3: nombre vacío → alerta, no se procesa como válido
            print(f"Cliente {posicion}: [ALERTA] Nombre no válido")
        else:
            # Parte 2 (optativa): .capitalize() → "mArIa" se vuelve "Maria"
            print(f"Cliente {posicion}: {nombre_limpio.capitalize()}")

    # ----------------------------------------------------------------------
    # ALTERNATIVA EQUIVALENTE usando range() (menos pythonica, pero muy
    # útil para practicar el tema de la clase). Descomentar para probar:
    #
    # for i in range(len(lista_clientes)):
    #     posicion = i + 1
    #     nombre = lista_clientes[i].strip()
    #     if not nombre:
    #         print(f"Cliente {posicion}: [ALERTA] Nombre no válido")
    #     else:
    #         print(f"Cliente {posicion}: {nombre.capitalize()}")
    # ----------------------------------------------------------------------


# ---------------------------------------------------------------------------
# BLOQUE 2: Carga interactiva con validación robusta
# ---------------------------------------------------------------------------
def solicitar_nombres_usuario() -> list:
    """
    Pide nombres al usuario uno por uno con validación robusta:
        - No permite cadenas vacías o de solo espacios (reintenta).
        - No permite caracteres que no sean letras ni espacios.
        - Permite finalizar escribiendo 'fin'.
        - Atrapa Ctrl+C / EOF para no romper la ejecución.

    Devuelve la lista de nombres válidos ingresados.
    """
    lista_nombres = []

    while True:
        try:
            entrada = input(
                "Ingrese un nombre ('fin' para terminar): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️  Entrada interrumpida. Se cierra la carga.")
            break

        # Condición de salida (se acepta 'fin' en cualquier capitalización)
        if entrada.lower() == "fin":
            break

        # Validación 1: campo vacío o solo espacios
        if not entrada:
            print("⚠️  El nombre no puede estar vacío. Intente de nuevo.\n")
            continue

        # Validación 2: solo letras y espacios (evita números o símbolos)
        if not entrada.replace(" ", "").isalpha():
            print("⚠️  Solo se permiten letras y espacios. Intente de nuevo.\n")
            continue

        # Nombre válido → se agrega a la lista
        lista_nombres.append(entrada)
        print(f"✔️  '{entrada}' agregado. Total: {len(lista_nombres)}\n")

    return lista_nombres


# ---------------------------------------------------------------------------
# BLOQUE 3 (EXTRA DIDÁCTICO): Demostración de range()
# ---------------------------------------------------------------------------
def demostrar_range() -> None:
    """
    Muestra los distintos usos de range() vistos en la clase:
    básico, con inicio, con paso, decreciente y para recorrer listas.
    """
    print("\n===== DEMOSTRACIÓN DE range() =====")
    print("range(5)              ->", list(range(5)))            # 0..4
    print("range(1, 6)           ->", list(range(1, 6)))         # 1..5
    print("range(0, 10, 2)       ->", list(range(0, 10, 2)))     # pares
    print("range(5, 0, -1)       ->", list(range(5, 0, -1)))     # 5..1
    print(
        f"len(LISTA_CLIENTES_DEMO) = {len(LISTA_CLIENTES_DEMO)} "
        f"→ se puede recorrer con range({len(LISTA_CLIENTES_DEMO)})"
    )


# ---------------------------------------------------------------------------
# BLOQUE 4: Función principal
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 55)
    print(" PROCESADOR DE CLIENTES — Bucles for y range() ")
    print("=" * 55)

    # ---- Parte 1: procesar la lista de demostración ----
    # Esta lista contiene entradas vacías a propósito para poder mostrar
    # el flujo de alerta del punto 3.
    procesar_lista_clientes(
        LISTA_CLIENTES_DEMO,
        titulo="PARTE 1 — Lista de demostración (con vacíos)",
    )

    # ---- Parte 1 ampliada: el usuario carga sus propios nombres ----
    print("\nAhora podés cargar tu propia lista de clientes.")
    lista_usuario = solicitar_nombres_usuario()

    if lista_usuario:
        procesar_lista_clientes(
            lista_usuario,
            titulo="PARTE 1 — Lista ingresada por el usuario",
        )
    else:
        print("\nNo se ingresaron nombres válidos.")

    # ---- Extra: demostración de range() ----
    demostrar_range()

    print("\n¡Programa finalizado con éxito! 🎉")


# Guard clause: ejecuta solo si se corre el archivo directamente
if __name__ == "__main__":
    main()