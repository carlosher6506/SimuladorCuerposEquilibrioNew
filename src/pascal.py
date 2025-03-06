import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# Game states
class GameState:
    def __init__(self):
        self.piston_height = 100  # Initial piston position
        self.platform_height = 300  # Initial platform position
        self.water_level = 400  # Initial water level
        self.draining = False
        
    def reset(self):
        self.__init__()

class PascalSimulator:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pascal's Principle Simulator")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        
        # Button positions
        self.reset_button = pygame.Rect(650, 50, 100, 40)
        self.drain_button = pygame.Rect(650, 100, 100, 40)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.reset_button.collidepoint(mouse_pos):
                    self.state.reset()
                elif self.drain_button.collidepoint(mouse_pos):
                    self.state.draining = not self.state.draining
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # Move piston down and platform up
                    if self.state.piston_height < 150:
                        self.state.piston_height += 2
                        self.state.platform_height -= 4
                        
        return True
        
    def update(self):
        # Handle draining
        if self.state.draining:
            if self.state.platform_height < 300:
                self.state.platform_height += 2
                self.state.piston_height -= 1
                
        # Natural return of piston when key is released
        if not pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.state.piston_height > 100:
                self.state.piston_height -= 1
                self.state.platform_height += 2
                
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw container
        pygame.draw.rect(self.screen, GRAY, (100, 200, 500, 300))
        
        # Draw water
        pygame.draw.rect(self.screen, BLUE, (100, self.state.water_level, 500, 100))
        
        # Draw piston
        pygame.draw.rect(self.screen, BLACK, (150, self.state.piston_height, 40, 100))
        
        # Draw platform with boxes
        platform_width = 200
        pygame.draw.rect(self.screen, GRAY, (350, self.state.platform_height, platform_width, 20))
        
        # Draw boxes on platform
        for i in range(2):
            for j in range(3):
                box_x = 320 + (j * 70)
                box_y = self.state.platform_height - (i * 60) - 60
                pygame.draw.rect(self.screen, BROWN, (box_x, box_y, 60, 50))
        
        # Draw buttons
        pygame.draw.rect(self.screen, GRAY, self.reset_button)
        pygame.draw.rect(self.screen, GRAY, self.drain_button)
        
        # Button text
        font = pygame.font.Font(None, 24)
        reset_text = font.render("Reset", True, BLACK)
        drain_text = font.render("Drain", True, BLACK)
        self.screen.blit(reset_text, (670, 60))
        self.screen.blit(drain_text, (670, 110))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulator = PascalSimulator()
    simulator.run()