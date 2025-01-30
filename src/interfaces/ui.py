import pygame
from constants.constant import *
from physics.physic import calculate_tensions, solution, calculate_body_position, conversor

class UI:
    def __init__(self, graphics_manager):
        self.graphics = graphics_manager
        self.conversor_visible = False
        self.mostrar_grafico = False
        self.superficie_grafico = None
        self.active = False
        self.text = '50'
        self.result_conversion = 0

    def draw_scene(self, screen, weight, theta1, theta2):
        """Draw the complete simulation scene."""
        screen.fill(WHITE)
        mass = weight / GRAVITY
        
        anchor1_x = WIDTH // 4
        anchor2_x = 3 * WIDTH // 4
        anchor_y = HEIGHT // 4
        
        T1, T2 = calculate_tensions(weight, theta1, theta2)
        T11, T22 = solution(weight, theta1, theta2)
        
        body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2)
        
        # Draw all visual elements using graphics manager
        self.graphics.draw_scene(screen, body_x, body_y, anchor1_x, anchor2_x, anchor_y, theta1, theta2)
        
        # Draw measurements and text
        self._draw_measurements(screen, body_x, body_y, T11, T22, theta1, theta2, weight, mass)
        
        # Draw UI elements
        self._draw_ui_elements(screen)
        
        # Draw converter if visible
        if self.conversor_visible:
            self._draw_converter(screen)
            
        # Draw graph if visible
        if self.mostrar_grafico and self.superficie_grafico:
            self._draw_graph(screen)

    def _draw_measurements(self, screen, body_x, body_y, T11, T22, theta1, theta2, weight, mass):
        """Draw all measurement text."""
        text_T1 = self.graphics.font.render(f"T1: {T11:.2f} N", True, BLACK)
        text_T2 = self.graphics.font.render(f"T2: {T22:.2f} N", True, BLACK)
        text_theta1 = self.graphics.font.render(f"θ1: {theta1:.1f}°", True, BLACK)
        text_theta2 = self.graphics.font.render(f"θ2: {theta2:.1f}°", True, BLACK)
        text_weight = self.graphics.font.render(f"P = {weight:.0f} N", True, BLACK)
        text_mass = self.graphics.font.render(f"W = {mass:.2f} kg", True, BLACK)
        
        # Position and draw text
        screen.blit(text_T1, (body_x - 150, body_y - 30))
        screen.blit(text_T2, (body_x + 50, body_y - 30))
        screen.blit(text_theta1, (body_x - 150, body_y - 60))
        screen.blit(text_theta2, (body_x + 50, body_y - 60))
        screen.blit(text_weight, (body_x - 30, body_y + 30))
        screen.blit(text_mass, (body_x - 30, body_y + 50))

    def _draw_ui_elements(self, screen):
        """Draw UI buttons and elements."""
        # Draw header and footer bars
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH + 400, 45))
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 25, WIDTH, 45))
        
        # Draw buttons
        buttons = [
            ("Conversor", 40, HEIGHT - 22, 180, 40),
            ("Graficar", 240, HEIGHT - 22, 180, 40),
            ("Regresar", 440, HEIGHT - 22, 180, 40)
        ]
        
        for text, x, y, w, h in buttons:
            pygame.draw.rect(screen, BLUE, (x, y, w, h))
            text_surface = self.graphics.font_large.render(text, True, WHITE)
            screen.blit(text_surface, (x + 10, y + 5))

    def _draw_converter(self, screen):
        """Draw the converter interface."""
        pygame.draw.rect(screen, BLUE, (0, 580, 440, 235))
        pygame.draw.rect(screen, WHITE, (7, 590, 422, 215))
        
        title = self.graphics.font_large.render('Conversor de Kg a N', True, BLACK)
        result = self.graphics.font_large.render(f"{self.result_conversion:.2f} N", True, BLACK)
        
        screen.blit(title, (70, 600))
        screen.blit(result, (145, 730))
        
        # Draw convert button
        pygame.draw.rect(screen, BLACK, (65, 680, 300, 40))
        convert_text = self.graphics.font_large.render('Convertir', True, WHITE)
        screen.blit(convert_text, (155, 685))
        
        # Draw input field
        input_rect = pygame.Rect(65, 630, 300, 45)
        color = 'dodgerblue2' if self.active else BLACK
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = self.graphics.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    def _draw_graph(self, screen):
        """Draw the force diagram graph."""
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