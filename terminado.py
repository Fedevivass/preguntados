import pygame
from constantes import *
from funciones import *

pygame.init()

fuente = pygame.font.SysFont("Arial Narrow",40)
cuadro = crear_elemento_juego("textura_respuesta.jpg",250,50,200,200)
guardado = crear_elemento_juego("textura_respuesta.jpg",200,50,200,300)
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict,jugadores:dict) -> str:
    retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            
            print(datos_juego["nombre"])
            
            if letra_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]
                print(datos_juego["nombre"])
                limpiar_superficie(cuadro,"textura_respuesta.jpg",250,50)
            
            if letra_presionada == "space":
                datos_juego["nombre"] += " "
            
            if len(letra_presionada) == 1:  
                if bloc_mayus != 0:
                    datos_juego["nombre"] += letra_presionada.upper()
                else:
                    datos_juego["nombre"] += letra_presionada
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if guardado["rectangulo"].collidepoint(evento.pos):
                    jugadores["Nombre"] = datos_juego["nombre"]
                    jugadores["Puntuacion"] = datos_juego["puntuacion"]
                    jugadores["Tiempo_final"] = datos_juego["tiempo_restante"]
                    guardar_puntuacion(jugadores,"partida.json")

                    reiniciar_estadisticas(datos_juego)
                    retorno = "menu"
                    
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro["superficie"],cuadro["rectangulo"])
    pantalla.blit(guardado["superficie"],guardado["rectangulo"])
    mostrar_texto(cuadro["superficie"],datos_juego["nombre"],(10,0),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego['puntuacion']} puntos",(250,100),fuente,COLOR_NEGRO)
    mostrar_texto(guardado["superficie"],"GUARDAR",(5,5),fuente,COLOR_NEGRO)
    
    return retorno
