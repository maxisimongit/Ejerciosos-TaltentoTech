# Ejercicio práctico:
# Desarrollar un programa que solicite al cliente su nombre, apellido, edad y correo electrónico.
# Comprobar que el nombre, el apellido y el correo no estén en blanco, y que la edad sea mayor o igual a 18 años.
# Mostrar los datos por la terminal en el orden que se ingresaron si se cumple; de lo contrario, mostrar sólo "ERROR!".

nombre = input("Ingrese el nombre del cliente: ")
apellido = input("Ingrese el apellido del cliente: ")
edad = int(input("Ingrese la edad del cliente: "))
correo = input("Ingrese el correo electrónico del cliente: ")

# Valido que ningún campo de texto esté vacío (usando .strip() para evitar espacios en blanco) 
# y que la edad sea mayor o igual a 18 años.
if nombre.strip() != "" and apellido.strip() != "" and correo.strip() != "" and edad >= 18:
    print(nombre)
    print(apellido)
    print(edad)
    print(correo)
else:
    print("ERROR!")