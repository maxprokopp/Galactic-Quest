import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ascii_art = [
            "  ^  ",
            " /|\\ ",
            "/_|_\\",
            " .:. "  # Simple thruster
        ]
        self.damage_timer = 0
        self.damage_duration = 60
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.rapid_fire_duration = 600

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def draw(self):
        # Calculate vibration offset when damaged
        if self.damage_timer > 0:
            vibration_x = random.choice([-1, 1]) * 2
            vibration_y = random.choice([-1, 1]) * 2
            ship_color = RED if self.damage_timer % 4 < 2 else (139, 0, 0)  # Dark red
        else:
            vibration_x = 0
            vibration_y = 0
            ship_color = GREEN
        
        # Draw the spaceship with vibration offset
        for i, line in enumerate(self.ascii_art[:-1]):  # Draw ship parts
            text_surface = font.render(line, True, ship_color)
            screen.blit(text_surface, (self.x + vibration_x, self.y + vibration_y + i * 10))
        
        # Draw thruster with alternating visibility
        if pygame.time.get_ticks() % 2 == 0:  # Flicker effect
            thruster_color = (255, 140, 0)  # Dark orange
            text_surface = font.render(self.ascii_art[-1], True, thruster_color)
            screen.blit(text_surface, (self.x + vibration_x, self.y + vibration_y + 30))
        
        # Update damage timer
        if self.damage_timer > 0:
            self.damage_timer -= 1

    def update_power_ups(self):
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False

# Enemy
class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = random.uniform(1, 3)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ascii_art = [
            " /-\\ ",
            "|o o|",
            " \\_/ "
        ]

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        for i, line in enumerate(self.ascii_art):
            text_surface = font.render(line, True, RED)
            screen.blit(text_surface, (self.x, self.y + i * 10))

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x
        self.y = y
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Explosion
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation = [
            ["   *   "],
            ["  ***  "],
            [" ***** ", "  ***  "],
            ["*******", " ***** ", "  ***  "],
            [" \\***/ ", "*******", " \\***/ "],
            ["--***--", " \\***/ ", "--***--"],
            [" * * * ", "--***--", " * * * "],
            ["  * *  ", " * * * ", "  * *  "],
            ["   *   ", "  * *  ", "   *   "],
            ["   .   ", "   *   ", "   .   "],
            ["   .   "],
            ["   ·   "]
        ]
        self.is_done = False

    def update(self):
        self.frame += 1
        if self.frame >= len(self.animation):
            self.is_done = True

    def draw(self):
        if not self.is_done:
            current_frame = self.animation[self.frame]
            for i, line in enumerate(current_frame):
                text_surface = font.render(line, True, WHITE)
                screen.blit(text_surface, (self.x - 20, self.y + i * 10))

# Hostile Explosion
class HostileExplosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation = [
            ["   *   "],
            ["  ***  "],
            [" ***** ", "  ***  "],
            ["*******", " ***** ", "  ***  "],
            [" \\***/ ", "*******", " \\***/ "],
            ["--***--", " \\***/ ", "--***--"],
            [" * * * ", "--***--", " * * * "],
            ["  * *  ", " * * * ", "  * *  "],
            ["   *   ", "  * *  ", "   *   "],
            ["   .   ", "   *   ", "   .   "],
            ["   .   "],
            ["   ·   "]
        ]
        self.is_done = False

    def update(self):
        self.frame += 1
        if self.frame >= len(self.animation):
            self.is_done = True

    def draw(self):
        if not self.is_done:
            current_frame = self.animation[self.frame]
            for i, line in enumerate(current_frame):
                color = RED if self.frame % 2 == 0 else (255, 165, 0)
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (self.x - 20, self.y - i * 10))

# Star
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.1, 0.5)  # Slow movement
        self.char = random.choice(['·', '.', '*'])  # Different star shapes

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self):
        text_surface = font.render(self.char, True, WHITE)
        screen.blit(text_surface, (self.x, self.y))

# Power-up
class PowerUp:
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.speed = 1.5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ascii_art = [
            "╔══╗",
            "║██║",
            "╚══╝"
        ]
        self.rainbow_index = 0
        self.rainbow_colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (148, 0, 211)   # Violet
        ]

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        color = self.rainbow_colors[self.rainbow_index]
        self.rainbow_index = (self.rainbow_index + 1) % len(self.rainbow_colors)
        
        for i, line in enumerate(self.ascii_art):
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (self.x, self.y + i * 10))

# Initialize game state
def reset_game():
    global player, enemies, bullets, explosions, hostile_explosions, power_ups, score, lives, game_over, font, stars
    player = Player()
    enemies = []
    bullets = []
    explosions = []
    hostile_explosions = []
    power_ups = []
    stars = [Star() for _ in range(50)]
    score = 0
    lives = 3
    game_over = False
    font = pygame.font.Font(None, 24)

# Create initial game objects and variables
reset_game()
font = pygame.font.Font(None, 36)
button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 50, 120, 40)

# Game loop
running = True
clock = pygame.time.Clock()
spawn_timer = 0
spawn_delay = 60
power_up_spawn_timer = 0
power_up_spawn_delay = 600  # Spawn power-up every 10 seconds

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(Bullet(player.x + player.width // 2 - 2, player.y))
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        spawn_timer += 1
        power_up_spawn_timer += 1
        
        # Spawn power-ups
        if power_up_spawn_timer >= power_up_spawn_delay:
            x = random.randint(0, WIDTH - 40)
            power_ups.append(PowerUp(x, -40))
            power_up_spawn_timer = 0

        # Update player power-ups
        player.update_power_ups()

        # Handle rapid fire
        if player.rapid_fire and pygame.time.get_ticks() % 5 == 0:  # Shoot every 5 ticks
            bullets.append(Bullet(player.x + player.width // 2 - 2, player.y))

        # Move power-ups and check collection
        for power_up in power_ups[:]:
            power_up.move()
            if power_up.y > HEIGHT:
                power_ups.remove(power_up)
            elif power_up.rect.colliderect(player.rect):
                power_ups.remove(power_up)
                player.rapid_fire = True
                player.rapid_fire_timer = player.rapid_fire_duration

        # Spawn new enemies
        if spawn_timer >= spawn_delay:
            x = random.randint(0, WIDTH - 40)
            enemies.append(Enemy(x, -40))
            spawn_timer = 0

        # Update game objects
        player.move()
        
        # Move enemies and check collisions with player
        for enemy in enemies[:]:
            enemy.move()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1
                hostile_explosions.append(HostileExplosion(enemy.x, HEIGHT))
                player.damage_timer = player.damage_duration  # Trigger damage flash and vibration
                if lives <= 0:
                    game_over = True
            if enemy.rect.colliderect(player.rect):
                lives = 0
                game_over = True

        # Move bullets and check collisions
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    explosions.append(Explosion(enemy.x, enemy.y))
                    enemies.remove(enemy)
                    score += 1

        # Update and draw explosions
        for explosion in explosions[:]:
            explosion.update()
            if explosion.is_done:
                explosions.remove(explosion)

        # Update and draw hostile explosions
        for explosion in hostile_explosions[:]:
            explosion.update()
            if explosion.is_done:
                hostile_explosions.remove(explosion)

    # Draw everything
    screen.fill(BLACK)
    
    # Update and draw stars
    for star in stars:
        star.move()
        star.draw()
    
    if not game_over:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()
        for explosion in explosions:
            explosion.draw()
        for explosion in hostile_explosions:
            explosion.draw()
        for power_up in power_ups:
            power_up.draw()

        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
    else:
        # Draw simple "GAME OVER" text
        large_font = pygame.font.Font(None, 72)  # Larger font size
        game_over_text = large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        # Draw final score below the text
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 80))
        screen.blit(final_score_text, final_score_rect)
        
        # Draw restart button
        pygame.draw.rect(screen, WHITE, button_rect, 2)
        restart_text = font.render("Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=button_rect.center)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

# Quit game
pygame.quit() 