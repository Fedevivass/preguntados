import pygame 
from constantes import *
from funciones import *

pygame.init()


fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)
cuadro_pregunta = crear_elemento_juego("textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,150,80)
lista_respuestas = crear_lista_respuestas("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,200,245)

comodin = crear_elemento_juego("bomba.png",70,70,530,300)
comodin["usado"] = False
comodin_pasar_preg = crear_elemento_juego("pasar.png",70,70,530,400)
comodin_pasar_preg["usado"] = False
comodin_x2 = crear_elemento_juego("icono_x2.png",70,70,530,230)
comodin_x2["usado"] = False
comodin_doble_oportunidad = crear_elemento_juego("icono.png",70,70,530,500)
comodin_doble_oportunidad["usado"] = False
comodin_doble_oportunidad["fallo"] = False
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo,1000)


def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict,lista_preguntas:list) -> str:
    retorno = "juego"


    pregunta_actual = lista_preguntas[datos_juego["indice"]]
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        comodin["usado"] = False
        comodin_pasar_preg["usado"] = False
        comodin_x2["usado"] = False
        comodin_doble_oportunidad["usado"] = False
        comodin_doble_oportunidad["fallo"] = False
        print("GAME OVER")
        retorno = "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
                if comodin["rectangulo"].collidepoint(evento.pos):
                    for i in range(len(lista_respuestas)-1):
                        respuesta = (i + 1)
                        if verificar_correcta(pregunta_actual,respuesta) != True and comodin["usado"] == False:    
                            tapar_respuesta(lista_respuestas[i],"textura_pregunta.jpg",ANCHO_BOTON,ALTO_BOTON)
                    comodin["usado"] = True
                if comodin_pasar_preg["rectangulo"].collidepoint(evento.pos):
                    if comodin_pasar_preg["usado"] == False:
                            datos_juego["indice"] += 1
                            pregunta_actual = pasar_pregunta(lista_preguntas,datos_juego["indice"],cuadro_pregunta,lista_respuestas)
                            comodin_pasar_preg["usado"] = True
                if comodin_x2["rectangulo"].collidepoint(evento.pos):
                    if comodin_x2["usado"] == False:
                        comodin_x2["usado"] = True
                if comodin_doble_oportunidad["rectangulo"].collidepoint(evento.pos):
                    if comodin_doble_oportunidad["usado"] == False:
                        comodin_doble_oportunidad["usado"] = True
                for i in range(len(lista_respuestas)):
                    if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                        respuesta = (i + 1)
                        if verificar_respuesta(datos_juego,pregunta_actual,respuesta,comodin_x2,comodin_doble_oportunidad) == True:
                            CLICK_SONIDO.play()
                            datos_juego["indice"] += 1
                            pregunta_actual = pasar_pregunta(lista_preguntas,datos_juego["indice"],cuadro_pregunta,lista_respuestas)
                            comodin_doble_oportunidad["usado"] = False
                            comodin_doble_oportunidad["fallo"] = False
                        else:
                            ERROR_SONIDO.play()
                            tapar_respuesta(lista_respuestas[i],"textura_pregunta.jpg",ANCHO_BOTON,ALTO_BOTON)
                            
                            if comodin_doble_oportunidad["usado"] == True:
                                if comodin_doble_oportunidad["fallo"] == False:
                                    comodin_doble_oportunidad["fallo"] = True
                                else:
                                    datos_juego["vidas"] -= 1
                                    datos_juego["racha"] = 0
                                    datos_juego["indice"] += 1
                                    pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)
                                    comodin_doble_oportunidad["usado"] = False
                                    comodin_doble_oportunidad["fallo_1"] = False
                            else:
                                datos_juego["indice"] += 1
                                datos_juego["vidas"] -= 1
                                datos_juego["racha"] = 0
                                pregunta_actual = pasar_pregunta(lista_preguntas,datos_juego["indice"],cuadro_pregunta,lista_respuestas)
                                comodin_doble_oportunidad["usado"] = False

                        if datos_juego["indice"] >= len(lista_preguntas):
                            datos_juego["indice"] = 0
                            mezclar_lista(lista_preguntas)

                                        
    
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])
    if comodin["usado"] == False:
        pantalla.blit(comodin["superficie"],comodin["rectangulo"])
    if comodin_pasar_preg["usado"] == False:
        pantalla.blit(comodin_pasar_preg["superficie"],comodin_pasar_preg["rectangulo"])
    if comodin_x2["usado"] == False:
        pantalla.blit(comodin_x2["superficie"],comodin_x2["rectangulo"])
    if comodin_doble_oportunidad["usado"] == False:
        pantalla.blit(comodin_doble_oportunidad["superficie"],comodin_doble_oportunidad["rectangulo"])
    for i in range(len(lista_respuestas)):
        pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])
    
    mostrar_texto(cuadro_pregunta["superficie"],pregunta_actual["pregunta"],(15,15),FUENTE_PREGUNTA,COLOR_NEGRO)
    mostrar_texto(lista_respuestas[0]["superficie"],pregunta_actual["respuesta_1"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(lista_respuestas[1]["superficie"],pregunta_actual["respuesta_2"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(lista_respuestas[2]["superficie"],pregunta_actual["respuesta_3"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(lista_respuestas[3]["superficie"],pregunta_actual["respuesta_4"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)



    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,10),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,40),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"TIEMPO: {datos_juego['tiempo_restante']} seg",(450,10),FUENTE_TEXTO,COLOR_NEGRO)

    return retorno