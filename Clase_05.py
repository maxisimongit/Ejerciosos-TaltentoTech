# Necesitamos un software que ayude a registrar y calcular
# información financiera básica para nuestros y nuestras clientes.
# Tu tarea para esta semana es la siguiente:
# 1. Registrar los ingresos mensuales de un cliente durante 6 meses usando un bucle
#    while para solicitar el ingreso de cada mes. Validar que los ingresos sean números
#    positivos. Si se ingresa un valor negativo, mostrá un mensaje indicando que el
#    valor no es válido y volvé a pedir el dato.
# 2. Calcular el total acumulado durante los 6 meses y el promedio mensual. Mostrá
#    este resultado al final del programa.

meses_totales = 6
mes_actual = 1
ingresos = []
total_acumulado = 0

while mes_actual <= meses_totales:
    ingreso = float(input(f"Ingrese el ingreso del mes {mes_actual}: "))
    
    if ingreso < 0:
        print("El valor no es válido. Por favor, ingrese un número positivo.")
    else:
        ingresos.append(ingreso)
        total_acumulado += ingreso
        mes_actual += 1

promedio_mensual = total_acumulado / meses_totales

print("\n" + "=" * 42)
print("         RESUMEN FINANCIERO         ")
print("=" * 42)
print(f"Ingresos mensuales : {ingresos}")
print(f"Total acumulado    : ${total_acumulado:.2f}")
print(f"Promedio mensual   : ${promedio_mensual:.2f}")
print("=" * 42)