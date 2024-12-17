import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Font
font = pygame.font.Font(None, 36)

# Clock to control game speed
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_to = 0

    def move(self):
        # Calculate new head position
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1]
        )
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.body.pop()

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * GRID_SIZE, 
                segment[1] * GRID_SIZE, 
                GRID_SIZE - 1, 
                GRID_SIZE - 1
            )
            pygame.draw.rect(surface, GREEN, rect)

    def check_collision(self):
        # Check wall collision
        head = self.body[0]
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False

class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in snake.body:
                return pos

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE, 
            self.position[1] * GRID_SIZE, 
            GRID_SIZE - 1, 
            GRID_SIZE - 1
        )
        pygame.draw.rect(surface, RED, rect)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    snake = Snake()
    food = Food(snake)
    score = 0
    high_score = 0

    # Restart button
    restart_button = Button(
        WIDTH // 2 - 100, 
        HEIGHT // 2 + 50, 
        200, 
        50, 
        "Restart", 
        GRAY, 
        WHITE
    )

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.is_clicked(event.pos):
                        # Reset game state
                        snake.reset()
                        food = Food(snake)
                        score = 0
                        game_over = False
                continue

            # Handle key events during active game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        if not game_over:
            # Move snake
            snake.move()

            # Check collision with food
            if snake.body[0] == food.position:
                snake.grow_to += 1
                score += 1
                # Update high score
                high_score = max(high_score, score)
                food = Food(snake)

            # Check game over
            if snake.check_collision():
                game_over = True

        # Clear screen
        screen.fill(BLACK)

        # Draw game objects if not game over
        if not game_over:
            snake.draw(screen)
            food.draw(screen)

        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        # Game over screen
        if game_over:
            game_over_text = font.render('Game Over!', True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(game_over_text, game_over_rect)
            
            # Draw restart button
            restart_button.draw(screen)

        # Update display
        pygame.display.flip()

        # Control game speed
        clock.tick(10)  # 10 FPS

    pygame.quit()

if __name__ == '__main__':
    main()