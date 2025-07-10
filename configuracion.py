import pygame
from constantes import *
from funciones import *

pygame.init()

boton_suma = crear_elemento_juego("mas.webp",60,60,550,170)
boton_resta = crear_elemento_juego("menos.webp",60,60,20,170)
boton_volver = crear_elemento_juego("atras.png",50,40,10,10)
volumen_musica = crear_elemento_juego("textura_respuesta.jpg",300,50,20,100)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "ajustes"
    
    fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            retorno = "menu"
            CLICK_SONIDO.play()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
      
    pantalla.blit(fondo_pantalla,(0,0))


    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    pantalla.blit(volumen_musica["superficie"],volumen_musica["rectangulo"])

    mostrar_texto(volumen_musica["superficie"],"Volumen Musica:",(5,5),FUENTE_PREGUNTA,COLOR_BLANCO)
    mostrar_texto(pantalla,f"{datos_juego['volumen_musica']} %",(270,170),FUENTE_VOLUMEN,COLOR_NEGRO)

    return retorno
    