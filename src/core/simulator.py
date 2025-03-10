import pygame
import subprocess
from config.constant import *
from core.physic import calculate_tensions, solution, calculate_body_position
from interfaces.graphicInterface import GraphicsManager
from interfaces.uiInterface import UI

class PhysicsSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Simulador de Cuerpos en Equilibrio")
        
        self.graphics = GraphicsManager()
        self.ui = UI(self.graphics)
        self.clock = pygame.time.Clock()
        
        # Simulation state
        self.weight = INITIAL_WEIGHT
        self.theta1 = INITIAL_THETA1
        self.theta2 = INITIAL_THETA2
        
        # Drag state
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.start_weight = INITIAL_WEIGHT
        
        # Change flags
        self.peso_cambiado = False
        self.theta1_cambiado = False
        self.theta2_cambiado = False

    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            self._handle_mouse_events(event)
            self._handle_keyboard_events(event)
            
        return True

    def _handle_mouse_events(self, event):
        """Handle mouse-related events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._handle_mouse_drag(event)

    def _handle_mouse_down(self, event):
        """Handle mouse button down events."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Converter button
        if pygame.Rect(40, HEIGHT - 22, 180, 40).collidepoint(mouse_pos):
            self.ui.conversor_visible = not self.ui.conversor_visible
        
        # Graph button
        elif pygame.Rect(240, HEIGHT - 22, 180, 40).collidepoint(mouse_pos):
            self._toggle_graph()
        
        
        # Convert button in converter
        elif self.ui.conversor_visible:
            convert_button = pygame.Rect(65, 680, 300, 40)
            input_field = pygame.Rect(65, 630, 300, 45)
            
            if convert_button.collidepoint(mouse_pos):
                try:
                    value = float(self.ui.text)
                    self.ui.result_conversion = value * GRAVITY
                except ValueError:
                    print("Please enter a valid number")
            elif input_field.collidepoint(mouse_pos):
                self.ui.active = True
            else:
                self.ui.active = False
        
        # Handle weight dragging
        else:
            self.dragging = True
            self.drag_start_x, self.drag_start_y = mouse_pos
            self.start_weight = self.weight

    def _handle_mouse_drag(self, event):
        """Handle mouse drag events."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_y = mouse_y - self.drag_start_y
        
        # Update weight based on drag
        self.weight = max(0, self.start_weight + delta_y * 2)
        self.peso_cambiado = True

    def _handle_keyboard_events(self, event):
        """Handle keyboard events."""
        if event.type == pygame.KEYDOWN:
            if self.ui.active:
                if event.key == pygame.K_RETURN:
                    try:
                        value = float(self.ui.text)
                        self.ui.result_conversion = value * GRAVITY
                    except ValueError:
                        print("Please enter a valid number")
                elif event.key == pygame.K_BACKSPACE:
                    self.ui.text = self.ui.text[:-1]
                else:
                    # Only allow numbers and decimal point
                    if event.unicode.isnumeric() or event.unicode == '.':
                        self.ui.text += event.unicode
        
        # Handle angle adjustments
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.theta1 = max(0, self.theta1 - 1)
            self.theta1_cambiado = True
        if keys[pygame.K_RIGHT]:
            self.theta1 = min(90, self.theta1 + 1)
            self.theta1_cambiado = True
        if keys[pygame.K_UP]:
            self.theta2 = max(0, self.theta2 - 1)
            self.theta2_cambiado = True
        if keys[pygame.K_DOWN]:
            self.theta2 = min(90, self.theta2 + 1)
            self.theta2_cambiado = True

    def _toggle_graph(self):
        """Toggle the force diagram graph."""
        self.ui.mostrar_grafico = not self.ui.mostrar_grafico
        if self.ui.mostrar_grafico:
            T1, T2 = calculate_tensions(self.weight, self.theta1, self.theta2)
            self.ui.superficie_grafico = self.graphics.create_graph(
                self.weight, self.theta1, self.theta2, T1, T2)

    #def _return_to_menu(self):
        """Return to the main menu."""
        #subprocess.Popen(["python", "sources/menu.py"])
        #pygame.quit()

    def update(self):
        """Update simulation state."""
        if self.ui.mostrar_grafico and (self.peso_cambiado or self.theta1_cambiado or self.theta2_cambiado):
            T1, T2 = calculate_tensions(self.weight, self.theta1, self.theta2)
            self.ui.superficie_grafico = self.graphics.create_graph(
                self.weight, self.theta1, self.theta2, T1, T2)
            
            # Reset change flags
            self.peso_cambiado = False
            self.theta1_cambiado = False
            self.theta2_cambiado = False
            
        

    def render(self):
        """Render the current frame."""
        self.ui.draw_scene(self.screen, self.weight, self.theta1, self.theta2)
        pygame.display.flip()

    def run(self):
        """Main simulation loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(90)