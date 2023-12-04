# Importamos cv2 para lectura de la imagen
import cv2
# Importamos random para que nos seleccione un numero aleatorio o una palabra aleatoria
import random
# Importamos para poder trabajar con datos de tipo fecha
from datetime import date
import time

# Importamos para poder realizar tablas en el ranking
import pandas as pd
# Importamos para realizar la ocultacion
from stegano import lsb
# Importamos para la lectura del fichero binario
import pickle

# Importamos para la realizacion del pdf
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Función de modificar la imagen de equipo


def cambio_imagen():
    img = cv2.imread("mastermind_logorigin.png")
    font = cv2.FONT_HERSHEY_DUPLEX
    font2 = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    # Colocar la imagen con sus respectivos tamaños
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
    # Generación de un numero aleatorio de 5 cifras
    numaleatorio = {
        1:random.randint(0,9),
        2:random.randint(0,9),
        3:random.randint(0,9),
        4:random.randint(0,9),
        5:random.randint(0,9)
    }
    list = []
    # Obtención de una palabra aleatoria del fichero palabras.dat
    for a in range(1,6):
        numero = numaleatorio.get(a)
        list.append(numero)
        numerogenerado = "".join(map(str, list))
    with open("palabras.dat", "rb") as f:
        palabra = f.readlines()
    elemento = random.randint(1,24)

    palabra2 = palabra[elemento].decode("utf-8").strip()
    # Ocultación de las palabras en la imagen
    secreto = lsb.hide("mastermind.png", palabra2)
    secreto2 = lsb.hide("mastermind.png", numerogenerado)
    secreto.save("mastermindsecreto.png")
    secreto2.save("mastermindsecreto2.png")
    palabrarevelada = lsb.reveal("mastermindsecreto.png")
    numerorevelado = lsb.reveal("mastermindsecreto2.png")

    return palabrarevelada, numerorevelado

########################################################################################################################


def masterpalabras(palabrarevelada, numerorevelado):
    global lista_final3
    lista_final3 = []
    fecha = date.today()
    # Menu del juego masterpalabras
    print("\033[1m" + "\n\n" + "\t"*11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    print("\t"*10 +"Se ha recuperado la combinación\n")
    nombre = input("\t"*10 +" Tu nickname, por favor: ")
    print()
    print("\t"*10 + f"¡Comienza el juego para {nombre}!\n\n")
    jugar = ""
    # Elegir que tipo de modo jugar
    while jugar != "P" and jugar != "p" and jugar != "N" and jugar != "n":
        jugar = input("\t"*8 +"¿Quieres jugar a palabras o a números? (P/N): ")
    print("\033[1m" + "\n\n\n" + "\t" * 11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    volver = "S"
    numero_partidas = 0
    conseguido = False
    # Bucle en caso de querer volver a jugar al modo seleccionado
    while volver == "S" or volver == "s":
        numero_partidas += 1
        intentos_realizados = 0
        tiempo = time.time()
        # Modo de juego numerico
        if jugar == "N" or jugar == "n":
            intentos = 4
            print("\t" * 11 + "¡Tienes 7 intentos!" + "\n" + "\t" * 12 + "¡Comenzamos!")
            # Intentos a poder realizar
            while intentos > intentos_realizados:
                intentos_realizados += 1
                numero_ingresado = input("\n"+"\t"*8+"Ingresa un número de 5 cifras: ")
                resultado = "\t"*12+""
                # Introduccion erronea de longitud de numero permitido
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
                    # Adivinación del numero
                    if numero_ingresado == numerorevelado:
                        print("¡Has adivinado la combinación!")
                        print("¡En {} intentos!".format(intentos_realizados))
                        conseguido = True
                        break
                    # Error a la hora de descubrir el numero
                    elif intentos_realizados == 4:
                        print("¡Has agotado los intentos!")
                        conseguido = False
                        break

        # Jugar en modo palabras
        elif jugar == "P" or jugar == "p":
            intentos = 7
            print("\t" * 11 + "¡Tienes 4 intentos!" + "\n" + "\t" * 12 + "¡Comenzamos!")
            # Intentos a poder realizar
            while intentos > intentos_realizados:
                intentos_realizados += 1
                palabra_ingresada = input("\n"+"\t"*8+"Ingresa una palabra de 8 caracteres: ")
                resultado = "\t"*12+""
                # Longitud de palabra erronea
                if len(palabra_ingresada) != len(palabrarevelada):
                    print("\t"*11+"Palabra no válida")
                    intentos_realizados -= 1
                else:
                    # Descubrir palabras acertadas, equivocadas o en posicion diferente
                    for e in range(8):
                        if palabra_ingresada[e] == palabrarevelada[e]:
                            resultado += 'o'
                        elif palabra_ingresada[e] in palabrarevelada:
                            resultado += '-'
                        else:
                            resultado += 'x'
                    print(resultado)
                    # Combinacion correcta
                    if palabra_ingresada == palabrarevelada:
                        print("\n"+"\t"*10+"¡Has adivinado la combinación!")
                        print("\t"*12+"¡En {} intentos!\n".format(intentos_realizados))
                        conseguido = True
                        break
                    # Combinacion erronea
                    elif intentos_realizados == 7:
                        print("\t"*9+"¡Has agotado los intentos!\n")
                        conseguido = False
                        break
        fin = time.time()
        tiempo_total = fin - tiempo
        # Volver a jugar
        volver = input("\t"*9+"¿Quieres volver a jugar, sí o no?(S/N): ")
        # Volver a jugar
        if jugar == "N" or jugar == "n":
            combinacion = numerorevelado
        else:
            combinacion = palabrarevelada
        # Almacenar en lista los datos del jugador
        lista_final = [fecha, numero_partidas, combinacion, intentos_realizados, round(tiempo_total, 2), conseguido]
        # Si acierta la combinación almacenar los datos en la lista_final2
        if conseguido == True:
            lista_final2 = [nombre, fecha, numero_partidas, combinacion, intentos_realizados, round(tiempo_total, 2), conseguido]
            lista_final3.append(lista_final2)
            numero_partidas2 = lista_final2[2]
        # Modificacion de partidas.txt añadiendo las nuevas listas
        with open("partidas.txt", "a") as partidas:
            linea = ",".join(map(str, lista_final))
            partidas.write(linea + "\n")
        # Volver a generar palabra y numero para poder jugar de nuevo
        palabrarevelada, numerorevelado = generacionocultacion()
    return nombre, numero_partidas2, tiempo_total





def ranking():
    # Creación del ranking
    lista_final4 = []
    # Añadir las listas nuevas jugadas al ranking
    lista_final4.append(lista_final3)
    nombres = []
    fechas = []
    numero_part = []
    combinaciones = []
    intento = []
    tiempos = []
    conseguidos = []

    # En caso de ya existir el archivo trabajar con este
    try:
        with open("ranking.dat", "rb") as datos2:
            lista_final4 = pickle.load(datos2)
        lista_final4.append(lista_final3)

        with open("ranking.dat", "wb") as datos:
            pickle.dump(lista_final4, datos)
    except:
        # Si no existe el archivo que trabajar crearlo
        with open("ranking.dat", "wb") as datos:
            pickle.dump(lista_final4, datos)
    # Hacer una lista con cada elemento de las listas del ranking.dat
    for u in lista_final4:
        for e in u:
            nombres.append(e[0])
            fechas.append(e[1])
            numero_part.append(e[2])
            combinaciones.append(e[3])
            intento.append(e[4])
            tiempos.append(e[5])
            conseguidos.append(e[6])
    # Crar mediante pandas la tabla
    datos = {'Nombre': nombres, 'fecha': fechas, 'numero': numero_part, 'combinacion': combinaciones,
             'intento': intento, 'tiempo': tiempos, 'conseguido': conseguidos}
    # Lectura de la tabla con pandas
    df = pd.DataFrame(datos)
    df_ordenado = df.sort_values(by=['intento', 'tiempo'])
    # Mostrar los 10 primeros elementos de la tabla
    print(df_ordenado.head(10).to_string(index=False).center(80))

    return df_ordenado


def pdf(nombre2, numero_partidas3, df_ordenado, tiempo_total):
    filastabla = []
    # Definimos los estilos del  título
    estilos = getSampleStyleSheet()
    estilo_negrita = estilos['BodyText'].clone('estilo_negrita')
    estilo_negrita.fontName = 'Helvetica-Bold'
    estilo_negrita.fontSize = 20
    # Definimos las posiciones del titulo y del cuadro gris
    x_titulo, y_titulo, width_titulo, height_titulo = 90, 570, 450, 25
    # Creamos el PDF y los diferentes titulos e imágenes
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
    # Cargamos los datos de las partidas para la tabla
    with open("partidas.txt", "r") as partidas:
        partidas2 = partidas.readlines()
    datos1 = [linea.strip().split(',') for linea in partidas2]
    filastabla.append(["fecha_hora", "número", "combinación", "intentos", "tiempo(secs)", "conseguido"])
    datos1.sort(key=lambda x: float(x[4]))
    mejor_partida = datos1[0]
    filastabla.extend(datos1)
    tabla = Table(filastabla)

    # Hacemos los estilos de la tabla
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

    # Dibujamos la tabla
    tabla.wrapOn(doc, 0, 0)
    tabla.drawOn(doc, 100, 470)

    #Definimos la mejor partida y la posición del ranking
    doc.drawString(100, 400 ,"Su mejor partida ha sido:")
    doc.drawString(100, 380, f"{mejor_partida[0]}---{mejor_partida[1]}---{mejor_partida[2]}---{mejor_partida[4]}---{mejor_partida[5]}")
    lista_ordenada = df_ordenado.to_records(index=False).tolist()
    b = True
    for t in range(len(lista_ordenada)):
        a = lista_ordenada[t]
        if round(tiempo_total, 2) == a[5]:
            b = False
            doc.drawString(100, 360, f"Actualmente {nombre2} ocupa la posición {t+1} de nuestro ranking")
    if b == True:
        doc.drawString(100,360,"No está en el ranking")

    doc.save()

opcion1 = 0
while opcion1 != 6:
    print("\033[1m" + "\n\n\n" + "\t" * 11 + "APLICACIÓN MASTERMIND\n" + "\033[0m")
    print("\t" * 9 + "1) Creación del logo de equipo")
    print("\t" * 9 + "2) Generación y ocultado de la combinación")
    print("\t" * 9 + "3) Juego Mastermind")
    print("\t" * 9 + "4) Ranking de récords")
    print("\t" * 9 + "5) Informe de las partidas (PDF)")
    print("\t" * 9 + "6) Salir\n")

    opcion = input("\t" * 9 + "Opción: ")

    if opcion == "1":
        cambio_imagen()
    elif opcion == "2":
        generacionocultacion()
    elif opcion == "3":
        palabrarevelada, numerorevelado = generacionocultacion()
        nombre,numero_partidas2, tiempo_total = masterpalabras(palabrarevelada, numerorevelado)
    elif opcion == "4":
        df_ordenado = ranking()
    elif opcion == "5":
        pdf(nombre, numero_partidas2, df_ordenado, tiempo_total)
    elif opcion == "6":
        opcion1 = 6
    else:
        print("Opción inválida. Intente nuevamente.")


