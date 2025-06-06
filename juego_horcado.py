import pygame
import sys
import random

pygame.init()

# Pantalla
ANCHO, ALTO = 1000, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Ahorcado del Pirata")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 150, 0)
AZUL = (0, 100, 255)
CAFE = (139, 69, 19)
DORADO = (184, 134, 11)
GRIS = (169, 169, 169)
CELESTE = (173, 216, 230)
BEIGE = (245, 245, 220)
ARENA = (237, 201, 175)

# Fuente
fuente = pygame.font.SysFont("serif", 48)
fuente_pequena = pygame.font.SysFont("serif", 30)

# Palabras y pistas (ordenadas por dificultad)
palabras_pistas = [
    ("MAPA", "Papel viejo con caminos invisibles"),
    ("COFRE", "Esconde riquezas tras madera y cerradura"),
    ("BRUJULA", "Indica rumbos, pero no caminos"),
    ("TESORO", "Muchos lo quieren, pocos lo encuentran"),
    ("AMOR", "El tesoro más buscado, sin mapa ni llave")
]

indice = 0
palabra, pista = palabras_pistas[indice]
letras_adivinadas = []
errores = 0
MAX_ERRORES = 6
mostrar_historia_final = False
estado_juego = "menu"  # puede ser 'menu', 'controles', 'jugando'

def fondo_suave():
    # Fondo celeste pastel muy suave
    color_fondo = (230, 245, 255)  
    pantalla.fill(color_fondo)
    # Líneas horizontales muy tenues
    color_lineas = (200, 220, 240)  
    for i in range(0, ALTO, 50):
        pygame.draw.line(pantalla, color_lineas, (0, i), (ANCHO, i), 1)

def mostrar_menu():
    fondo_suave()
    titulo = fuente.render("El Ahorcado del Pirata", True, NEGRO)
    subtitulo = fuente_pequena.render("Presiona ENTER para jugar", True, AZUL)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 250))
    pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 320))
    pygame.display.flip()

def mostrar_controles():
    fondo_suave()
    instrucciones = [
        "¿Cómo jugar?",
        "Adivina la palabra letra por letra.",
        "Cada error dibuja parte del ahorcado.",
        "Pierdes al cometer 6 errores.",
        "",
        "Controles:",
        "1 - Volver al menú",
        "2 - Reiniciar nivel actual",
        "3 - Salir del juego"
    ]
    y = 150
    for linea in instrucciones:
        texto = fuente_pequena.render(linea, True, NEGRO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, y))
        y += 40
    pygame.display.flip()

def mostrar_palabra():
    display = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            display += letra + " "
        else:
            display += "_ "
    texto = fuente.render(display.strip(), True, NEGRO)
    pantalla.blit(texto, (30, 600))

def mostrar_pista():
    texto_pista = fuente_pequena.render("Pista: " + pista, True, (50, 50, 50))
    pantalla.blit(texto_pista, (30, 50))

def mostrar_nivel():
    nivel = f"Nivel {indice + 1}"
    texto_nivel = fuente_pequena.render(nivel, True, AZUL)
    pantalla.blit(texto_nivel, (ANCHO - texto_nivel.get_width() - 30, 50))

def mostrar_controles_pequenos():
    texto_controles = fuente_pequena.render("1-Menú   2-Reiniciar   3-Salir", True, (50, 50, 50))
    pantalla.blit(texto_controles, (ANCHO - texto_controles.get_width() - 30, ALTO - 100))

def dibujar_base():
    pygame.draw.line(pantalla, CAFE, (150, 600), (450, 600), 5)
    pygame.draw.line(pantalla, CAFE, (300, 600), (300, 150), 5)
    pygame.draw.line(pantalla, CAFE, (300, 150), (500, 150), 5)
    pygame.draw.line(pantalla, CAFE, (500, 150), (500, 200), 5)

def dibujar_ahorcado(errores):
    if errores > 0:
        pygame.draw.circle(pantalla, NEGRO, (500, 230), 30, 5)
    if errores > 1:
        pygame.draw.line(pantalla, NEGRO, (500, 260), (500, 370), 5)
    if errores > 2:
        pygame.draw.line(pantalla, NEGRO, (500, 280), (460, 320), 5)
    if errores > 3:
        pygame.draw.line(pantalla, NEGRO, (500, 280), (540, 320), 5)
    if errores > 4:
        pygame.draw.line(pantalla, NEGRO, (500, 370), (460, 430), 5)
    if errores > 5:
        pygame.draw.line(pantalla, NEGRO, (500, 370), (540, 430), 5)

def mostrar_mensaje(texto, color=ROJO):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, 80))

def mostrar_historia():
    fondo_suave()
    historia = [
        "El joven pirata navegó por los mares siguiendo pistas misteriosas.",
        "Cada objeto lo acercaba más a su verdadero destino...",
        "El tesoro no era oro, sino el amor perdido de su vida.",
        "Finalmente, tras resolver todas las claves, ¡la encontró!"
    ]
    y = 250
    for linea in historia:
        texto = fuente_pequena.render(linea, True, NEGRO)
        pantalla.blit(texto, (100, y))
        y += 50
    pygame.display.flip()
    esperar_historia = True
    while esperar_historia:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_1:
                    esperar_historia = False

def reiniciar():
    global palabra, pista, letras_adivinadas, errores, indice, mostrar_historia_final
    indice += 1
    if indice < len(palabras_pistas):
        palabra, pista = palabras_pistas[indice]
        letras_adivinadas = []
        errores = 0
    else:
        mostrar_historia_final = True

def reset_nivel():
    global letras_adivinadas, errores
    letras_adivinadas = []
    errores = 0

# Bucle principal
corriendo = True
while corriendo:
    if estado_juego == "menu":
        mostrar_menu()
    elif estado_juego == "controles":
        mostrar_controles()
    elif estado_juego == "jugando":
        fondo_suave()
        dibujar_base()
        dibujar_ahorcado(errores)
        mostrar_palabra()
        mostrar_pista()
        mostrar_nivel()
        mostrar_controles_pequenos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if estado_juego == "menu":
                if evento.key == pygame.K_RETURN:
                    estado_juego = "controles"
            elif estado_juego == "controles":
                estado_juego = "jugando"
            elif estado_juego == "jugando":
                if evento.key == pygame.K_3:
                    corriendo = False
                elif evento.key == pygame.K_2:
                    reset_nivel()
                elif evento.key == pygame.K_1:
                    estado_juego = "menu"
                else:
                    letra = evento.unicode.upper()
                    if letra.isalpha() and letra not in letras_adivinadas and len(letra) == 1:
                        letras_adivinadas.append(letra)
                        if letra not in palabra:
                            errores += 1

    if estado_juego == "jugando":
        if errores >= MAX_ERRORES:
            mostrar_mensaje("¡Perdiste! Era: " + palabra)
            pygame.display.flip()
            pygame.time.wait(2000)
            estado_juego = "menu"
            indice = 0
            palabra, pista = palabras_pistas[indice]
            letras_adivinadas = []
            errores = 0
        elif all(letra in letras_adivinadas for letra in palabra):
            mostrar_mensaje("¡Correcto!", VERDE)
            pygame.display.flip()
            pygame.time.wait(2000)
            reiniciar()

    if mostrar_historia_final:
        mostrar_historia()
        mostrar_historia_final = False
        indice = 0
        palabra, pista = palabras_pistas[indice]
        letras_adivinadas = []
        errores = 0
        estado_juego = "menu"

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()