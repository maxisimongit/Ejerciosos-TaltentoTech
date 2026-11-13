"""
Ejercicio a hacer:
¡Hola!
En nuestro día a día, interactuamos con muchos clientes, y uno de
los pasos iniciales es recopilar y organizar su información básica.
Para eso, necesito que desarrolles un pequeño programa en
Python que haga lo siguiente:

- Solicite al cliente su nombre, apellido, edad y correo electrónico.
- Almacene estos datos en variables.
- Los muestre organizados en forma de una tarjeta de presentación en la pantalla.
"""

nombre = input("Ingrese el nombre del cliente: ")
apellido = input("Ingrese el apellido del cliente: ")
edad = int(input("Ingrese la edad del cliente: "))
correo = input("Ingrese el correo electrónico del cliente: ")

print("\n" + "=" * 42)
print("         TARJETA DE PRESENTACIÓN         ")
print("=" * 42)
print(f"Nombre y Apellido : {nombre} {apellido}")
print(f"Edad              : {edad} años")
print(f"Correo electrónico: {correo}")
print("=" * 42)