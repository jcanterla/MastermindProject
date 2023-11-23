import cv2
import random


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


def generacion():
    global palabra2
    global numerogenerado
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
    print(palabra2)
    print(numerogenerado)

def masternumeros():
    def generar_combinacion(longitud):
    numeros_posibles = ''.join(str(random.randint(0, 9)) for i in range(4))
    combinacion = []
    while len(combinacion) < longitud:
        numero = random.choice(numeros_posibles)
        if numero not in combinacion:
            combinacion.append(numero)
    return combinacion

def jugar():
    longitud_combinacion = 4
    combinacion = generar_combinacion(longitud_combinacion)
    max_intentos = 10

    print("Bienvenido al juego de combinación secreta. Adivina la combinación de {} números.".format(
        longitud_combinacion))
    print("Recibirás indicadores 'o', '-', 'x' después de cada dígito introducido.")
    print("o = número correcto en el lugar correcto")
    print("- = número correcto en el lugar incorrecto")
    print("x = número incorrecto")
    print("")

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
            break

        intentos += 1

    if intentos == max_intentos:
        print("Lo siento, has alcanzado el número máximo de intentos. La combinación secreta era: {}".format(
            ''.join(combinacion)))
    return jugar()

jugar()


def masterpalabras():
    print("\t\t¡Tienes 7 intentos!\n\t\t\t¡Comenzamos!")

    palabra = palabra2
    print(palabra)
    separar = []
    for letra in palabra:
        separar.append(letra)
    intentos = 7
    intentos_realizados = 0

    while intentos_realizados < intentos:
        palabra3 = len(palabra2)
        guiones = []

        for contar in range(palabra3):
            guiones.append("-")
        print(guiones)
        
        caracter = input("Introduce la palabra que crees que es: ")
        almacen = []
        for letra2 in caracter:
            almacen.append(letra2)
        caractAlma = len(almacen)
        for i in range(caractAlma):
            if almacen[i] == separar[i]:
                almacen[i] = "o"
            else:
                almacen[i] = "-"
        print(almacen)
        intentos_realizados += 1

        if palabra == caracter:
            print("Felicidades")
            break


generacion()
masterpalabras()
