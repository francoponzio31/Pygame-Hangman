import pygame, sys 
from random import choice
from time import sleep
from math import sqrt
import json

pygame.init()


# ________________________________ Carga de sonidos _________________________________________

right_letter_sound = pygame.mixer.Sound("data\media\Right_letter.wav")
wrong_letter_sound = pygame.mixer.Sound("data\media\wrong_letter.wav")

you_win_sound = pygame.mixer.Sound("data\media\you_win.wav")
you_lose_sound = pygame.mixer.Sound("data\media\you_lose.wav")

# __________________________________________________________________________________________

# ___________________ Creacion y configuracion de la ventana _______________________________

pantalla = pygame.display.set_mode((940,640))
pygame.display.set_caption("__AHORCADO__")

# Clock:
clock = pygame.time.Clock()

icono = pygame.image.load("data\media\hangman_icon.png")
pygame.display.set_icon(icono)

# __________________________________________________________________________________________

# ____________________________ Inicializo variables ________________________________________

# Fuentes a usar:
fuente_incognita = pygame.font.SysFont("Verdana", 55)
fuente_racha = pygame.font.SysFont("Verdana", 25)

# Color fondo:
color_fondo = (0,112,112)

# Inicializo la variable de racha en 0:
racha_victorias = 0

# Inicializo la variable perdio como True para que inicie el programa correctamente cargando 
# el contenido del archivo palabras.py a la lista:
perdio = True


# __________________________________________________________________________________________


# Bucle al que vuelve para reiniciar la pantalla cuando se pasa una palabra: 

while True:

    if perdio:    # Si perdio que reinicie la lista de palabras

        # Leo el json con la lista de palabras y lo meto en una nueva lista:
        with open("data\words.json", "r", encoding="utf-8") as file:
            json_data = file.read()

        lista_palabras = json.loads(json_data)

# __________________________________________________________________________________________



    # _______________________________ Seteos previos ____________________________________________

    # elijo una palabra al azar de
    # esa lista para que sea adivinada:
    palabra = choice(lista_palabras)

    # Elimino la palabra elegida de la lista para que no se vuelva a alegir hasta que se resetee
    # cuando el jugador pierda:
    lista_palabras.remove(palabra)

    # Se estandariza la palabra en mayusculas:
    palabra = palabra.upper()

    # creo un string "incognita", que va a tener la mismas cantidad de caracteres que la palabra a 
    # adivinar, y que va a reemplazar las letras de las palabras por guiones. A medida que se vayan
    # adivinando las letras que contiene la palabra se van a reemplazar esos guiones por la letra
    # correspondiente.
    
    incognita_palabra = ""
    while len(palabra) > len(incognita_palabra):  
        incognita_palabra += "_"

    # transformo el string en una lista para manipularlo con mayor facilidad:
    incognita_palabra = list(incognita_palabra)    

    # seteo el contador de errores en 0:
    contador_error = 0

    # Variables para saber si ganó o perdió:
    gano, perdio = False, False

    # ___________________________________________________________________________________________


    # ______________________________ Impresion en la ventana ___________________________________


    pantalla.fill(color_fondo)

    # --------------------------------- Impresion ahorcado -------------------------------------

    dibujo = pygame.image.load(f"data\media\hangman_{contador_error}.png").convert_alpha()
    pantalla.blit(dibujo, (360, 50))

    #-------------------------------- Tablero letras ------------------------------------------

    lista_letras = list() # cada elemento de esta lista va a estar compuesto por tres datos: (coordenada en X del  
                        # centro de la letra, coordenada en Y del centro de la letra, la letra en cuestion, y un
                        # valor booleano que va a indicar si la letra esta habilitada o deshabilitada) 
                        

    # Carga de imagenes de la fila 1:
    letras_fila_1 = list()

    for i in ("A","B","C","D","E","F","G","H","I","J","K","L","M","N"):
        letras_fila_1.append((i, pygame.image.load(f"data\media\letters\{i}.png").convert_alpha()))

    # impresion fila 1:
    start_x=55
    for i in letras_fila_1:
        letra, imagen = i
        pantalla.blit(imagen, (start_x, 490))
        lista_letras.append([start_x + 25, 490 + 25, letra, True])
        start_x+=60


    # Carga de imagenes de la fila 2:
    letras_fila_2 = list()

    for i in ("Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"):
        letras_fila_2.append((i, pygame.image.load(f"data\media\letters\{i}.png").convert_alpha()))

    #impresion fila 2:
    start_x=85
    for j in letras_fila_2:
        letra, imagen = j
        pantalla.blit(imagen, (start_x, 550))
        lista_letras.append([start_x + 25, 550 + 25, letra, True])
        start_x+=60


    # --------------------------- Impresion incognita ---------------------------

    impresion_incognita = fuente_incognita.render(" ".join(incognita_palabra), True, (0,0,0))
    pantalla.blit(impresion_incognita, ((940 - impresion_incognita.get_width())/2, 340))

    # ---------------------------- Impresion racha -----------------------------

    if racha_victorias > 0:
        parche_racha = pygame.draw.rect(pantalla, color_fondo, (25, 30, 80, 50))
        impresion_racha = fuente_racha.render(f"RACHA: {racha_victorias}", True, (0,0,0))
        pantalla.blit(impresion_racha, (30,35))


    pygame.display.flip()

    # __________________________________________________________________________________________




    # _____________________________ Bucle principal ____________________________________________

    while True:

        if gano == True or perdio == True:
            break

        if "".join(incognita_palabra) == palabra:
            #GANÓ
            gano = True
            you_win_sound.play()
            racha_victorias += 1

            # Muestro la palabra en color verde: 
            parche_incognita_palabra = pygame.draw.rect(pantalla, color_fondo, (20, 300, 900, 150))
            impresion_incognita = fuente_incognita.render(" ".join(incognita_palabra), True, (40, 181, 7))
            pantalla.blit(impresion_incognita, ((940 - impresion_incognita.get_width())/2, 340))
            pygame.display.update(parche_incognita_palabra)

  
            
            # Si se adivinan todas las palabras de la lista:
            if len(lista_palabras) ==  0: 
                sleep(0.3) 
                parche_incognita_palabra = pygame.draw.rect(pantalla, color_fondo, (20, 300, 900, 150))
                texto_todas_las_palabras_adivinadas = fuente_racha.render("FELICIDADES, ADIVINASTE TODAS LAS PALABRAS DISPONIBLES !!!", True, (35, 179, 16))
                pantalla.blit(texto_todas_las_palabras_adivinadas, ((940 - texto_todas_las_palabras_adivinadas.get_width())/2, 360))
                pygame.display.update(parche_incognita_palabra)
                sleep(5)
                sys.exit() 


        for evento in pygame.event.get():
        
            # Configuracion del cierre de la ventana:
            if evento.type == pygame.QUIT:
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                # mecanismo y logica de los botones:
                mouse_x_cord, mouse_y_cord = pygame.mouse.get_pos()
                for indice, informacion_letra in enumerate(lista_letras):
                    letra_x_cord, letra_y_cord, letra, habilitado = informacion_letra
                    distancia = sqrt((letra_x_cord-mouse_x_cord)**2 + (letra_y_cord-mouse_y_cord)**2)
                    if distancia <= 25 and habilitado == True:
                        letra_ingresada = letra
                        lista_letras[indice] = [letra_x_cord, letra_y_cord, letra, False]
                                            
                        # Actualizacion tablero letras:
                        parche_letras = pygame.draw.circle(pantalla, color_fondo, (letra_x_cord, letra_y_cord), 30)
                        pygame.display.update(parche_letras)



                        if letra_ingresada in palabra:

                            right_letter_sound.play()

                            for i, letra_en_palabra in enumerate(palabra):
                                if letra_ingresada == letra_en_palabra:    
                                    incognita_palabra[i]=letra_ingresada

                                    # Actualizacion imagen incongita:
                                    parche_incognita_palabra = pygame.draw.rect(pantalla, color_fondo, (20, 300, 900, 150))
                                    impresion_incognita = fuente_incognita.render(" ".join(incognita_palabra), True, (0,0,0))
                                    pantalla.blit(impresion_incognita, ((940 - impresion_incognita.get_width())/2, 340))
                                    pygame.display.update(parche_incognita_palabra)

                        else:
                            if contador_error < 6:
                                contador_error += 1 

                                if contador_error < 6:
                                    wrong_letter_sound.play()

                                # Actualizacion imagen ahorcado:
                                parche_ahorcado = pygame.draw.rect(pantalla, color_fondo, (350, 40, 250, 250))
                                dibujo = pygame.image.load(f"data\media\hangman_{contador_error}.png").convert_alpha()
                                pantalla.blit(dibujo, (360, 50))
                                pygame.display.update(parche_ahorcado)

                                                        
                            if contador_error == 6:
                                # PERDIÓ 
                                you_lose_sound.play()
                                racha_victorias = 0
                                perdio = True      

                                # Muestro en pantalla cual era la palabra:  
                                sleep(0.3) 
                                parche_incognita_palabra = pygame.draw.rect(pantalla, color_fondo, (20, 300, 900, 150))
                                impresion_palabra = fuente_incognita.render(palabra, True, (191, 8, 8))
                                pantalla.blit(impresion_palabra, ((940 - impresion_palabra.get_width())/2, 340))
                                pygame.display.update(parche_incognita_palabra)
  
        # -------------------------- CONTROL DE FRAMES ----------------------------
        clock.tick(30)
           
    sleep(1.3)