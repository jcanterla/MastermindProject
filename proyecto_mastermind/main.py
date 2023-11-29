import cv2
import random
from datetime import datetime
import time
from stegano import lsb
img = cv2.imread("mastermind_logorigin.png")


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


def generacionocultacion():
    numaleatorio = {
        1:random.randint(0,9),
        2:random.randint(0,9),
        3:random.randint(0,9),
        4:random.randint(0,9),
        5:random.randint(0,9)
    }
    list = []
    for a in range(1,6):
        numero = numaleatorio.get(a)
        list.append(numero)
        numerogenerado = "".join(map(str, list))
    with open("palabras.dat", "rb") as f:
        palabra = f.readlines()
    elemento = random.randint(1,24)

    palabra2 = palabra[elemento].decode("utf-8").strip()

    secreto = lsb.hide("mastermind.png", palabra2)
    secreto2 = lsb.hide("mastermind.png", numerogenerado)
    secreto.save("mastermindsecreto.png")
    secreto2.save("mastermindsecreto2.png")
    palabrarevelada = lsb.reveal("mastermindsecreto.png")
    numerorevelado = lsb.reveal("mastermindsecreto2.png")

    print(palabrarevelada)
    print(numerorevelado)
    return palabrarevelada, numerorevelado
def masterpalabras():
    partidas = 0
    rellenado = False
    while not rellenado:
        print("\033[1m" + "APLICACIÓN MASTERMIND" + "\033[0m")
        nombre = input("Tu nickname, por favor: ")
        respuestajuego = input("¿Quieres jugar con números o palabras? (indica con N/P) ")
        print("¡Comienza el juego para {}!".format(nombre))
        rellenado = True
    if respuestajuego == 'n' or respuestajuego == 'N':
        palabrarevelada, numerorevelado = generacionocultacion()
        inicio = time.time()
        longitud_combinacion = 5
        combinacion = numerorevelado
        max_intentos = 10
        intentos = 0
        while intentos < max_intentos:
            intento = input("Introduce tu intento ({} dígitos): ".format(longitud_combinacion))

            if len(intento) != longitud_combinacion or not intento.isdigit():
                print("Por favor, introduce {} números.".format(longitud_combinacion))
                continue

            verificacion = ""
            for i in range(longitud_combinacion):
                if intento[i] == combinacion[i]:
                    verificacion += "o"
                elif intento[i] in combinacion:
                    verificacion += "-"
                else:
                    verificacion += "x"

            print("Resultado del intento {}: {}".format(intentos + 1, verificacion))

            if verificacion == 'o' * longitud_combinacion:
                print("¡Felicidades! Has adivinado la combinación secreta: {}".format(''.join(combinacion)))
                volver = input("¿Quieres volver a jugar? ")
                if volver == "S" or volver == "s":
                    masterpalabras()
                elif volver == "N" or volver == "n":
                    print("Volver al juego")

            intentos += 1

        if intentos == max_intentos:
            print("Lo siento, has alcanzado el número máximo de intentos. La combinación secreta era: {}".format(
                ''.join(combinacion)))
            volver = input("¿Quieres volver a jugar? ")
            if volver == "S" or volver == "s":
                masterpalabras()
            elif volver == "N" or volver == "n":
                print("Fin del juego")

        print("Bienvenido al juego de combinación secreta. Adivina la combinación de {} números.".format(
            longitud_combinacion))
        print("Recibirás indicadores 'o', '-', 'x' después de cada dígito introducido.")
        print("o = número correcto en el lugar correcto")
        print("- = número correcto en el lugar incorrecto")
        print("x = número incorrecto")
        print("")

    elif respuestajuego == 'P' or respuestajuego == 'p':
        palabrarevelada, numerorevelado = generacionocultacion()
        inicio = time.time()
        print("\033[1m" + "APLICACIÓN MASTERMIND" + "\033[0m")
        print()
        print("\t\t¡Tienes 7 intentos!\n\t\t\t¡Comenzamos!")
        partidas += 1
        palabra = palabrarevelada
        print(palabra)
        separar = []
        for letra in palabra:
            separar.append(letra)

        intentos = 7
        intentos_realizados = 0

        while intentos_realizados < intentos:

            caracter = input("Introduce la palabra que crees que es: ")
            almacen = []
            for letra2 in caracter:
                almacen.append(letra2)
            for i in range(len(almacen)):
                if almacen[i] == separar[i]:
                    almacen[i] = "o"
                elif almacen[i] in separar:
                    almacen[i] = "-"
                else:
                    almacen[i] = "x"
            almacen = " ".join(almacen)
            print(almacen)
            intentos_realizados += 1
            fecha = datetime.now()
            if palabra == caracter:
                print("Has adivinado la combinación")
                print("¡En {} intentos!".format(intentos_realizados))
                volver = input("¿Volvemos a jugar (S/N)? ")
                conseguido = True
                if volver == "S" or volver == "s":
                    masterpalabras()
                elif volver == "N" or volver == "n":
                    fin = time.time()
                    tiempo = fin - inicio
                    datos_partida = {'fecha':fecha, 'numero':partidas, 'combinacion':palabra,'intentos':intentos_realizados, 'tiempo':tiempo, 'conseguido':conseguido}
                    with open('partidas.txt', 'a') as f:
                        f.writelines(f"{datos_partida}\n")
                    break
        conseguido = False
        datos_partida = {'fecha': fecha, 'numero': partidas, 'combinacion': palabra, 'intentos': intentos_realizados,'tiempo': tiempo, 'conseguido': conseguido}
        with open('partidas.txt', 'a') as f:
            f.writelines(f"{datos_partida}\n")
        print("Máximos de intentos realizados")
palabrarevelada, numerorevelado = generacionocultacion()
masterpalabras()

def ranking():
    pass
