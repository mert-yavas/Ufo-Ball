import pygame
import sys
import random 

game_started = False
# Resolution
WIDTH, HEIGHT = 1024, 768

# Screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ufo-Ball")

# Background
background_image = pygame.image.load("background.jpg")

# Paddle Options
paddle_width = 150
paddle_height = 100
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 110
paddle_speed = 3.5

# Health
health = 3

# Colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Blocks Options
block_width, block_height = 50, 50
block_x = block_width + 10
block_y = block_height + 10
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (block_width, block_height))

# Sound
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("hit2.wav")
destroy_sound = pygame.mixer.Sound("destroy2.wav")

        
# Draw the board
def draw_board():
    board_image = pygame.image.load("board.png")
    board_image = pygame.transform.scale(board_image, (paddle_width, paddle_height))
    screen.blit(board_image, (paddle_x, paddle_y))

def draw_start_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Press Any Button", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_game_over_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_health ():
    font = pygame.font.Font(None, 36)
    text = font.render(str(health), True, WHITE)
    text_rect = text.get_rect(center=(WIDTH -30 , HEIGHT - 738))
    screen.blit(text, text_rect)

# Ball class
class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = random.choice([-2,2,1.9,-1.9,-2.5,2.5])
        self.velocity_y = 2  
        self.image = pygame.image.load("ball2.png")
        self.scale = pygame.transform.scale(self.image, (2 * radius, 2 * radius))

    def reset(self):
        self.x = WIDTH // random.choice([2,3,4,5,6,7,8,9])
        self.y = HEIGHT // 2
        self.velocity_x = random.choice([-2,2,1.9,-1.9,-2.5,2.5]) 
        self.velocity_y = 2

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Collision checks
        if self.x < 0 or self.x > WIDTH:
            self.velocity_x = -self.velocity_x
            
        if self.y < 0:
            self.velocity_y = -self.velocity_y
        elif self.y > HEIGHT:
            # Decrease health and reset ball position
            global health
            health -= 1
            if health > 0:
                self.reset()
            else:
                pygame.quit()
                sys.exit()  # Exit the game when health runs out

        if (
            self.x + self.radius > paddle_x
            and self.x - self.radius < paddle_x + paddle_width
            and self.y + self.radius - 50 > paddle_y
        ):
            self.velocity_y = -self.velocity_y
            hit_sound.play()

        # Block Collision Mechanic
        for block in blocks[:]:
            if block.colliderect(
                    self.x - self.radius + 20, 
                    self.y - self.radius + 20, 
                    self.radius * 2, 
                    self.radius * 2
                    ):
                self.velocity_y = -self.velocity_y
                blocks.remove(block)
                destroy_sound.play()
            

    def draw(self, screen):
        screen.blit(self.scale, (self.x, self.y))

ball = Ball(WIDTH // 2, HEIGHT // 2, 10)

# Create Blocks
def create_blocks():
    blocks = []
    for i in range(5):
        for j in range(15):
            block = pygame.Rect(j * block_x + 70, i * block_y + 50, block_width, block_height)
            blocks.append(block)
    return blocks

# Draw Blocks
def draw_blocks(blocks):
    for block in blocks:
        screen.blit(block_image, block.topleft)

# Game Engine
pygame.init()
running = True
blocks = create_blocks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game_started = True

    if not game_started:
        screen.blit(background_image, (0, 0))
        draw_start_screen()
    else:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 1:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x + paddle_width < WIDTH:
            paddle_x += paddle_speed
            
        screen.blit(background_image, (0, 0))
        draw_blocks(blocks)
        draw_board()
        draw_health()
        ball.update()
        ball.draw(screen)
        if len(blocks) == 0:
            screen.blit(background_image, (0, 0))
            draw_game_over_screen()
    pygame.display.flip()

pygame.quit()