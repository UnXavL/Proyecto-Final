import pygame
import random
import math
import time
import json

# Inicializa Pygame y el mixer
pygame.init()
pygame.mixer.init()

# Cambiar el nombre de la ventana
pygame.display.set_caption("Mi Juego de Pac-Man")

# Cargar la imagen del icono
icono = pygame.image.load("Assets/Dibujos/icono.png")  # Reemplaza "icono.png" con la ruta de tu imagen de icono
pygame.display.set_icon(icono)  # Establecer el icono de la ventana

# Cargar música de fondo
pygame.mixer.music.load("Assets/Fondo_Música/musica_fondo1.mp3")  # Asegúrate de tener el archivo en la misma carpeta
pygame.mixer.music.set_volume(0.2)  # Ajusta el volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproduce en bucle indefinidamente

# Dimensiones de la pantalla
pantalla_info = pygame.display.Info()
ANCHO_PANTALLA = int(pantalla_info.current_w * 0.8)
ALTO_PANTALLA = int(pantalla_info.current_h * 0.8)

# Ajusta el tamaño del laberinto
ESCALA = 0.5
TAM_CELDA = int(min(ANCHO_PANTALLA // 20, ALTO_PANTALLA // 15) * ESCALA)
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
ROSADO = (255, 192, 203)
CIAN = (0, 255, 255)
NARANJA = (255, 128, 0)

# Laberinto de Pac-Man
laberinto = [
    "1111111111111111111111111111111111111111111111111111111",
    "1000000000000010000000000000000000000000100000000000001",
    "1011011011011010111111111101011111111110101101101101101",
    "1011011011011000000011000000000001100000001101101101101",
    "1000000000000010111011011111111101101110100000000000001",
    "1011011011011010010010011111111100100100101101101101101",
    "1011011011011010010000011111111100000100101101101101101",
    "1000000000000010010010000000000000100100100000000000001",
    "1011011011011000010000000000000000000100001101101101101",
    "1011011011011010000000000000000000000000101101101101101",
    "1000000000000010000000000000000000000000100000000000001",
    "1111111111111110000000000000000000000000111111111111111",
    "1000000000000000000000000000000000000000000000000000001",
    "1010111001111010000000111112111110000000101111001110101",
    "1010001100000010000000122222222210000000100000011000101",
    "1011101011111010000000122222222210000000101111101011101",
    "1000101000000010000000122222222210000000100000001010001",
    "1010101011111110000000111111111110000000111111101010101",
    "1000000000000000000000000000000000000000000000000000001",
    "1111111111111110000000000000000000000000111111111111111",
    "1000000000000010000000000000000000000000100000000000001",
    "1011011011011010000000000000000000000000101101101101101",
    "1011011011011000010000111111111110000100001101101101101",
    "1000000000000010010010000000000000100100100000000000001",
    "1011011011011010010000011111111100000100101101101101101",
    "1011011011011010010010011111111100100100101101101101101",
    "1000000000000010111011011111111101101110100000000000001",
    "1011011011011000000011000000000001100000001101101101101",
    "1011011011011010111111111101011111111110101101101101101",
    "1000000000000010000000000002000000000000100000000000001",
    "1111111111111111111111111111111111111111111111111111111"
    ]

# Dimensiones del laberinto
alto_laberinto = len(laberinto)
ancho_laberinto = len(laberinto[0])

# Inicialización de variables
seleccion = 0
posicion_pacman_inicial = [27, 29]
posicion_pacman = posicion_pacman_inicial[:]
puntuacion = 0
vidas = 3
tiempo_inicio = pygame.time.get_ticks()
dificultad = 2  # Normal por defecto
reloj = pygame.time.Clock()

# Cargar récords
def cargar_record():
    try:
        with open("records.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guardar récord
def guardar_record(puntuacion):
    records = cargar_record()
    records.append(puntuacion)
    records.sort(reverse=True)
    records = records[:5]
    with open("records.json", "w") as f:
        json.dump(records, f)

def crear_fuente(tamano):
    return pygame.font.SysFont(None, tamano * (ANCHO_PANTALLA // 800))

def desvanecer(aumento=True):
    alpha = 0 if aumento else 255
    surface = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    surface.fill(NEGRO)

    for _ in range(255):
        surface.set_alpha(alpha)
        pantalla.blit(surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)
        alpha += 1 if aumento else -1

def mostrar_menu_principal():
    pantalla.fill(NEGRO)
    fuente_titulo = crear_fuente(64)  # Título más grande
    fuente_opciones = crear_fuente(36)  # Opciones más pequeñas
    titulo = fuente_titulo.render("Pac-Man", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, ALTO_PANTALLA // 2 - 150))

    opciones = ["Jugar", "Ver Puntuaciones", "Ajustes", "Salir"]

    for i, texto in enumerate(opciones):
        color = AMARILLO if i == seleccion else BLANCO
        renderizado = fuente_opciones.render(texto, True, color)
        pantalla.blit(renderizado, (ANCHO_PANTALLA // 2 - renderizado.get_width() // 2, ALTO_PANTALLA // 2 - 50 + i * 50))

        # Aumentar tamaño de la opción seleccionada
        if i == seleccion:
            renderizado = fuente_opciones.render(texto, True, AMARILLO)
            pantalla.blit(renderizado, (ANCHO_PANTALLA // 2 - renderizado.get_width() // 2, ALTO_PANTALLA // 2 - 50 + i * 50))

    instrucciones = crear_fuente(24).render('Usa W/S para navegar', True, BLANCO)
    pantalla.blit(instrucciones, (ANCHO_PANTALLA // 2 - instrucciones.get_width() // 2, ALTO_PANTALLA // 2 + 150))
    pygame.display.update()

def manejar_input_menu():
    global seleccion
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_s]:
        seleccion = (seleccion + 1) % 4
        pygame.time.delay(150)  # Delay para prevenir saltos rápidos
    elif teclas[pygame.K_w]:
        seleccion = (seleccion - 1) % 4
        pygame.time.delay(150)  # Delay para prevenir saltos rápidos

def crear_fondo_degradado_redondeado(superficie, rect, color_inicio, color_fin, radio_borde, opacidad):
    # Crear una superficie temporal con transparencia y bordes redondeados
    fondo_temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Aplicar el degradado
    for y in range(rect.height):
        # Interpolar entre el color de inicio y el color de fin para crear el degradado
        factor = y / rect.height
        color = (
            int(color_inicio[0] * (1 - factor) + color_fin[0] * factor),
            int(color_inicio[1] * (1 - factor) + color_fin[1] * factor),
            int(color_inicio[2] * (1 - factor) + color_fin[2] * factor)
        )
        pygame.draw.line(fondo_temp, color, (0, y), (rect.width, y))

    # Crear una máscara de bordes redondeados y aplicarla
    mascara = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mascara, (255, 255, 255), (0, 0, rect.width, rect.height), border_radius=radio_borde)
    fondo_temp.blit(mascara, (0, 0), None, pygame.BLEND_RGBA_MULT)

    # Ajustar opacidad
    fondo_temp.set_alpha(opacidad)

    # Dibujar el fondo en la pantalla
    superficie.blit(fondo_temp, rect.topleft)

def mostrar_records():
    pantalla.fill(NEGRO)
    fuente_titulo = crear_fuente(52)
    fuente_score = crear_fuente(36)

    # Título
    titulo = fuente_titulo.render('Récords:', True, AMARILLO)
    pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, ALTO_PANTALLA // 2 - 150))

    records = cargar_record()

    # Dimensiones del fondo
    fondo_ancho = 300
    fondo_alto = max(150, 60 + len(records) * 35)  # Ajuste de altura
    fondo_rect = pygame.Rect(ANCHO_PANTALLA // 2 - fondo_ancho // 2, ALTO_PANTALLA // 2 - fondo_alto // 2, fondo_ancho, fondo_alto)

    # Animación de opacidad
    for opacidad in range(0, 256, 5):  # De 0 a 255 en pasos de 5
        crear_fondo_degradado_redondeado(pantalla, fondo_rect, (0, 0, 155), (0, 0, 255), 20, opacidad)
        pygame.display.update()
        time.sleep(0.02)  # Pausa breve para hacer visible la animación

    # Mostrar los récords
    for i, score in enumerate(records):
        renderizado = fuente_score.render(f'{i + 1}. {score}', True, BLANCO)
        pantalla.blit(renderizado, (fondo_rect.left + 20, fondo_rect.top + 30 + i * 35))
        # Separador entre los récords
        if i < len(records) - 1:  # No dibujar una línea después del último récord
            pygame.draw.line(pantalla, BLANCO, (fondo_rect.left + 20, fondo_rect.top + 30 + (i + 1) * 35 - 5), (fondo_rect.right - 20, fondo_rect.top + 30 + (i + 1) * 35 - 5), 1)

    # Mensaje de instrucciones
    instrucciones = crear_fuente(24).render('Presiona Enter para volver', True, BLANCO)
    pantalla.blit(instrucciones, (ANCHO_PANTALLA // 2 - instrucciones.get_width() // 2, fondo_rect.bottom + 20))

    pygame.display.update()

    # Espera hasta que el usuario decida salir
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Regresar al menú al presionar Enter
                    return

def mostrar_ajustes():
    global seleccion
    opciones = [
        "Música seleccionada : Dispara, Nicki Nicole y Milo J",
        "Música seleccionada : 3 Pecados despues, Milo J",
        "Música seleccionada : El Amor de Mi Vida, Los Ángeles Azules y Maria Becerra"
    ]
    
    seleccion = 0  # Inicializar selección

    while True:
        pantalla.fill(NEGRO)
        fuente = crear_fuente(36)

        # Renderizar texto de la opción
        texto_opcion = opciones[seleccion]
        renderizado = fuente.render(texto_opcion, True, AMARILLO)
        
        # Calcular posiciones
        flecha_izquierda = "<" if seleccion > 0 else " "
        flecha_derecha = ">" if seleccion < len(opciones) - 1 else " "
        
        # Renderizar flechas
        renderizado_flecha_izquierda = fuente.render(flecha_izquierda, True, AMARILLO)
        renderizado_flecha_derecha = fuente.render(flecha_derecha, True, AMARILLO)

        # Posicionamiento
        flecha_izquierda_x = ANCHO_PANTALLA // 2 - renderizado.get_width() // 2 - renderizado_flecha_izquierda.get_width() - 10
        flecha_derecha_x = ANCHO_PANTALLA // 2 + renderizado.get_width() // 2 + 10

        # Dibujar en la pantalla
        pantalla.blit(renderizado_flecha_izquierda, (flecha_izquierda_x, ALTO_PANTALLA // 2 + 40))
        pantalla.blit(renderizado, (ANCHO_PANTALLA // 2 - renderizado.get_width() // 2, ALTO_PANTALLA // 2 + 40))
        pantalla.blit(renderizado_flecha_derecha, (flecha_derecha_x, ALTO_PANTALLA // 2 + 40))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d and seleccion < len(opciones) - 1:  # Tecla D para derecha
                    seleccion += 1
                elif evento.key == pygame.K_a and seleccion > 0:  # Tecla A para izquierda
                    seleccion -= 1
                elif evento.key == pygame.K_RETURN:
                    # Cambiar la música según la selección
                    if seleccion == 0:
                        pygame.mixer.music.load("Assets/Música_Ajuste/musica1.mp3")
                    elif seleccion == 1:
                        pygame.mixer.music.load("Assets/Música_Ajuste/musica2.mp3")
                    elif seleccion == 2:
                        pygame.mixer.music.load("Assets/Música_Ajuste/musica3.mp3")
                    pygame.mixer.music.play(-1)  # Reproduce en loop
                elif evento.key == pygame.K_ESCAPE:  # O usa ESC para volver
                    return  # Salir de la función y volver al menú

def mostrar_game_over():
    # Cargar música de Game Over (si es diferente, puedes cambiar la ruta)
    pygame.mixer.music.load("Assets/Fondo_Música/game_over_musica.mp3")  # Asegúrate de tener el archivo correcto
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # Reproduce en bucle indefinidamente

    seleccion = 0  # Reiniciar selección al mostrar el Game Over
    while True:
        pantalla.fill(NEGRO)
        fuente_titulo = crear_fuente(64)  # Título más grande
        fuente_puntuacion = crear_fuente(36)  # Puntuación más pequeña
        fuente_opciones = crear_fuente(36)  # Opciones del menú

        # Título
        titulo = fuente_titulo.render('GAME OVER', True, BLANCO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, ALTO_PANTALLA // 2 - 150))

        # Puntuación
        puntuacion_texto = fuente_puntuacion.render(f'Puntuación: {puntuacion}', True, AMARILLO)
        pantalla.blit(puntuacion_texto, (ANCHO_PANTALLA // 2 - puntuacion_texto.get_width() // 2, ALTO_PANTALLA // 2 - 50))

        # Opciones del menú de Game Over
        opciones = ["Reiniciar", "Volver al menú"]
        for i, texto in enumerate(opciones):
            color = AMARILLO if i == seleccion else BLANCO
            renderizado = fuente_opciones.render(texto, True, color)
            pantalla.blit(renderizado, (ANCHO_PANTALLA // 2 - renderizado.get_width() // 2, ALTO_PANTALLA // 2 + 50 + i * 40))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:  # Abajo
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_w:  # Arriba
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()  # Detener música al salir de la pantalla
                    return seleccion == 0  # Reiniciar si 0, volver al menú si 1

def reiniciar_juego():
    global posicion_pacman, puntuacion, vidas, posiciones_comida, tiempo_inicio
    posicion_pacman = posicion_pacman_inicial[:]
    puntuacion = 0
    vidas = 3
    posiciones_comida = [(x, y) for y in range(alto_laberinto) for x in range(ancho_laberinto) if laberinto[y][x] == '0']
    tiempo_inicio = pygame.time.get_ticks()

# Cargar y escalar la imagen del muro
imagen_muro = pygame.image.load("Assets/Dibujos/muros.png")
imagen_muro = pygame.transform.scale(imagen_muro, (TAM_CELDA, TAM_CELDA))

def dibujar_laberinto():
    for y in range(alto_laberinto):
        for x in range(ancho_laberinto):
            if laberinto[y][x] == '1':
                # Dibujar la imagen del muro en la posición correspondiente
                pantalla.blit(imagen_muro, (x * TAM_CELDA, y * TAM_CELDA))
            elif laberinto[y][x] == '2':
                pygame.draw.rect(pantalla, NEGRO, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA))  # Dibuja el bloque negro


# Cargar las imágenes de animación para cada dirección
animacion_derecha = [
    pygame.image.load("Assets/Dibujos/PacMan/PacMan.png"),
    pygame.image.load("Assets/Dibujos/PacMan/PacMan_Derecha.png"),
]
animacion_izquierda = [
    pygame.image.load("Assets/Dibujos/PacMan/PacMan.png"),
    pygame.image.load("Assets/Dibujos/PacMan/PacMan_Izquierda.png"),
]
animacion_arriba = [
    pygame.image.load("Assets/Dibujos/PacMan/PacMan.png"),
    pygame.image.load("Assets/Dibujos/PacMan/PacMan_Arriba.png"),
]
animacion_abajo = [
    pygame.image.load("Assets/Dibujos/PacMan/PacMan.png"),
    pygame.image.load("Assets/Dibujos/PacMan/PacMan_Abajo.png"),
]

# Ajustar el tamaño de cada imagen al tamaño de la celda
animacion_derecha = [pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA)) for imagen in animacion_derecha]
animacion_izquierda = [pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA)) for imagen in animacion_izquierda]
animacion_arriba = [pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA)) for imagen in animacion_arriba]
animacion_abajo = [pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA)) for imagen in animacion_abajo]

# Variables para controlar la animación
indice_animacion = 0
contador_tiempo = 0
duracion_cuadro = 1  # Cambia cada 5 fotogramas
direccion_actual = "derecha"  # Dirección inicial de Pac-Man

# Función para dibujar a Pac-Man con animación según la dirección
def dibujar_pacman():
    global indice_animacion, contador_tiempo

    # Seleccionar la animación según la dirección actual
    if direccion_actual == "derecha":
        animacion = animacion_derecha
    elif direccion_actual == "izquierda":
        animacion = animacion_izquierda
    elif direccion_actual == "arriba":
        animacion = animacion_arriba
    elif direccion_actual == "abajo":
        animacion = animacion_abajo

    # Calcular la posición en pantalla de Pac-Man
    posicion_x = posicion_pacman[0] * TAM_CELDA
    posicion_y = posicion_pacman[1] * TAM_CELDA

    # Cambiar de cuadro de animación cada ciertos fotogramas
    contador_tiempo += 1
    if contador_tiempo >= duracion_cuadro:
        contador_tiempo = 0
        indice_animacion = (indice_animacion + 1) % len(animacion)  # Alterna entre las imágenes

    # Dibujar el cuadro actual de la animación en la posición de Pac-Man
    pantalla.blit(animacion[indice_animacion], (posicion_x, posicion_y))

# Cargar la imagen de la comida y redimensionarla a un tamaño más pequeño (8x8 píxeles)
imagen_comida = pygame.image.load("Assets/Dibujos/Punto.png")
imagen_comida = pygame.transform.scale(imagen_comida, (8, 8))  # Escala la imagen a 8x8 píxeles

def dibujar_comida():
    for comida in posiciones_comida:
        # Calcular la posición en pantalla para cada comida
        posicion_x = comida[0] * TAM_CELDA + (TAM_CELDA - 8) // 2  # Centra la imagen en la celda
        posicion_y = comida[1] * TAM_CELDA + (TAM_CELDA - 8) // 2  # Centra la imagen en la celda
        # Dibujar la imagen de la comida en la posición calculada
        pantalla.blit(imagen_comida, (posicion_x, posicion_y))

# Cargar imágenes de los fantasmas
imagen_fantasma_rojo = pygame.image.load('Assets/Dibujos/Fantasmas/Fantasma_Rojo.png')
imagen_fantasma_rosado = pygame.image.load('Assets/Dibujos/Fantasmas/Fantasma_Rosado.png')
imagen_fantasma_naranja = pygame.image.load('Assets/Dibujos/Fantasmas/Fantasma_Naranja.png')
imagen_fantasma_cian = pygame.image.load('Assets/Dibujos/Fantasmas/Fantasma_Cian.png')

# Almacenar las imágenes en un diccionario
imagenes_fantasmas = {
    ROJO: imagen_fantasma_rojo,
    ROSADO: imagen_fantasma_rosado,
    NARANJA: imagen_fantasma_naranja,
    CIAN: imagen_fantasma_cian
}

# Definir la lista de fantasmas con posiciones específicas
fantasmas = [
    [24, 15, ROJO],    # Fantasma rojo
    [26, 15, ROSADO],  # Fantasma rosado
    [28, 15, NARANJA], # Fantasma naranja
    [30, 15, CIAN]     # Fantasma cian
]

def dibujar_fantasmas():
    for fantasma in fantasmas:
        imagen = imagenes_fantasmas[fantasma[2]]
        pos_x = fantasma[0] * TAM_CELDA
        pos_y = fantasma[1] * TAM_CELDA
        pantalla.blit(imagen, (pos_x, pos_y))

def mover_pacman():
    global posicion_pacman, direccion_actual
    teclas = pygame.key.get_pressed()
    nuevo_x, nuevo_y = posicion_pacman[:]

    # Inicializar variables de movimiento
    movimiento_horizontales = 0
    movimiento_verticales = 0

    # Comprobar el movimiento horizontal
    if teclas[pygame.K_a]:  # Izquierda
        movimiento_horizontales = -1
        direccion_actual = "izquierda"
    elif teclas[pygame.K_d]:  # Derecha
        movimiento_horizontales = 1
        direccion_actual = "derecha"

    # Comprobar el movimiento vertical
    if teclas[pygame.K_w]:  # Arriba
        movimiento_verticales = -1
        direccion_actual = "arriba"
    elif teclas[pygame.K_s]:  # Abajo
        movimiento_verticales = 1
        direccion_actual = "abajo"

    # Permitir movimiento solo si hay un solo movimiento (horizontal o vertical)
    if movimiento_horizontales != 0 and movimiento_verticales == 0:
        nuevo_x += movimiento_horizontales
    elif movimiento_verticales != 0 and movimiento_horizontales == 0:
        nuevo_y += movimiento_verticales

    # Verificar si la nueva posición está dentro del laberinto
    if 0 <= nuevo_x < ancho_laberinto and 0 <= nuevo_y < alto_laberinto:
        # Permitir moverse a celdas '0' y '2', además de recoger comida
        if laberinto[nuevo_y][nuevo_x] in ('0', '2') or (nuevo_x, nuevo_y) in posiciones_comida:
            posicion_pacman[0] = nuevo_x
            posicion_pacman[1] = nuevo_y

def verificar_colisiones():
    global vidas
    pacman_rect = pygame.Rect(posicion_pacman[0] * TAM_CELDA, posicion_pacman[1] * TAM_CELDA, TAM_CELDA, TAM_CELDA)
    
    for fantasma in fantasmas:
        fantasma_rect = pygame.Rect(fantasma[0] * TAM_CELDA, fantasma[1] * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        if pacman_rect.colliderect(fantasma_rect):
            vidas -= 1
            return True
    return False

def mostrar_info_juego():
    tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000
    fuente = crear_fuente(24)
    pantalla.blit(fuente.render(f'Puntuación: {puntuacion}', True, BLANCO), (10, 10))
    pantalla.blit(fuente.render(f'Tiempo: {tiempo_transcurrido} s', True, BLANCO), (ANCHO_PANTALLA // 2 - 100, 10))
    pantalla.blit(fuente.render(f'Vidas: {vidas}', True, BLANCO), (ANCHO_PANTALLA - 100, 10))

# Probabilidad inicial de persecución
probabilidad_perseguir = 0.2  # Puedes ajustar este valor para que sea más o menos probable al principio

def movimiento_fantasmas():
    global probabilidad_perseguir
    for i, fantasma in enumerate(fantasmas):
        # Calcular distancia a Pac-Man
        dx = posicion_pacman[0] - fantasma[0]
        dy = posicion_pacman[1] - fantasma[1]
        
        # Calcular la dirección hacia Pac-Man
        direccion = None
        if random.random() < probabilidad_perseguir:
            if abs(dx) > abs(dy):
                direccion = 'derecha' if dx > 0 else 'izquierda'
            else:
                direccion = 'abajo' if dy > 0 else 'arriba'

            # Intentar bloquear el camino de Pac-Man
            if abs(dx) < 2 or abs(dy) < 2:
                if random.random() < 0.5:  # 50% de probabilidad de intentar bloquear
                    # Intentar mover en dirección perpendicular
                    if direccion in ['derecha', 'izquierda']:
                        direccion = 'arriba' if dy > 0 else 'abajo'
                    else:
                        direccion = 'izquierda' if dx > 0 else 'derecha'
        
        if direccion is None:  # Movimiento aleatorio si no está persiguiendo
            direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])

        # Calcular nueva posición según la dirección elegida
        nueva_posicion = list(fantasma[:2])  # Copiar la posición actual del fantasma
        if direccion == 'arriba':
            nueva_posicion[1] -= 1
        elif direccion == 'abajo':
            nueva_posicion[1] += 1
        elif direccion == 'izquierda':
            nueva_posicion[0] -= 1
        elif direccion == 'derecha':
            nueva_posicion[0] += 1

        # Verificar si la nueva posición está dentro de los límites y en una casilla permitida
        if (0 <= nueva_posicion[0] < len(laberinto[0]) and
            0 <= nueva_posicion[1] < len(laberinto) and
            (laberinto[nueva_posicion[1]][nueva_posicion[0]] in '02')):  # Permitir solo '0' y '2'
            
            # Verificar que no haya otro fantasma en la nueva posición
            if not any(otro_fantasma[:2] == nueva_posicion for otro_fantasma in fantasmas if otro_fantasma != fantasma):
                # Actualizar la posición del fantasma
                fantasma[0], fantasma[1] = nueva_posicion

    # Incrementar la probabilidad de persecución gradualmente
    if probabilidad_perseguir < 1.0:
        probabilidad_perseguir += 0.01  # Ajusta este valor para que incremente más o menos rápido

# Variables para el control del tiempo y otras funciones
tiempo_fantasmas = 0
intervalo_movimiento_fantasmas = 300  # milisegundos (ajusta este valor para cambiar la velocidad)

def main():
    global puntuacion, posicion_pacman, tiempo_fantasmas

    while True:
        mostrar_menu_principal()
        desvanecer(aumento=False)
        while True:
            manejar_input_menu()
            mostrar_menu_principal()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if seleccion == 0:
                            pygame.mixer.music.pause()
                            reiniciar_juego()
                            juego_en_curso = True
                            while juego_en_curso:
                                for evento in pygame.event.get():
                                    if evento.type == pygame.QUIT:
                                        pygame.mixer.music.stop()
                                        pygame.quit()
                                        return

                                mover_pacman()
                                
                                tiempo_actual = pygame.time.get_ticks()
                                if tiempo_actual - tiempo_fantasmas >= intervalo_movimiento_fantasmas:
                                    movimiento_fantasmas()
                                    tiempo_fantasmas = tiempo_actual

                                if verificar_colisiones():
                                    if vidas > 0:
                                        posicion_pacman = posicion_pacman_inicial[:]
                                    if vidas <= 0:
                                        guardar_record(puntuacion)
                                        pygame.mixer.music.pause()
                                        if mostrar_game_over():
                                            reiniciar_juego()
                                        else:
                                            juego_en_curso = False
                                            pygame.mixer.music.load("Assets/Fondo_Música/musica_fondo1.mp3")
                                            pygame.mixer.music.set_volume(0.2)
                                            pygame.mixer.music.play(-1)

                                pantalla.fill(NEGRO)
                                dibujar_laberinto()
                                dibujar_pacman()
                                dibujar_comida()
                                dibujar_fantasmas()
                                mostrar_info_juego()

                                if (posicion_pacman[0], posicion_pacman[1]) in posiciones_comida:
                                    posiciones_comida.remove((posicion_pacman[0], posicion_pacman[1]))
                                    puntuacion += 10

                                pygame.display.update()
                                reloj.tick(10)

                        elif seleccion == 1:
                            mostrar_records()
                        elif seleccion == 2:
                            mostrar_ajustes()
                        elif seleccion == 3:
                            pygame.mixer.music.stop()
                            pygame.quit()
                            return
        desvanecer(aumento=True)

if __name__ == "__main__":
    main()