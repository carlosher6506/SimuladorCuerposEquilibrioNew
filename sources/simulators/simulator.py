import pygame
import subprocess
from constants import *
from physics import calculate_tensions, solution, calculate_body_position
from graphics import GraphicsManager
from ui import UI
import math

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
        self.body_image_rect = self.graphics.peso_image.get_rect(center=(675, 270))
        
        # Change flags
        self.peso_cambiado = False
        self.theta1_cambiado = False
        self.theta2_cambiado = False

    def handle_events(self):
        """Handle all pygame events."""
        ui = UI(self.graphics)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            self._handle_mouse_events(event)
            self._handle_keyboard_events(event)
            ui.handle_event(event, weight, theta1, theta2)
            
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
        # Coordenadas de las cuerdas
        anchor1_x = WIDTH // 4
        anchor2_x = 3 * WIDTH // 4
        anchor_y = HEIGHT // 4
        
        if self.body_image_rect.collidepoint(event.pos):
            self.dragging = True
            self.drag_start_y = event.pos[1] - self.body_image_rect.centery

        # Verificar si se hace clic sobre las cuerdas
        if pygame.Rect(anchor1_x - 10, anchor_y - 200, 20, 400).collidepoint(event.pos):
            # Si se hace clic en la cuerda 1, anclamos la pesa en esta cuerda
            self.body_image_rect.center = (anchor1_x, self.body_image_rect.centery)
        elif pygame.Rect(anchor2_x - 10, anchor_y - 200, 20, 400).collidepoint(event.pos):
            # Si se hace clic en la cuerda 2, anclamos la pesa en esta cuerda
            self.body_image_rect.center = (anchor2_x, self.body_image_rect.centery)

        self.dragging = True
        self.drag_start_x, self.drag_start_y = pygame.mouse.get_pos()

    def _handle_mouse_drag(self, event):
        if self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Coordenadas de las cuerdas
                    anchor1_x = WIDTH // 4
                    anchor2_x = 3 * WIDTH // 4
                    anchor_y = HEIGHT // 4
                    
                    # Calculamos la nueva posición y limitamos el movimiento en el eje Y
                    new_y = mouse_y - self.drag_start_y
                    new_y = max(min(new_y, HEIGHT - 50), 50)

                    # Actualizar el peso en función de la distancia vertical
                    self.weight = max(50, min(1000, self.start_weight + (mouse_y - self.drag_start_y) * 2))


    def _handle_keyboard_events(self, event):
        """Handle keyboard events."""
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

    def _return_to_menu(self):
        """Return to the main menu."""
        subprocess.Popen(["python", "sources/menu.py"])
        pygame.quit()

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
        
        # Dibuja la imagen del peso en la nueva posición
        self.screen.blit(self.graphics.peso_image, self.body_image_rect)
        
        pygame.display.flip()

    def run(self):
        """Main simulation loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(90)
