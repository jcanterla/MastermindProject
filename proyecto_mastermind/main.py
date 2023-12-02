import cv2
import random
from datetime import date
import time

import pandas as pd
from stegano import lsb
import pickle

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


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




########################################################################################################################


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

########################################################################################################################


def masterpalabras(palabrarevelada, numerorevelado):
    global lista_final3
    lista_final3 = []
    fecha = date.today()
    print("\033[1m" + "APLICACIÓN MASTERMIND" + "\033[0m")
    nombre = input("Tu nickname, por favor: ")
    jugar = ""
    while jugar != "P" and jugar != "p" and jugar != "N" and jugar != "n":
        jugar = input("¿Qué quieres jugar a palabras o a números? (P/N): ")
    print("¡Comienza el juego para {}!".format(nombre))
    volver = "S"
    numero_partidas = 0
    conseguido = False
    while volver == "S" or volver == "s":
        numero_partidas += 1
        intentos_realizados = 0
        tiempo = time.time()
        if jugar == "N" or jugar == "n":
            intentos = 4
            while intentos > intentos_realizados:
                intentos_realizados += 1
                numero_ingresado = input("Ingresa un número de 5 cifras: ")
                resultado = ""
                if len(numero_ingresado) != len(numerorevelado):
                    print("Número no válido")
                    intentos_realizados -= 1
                else:
                    for e in range(5):
                        if numero_ingresado[e] == numerorevelado[e]:
                            resultado += 'o'
                        elif numero_ingresado[e] in numerorevelado:
                            resultado += '-'
                        else:
                            resultado += 'x'
                    print(resultado)
                    if numero_ingresado == numerorevelado:
                        print("¡Has adivinado la combinación!")
                        print("¡En {} intentos!".format(intentos_realizados))
                        conseguido = True
                        break
                    elif intentos_realizados == 4:
                        print("¡Has agotado los intentos!")
                        conseguido = False
                        break


        elif jugar == "P" or jugar == "p":
            intentos = 7
            while intentos > intentos_realizados:
                intentos_realizados += 1
                palabra_ingresada = input("Ingresa una palabra de 8 caracteres: ")
                resultado = ""
                if len(palabra_ingresada) != len(palabrarevelada):
                    print("Palabra no válida")
                    intentos_realizados -= 1
                else:
                    for e in range(8):
                        if palabra_ingresada[e] == palabrarevelada[e]:
                            resultado += 'o'
                        elif palabra_ingresada[e] in palabrarevelada:
                            resultado += '-'
                        else:
                            resultado += 'x'
                    print(resultado)
                    if palabra_ingresada == palabrarevelada:
                        print("¡Has adivinado la combinación!")
                        print("¡En {} intentos!".format(intentos_realizados))
                        conseguido = True
                        break
                    elif intentos_realizados == 7:
                        print("¡Has agotado los intentos!")
                        conseguido = False
                        break

        fin = time.time()
        tiempo_total = fin - tiempo
        volver = input("¿Quieres volver a jugar, si o no?(S/N): ")
        if jugar == "N" or jugar == "n":
            combinacion = numerorevelado
        else:
            combinacion = palabrarevelada
        lista_final = [fecha, numero_partidas, combinacion, intentos_realizados, tiempo_total, conseguido]
        if conseguido == True:
            lista_final2 = [nombre, fecha, numero_partidas, combinacion, intentos_realizados, tiempo_total, conseguido]
            lista_final3.append(lista_final2)
        with open("partidas.txt", "a") as partidas:
            partidas.writelines(f"{lista_final}\n")
        palabrarevelada, numerorevelado = generacionocultacion()





def ranking():
    lista_final4 = []
    lista_final4.append(lista_final3)
    nombres = []
    fechas = []
    numero_part = []
    combinaciones = []
    intento = []
    tiempos = []
    conseguidos = []

    try:
        with open("ranking.dat", "rb") as datos2:
            lista_final4 = pickle.load(datos2)
        lista_final4.append(lista_final3)
        with open("ranking.dat", "wb") as datos:
            pickle.dump(lista_final4, datos)
    except:
        with open("ranking.dat", "wb") as datos:
            pickle.dump(lista_final4, datos)

    for u in lista_final4:
        for e in u:
            nombres.append(e[0])
            fechas.append(e[1])
            numero_part.append(e[2])
            combinaciones.append(e[3])
            intento.append(e[4])
            tiempos.append(e[5])
            conseguidos.append(e[6])

    datos = {'Nombre': nombres, 'fecha': fechas, 'numero': numero_part, 'combinacion': combinaciones,
             'intento': intento, 'tiempo': tiempos, 'conseguido': conseguidos}

    df = pd.DataFrame(datos)
    df_ordenado = df.sort_values(by=['intento', 'tiempo'])
    print(df_ordenado.head(10).to_string(index=False))


def pdf():
    doc = canvas.Canvas("partidas.pdf")
    doc.drawInlineImage("mastermind.png", 150, 600, width=300, height=200)
    color_subrayado = colors.gray
    doc.setFillColor(colors.black)
    doc.setFont("Helvetica", 14)
    doc.drawCentredString(165, 550, "INFORME DE LA PARTIDAS")
    doc.rect(165, 550, doc.stringWidth("INFORME DE LAS PARTIDAS", "Helvetica-Bold", 20), 20, fill=True)
    doc.setFillColor(color_subrayado)
    doc.save()

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
        generacionocultacion()
    elif opcion == "3":
        palabrarevelada, numerorevelado = generacionocultacion()
        masterpalabras(palabrarevelada, numerorevelado)
    elif opcion == "4":
        ranking()
    elif opcion == "5":
        pdf()
    elif opcion == "6":
        salir()
    else:
        print("Opción inválida. Intente nuevamente.")


