import random
from constantes import *
import pygame
import json
import os

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """
    Dibuja un texto multilínea sobre una superficie de Pygame, respetando
    automáticamente los saltos de línea y el ancho máximo disponible.

    Parámetros
    surface : pygame.Surface
        Superficie destino donde se quiere dibujar el texto.
    text : str
        Texto completo a renderizar. Puede contener saltos de línea (\n).
    pos : tuple[int, int]
        Coordenadas (x, y) iniciales —en píxeles— dentro de la superficie.
    font : pygame.font.Font
        Objeto fuente ya creado con tamaño y tipografía deseados.
    color : pygame.Color, opcional
        Color del texto (por defecto, negro).
    """
    words = [line.split(' ') for line in text.splitlines()]

    space = font.size(' ')[0]

    max_width, _ = surface.get_size()

    x, y = pos

    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            if x + word_width >= max_width:
                x = pos[0]
                y += word_height

            surface.blit(word_surface, (x, y))

            x += word_width + space

        x = pos[0]
        y += word_height

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    """Se encarga de crear un elemento en el juego guardando su superficie (textura) y su rectangulo (comportamiento) 

    Args:
        textura (str): Tiene que ser una ruta ya sea relativa o absoluta
        ancho (int): En pixeles el ancho de ese elemento
        alto (int): En pixeles el alto de ese elemento
        pos_x (int): Donde se va a ubicar en el eje x
        pos_y (int): Donde se va a ubicar en el eje y

    Returns:
        dict: El diccionario con el elemento creado
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x,pos_y,ancho,alto)
    
    return elemento_juego

def crear_lista_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int):
    """
    Genera y devuelve una lista con cuatro “botones” de respuesta
    alineados verticalmente para un juego de preguntas.

    Parámetros
    textura : str
        Ruta o identificador de la imagen que se usará como textura
        para cada botón de respuesta.
    ancho : int
        Ancho, en píxeles, que tendrá cada botón.
    alto : int
        Alto, en píxeles, que tendrá cada botón.
    pos_x : int
        Coordenada X inicial (margen izquierdo) donde se dibujará
        el primer botón.
    pos_y : int
        Coordenada Y inicial (margen superior) donde se dibujará
        el primer botón. Cada botón siguiente se colocará 80 px
        más abajo que el anterior.

    Retorna
    list[dict | pygame.Rect | objeto personalizado]
        Lista con los cuatro elementos de respuesta creados,
        tal como los devuelve `crear_elemento_juego`.
    """
    lista_respuestas = []

    for i in range(4):
        respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 80    
        
    return lista_respuestas

def crear_botones_menu() -> list:
    """
    Crea y devuelve una lista con cuatro botones para el menú principal,
    dispuestos verticalmente y con separación fija entre ellos.

    Detalles
    - Usa la textura «textura_respuesta.jpg» para todos los botones.
    - Cada botón mantiene el mismo tamaño, definido por las constantes
      globales `ANCHO_BOTON` y `ALTO_BOTON`.
    - El primer botón se sitúa en (200, 200).  
      Cada botón siguiente se coloca 80 px más abajo que el anterior.

    Retorna
    list
        Colección con los cuatro objetos retornados por
        `crear_elemento_juego`, normalmente sprites, rects o diccionarios,
        según la implementación de esa función auxiliar.
    """
    lista_botones = []
    pos_x = 200
    pos_y = 200

    for i in range(4):
        boton = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    
    return lista_botones

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int)->None:
    """
    Restaura o "limpia" la superficie gráfica de un elemento de juego,
    recargando su textura original y escalándola al tamaño especificado.

    Parámetros
    elemento_juego : dict
        Diccionario que representa un componente del juego (por ejemplo,
        un botón o cuadro de texto) y que contiene la clave "superficie",
        donde se almacena su imagen actual.
    textura : str
        Ruta al archivo de imagen que se usará para restaurar la textura.
    ancho : int
        Nuevo ancho de la superficie.
    alto : int
        Nuevo alto de la superficie.

    Retorna
    None
        La función modifica el diccionario `elemento_juego` directamente.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))

def tapar_respuesta(elemento_juego:dict,textura:str,ancho:int,alto:int)->None:
    """
    Cubre o reemplaza visualmente una respuesta en pantalla,
    modificando la superficie del elemento con una nueva textura.

    Este comportamiento es útil, por ejemplo, para ocultar respuestas
    ya seleccionadas o deshabilitadas durante una partida.

    Parámetros
    elemento_juego : dict
        Diccionario que representa una respuesta del juego y contiene
        una clave "superficie" que almacena su imagen actual.
    textura : str
        Ruta al archivo de imagen que se usará para tapar la respuesta.
    ancho : int
        Ancho de la nueva superficie.
    alto : int
        Alto de la nueva superficie.

    Retorna
    None
        La función modifica directamente la clave "superficie" del diccionario.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))  

def verificar_correcta(pregunta_actual:dict,respuesta:int)->bool:
    """
    Verifica si la respuesta seleccionada por el jugador es correcta.

    Parámetros
    pregunta_actual : dict
        Diccionario que representa una pregunta, y debe contener la clave
        "respuesta_correcta", con el número de la opción correcta (por ejemplo, 1, 2, 3 o 4).
    respuesta : int
        Número de la respuesta elegida por el jugador.

    Retorna
    bool
        True si la respuesta es correcta, False si es incorrecta.
    """
    if pregunta_actual["respuesta_correcta"] == respuesta:
        retorno = True
    else:
        retorno = False

    return retorno

def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    """
    Verifica si la respuesta seleccionada es correcta y actualiza los datos del juego
    según el resultado (puntaje, racha, vidas y tiempo).

    Parámetros
    datos_juego : dict
        Diccionario que contiene la información actual del juego. Debe incluir:
        - "puntuacion": int
        - "vidas": int
        - "racha": int
        - "tiempo_restante": int
    pregunta_actual : dict
        Diccionario que representa una pregunta. Debe tener la clave
        "respuesta_correcta" con el número de la respuesta válida.
    respuesta : int
        Número de la opción seleccionada por el jugador.

    Retorna
    bool
        True si la respuesta fue correcta, False si fue incorrecta.
    """
    if pregunta_actual["respuesta_correcta"] == respuesta:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        datos_juego["racha"] += 1
        if datos_juego["racha"] == 5:
            datos_juego["vidas"] += 1
            datos_juego["tiempo_restante"] += 15
        retorno = True
    else:
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
        datos_juego["vidas"] -= 1
        retorno = False
        
    return retorno

def reiniciar_estadisticas(datos_juego:dict):
    """
    Reinicia los valores principales del estado del juego al comenzar
    una nueva partida.

    Parámetros
    datos_juego : dict
        Diccionario que almacena las estadísticas del jugador durante la partida.
        Se espera que tenga al menos las claves:
        - "vidas"
        - "puntuacion"
        - "nombre"
        - "tiempo_restante"

    Retorna
    None
        La función modifica el diccionario `datos_juego` directamente.
    """
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = TIEMPO_JUEGO

def pasar_pregunta(lista_preguntas:list,indice:int,cuadro_pregunta:dict,lista_respuestas:list) -> dict:
    """
    Prepara y muestra una nueva pregunta en pantalla, restaurando
    visualmente el cuadro de pregunta y las respuestas.

    Parámetros
    lista_preguntas : list
        Lista de preguntas del juego. Cada pregunta es un diccionario
        con sus opciones y la respuesta correcta.
    indice : int
        Índice de la pregunta actual que se desea mostrar.
    cuadro_pregunta : dict
        Elemento visual (con clave "superficie") que representa el cuadro
        donde se muestra la pregunta.
    lista_respuestas : list
        Lista de elementos visuales para mostrar las opciones de respuesta.

    Retorna
    dict
        La pregunta actual seleccionada según el índice, lista para ser utilizada.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(cuadro_pregunta,"textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    
    return pregunta_actual

def mezclar_lista(lista_preguntas:list) -> None:
    """
    Mezcla aleatoriamente el orden de las preguntas en la lista
    para que el juego no repita siempre la misma secuencia.

    Parámetros
    lista_preguntas : list
        Lista de preguntas (cada una representada como un diccionario)
        que se desea reordenar aleatoriamente.

    Retorna
    None
        La función modifica la lista original directamente.
    """
    random.shuffle(lista_preguntas)

def guardar_puntuacion(puntos:int,nombre:str,nombre_archivo:str)-> dict|list:
    """
    Guarda la puntuación y el nombre del jugador en un archivo JSON llamado "partidas.json".
    Si el archivo no existe o está vacío, crea una nueva lista para almacenar las puntuaciones.

    Parámetros
    puntos : int
        Puntuación obtenida por el jugador.
    nombre : str
        Nombre del jugador.

    Retorna
    dict | list
        Lista actualizada con todas las puntuaciones guardadas.
    """
    datos = {"Puntuacion": puntos, "Nombre": nombre}
    if os.path.exists(nombre_archivo) == True:
        with open(nombre_archivo, "r") as archivo:
                puntuaciones = json.load(archivo)
    else:
        puntuaciones = []

    puntuaciones.append(datos)  
    
    with open(nombre_archivo, "w") as archivo:
        json.dump(puntuaciones, archivo, indent=4)

    return puntuaciones

def ordenar_jugadores(lista:list):
    """
    Ordena la lista de jugadores (o puntuaciones) en orden descendente
    usando un algoritmo de selección o burbuja simple.

    Parámetros
    lista : list
        Lista de números (por ejemplo, puntuaciones) que se desea ordenar.

    Retorna
    None
        La función modifica la lista original directamente.
    """
    for izq in range(len(lista)-1):
        for der in range((izq + 1), len(lista)):
            numero_izq = lista[izq]
            numero_der = lista[der]

        if numero_izq < numero_der:
            intercambiar_elementos(lista, izq, der)

def intercambiar_elementos(array: list, izq: int, der: int) -> None:
    """
    Intercambia los elementos en las posiciones `izq` y `der` dentro de la lista `array`.

    Parámetros
    array : list
        Lista donde se realizará el intercambio.
    izq : int
        Índice del primer elemento a intercambiar.
    der : int
        Índice del segundo elemento a intercambiar.

    Retorna
    None
        Modifica la lista `array` directamente.
    """
    auxilar = array[izq]
    array[izq] = array[der]
    array[der] = auxilar

def crear_pregunta(linea:str,separador:str=",")-> dict:
    linea = linea[0:len(linea)-1]
    lista_datos = linea.split(separador)
    pregunta = {}
    pregunta["pregunta"] = lista_datos[0]
    pregunta["respuesta_1"] = lista_datos[1]
    pregunta["respuesta_2"] = lista_datos[2]
    pregunta["respuesta_3"] = lista_datos[3]
    pregunta["respuesta_4"] = lista_datos[4]
    pregunta["respuesta_correcta"] = lista_datos[5]

    return pregunta

def leer_csv(nombre_archivo:str,lista:list,separador:str= ",")->bool:
    if os.path.exists(nombre_archivo) == True:
        with open(nombre_archivo,"r",encoding="utf-8") as archivo:
            archivo.readline()

            for linea in archivo:
                diccionario_preguntas = crear_pregunta(linea,separador)
                lista.append(diccionario_preguntas)
        retorno = True
    else:
        retorno = False
    
    return retorno


        
