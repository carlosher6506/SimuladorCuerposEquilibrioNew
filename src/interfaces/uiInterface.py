import pygame
import requests
from config.constant import *
from core.physic import calculate_tensions, solution, calculate_body_position, conversor

class UI:
    def __init__(self, graphics_manager):
        self.graphics = graphics_manager
        self.conversor_visible = False
        self.mostrar_grafico = False
        self.historial_visible = False
        self.superficie_grafico = None
        self.superficie_historial = None
        self.active = False
        self.text = '50'
        self.result_conversion = 0
        self.scroll_y = 0  # Para el scroll del historial
        self.last_simulation = {
            'weight': 0,
            'theta1': 0,
            'theta2': 0,
            'tension1': 0,
            'tension2': 0
        }
        self.button_cooldown = 0  # Evitar múltiples clics
        
    def save_simulation(self):
        """Envía los datos de la simulación al backend para guardarlos."""
        url = "http://localhost:5000/api/simulations"
        try:
            response = requests.post(url, json=self.last_simulation)
            if response.status_code == 201:
                print("Simulación guardada exitosamente!")
            else:
                print("Error guardando la simulación:", response.text)
        except Exception as e:
            print("Error de conexión:", e)
            
    def load_simulation(self, simulation_id):
        """Carga una simulación guardada desde el backend."""
        url = f"http://localhost:5000/api/simulations/{simulation_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error cargando la simulación:", response.text)
        except Exception as e:
            print("Error de conexión:", e)
        return None

    def draw_scene(self, screen, weight, theta1, theta2):
        """Draw the complete simulation scene."""
        screen.fill(WHITE)
        mass = weight / GRAVITY
        
        anchor1_x = WIDTH // 4
        anchor2_x = 3 * WIDTH // 4
        anchor_y = HEIGHT // 4
        
        # Calcular tensiones y actualizar last_simulation
        T1, T2 = calculate_tensions(weight, theta1, theta2)
        T11, T22 = solution(weight, theta1, theta2)
        
        # Actualizar valores de la última simulación con valores enteros
        self.last_simulation = {
            'weight': int(weight),
            'theta1': int(theta1),
            'theta2': int(theta2),
            'tension1': T11,
            'tension2': T22
        }
        
        body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2)
        
        # Draw all visual elements using graphics manager
        self.graphics.draw_scene(screen, body_x, body_y, anchor1_x, anchor2_x, anchor_y, theta1, theta2)
        
        # Draw measurements and text
        self._draw_measurements(screen, body_x, body_y, T11, T22, theta1, theta2, weight, mass)
        
        # Draw UI elements
        self._draw_ui_elements(screen, weight, theta1, theta2)
        
        # Draw converter if visible
        if self.conversor_visible:
            self._draw_converter(screen)
            
        # Draw graph if visible
        if self.mostrar_grafico and self.superficie_grafico:
            self._draw_graph(screen)
            
        # Dibujar el historial si está visible
        if self.historial_visible:
            self._draw_historial(screen)
            
        # Reducir el cooldown de botones si está activo
        if self.button_cooldown > 0:
            self.button_cooldown -= 1

    def _draw_measurements(self, screen, body_x, body_y, T11, T22, theta1, theta2, weight, mass):
        """Draw all measurement text."""
        text_T1 = self.graphics.font.render(f"T1: {T11:.2f} N", True, BLACK)
        text_T2 = self.graphics.font.render(f"T2: {T22:.2f} N", True, BLACK)
        text_theta1 = self.graphics.font.render(f"θ1: {int(theta1)}°", True, BLACK)
        text_theta2 = self.graphics.font.render(f"θ2: {int(theta2)}°", True, BLACK)
        text_weight = self.graphics.font.render(f"P = {int(weight)} N", True, BLACK)
        text_mass = self.graphics.font.render(f"W = {mass:.2f} kg", True, BLACK)
        
        screen.blit(text_T1, (body_x - 150, body_y - 30))
        screen.blit(text_T2, (body_x + 50, body_y - 30))
        screen.blit(text_theta1, (body_x - 150, body_y - 60))
        screen.blit(text_theta2, (body_x + 50, body_y - 60))
        screen.blit(text_weight, (body_x - 30, body_y + 30))
        screen.blit(text_mass, (body_x - 30, body_y + 50))

    def _draw_ui_elements(self, screen, weight, theta1, theta2):
        """Draw UI buttons and elements."""
        # Draw header and footer bars
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 45))
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 45, WIDTH, 45))
        
        # Draw current values in header with integer values
        weight_text = self.graphics.font.render(f"Weight: {int(weight)}N", True, WHITE)
        theta1_text = self.graphics.font.render(f"θ1: {int(theta1)}°", True, WHITE)
        theta2_text = self.graphics.font.render(f"θ2: {int(theta2)}°", True, WHITE)
        tension1_text = self.graphics.font.render(f"T1: {self.last_simulation['tension1']:.1f}N", True, WHITE)
        tension2_text = self.graphics.font.render(f"T2: {self.last_simulation['tension2']:.1f}N", True, WHITE)
        
        screen.blit(weight_text, (10, 10))
        screen.blit(theta1_text, (200, 10))
        screen.blit(theta2_text, (350, 10))
        screen.blit(tension1_text, (500, 10))
        screen.blit(tension2_text, (650, 10))
        
        # Draw buttons with proper spacing
        button_width = 150
        button_height = 35
        button_margin = 20
        start_x = (WIDTH - (4 * button_width + 3 * button_margin)) // 2
        button_y = HEIGHT - 40
        
        buttons = [
            ("Conversor", start_x),
            ("Graficar", start_x + button_width + button_margin),
            ("Historial", start_x + 2 * (button_width + button_margin)),
            ("Guardar", start_x + 3 * (button_width + button_margin))
        ]
        
        # Obtener estado del mouse una sola vez
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and self.button_cooldown == 0
        
        for text, x in buttons:
            button_rect = pygame.Rect(x, button_y, button_width, button_height)
            
            # Cambiar color si el mouse está sobre el botón
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (0, 50, 100), button_rect)  # Color más oscuro al pasar el mouse
                
                # Manejar clics solo si no hay cooldown
                if mouse_clicked:
                    self.button_cooldown = 10  # Establecer cooldown para evitar múltiples clics
                    
                    if text == "Guardar":
                        self.save_simulation()
                    elif text == "Historial":
                        self.historial_visible = not self.historial_visible
                    elif text == "Conversor":
                        self.conversor_visible = not self.conversor_visible
                    elif text == "Graficar":
                        if self.superficie_grafico is not None:
                            self.mostrar_grafico = not self.mostrar_grafico
                        else:
                            # Crear gráfico si no existe
                            self.superficie_grafico = self.graphics.create_graph(
                                int(weight), int(theta1), int(theta2), 
                                self.last_simulation['tension1'], 
                                self.last_simulation['tension2']
                            )
                            self.mostrar_grafico = True
            else:
                pygame.draw.rect(screen, BLUE, button_rect)
                
            pygame.draw.rect(screen, WHITE, button_rect, 1)  # Borde blanco
            
            # Centrar el texto en el botón
            text_surface = self.graphics.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

    def _draw_converter(self, screen):
        """Draw the converter interface."""
        pygame.draw.rect(screen, BLUE, (0, 580, 440, 235))
        pygame.draw.rect(screen, WHITE, (7, 590, 422, 215))
        
        title = self.graphics.font_large.render('Conversor de Kg a N', True, BLACK)
        result = self.graphics.font_large.render(f"{self.result_conversion:.2f} N", True, BLACK)
        
        screen.blit(title, (70, 600))
        screen.blit(result, (145, 730))
        
        # Draw convert button
        convert_button = pygame.Rect(65, 680, 300, 40)
        pygame.draw.rect(screen, BLACK, convert_button)
        convert_text = self.graphics.font_large.render('Convertir', True, WHITE)
        screen.blit(convert_text, (155, 685))
        
        # Draw input field
        input_rect = pygame.Rect(65, 630, 300, 45)
        color = (30, 144, 255) if self.active else BLACK  # dodgerblue2
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = self.graphics.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        # Manejar eventos del conversor
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and self.button_cooldown == 0
        
        # Manejar clic en el botón de convertir
        if convert_button.collidepoint(mouse_pos) and mouse_clicked:
            self.button_cooldown = 10
            try:
                kg = float(self.text)
                self.result_conversion = conversor(kg)
            except ValueError:
                self.result_conversion = 0
                
        # Manejar clic en el campo de entrada
        if input_rect.collidepoint(mouse_pos) and mouse_clicked:
            self.active = not self.active
            self.button_cooldown = 10
            
        # Manejar entrada de texto si el campo está activo
        if self.active:
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        kg = float(self.text)
                        self.result_conversion = conversor(kg)
                    except ValueError:
                        self.result_conversion = 0
                    self.active = False
                elif event.unicode.isdigit() or event.unicode == '.':
                    self.text += event.unicode

    def _draw_graph(self, screen):
        """Draw the force diagram graph."""
        if self.superficie_grafico is None:
            return
            
        grafico_x = WIDTH - self.superficie_grafico.get_width() - 10
        grafico_y = HEIGHT - self.superficie_grafico.get_height() - 70
        
        fondo_grafico = pygame.Surface((self.superficie_grafico.get_width() + 20, 
                                      self.superficie_grafico.get_height() + 20))
        fondo_grafico.fill(WHITE)
        screen.blit(fondo_grafico, (grafico_x - 10, grafico_y - 10))
        
        pygame.draw.rect(screen, BLACK, (grafico_x - 10, grafico_y - 10, 
                     self.superficie_grafico.get_width() + 20, 
                     self.superficie_grafico.get_height() + 20), 2)
        
        screen.blit(self.superficie_grafico, (grafico_x, grafico_y))
        
        # Botón para cerrar el gráfico
        close_button = pygame.Rect(grafico_x + self.superficie_grafico.get_width() - 20, grafico_y - 5, 20, 20)
        pygame.draw.rect(screen, BLUE, close_button)
        close_text = self.graphics.font.render("X", True, WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_rect)
        
        # Manejar clic en el botón de cerrar
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and self.button_cooldown == 0
        
        if close_button.collidepoint(mouse_pos) and mouse_clicked:
            self.mostrar_grafico = False
            self.button_cooldown = 10
        
    def _draw_historial(self, screen):
        """Dibuja la ventana de historial."""
        if not self.historial_visible:
            return

        # Dimensiones y posición de la ventana de historial
        padding = 20
        historial_width = 600
        historial_height = 400
        x = (WIDTH - historial_width) // 2
        y = (HEIGHT - historial_height) // 2

        # Crear superficie para el historial con fondo semitransparente
        background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(background, (0, 0, 0, 128), (0, 0, WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Dibujar ventana principal del historial
        pygame.draw.rect(screen, WHITE, (x, y, historial_width, historial_height))
        pygame.draw.rect(screen, BLUE, (x, y, historial_width, historial_height), 2)

        # Título
        title = self.graphics.font_large.render("Historial de Simulaciones", True, BLUE)
        title_rect = title.get_rect(centerx=x + historial_width//2, top=y + padding)
        screen.blit(title, title_rect)

        # Área de contenido
        content_rect = pygame.Rect(x + padding, y + title_rect.height + padding*2,
                                 historial_width - padding*2, historial_height - title_rect.height - padding*3)
        pygame.draw.rect(screen, (240, 240, 240), content_rect)

        # Obtener y mostrar simulaciones
        historial = self.obtener_historial()
        line_height = 30
        visible_lines = (content_rect.height) // line_height
        
        # Dibujar simulaciones
        for i, sim in enumerate(historial):
            y_pos = content_rect.top + i * line_height - self.scroll_y
            
            # Solo dibujar las líneas visibles
            if content_rect.top <= y_pos <= content_rect.bottom:
                if i % 2 == 0:
                    pygame.draw.rect(screen, (230, 230, 230),
                                  (content_rect.left, y_pos, content_rect.width, line_height))
                
                text = f"#{i+1}: P={sim['weight']}N, θ1={sim['theta1']}°, θ2={sim['theta2']}°"
                text2 = f"T1={sim['tension1']:.1f}N, T2={sim['tension2']:.1f}N"
                
                text_surface = self.graphics.font.render(text, True, BLACK)
                text_surface2 = self.graphics.font.render(text2, True, BLACK)
                
                screen.blit(text_surface, (content_rect.left + 5, y_pos + 5))
                screen.blit(text_surface2, (content_rect.left + 5, y_pos + line_height//2))

        # Botón de cerrar
        close_button = pygame.Rect(x + historial_width - 40, y + 10, 30, 30)
        pygame.draw.rect(screen, BLUE, close_button)
        close_text = self.graphics.font.render("X", True, WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_rect)

        # Manejar clic en botón de cerrar
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and self.button_cooldown == 0
        
        if close_button.collidepoint(mouse_pos) and mouse_clicked:
            self.historial_visible = False
            self.button_cooldown = 10

        # Manejar scroll
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            if content_rect.collidepoint(mouse_pos):
                self.scroll_y = max(0, min(self.scroll_y - event.y * 20,
                                         max(0, len(historial) * line_height - content_rect.height)))

    def obtener_historial(self):
        """Obtiene el historial de simulaciones desde el backend."""
        url = "http://localhost:5000/api/simulations"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error obteniendo el historial:", response.text)
        except Exception as e:
            print("Error de conexión:", e)
        return []