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
        self.scroll_y = 0
        self.last_simulation = {
            'weight': 0,
            'theta1': 0,
            'theta2': 0,
            'tension1': 0,
            'tension2': 0
        }
        # Sistema de control de clics
        self.last_click_time = 0
        self.CLICK_COOLDOWN = 300  # 300ms entre clics
        self.last_clicked_button = None
        self.mouse_pressed = False
        self.has_loaded_simulation = False
        self.loaded_weight = 0
        self.loaded_theta1 = 0
        self.loaded_theta2 = 0
        self.selected_simulation = None
        
    def handle_click(self, button_id):
        """Sistema mejorado de control de clics"""
        current_time = pygame.time.get_ticks()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Si el mouse está presionado pero no estaba presionado antes
        if mouse_pressed and not self.mouse_pressed:
            if current_time - self.last_click_time > self.CLICK_COOLDOWN:
                self.last_click_time = current_time
                self.last_clicked_button = button_id
                self.mouse_pressed = True
                return True
        # Si el mouse no está presionado, resetear el estado
        elif not mouse_pressed:
            self.mouse_pressed = False
            
        return False

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
        
        if hasattr(self, 'has_loaded_simulation') and self.has_loaded_simulation:
            weight = self.loaded_weight
            theta1 = self.loaded_theta1
            theta2 = self.loaded_theta2
            self.has_loaded_simulation = True # Reiniciar flag después de aplicar
        
        screen.fill(WHITE)
        mass = weight / GRAVITY
        
        anchor1_x = WIDTH // 4
        anchor2_x = 3 * WIDTH // 4
        anchor_y = HEIGHT // 4
        
        T1, T2 = calculate_tensions(weight, theta1, theta2)
        T11, T22 = solution(weight, theta1, theta2)
        
        self.last_simulation = {
            'weight': int(weight),
            'theta1': int(theta1),
            'theta2': int(theta2),
            'tension1': T11,
            'tension2': T22
        }
        
        body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2)
        
        self.graphics.draw_scene(screen, body_x, body_y, anchor1_x, anchor2_x, anchor_y, theta1, theta2)
        self._draw_measurements(screen, body_x, body_y, T11, T22, theta1, theta2, weight, mass)
        self._draw_ui_elements(screen, weight, theta1, theta2)
        
        if self.conversor_visible:
            self._draw_converter(screen)
            
        if self.mostrar_grafico and self.superficie_grafico:
            self._draw_graph(screen)
            
        if self.historial_visible:
            self._draw_historial(screen)
    
    
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
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 45))
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 45, WIDTH, 45))
        
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
        
        button_width = 150
        button_height = 35
        button_margin = 20
        start_x = (WIDTH - (4 * button_width + 3 * button_margin)) // 2
        button_y = HEIGHT - 40
        
        buttons = [
            ("Conversor", start_x, "conversor"),
            ("Graficar", start_x + button_width + button_margin, "graficar"),
            ("Historial", start_x + 2 * (button_width + button_margin), "historial"),
            ("Guardar", start_x + 3 * (button_width + button_margin), "guardar")
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for text, x, button_id in buttons:
            button_rect = pygame.Rect(x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (0, 50, 100), button_rect)
                
                if self.handle_click(button_id):
                    if text == "Guardar":
                        self.save_simulation()
                    elif text == "Historial":
                        self.historial_visible = not self.historial_visible
                    elif text == "Conversor":
                        self.conversor_visible = not self.conversor_visible
                    elif text == "Graficar":
                        if self.superficie_grafico is None:
                            self.superficie_grafico = self.graphics.create_graph(
                                int(weight), int(theta1), int(theta2),
                                self.last_simulation['tension1'],
                                self.last_simulation['tension2']
                            )
                        self.mostrar_grafico = not self.mostrar_grafico
            else:
                pygame.draw.rect(screen, BLUE, button_rect)
                
            pygame.draw.rect(screen, WHITE, button_rect, 1)
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
        
        convert_button = pygame.Rect(65, 680, 300, 40)
        pygame.draw.rect(screen, BLACK, convert_button)
        convert_text = self.graphics.font_large.render('Convertir', True, WHITE)
        screen.blit(convert_text, (155, 685))
        
        input_rect = pygame.Rect(65, 630, 300, 45)
        color = (30, 144, 255) if self.active else BLACK
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = self.graphics.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        mouse_pos = pygame.mouse.get_pos()
        
        if convert_button.collidepoint(mouse_pos):
            if self.handle_click("convert"):
                try:
                    kg = float(self.text)
                    self.result_conversion = conversor(kg)
                except ValueError:
                    self.result_conversion = 0
                
        if input_rect.collidepoint(mouse_pos):
            if self.handle_click("input"):
                self.active = not self.active
            
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
        
        close_button = pygame.Rect(grafico_x + self.superficie_grafico.get_width() - 20, grafico_y - 5, 20, 20)
        pygame.draw.rect(screen, BLUE, close_button)
        close_text = self.graphics.font.render("X", True, WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if close_button.collidepoint(mouse_pos):
            if self.handle_click("close_graph"):
                self.mostrar_grafico = False
        
    def _draw_historial(self, screen):
        """Dibuja la ventana de historial con mejor organización y función de cargar."""
        if not self.historial_visible:
            return

        padding = 20
        historial_width = 600
        historial_height = 450  # Aumentado para dar más espacio
        x = (WIDTH - historial_width) // 2
        y = (HEIGHT - historial_height) // 2
        
        # Fondo semitransparente
        background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(background, (0, 0, 0, 128), (0, 0, WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Ventana principal
        pygame.draw.rect(screen, WHITE, (x, y, historial_width, historial_height))
        pygame.draw.rect(screen, BLUE, (x, y, historial_width, historial_height), 2)

        # Título
        title = self.graphics.font_large.render("Historial de Simulaciones", True, BLUE)
        title_rect = title.get_rect(centerx=x + historial_width//2, top=y + padding)
        screen.blit(title, title_rect)

        # Área de contenido
        content_rect = pygame.Rect(
            x + padding, 
            y + title_rect.height + padding*2,
            historial_width - padding*2, 
            historial_height - title_rect.height - padding*4 - 40  # Espacio para botón cargar
        )
        pygame.draw.rect(screen, (240, 240, 240), content_rect)

        # Encabezados de columnas
        header_y = content_rect.top + 5
        col_widths = [45, 100, 80, 80, 140, 135]  # Ancho de cada columna
        header_texts = ["#", "Peso", "Ángulo 1", "Ángulo 2", "Tensión 1", "Tensión 2"]
        header_x = content_rect.left + 5
        
        for i, text in enumerate(header_texts):
            header_surface = self.graphics.font.render(text, True, BLUE)
            screen.blit(header_surface, (header_x, header_y))
            header_x += col_widths[i]
        
        # Línea divisora debajo de los encabezados
        pygame.draw.line(screen, BLUE, 
                        (content_rect.left, header_y + 25), 
                        (content_rect.right, header_y + 25), 1)

        # Mostrar datos de simulaciones
        historial = self.obtener_historial()
        line_height = 35  # Altura de cada fila
        self.selected_simulation = getattr(self, 'selected_simulation', None)
        
        # Área visible para las filas (después de los encabezados)
        data_start_y = header_y + 30
        visible_height = content_rect.bottom - data_start_y
        
        # Calcular simulaciones visibles
        simulaciones_visibles = len(historial)
        max_scroll = max(0, (simulaciones_visibles * line_height) - visible_height)
        self.scroll_y = min(self.scroll_y, max_scroll)  # Prevenir scroll excesivo
        
        for i, sim in enumerate(historial):
            y_pos = data_start_y + i * line_height - self.scroll_y
            
            # Solo dibujar si está dentro del área visible
            if data_start_y <= y_pos < content_rect.bottom:
                # Alternar colores para filas
                row_color = (230, 230, 240) if i % 2 == 0 else (245, 245, 250)
                
                # Si esta fila está seleccionada, usar un color distinto
                if self.selected_simulation == i:
                    row_color = (200, 220, 255)
                    
                pygame.draw.rect(screen, row_color,
                            (content_rect.left, y_pos, content_rect.width, line_height))
                
                # Dibujar datos en columnas
                col_x = content_rect.left + 5
                
                # Número de simulación
                num_text = f"#{i+1}"
                num_surface = self.graphics.font.render(num_text, True, BLACK)
                screen.blit(num_surface, (col_x, y_pos + (line_height - num_surface.get_height())//2))
                col_x += col_widths[0]
                
                # Peso
                weight_text = f"P={sim['weight']}N"
                weight_surface = self.graphics.font.render(weight_text, True, BLACK)
                screen.blit(weight_surface, (col_x, y_pos + (line_height - weight_surface.get_height())//2))
                col_x += col_widths[1]
                
                # Ángulo 1
                theta1_text = f"θ1={sim['theta1']}°"
                theta1_surface = self.graphics.font.render(theta1_text, True, BLACK)
                screen.blit(theta1_surface, (col_x, y_pos + (line_height - theta1_surface.get_height())//2))
                col_x += col_widths[2]
                
                # Ángulo 2
                theta2_text = f"θ2={sim['theta2']}°"
                theta2_surface = self.graphics.font.render(theta2_text, True, BLACK)
                screen.blit(theta2_surface, (col_x, y_pos + (line_height - theta2_surface.get_height())//2))
                col_x += col_widths[3]
                
                # Tensión 1
                t1_text = f"T1={sim['tension1']:.1f}N"
                t1_surface = self.graphics.font.render(t1_text, True, BLACK)
                screen.blit(t1_surface, (col_x, y_pos + (line_height - t1_surface.get_height())//2))
                col_x += col_widths[4]
                
                # Tensión 2
                t2_text = f"T2={sim['tension2']:.1f}N"
                t2_surface = self.graphics.font.render(t2_text, True, BLACK)
                screen.blit(t2_surface, (col_x, y_pos + (line_height - t2_surface.get_height())//2))
                
                # Línea divisora entre filas
                pygame.draw.line(screen, (200, 200, 200), 
                                (content_rect.left, y_pos + line_height), 
                                (content_rect.right, y_pos + line_height), 1)
                
                # Detectar clic en la fila para selección
                mouse_pos = pygame.mouse.get_pos()
                row_rect = pygame.Rect(content_rect.left, y_pos, content_rect.width, line_height)
                if row_rect.collidepoint(mouse_pos) and self.handle_click(f"select_sim_{i}"):
                    self.selected_simulation = i

        # Botón de cargar
        cargar_button_rect = pygame.Rect(
            x + historial_width//2 - 75,
            y + historial_height - padding - 35,
            150,
            35
        )
        cargar_color = (0, 120, 0) if self.selected_simulation is not None else (150, 150, 150)
        pygame.draw.rect(screen, cargar_color, cargar_button_rect)
        pygame.draw.rect(screen, WHITE, cargar_button_rect, 1)
        
        cargar_text = self.graphics.font.render("Cargar Simulación", True, WHITE)
        cargar_text_rect = cargar_text.get_rect(center=cargar_button_rect.center)
        screen.blit(cargar_text, cargar_text_rect)
        
        # Botón de cerrar
        close_button = pygame.Rect(x + historial_width - 40, y + 10, 30, 30)
        pygame.draw.rect(screen, BLUE, close_button)
        close_text = self.graphics.font.render("X", True, WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_rect)

        # Barra de desplazamiento (si es necesaria)
        if simulaciones_visibles * line_height > visible_height:
            scrollbar_width = 10
            scrollbar_height = visible_height * (visible_height / (simulaciones_visibles * line_height))
            scrollbar_y = data_start_y + (self.scroll_y / max_scroll) * (visible_height - scrollbar_height)
            
            # Fondo de la barra
            pygame.draw.rect(screen, (200, 200, 200),
                        (content_rect.right - scrollbar_width - 3, data_start_y,
                            scrollbar_width, visible_height))
            
            # Barra de desplazamiento
            pygame.draw.rect(screen, BLUE,
                        (content_rect.right - scrollbar_width - 3, scrollbar_y,
                            scrollbar_width, scrollbar_height))

        # Manejo de eventos
        mouse_pos = pygame.mouse.get_pos()
        
        # Cerrar historial
        if close_button.collidepoint(mouse_pos):
            if self.handle_click("close_historial"):
                self.historial_visible = False
                
        # Cargar simulación seleccionada
        if cargar_button_rect.collidepoint(mouse_pos) and self.selected_simulation is not None:
            if self.handle_click("cargar_simulacion"):
                self.cargar_simulacion_seleccionada()

        # Manejo del scroll
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            if content_rect.collidepoint(mouse_pos):
                self.scroll_y = max(0, min(self.scroll_y - event.y * 20, max_scroll))

    def cargar_simulacion_seleccionada(self):
        """Carga la simulación seleccionada a la interfaz."""
        if self.selected_simulation is None:
            return
            
        historial = self.obtener_historial()
        if 0 <= self.selected_simulation < len(historial):
            sim = historial[self.selected_simulation]
            
            # Aquí devolvemos los valores para ser utilizados en la interfaz principal
            # Se pueden devolver como variables globales o como atributos de la clase
            # para que el programa principal los utilice
            self.loaded_weight = sim['weight']
            self.loaded_theta1 = sim['theta1']
            self.loaded_theta2 = sim['theta2']
            
            # Notificar que se ha cargado una simulación
            print(f"Simulación cargada: Peso={sim['weight']}N, θ1={sim['theta1']}°, θ2={sim['theta2']}°")
            
            # Opcional: cerrar el historial después de cargar
            self.historial_visible = False
            
            # Este flag indicará que hay valores cargados pendientes de aplicar
            self.has_loaded_simulation = True


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