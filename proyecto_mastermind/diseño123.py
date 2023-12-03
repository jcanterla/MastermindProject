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

    print("\t"*12, palabrarevelada)
    print("\t"*12, numerorevelado, "\n")
    return palabrarevelada, numerorevelado

########################################################################################################################


def masterpalabras(palabrarevelada, numerorevelado):
    global lista_final3
    lista_final3 = []
    fecha = date.today()
    print("\033[1m" + "\n\n" + "\t"*11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    print("\t"*10 +"Se ha recuperado la combinación\n")
    nombre = input("\t"*10 +" Tu nickname, por favor: ")
    print()
    print("\t"*10 + f"¡Comienza el juego para {nombre}!\n\n")
    jugar = ""
    while jugar != "P" and jugar != "p" and jugar != "N" and jugar != "n":
        jugar = input("\t"*8 +"¿Quieres jugar a palabras o a números? (P/N): ")
    print("\033[1m" + "\n\n\n" + "\t" * 11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    volver = "S"
    numero_partidas = 0
    conseguido = False
    while volver == "S" or volver == "s":
        numero_partidas += 1
        intentos_realizados = 0
        tiempo = time.time()
        if jugar == "N" or jugar == "n":
            intentos = 4
            print("\t" * 11 + "¡Tienes 7 intentos!" + "\n" + "\t" * 12 + "¡Comenzamos!")
            while intentos > intentos_realizados:
                intentos_realizados += 1
                numero_ingresado = input("\n"+"\t"*8+"Ingresa un número de 5 cifras: ")
                resultado = "\t"*12+""
                if len(numero_ingresado) != len(numerorevelado):
                    print("\t"*11+"Número no válido")
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
            print("\t" * 11 + "¡Tienes 4 intentos!" + "\n" + "\t" * 12 + "¡Comenzamos!")
            while intentos > intentos_realizados:
                intentos_realizados += 1
                palabra_ingresada = input("\n"+"\t"*8+"Ingresa una palabra de 8 caracteres: ")
                resultado = "\t"*12+""
                if len(palabra_ingresada) != len(palabrarevelada):
                    print("\t"*11+"Palabra no válida")
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
                        print("\n"+"\t"*10+"¡Has adivinado la combinación!")
                        print("\t"*12+"¡En {} intentos!\n".format(intentos_realizados))
                        conseguido = True
                        break
                    elif intentos_realizados == 7:
                        print("\t"*9+"¡Has agotado los intentos!\n")
                        conseguido = False
                        break

        fin = time.time()
        tiempo_total = fin - tiempo
        volver = input("\t"*9+"¿Quieres volver a jugar, sí o no?(S/N): ")
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
    print("\033[1m" + "\n\n\n" + "\t"*11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    print("\t"*9 +"1) Creación del logo de equipo")
    print("\t"*9 +"2) Generación y ocultado de la combinación")
    print("\t"*9 +"3) Juego Mastermind")
    print("\t"*9 +"4) Ranking de récords")
    print("\t"*9 +"5) Informe de las partidas (PDF)")
    print("\t"*9 +"6) Salir\n")

    opcion = input("\t"*9 +"Opción: ")

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


