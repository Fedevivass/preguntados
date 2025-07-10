import pygame
from constantes import *
from funciones import *

pygame.init()
lista_botones = crear_botones_menu()
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)


def mostrar_menu(pantlla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    retorno = "menu"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for i in range(len(lista_botones)):
                    if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                        if i == BOTON_JUGAR:
                            retorno = "juego"
                        elif i == BOTON_CONFIG:
                            retorno = "ajustes"
                        elif i == BOTON_PUNTUACIONES:
                            retorno = "rankings"
                        else:
                            retorno = "salir"
    
    pantlla.blit(fondo_pantalla,(0,0))
    
    for i in range(len(lista_botones)):
        pantlla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
        
    mostrar_texto(lista_botones[BOTON_JUGAR]["superficie"],"JUGAR",(80,10),FUENTE_TEXTO,COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_CONFIG]["superficie"],"AJUSTES",(80,10),FUENTE_TEXTO,COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_PUNTUACIONES]["superficie"],"RANKINGS",(80,10),FUENTE_TEXTO,COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_SALIR]["superficie"],"SALIR",(80,10),FUENTE_TEXTO,COLOR_BLANCO)


    return retorno