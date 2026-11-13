# Nuestro cliente nos pide que el programa ahora haga lo siguiente:
# ● Formatee correctamente los textos ingresados en “apellido” y “nombre”, 
#   convirtiendo la primera letra de cada palabra a mayúsculas y el resto en minúsculas.
# ● Asegurarse que el correo electrónico no tenga espacios y contenga solo una “@”.
# ● Que clasifique a sus clientes por rango etario basándose en su edad 
#   (“Niño/a” para los y las menores de 15 años, “Adolescente” de 15 a 18 y “Adulto/a” para personas mayores de 18 años).
# El programa debe mostrar el apellido, nombre y dirección de correo con el formato pedido, y el texto correspondiente a su rango etario.

nombre = input("Ingrese el nombre del cliente: ")
apellido = input("Ingrese el apellido del cliente: ")
edad = int(input("Ingrese la edad del cliente: "))
correo = input("Ingrese el correo electrónico del cliente: ")

# Valida que el correo no tenga espacios y contenga exactamente una sola '@'
if " " not in correo and correo.count("@") == 1:
    # Formatea nombre y apellido con la primera letra en mayúscula y el resto en minúsculas
    nombre_formateado = nombre.strip().title()
    apellido_formateado = apellido.strip().title()
    
    # Clasificación por rango etario usando estructuras condicionales avanzadas (elif)
    if edad < 15:
        rango_etario = "Niño/a"
    elif 15 <= edad <= 18:
        rango_etario = "Adolescente"
    else:
        rango_etario = "Adulto/a"
        
    print("\n" + "=" * 42)
    print("         TARJETA DE PRESENTACIÓN         ")
    print("=" * 42)
    print(f"Nombre y Apellido : {nombre_formateado} {apellido_formateado}")
    print(f"Correo electrónico: {correo}")
    print(f"Rango etario      : {rango_etario}")
    print("=" * 42)
else:
    print("ERROR!")