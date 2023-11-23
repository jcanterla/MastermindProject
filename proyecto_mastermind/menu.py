import cv2
import random
import sys

img = cv2.imread("mastermind_logorigin.png")

# Funciones de cada opción
def cambio_imagen():
    font = cv2.FONT_HERSHEY_DUPLEX
    font2 = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    posicion = (105, 55)
    posicion2 = (355, 55)
    posicion3 = (65, 310)
    posicion4 = (190, 310)
    escalado = 2
    escalado2 = 1
    color = (29, 152, 248)
    color2 = (36, 45, 238)

    cv2.putText(img, "Equipo", posicion, font, escalado, color, 2)
    cv2.putText(img, "5", posicion2, font, escalado, color, 2)
    cv2.putText(img, "1DAM", posicion3, font2, escalado2, color2, 2)
    cv2.putText(img, "Curso 2023/24", posicion4, font2, escalado2, color2, 2)
    cv2.imwrite("mastermind.png", img)
    cv2.imshow("imagen", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cambio_imagen

cambio_imagen()
def generacion():
    numaleatorio = {
        1: random.randint(0, 9),
        2: random.randint(0, 9),
        3: random.randint(0, 9),
        4: random.randint(0, 9),
        5: random.randint(0, 9)
    }
    list = []
    for a in range(1, 6):
        numero = numaleatorio.get(a)
        list.append(numero)
        numerogenerado = "".join(map(str, list))
    with open("palabras.dat", "rb") as f:
        palabra = f.readlines()
    elemento = random.randint(1, 24)
    palabra2 = palabra[elemento].decode("utf-8").strip()
    print(palabra2)
    print(numerogenerado)

print(generacion())
def juego():
    print("3")
def ranking():
    print("4")
def informe():
    print("5")

# Función para la opción de salir.
# Debe aparecer fichero donde se almacena el ranking y el de las 8 letras
def salir():
    print("")
    sys.exit()

# Visualización del menú en la pantalla
while True:
    print("APLICACIÓN MASTENMIND")
    print("1) Creación del logo de equipo")
    print("2) Generación y ocultado de la combinación")
    print("3) Juego Mastermind")
    print("4) Ranking de récords")
    print("5) Informe de las partidas (PDF)")
    print("6) Salir")

    opcion = input("Opción: ")

    if opcion == "1":
        cambio_imagen()
    elif opcion == "2":
        generacion()
    elif opcion == "3":
        juego()
    elif opcion == "4":
        ranking()
    elif opcion == "5":
        informe()
    elif opcion == "6":
        salir()
    else:
        print("Opción inválida. Intente nuevamente.")

