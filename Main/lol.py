import pygame
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Game with Asteroids")

# Colors (white for score text)
WHITE = (255, 255, 255)

# FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Load large background image for scrolling effect and scale it to screen size
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ensure background fits the screen
background_height = background.get_height()
scroll_speed = 2  # Speed at which the background scrolls

# Load jet image and resize it
jet = pygame.image.load('jet.png')
jet_size = (80, 80)  # Adjust size as necessary
jet = pygame.transform.scale(jet, jet_size)

# Load asteroid image and resize it
asteroid = pygame.image.load('asteroid.png')
asteroid_size = (100, 100)  # Same size as obstacle was
asteroid = pygame.transform.scale(asteroid, asteroid_size)

# Load collectible image and resize it
collectible = pygame.image.load('collectible.png')  # Ensure you have this image
collectible_size = (50, 50)  # Size of the collectible
collectible = pygame.transform.scale(collectible, collectible_size)

# Player settings
player_size = jet_size[0]
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 5

# Obstacle (asteroid) settings
obstacle_pos = [random.randint(0, WIDTH - asteroid_size[0]), 0]
obstacle_speed = 5

# Collectible settings
collectible_pos = [random.randint(0, WIDTH - collectible_size[0]), -50]  # Start above the screen
collectible_speed = 3  # Speed at which the collectible falls

# Score
score = 0
font = pygame.font.SysFont("monospace", 35)

# Background scroll positions
bg_y1 = 0
bg_y2 = -background_height  # The second copy of the background starts off-screen

# Game states
game_state = "menu"  # 'menu', 'playing', or 'game_over'


def detect_collision(player_pos, obstacle_pos):
    p_x, p_y = player_pos
    o_x, o_y = obstacle_pos

    if (p_x < o_x + asteroid_size[0] and p_x + player_size > o_x) and (
            p_y < o_y + asteroid_size[1] and p_y + player_size > o_y):
        return True
    return False


def detect_collectible_collision(player_pos, collectible_pos):
    p_x, p_y = player_pos
    c_x, c_y = collectible_pos

    if (p_x < c_x + collectible_size[0] and p_x + player_size > c_x) and (
            p_y < c_y + collectible_size[1] and p_y + player_size > c_y):
        return True
    return False


def main_menu():
    screen.fill((0, 0, 0))
    title_text = font.render("JET GAME WITH ASTEROIDS", True, WHITE)
    start_text = font.render("Press ENTER to start", True, WHITE)
    quit_text = font.render("Press Q to quit", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()


def game_over_screen(final_score):
    screen.fill((0, 0, 0))
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Your score: {final_score}", True, WHITE)
    restart_text = font.render("Press R to restart", True, WHITE)
    quit_text = font.render("Press Q to quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()


# Game loop
while True:
    if game_state == "menu":
        main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    game_state = "playing"
                    # Start playing the background music when gameplay starts
                    pygame.mixer.music.load('NEXT!.mp3')
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    quit()

    elif game_state == "playing":
        # Event handling for in-game actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # Scroll background
        bg_y1 += scroll_speed
        bg_y2 += scroll_speed

        # If the background moves off the screen, reset its position
        if bg_y1 >= HEIGHT:
            bg_y1 = -background_height
        if bg_y2 >= HEIGHT:
            bg_y2 = -background_height

        # Draw the two copies of the background to create a looping effect
        screen.blit(background, (0, bg_y1))
        screen.blit(background, (0, bg_y2))

        # Draw jet (player)
        screen.blit(jet, (player_pos[0], player_pos[1]))

        # Move obstacle (asteroid)
        obstacle_pos[1] += obstacle_speed
        if obstacle_pos[1] > HEIGHT:
            obstacle_pos[1] = 0 - asteroid_size[1]  # Reset to the top
            obstacle_pos[0] = random.randint(0, WIDTH - asteroid_size[0])
            score += 1  # Increase score when the asteroid passes

        # Draw asteroid (obstacle)
        screen.blit(asteroid, (obstacle_pos[0], obstacle_pos[1]))

        # Check collision with asteroid
        if detect_collision(player_pos, obstacle_pos):
            game_state = "game_over"
            # Stop the music when the game ends
            pygame.mixer.music.stop()

        # Move collectible
        collectible_pos[1] += collectible_speed
        if collectible_pos[1] > HEIGHT:
            collectible_pos[1] = 0 - collectible_size[1]  # Reset to the top
            collectible_pos[0] = random.randint(0, WIDTH - collectible_size[0])  # Random x position

        # Check collision with collectible
        if detect_collectible_collision(player_pos, collectible_pos):
            score += 5  # Increase score when collectible is collected
            collectible_pos[1] = 0 - collectible_size[1]  # Reset collectible position
            collectible_pos[0] = random.randint(0, WIDTH - collectible_size[0])  # Random x position

        # Draw collectible
        screen.blit(collectible, (collectible_pos[0], collectible_pos[1]))

        # Display the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(FPS)

    elif game_state == "game_over":
        game_over_screen(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    game_state = "playing"
                    score = 0  # Reset the score
                    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]  # Reset player position
                    collectible_pos = [random.randint(0, WIDTH - collectible_size[0]), -50]  # Reset collectible position
                    pygame.mixer.music.play(-1)  # Restart the music when the game restarts
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    quit()
