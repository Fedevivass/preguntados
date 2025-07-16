import pygame 
from constantes import *
from menu import *
from Juego import *
from configuracion import *
from ranking import *
from terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True
datos_juego = {"puntuacion":0,"vidas":3,"nombre":"","tiempo_restante":TIEMPO_JUEGO,"volumen_musica":0,"indice":0,"racha":0}

reloj = pygame.time.Clock()
ventana_actual = "menu"

bandera_juego = False
jugadores = {}
while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "salir":
        corriendo = False
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla,cola_eventos)
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "juego":
        if bandera_juego == False:
            pygame.mixer.init()
            pygame.mixer.music.load("musica.mp3")
            porcentaje_musica = datos_juego["volumen_musica"] / 100
            pygame.mixer.music.set_volume(porcentaje_musica)
            pygame.mixer.music.play(-1)
            bandera_juego = True
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego,lista_preguntas)
    elif ventana_actual == "terminado":
        if bandera_juego == True:
            bandera_juego = False
            pygame.mixer.music.stop()
        ventana_actual = mostrar_fin_juego(pantalla,cola_eventos,datos_juego,jugadores)

    pygame.display.flip()
pygame.quit()