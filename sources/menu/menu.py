import pygame
import sys
from pages.Static_Balance import main 

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1350, 840
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Menú de Física")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AQUA = (0, 255, 204)
GRAY = (169, 169, 169)

# Fuentes
font = pygame.font.SysFont("Helvetica", 32, bold=True)
button_font = pygame.font.SysFont("Helvetica", 24, bold=True)

# Variables para las opciones
brightness = 100  # Nivel de brillo de la pantalla (0-100)
sound_volume = 50  # Volumen del sonido (0-100)
fullscreen = False  # Estado de pantalla completa

# Cargar la imagen de fondo
background_image = pygame.image.load("C:/Users/carli/Documents/Proyectos/SimuladorCuerposEquilibrio/sources/img/log.png")  # Cambia por la ruta de tu imagen
background_image = pygame.transform.scale(background_image, (1300,750))  # Escala la imagen al tamaño de la ventana

# Cargar música
pygame.mixer.music.load("C:/Users/carli/Documents/Proyectos/SimuladorCuerposEquilibrio/sources/music/logr.mp3")  # Cambia por la ruta de tu archivo de música
pygame.mixer.music.set_volume(sound_volume / 100)
pygame.mixer.music.play(-1)  # Reproducir en bucle (-1)

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Función de los botones
def button(x, y, width, height, color, text, font, text_color, action=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(screen, AQUA, (x, y, width, height))  # Hover effect
        if click[0] == 1 and action:
            action()
            pygame.time.wait(300)  # Espera un poco para que la acción no se ejecute demasiado rápido
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    
    draw_text(text, font, text_color, screen, x + width // 2, y + height // 2)

# Función para iniciar el simulador de equilibrio
def game_start():
    screen.fill(BLACK)  # Limpia la pantalla antes de cambiar a la nueva ventana
    pygame.display.update()  # Actualiza la pantalla antes de cambiar a la otra ventana
    main()  # Llama a la función del simulador

# Función para ajustar el brillo
def adjust_brightness():
    global brightness
    brightness = (brightness + 10) % 110  # Incrementa en 10 el brillo, pero no puede superar 100
    if brightness == 0:
        brightness = 10
    pygame.display.set_gamma(brightness / 100)

# Función para ajustar el sonido
def adjust_sound():
    global sound_volume
    sound_volume = (sound_volume + 10) % 110
    if sound_volume == 0:
        sound_volume = 10
    pygame.mixer.music.set_volume(sound_volume / 100)

# Función para alternar pantalla completa
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((WIDTH, HEIGHT))

# Función para regresar al menú principal
def return_to_menu():
    main_menu()  # Llama a la función principal del menú

# Función para salir del juego
def salir():
    pygame.quit()  # Cierra Pygame
    sys.exit()  # Termina la ejecución del programa

# Función para mostrar las opciones
def show_options():
    running = True
    while running:
        screen.blit(background_image, (10, 25))  # Dibujar la imagen de fondo
        
        # Título
        draw_text("Opciones", font, AQUA, screen, WIDTH // 2, 100)
        
        # Botones centrados
        button_x = (WIDTH - 400) // 2
        button_height_start = 250
        button_spacing = 100
        button_width = 400
        button_height = 50
        
        draw_text(f"Brillo: {brightness}", button_font, WHITE, screen, WIDTH // 2, button_height_start + 5550)
        button(button_x, button_height_start, button_width, button_height, GRAY, "Ajustar Brillo", button_font, WHITE, adjust_brightness)
        
        draw_text(f"Volumen: {sound_volume}", button_font, WHITE, screen, WIDTH // 2, button_height_start + button_spacing + 1110)
        button(button_x, button_height_start + button_spacing, button_width, button_height, GRAY, "Ajustar Volumen", button_font, WHITE, adjust_sound)
        
        button(button_x, button_height_start + 2 * button_spacing, button_width, button_height, GRAY, "Pantalla Completa", button_font, WHITE, toggle_fullscreen)
        button(button_x, button_height_start + 3 * button_spacing, button_width, button_height, GRAY, "Regresar", button_font, WHITE, return_to_menu)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

# Función principal del menú
def main_menu():
    running = True
    while running:
        screen.blit(background_image, (10, 25))  # Dibujar la imagen de fondo
        
        # Título
        draw_text("Physics Simulator", font, AQUA, screen, WIDTH // 2, 100)
        
        # Botones centrados
        button_x = (WIDTH - 400) // 2
        button_spacing = 100
        button(button_x, 300, 400, 50, GRAY, "Cuerpos en Equilibrio", button_font, WHITE, game_start)
        button(button_x, 400, 400, 50, GRAY, "Opciones", button_font, WHITE, show_options)
        button(button_x, 500, 400, 50, GRAY, "Salir", button_font, WHITE, salir)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()