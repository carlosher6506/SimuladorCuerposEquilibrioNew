import pygame
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from constants import *

class GraphicsManager:
    def __init__(self):
        self.load_images()
        self.font_large = pygame.font.SysFont(None, 40)
        self.font = pygame.font.SysFont(None, 24)

    def load_images(self):
        """Load and scale all required images."""
        self.rotacion_image = pygame.image.load(ROTACION_IMAGE_PATH)
        self.peso_image = pygame.image.load(PESO_IMAGE_PATH)
        self.polea_image = pygame.image.load(POLEA_IMAGE_PATH)
        self.rope_image = pygame.image.load(ROPE_IMAGE_PATH)
        self.fondo_image = pygame.image.load(FONDO_IMAGE_PATH)

        # Scale images
        self.peso_image = pygame.transform.scale(self.peso_image, (520, 450))
        self.polea_image = pygame.transform.scale(self.polea_image, (200, 140))
        self.rotacion_image = pygame.transform.scale(self.rotacion_image, (90, 70))
        self.rope_image = pygame.transform.scale(self.rope_image, (420, 420))

    def draw_rope(self, screen, start, end):
        """Draw a rope between two points."""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx)
        length = math.hypot(dx, dy)

        scaled_rope = pygame.transform.scale(self.rope_image, (int(length), self.rope_image.get_height()))
        rotated_rope = pygame.transform.rotate(scaled_rope, math.degrees(-angle))

        rope_rect = rotated_rope.get_rect()
        rope_rect.center = (start[0] + dx/2, start[1] + dy/2)
        
        peso_rect = self.peso_image.get_rect(center=(520, 450))  # Calcula el rectángulo centrado en (body_x, body_y)
        screen.blit(self.peso_image, peso_rect)

        screen.blit(rotated_rope, rope_rect)



    def create_graph(self, peso, theta1, theta2, T11, T22):
        """Create force diagram using matplotlib."""
        plt.switch_backend('Agg')
        fig = plt.figure(figsize=(300/100, 300/100), dpi=100)
        ax = fig.add_subplot(111)

        theta1_rad = math.radians(theta1)
        theta2_rad = math.radians(theta2)

        ancla1_x, ancla2_x = 0, 10
        ancla_y = 10
        cuerpo_x = (ancla1_x + ancla2_x) / 2
        cuerpo_y = ancla_y - 5

        ax.plot([cuerpo_x], [cuerpo_y], 'ro', markersize=10)
        ax.quiver(cuerpo_x, cuerpo_y, 0, -1, scale=3, color='g', width=0.005, label=f'Peso: {peso:.2f}N')
        ax.quiver(cuerpo_x, cuerpo_y, math.cos(theta1_rad), math.sin(theta1_rad), 
                scale=2, color='b', width=0.005, label=f'Angulo 1: {theta1}')
        ax.quiver(cuerpo_x, cuerpo_y, -math.cos(theta2_rad), math.sin(theta2_rad), 
                scale=2, color='r', width=0.005, label=f'Angulo 2: {theta2}')

        ax.set_xlim(-2, 12)
        ax.set_ylim(0, 12)
        ax.set_aspect('equal')
        ax.legend(fontsize='x-small')
        ax.set_title('Diagrama de Equilibrio', fontsize='small')
        ax.grid(True)

        plt.tight_layout()

        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        plt.close(fig)

        return pygame.image.fromstring(raw_data, size, "RGB")