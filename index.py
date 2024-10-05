import pygame
import random
import os

pygame.init()

# Colores básicos
colores_rgb = {
    'rojo': (255, 0, 0),
    'azul': (0, 0, 255),
    'verde': (0, 255, 0),
    'amarillo': (255, 255, 0),
    'negro': (0, 0, 0),
    'blanco': (255, 255, 255),
    'gris': (200, 200, 200),
    'gris_claro': (240, 240, 240),
    'gris_oscuro': (100, 100, 100),
    'marron_claro': (210, 180, 140)
}

# Parámetros del juego
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Mastermind con IA - Mejorado")

# Cargar fuentes
fuente = pygame.font.Font(None, 36)
fuente_pequeña = pygame.font.Font(None, 24)

# Cargar imágenes de fondo
fondo_menu = pygame.image.load(os.path.join('master.jpg'))
fondo_ia = pygame.image.load(os.path.join('ima.jpg'))
fondo_jugar = pygame.image.load(os.path.join('ima2.jpg'))

# Ajustar tamaño de las imágenes
fondo_menu = pygame.transform.scale(fondo_menu, (ancho, alto))
fondo_ia = pygame.transform.scale(fondo_ia, (ancho, alto))
fondo_jugar = pygame.transform.scale(fondo_jugar, (ancho, alto))

colores = ['rojo', 'azul', 'verde', 'amarillo']
secuencia_secreta = []
intentos_ia = 0
adivinanzas_ia = []
pistas_ia = []
combinaciones_intentadas = set()
juego_terminado = False
modo_juego = ""
intentos_jugador = []
pistas_jugador = []
secuencia_jugador = []

def mostrar_texto(texto, pos_x, pos_y, color=colores_rgb['blanco'], fuente_usar=fuente):
    sombra = fuente_usar.render(texto, True, colores_rgb['negro'])
    render = fuente_usar.render(texto, True, color)
    pantalla.blit(sombra, (pos_x + 2, pos_y + 2))
    pantalla.blit(render, (pos_x, pos_y))

def dibujar_circulo_3d(superficie, color, pos, radio):
    pygame.draw.circle(superficie, color, pos, radio)
    pygame.draw.circle(superficie, (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)), pos, radio - 3)
    pygame.draw.circle(superficie, (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50)), (pos[0] - 3, pos[1] - 3), radio - 6)

def dibujar_adivinanzas_y_pistas(adivinanzas, pistas, x_offset, y_offset, max_mostrar=8):
    y = y_offset
    for idx, (adivinanza, pista) in enumerate(list(zip(adivinanzas, pistas))[-max_mostrar:]):
        # Dibujar rectángulo de fondo para cada intento
        pygame.draw.rect(pantalla, colores_rgb['marron_claro'], (x_offset - 10, y - 15, 280, 40), border_radius=10)
        
        for j, color in enumerate(adivinanza):
            dibujar_circulo_3d(pantalla, colores_rgb[color], (x_offset + j * 35, y), 12)
        
        for j in range(pista['correctos']):
            dibujar_circulo_3d(pantalla, colores_rgb['negro'], (x_offset + 160 + j * 20, y), 6)
        for j in range(pista['mal_colocados']):
            dibujar_circulo_3d(pantalla, colores_rgb['blanco'], (x_offset + 160 + (pista['correctos'] + j) * 20, y), 6)
            pygame.draw.circle(pantalla, colores_rgb['negro'], (x_offset + 160 + (pista['correctos'] + j) * 20, y), 6, 1)
        
        y += 50

def dar_pistas(adivinanza, secuencia):
    correctos = sum([1 for i in range(4) if adivinanza[i] == secuencia[i]])
    mal_colocados = sum([min(adivinanza.count(color), secuencia.count(color)) for color in set(adivinanza)]) - correctos
    return {'correctos': correctos, 'mal_colocados': mal_colocados}

def intento_ia_paso_a_paso():
    global adivinanzas_ia, intentos_ia, juego_terminado
    
    while True:
        intento = random.sample(colores, 4)
        if tuple(intento) not in combinaciones_intentadas:
            combinaciones_intentadas.add(tuple(intento))
            break

    pistas = dar_pistas(intento, secuencia_secreta)
    adivinanzas_ia.append(intento)
    pistas_ia.append(pistas)
    
    intentos_ia += 1

    if intento == secuencia_secreta:
        juego_terminado = True

def reiniciar_juego():
    global secuencia_secreta, intentos_ia, adivinanzas_ia, pistas_ia, combinaciones_intentadas, juego_terminado, intentos_jugador, pistas_jugador, secuencia_jugador
    secuencia_secreta = []
    intentos_ia = 0
    adivinanzas_ia = []
    pistas_ia = []
    combinaciones_intentadas = set()
    juego_terminado = False
    intentos_jugador = []
    pistas_jugador = []
    secuencia_jugador = []

def dibujar_boton(texto, x, y, ancho, alto, color_normal, color_hover):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto), border_radius=15)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(pantalla, color_normal, (x, y, ancho, alto), border_radius=15)
    
    texto_surf = fuente.render(texto, True, colores_rgb['blanco'])
    texto_rect = texto_surf.get_rect(center=(x + ancho/2, y + alto/2))
    pantalla.blit(texto_surf, texto_rect)
    return False

def mostrar_mensaje_adivinanza(intentos):
    pygame.draw.rect(pantalla, colores_rgb['verde'], (ancho - 300, alto - 60, 280, 40), border_radius=10)
    mostrar_texto(f"¡Adivinado en {intentos} intentos!", ancho - 290, alto - 50, color=colores_rgb['blanco'])

def jugar_mastermind():
    global juego_terminado, secuencia_secreta, modo_juego, intentos_ia, intentos_jugador, pistas_jugador, secuencia_jugador
    
    seleccion_jugador = []
    temporizador_ia = 0
    tiempo_espera = 1000

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if modo_juego == "IA":
                    for idx, color in enumerate(colores):
                        if (50 + idx * 80 - 30) <= event.pos[0] <= (50 + idx * 80 + 30) and 45 <= event.pos[1] <= 105:
                            if len(seleccion_jugador) < 4 and color not in seleccion_jugador:
                                seleccion_jugador.append(color)
                elif modo_juego == "JUGAR":
                    for idx, color in enumerate(colores):
                        if (50 + idx * 80 - 30) <= event.pos[0] <= (50 + idx * 80 + 30) and 45 <= event.pos[1] <= 105:
                            if len(secuencia_jugador) < 4:
                                secuencia_jugador.append(color)

        if modo_juego == "":
            pantalla.blit(fondo_menu, (0, 0))
            mostrar_texto("Seleccione un modo de juego:", 200, 50)
            if dibujar_boton("IA", 250, 150, 150, 50, colores_rgb['gris_oscuro'], colores_rgb['gris']):
                modo_juego = "IA"
                reiniciar_juego()
            if dibujar_boton("JUGAR", 450, 150, 150, 50, colores_rgb['gris_oscuro'], colores_rgb['gris']):
                modo_juego = "JUGAR"
                reiniciar_juego()

        elif modo_juego == "IA":
            pantalla.blit(fondo_ia, (0, 0))
            mostrar_texto("Selecciona 4 colores para la IA", 20, 20)

            for idx, color in enumerate(colores):
                dibujar_circulo_3d(pantalla, colores_rgb[color], (50 + idx * 80, 75), 30)
                mostrar_texto(color, 30 + idx * 80, 110, color=colores_rgb['blanco'], fuente_usar=fuente_pequeña)

            if len(seleccion_jugador) == 4:
                secuencia_secreta = seleccion_jugador.copy()
                mostrar_texto("Secuencia seleccionada:", 20, 150, color=colores_rgb['blanco'])
                for i, color in enumerate(seleccion_jugador):
                    dibujar_circulo_3d(pantalla, colores_rgb[color], (50 + i * 80, 200), 30)

                pygame.draw.rect(pantalla, colores_rgb['marron_claro'], (20, 250, 760, 330), border_radius=10)
                mostrar_texto("Intentos de la IA:", 30, 260, color=colores_rgb['negro'])

                dibujar_adivinanzas_y_pistas(adivinanzas_ia, pistas_ia, 50, 300)

                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - temporizador_ia >= tiempo_espera and not juego_terminado:
                    intento_ia_paso_a_paso()
                    temporizador_ia = tiempo_actual

                if juego_terminado:
                    mostrar_mensaje_adivinanza(intentos_ia)

        elif modo_juego == "JUGAR":
            pantalla.blit(fondo_jugar, (0, 0))
            if not secuencia_secreta:
                secuencia_secreta = random.sample(colores, 4)
            
            mostrar_texto("Adivina la secuencia secreta", 20, 20)
            
            for idx, color in enumerate(colores):
                dibujar_circulo_3d(pantalla, colores_rgb[color], (50 + idx * 80, 75), 30)
                mostrar_texto(color, 30 + idx * 80, 110, color=colores_rgb['blanco'], fuente_usar=fuente_pequeña)

            mostrar_texto("Tu intento:", 20, 150, color=colores_rgb['blanco'])
            for i, color in enumerate(secuencia_jugador):
                dibujar_circulo_3d(pantalla, colores_rgb[color], (50 + i * 80, 200), 30)

            if dibujar_boton("Enviar", 350, 180, 100, 40, colores_rgb['gris_oscuro'], colores_rgb['gris']) and len(secuencia_jugador) == 4:
                pistas = dar_pistas(secuencia_jugador, secuencia_secreta)
                intentos_jugador.append(secuencia_jugador.copy())
                pistas_jugador.append(pistas)
                if secuencia_jugador == secuencia_secreta:
                    juego_terminado = True
                secuencia_jugador = []

            pygame.draw.rect(pantalla, colores_rgb['marron_claro'], (20, 250, 760, 330), border_radius=10)
            mostrar_texto("Tus intentos:", 30, 260, color=colores_rgb['negro'])
            dibujar_adivinanzas_y_pistas(intentos_jugador, pistas_jugador, 50, 300)

            if juego_terminado:
                mostrar_mensaje_adivinanza(len(intentos_jugador))

        pygame.display.flip()

jugar_mastermind()