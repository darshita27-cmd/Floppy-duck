import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Game settings for different difficulties
DIFFICULTY_SETTINGS = {
    'easy': {
        'gravity': 0.5,
        'flap_strength': -10,
        'pipe_gap': 250,
        'pipe_speed': 3,
        'pipe_frequency': 90
    },
    'mid': {
        'gravity': 0.7,
        'flap_strength': -11,
        'pipe_gap': 200,
        'pipe_speed': 5,
        'pipe_frequency': 70
    },
    'hard': {
        'gravity': 0.9,
        'flap_strength': -12,
        'pipe_gap': 160,
        'pipe_speed': 7,
        'pipe_frequency': 60
    }
}

class Duck:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 50
        self.height = 40
    
    def flap(self, flap_strength):
        self.velocity = flap_strength
    
    def update(self, gravity):
        self.velocity += gravity
        self.y += self.velocity
        
        # Limit fall speed
        if self.velocity > 10:
            self.velocity = 10
    
    def draw(self, screen):
        # Duck body (yellow circle)
        pygame.draw.circle(screen, YELLOW, (int(self.x + 25), int(self.y + 20)), 20)
        
        # Duck head (smaller yellow circle)
        pygame.draw.circle(screen, YELLOW, (int(self.x + 35), int(self.y + 10)), 15)
        
        # Duck beak (orange triangle)
        beak_points = [
            (self.x + 50, self.y + 10),
            (self.x + 65, self.y + 8),
            (self.x + 50, self.y + 15)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)
        
        # Duck eye (black dot)
        pygame.draw.circle(screen, BLACK, (int(self.x + 40), int(self.y + 8)), 3)
        
        # Duck wing (small oval)
        pygame.draw.ellipse(screen, YELLOW, (self.x + 15, self.y + 20, 20, 15))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self, x, gap, gap_y):
        self.x = x
        self.width = 70
        self.gap = gap
        self.gap_y = gap_y
        self.passed = False
        
        # Top pipe height
        self.top_height = gap_y
        # Bottom pipe starts after gap
        self.bottom_y = gap_y + gap
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, self.width, self.top_height), 3)
        # Top pipe cap
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.top_height - 20, self.width + 10, 20))
        
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y), 3)
        # Bottom pipe cap
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.bottom_y, self.width + 10, 20))
    
    def collides_with(self, duck):
        duck_rect = duck.get_rect()
        
        # Check collision with top pipe
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        if duck_rect.colliderect(top_pipe_rect):
            return True
        
        # Check collision with bottom pipe
        bottom_pipe_rect = pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)
        if duck_rect.colliderect(bottom_pipe_rect):
            return True
        
        return False
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Duck Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.difficulty = None
        self.reset_game()
    
    def reset_game(self):
        self.duck = Duck()
        self.pipes = []
        self.score = 0
        self.frame_count = 0
        self.game_over = False
        self.game_started = False
    
    def show_menu(self):
        """Show difficulty selection menu"""
        menu_running = True
        
        while menu_running:
            self.screen.fill(SKY_BLUE)
            
            # Title
            title_text = self.big_font.render("Duck Game", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Instructions
            inst_text = self.font.render("Click or Space to Flap!", True, BLACK)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
            self.screen.blit(inst_text, inst_rect)
            
            # Difficulty buttons
            easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250, 300, 60)
            mid_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 330, 300, 60)
            hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 410, 300, 60)
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw buttons with hover effect
            for button, text, difficulty in [(easy_button, "EASY", 'easy'), 
                                               (mid_button, "MEDIUM", 'mid'), 
                                               (hard_button, "HARD", 'hard')]:
                color = YELLOW if button.collidepoint(mouse_pos) else WHITE
                pygame.draw.rect(self.screen, color, button)
                pygame.draw.rect(self.screen, BLACK, button, 3)
                
                button_text = self.font.render(text, True, BLACK)
                button_text_rect = button_text.get_rect(center=button.center)
                self.screen.blit(button_text, button_text_rect)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(mouse_pos):
                        self.difficulty = 'easy'
                        menu_running = False
                    elif mid_button.collidepoint(mouse_pos):
                        self.difficulty = 'mid'
                        menu_running = False
                    elif hard_button.collidepoint(mouse_pos):
                        self.difficulty = 'hard'
                        menu_running = False
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def run(self):
        # Show menu to select difficulty
        self.show_menu()
        
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    if not self.game_started:
                        self.game_started = True
                    
                    if not self.game_over:
                        self.duck.flap(settings['flap_strength'])
                    else:
                        # Restart game
                        self.reset_game()
                        self.show_menu()
                        settings = DIFFICULTY_SETTINGS[self.difficulty]
            
            if self.game_started and not self.game_over:
                # Update duck
                self.duck.update(settings['gravity'])
                
                # Check if duck hits ground or ceiling
                if self.duck.y > SCREEN_HEIGHT - 40 or self.duck.y < 0:
                    self.game_over = True
                
                # Spawn pipes
                self.frame_count += 1
                if self.frame_count % settings['pipe_frequency'] == 0:
                    gap_y = random.randint(100, SCREEN_HEIGHT - settings['pipe_gap'] - 100)
                    self.pipes.append(Pipe(SCREEN_WIDTH, settings['pipe_gap'], gap_y))
                
                # Update pipes
                for pipe in self.pipes[:]:
                    pipe.update(settings['pipe_speed'])
                    
                    # Check collision
                    if pipe.collides_with(self.duck):
                        self.game_over = True
                    
                    # Check if passed pipe
                    if not pipe.passed and pipe.x + pipe.width < self.duck.x:
                        pipe.passed = True
                        self.score += 1
                    
                    # Remove off-screen pipes
                    if pipe.is_off_screen():
                        self.pipes.remove(pipe)
            
            # Drawing
            self.screen.fill(SKY_BLUE)
            
            # Draw pipes
            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            # Draw duck
            self.duck.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            # Draw difficulty
            diff_text = self.font.render(f"Level: {self.difficulty.upper()}", True, BLACK)
            self.screen.blit(diff_text, (10, 50))
            
            # Draw game over screen
            if self.game_over:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.big_font.render("Game Over!", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(game_over_text, game_over_rect)
                
                final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(final_score_text, final_score_rect)
                
                restart_text = self.font.render("Click or Press Space to Restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
                self.screen.blit(restart_text, restart_rect)
            
            # Draw start message
            if not self.game_started:
                start_text = self.font.render("Click or Press Space to Start!", True, BLACK)
                start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(start_text, start_rect)
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()