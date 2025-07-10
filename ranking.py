import pygame
from constantes import *
from funciones import *

pygame.init()

boton_volver = crear_elemento_juego("atras.png",50,40,10,10)

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    retorno = "rankings"
    
    fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.KEYDOWN:
            retorno = "menu"
            CLICK_SONIDO.play()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    ordenar_jugadores(lista_rankings)
    pantalla.blit(fondo_pantalla,(0,0))

    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    if len(lista_rankings) > 0 and len(lista_rankings) <= 10:
        mostrar_texto(pantalla,f"{lista_rankings} PUNTOS\n",(50,50),FUENTE_RANKING,COLOR_NEGRO)
    else:
        mostrar_texto(pantalla,"NINGUN JUGADOR REGISTRADO",(50,50),FUENTE_RANKING,COLOR_NEGRO)

    return retorno
    