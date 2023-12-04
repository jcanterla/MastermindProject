import cv2
import random
from datetime import date
import time

import pandas as pd
from stegano import lsb
import pickle

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

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
    with open("partidas.txt", "w") as f:
        pass
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
                        numero_partidas += 1
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
                        numero_partidas += 1
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
            numero_partidas2 = lista_final2[2]
        with open("partidas.txt", "a") as partidas:
            linea = ",".join(map(str, lista_final))
            partidas.write(linea + "\n")
        palabrarevelada, numerorevelado = generacionocultacion()
    return nombre, numero_partidas2, intentos_realizados, tiempo_total





def ranking(intentos_realizados, tiempo_total):
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
        for h in range(len(lista_final4)):
            lista1 = lista_final4[h]
            intentoss = lista1[4]
            if intentoss < intentos_realizados:
               lista_final4.insert(h, lista_final3)
               break
            elif intentoss == intentos_realizados:
                tiempoo = lista1[5]
                if tiempoo < tiempo_total:
                    lista_final4.insert(h,lista_final3)
                    break
                else:
                    lista_final4.append(lista_final3)
                    break
            else:
                lista_final4.append(lista_final3)
                break

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


def pdf(nombre2, numero_partidas3):
    filastabla = []
    estilos = getSampleStyleSheet()
    estilo_negrita = estilos['BodyText'].clone('estilo_negrita')
    estilo_negrita.fontName = 'Helvetica-Bold'
    estilo_negrita.fontSize = 20

    x_titulo, y_titulo, width_titulo, height_titulo = 90, 570, 450, 25

    doc = canvas.Canvas("partidas.pdf")
    doc.drawInlineImage("mastermind.png", 150, 600, width=300, height=200)
    doc.setFont(estilo_negrita.fontName, estilo_negrita.fontSize)
    doc.setFillColor(colors.lightgrey)
    doc.rect(x_titulo, y_titulo, width_titulo, height_titulo, fill=True, stroke=0)
    doc.setFillColor(colors.black)
    doc.drawString(170, 575, "INFORME DE LAS PARTIDAS")

    estilo_texto = estilos['BodyText'].clone('estilo_texto')
    estilo_texto.fontSize = 12
    doc.setFont(estilos['BodyText'].fontName, estilos['BodyText'].fontSize)
    doc.setFont(estilo_texto.fontName, estilo_texto.fontSize)
    doc.drawString(170, 540, f"El jugador {nombre2} ha jugado las siguientes {numero_partidas3} partidas: ")
    doc.setFont(estilos['BodyText'].fontName, estilos['BodyText'].fontSize)

    with open("partidas.txt", "r") as partidas:
        partidas2 = partidas.readlines()
    datos1 = [linea.strip().split(',') for linea in partidas2]
    filastabla.append(["fecha_hora", "número", "combinación", "intentos", "tiempo(secs)", "conseguido"])
    datos1.sort(key=lambda x: float(x[4]))
    mejor_partida = datos1[0]
    filastabla.extend(datos1)
    tabla = Table(filastabla)


    estilo_tabla = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.blue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.orange),
    ])
    tabla.setStyle(estilo_tabla)

    tabla.wrapOn(doc, 0, 0)
    tabla.drawOn(doc, 100, 480)

    doc.drawString(100, 400 ,"Su mejor partida ha sido:")
    doc.drawString(100, 380, f"{mejor_partida[0]}---{mejor_partida[1]}---{mejor_partida[2]}---{mejor_partida[4]}---{mejor_partida[5]}")
    with open("ranking.dat", "rb") as f:
        rankings = pickle.load(f)
        for cadarank in rankings:
            pass

    doc.save()
def salir():
    pass
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
        nombre,numero_partidas2, intentos_realizados, tiempo_total = masterpalabras(palabrarevelada, numerorevelado)
    elif opcion == "4":
        ranking(intentos_realizados, tiempo_total)
    elif opcion == "5":
        pdf(nombre, numero_partidas2)
    elif opcion == "6":
        salir()
    else:
        print("Opción inválida. Intente nuevamente.")


