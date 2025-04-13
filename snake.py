import pygame
import random
import os
import sys

# Initialize pygame
pygame.init()

# Grid settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

# Window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Grid & Menus")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY  = (40, 40, 40)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 70)

# Clock and speed
clock = pygame.time.Clock()
speed = 10  # Speed of the game (can be adjusted)

# Highscore file
HIGHSCORE_FILE = "highscore.txt"

# Load highscore from file
def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write("0")
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip())

# Save highscore to file
def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Draw text
def draw_text(text, color, x, y, center=False, big=False):
    f = big_font if big else font
    surface = f.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    win.blit(surface, rect)
    return rect

# Draw grid (optional visual)
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, GRAY, (0, y), (WIDTH, y))

# Button class
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect, border_radius=10)
        draw_text(self.text, BLACK, self.rect.centerx, self.rect.centery, center=True)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# Title screen
def title_screen():
    playing = True

    def start_game():
        nonlocal playing
        playing = False

    def quit_game():
        pygame.quit()
        sys.exit()

    play_button = Button("Play", WIDTH//2 - 75, HEIGHT//2 - 30, 150, 50, start_game)
    quit_button = Button("Quit", WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50, quit_game)

    while playing:
        win.fill(BLACK)
        draw_text("Snake", GREEN, WIDTH//2, HEIGHT//4, center=True, big=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                play_button.click(event.pos)
                quit_button.click(event.pos)

        play_button.draw()
        quit_button.draw()
        pygame.display.update()
        clock.tick(60)

# Death screen
def death_screen(score):
    highscore = load_highscore()
    if score > highscore:
        save_highscore(score)

    waiting = True

    def replay():
        nonlocal waiting
        waiting = False

    replay_button = Button("Replay", WIDTH//2 - 75, HEIGHT//2 + 10, 150, 50, replay)

    while waiting:
        win.fill(BLACK)
        draw_text("You Died!", RED, WIDTH//2, HEIGHT//3, center=True, big=True)
        draw_text(f"Your score: {score}", WHITE, WIDTH//2, HEIGHT//3 + 50, center=True)
        replay_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                replay_button.click(event.pos)

        pygame.display.update()
        clock.tick(60)

# Pause menu
def pause_menu():
    paused = True

    def resume():
        nonlocal paused
        paused = False

    def restart():
        raise Exception("restart")

    def to_title():
        raise Exception("title")

    cont_btn = Button("Continue", WIDTH//2 - 75, HEIGHT//2 - 70, 150, 50, resume)
    restart_btn = Button("Restart", WIDTH//2 - 75, HEIGHT//2, 150, 50, restart)
    quit_btn = Button("Quit", WIDTH//2 - 75, HEIGHT//2 + 70, 150, 50, to_title)

    while paused:
        win.fill(BLACK)
        draw_text("Paused", YELLOW, WIDTH//2, HEIGHT//4, center=True, big=True)
        cont_btn.draw()
        restart_btn.draw()
        quit_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cont_btn.click(event.pos)
                restart_btn.click(event.pos)
                quit_btn.click(event.pos)

        pygame.display.update()
        clock.tick(60)

# Main game loop
def game_loop():
    while True:
        try:
            snake = [(5, 5)]
            direction = (1, 0)
            score = 0

            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and direction != (0, 1):
                            direction = (0, -1)
                        elif event.key == pygame.K_DOWN and direction != (0, -1):
                            direction = (0, 1)
                        elif event.key == pygame.K_LEFT and direction != (1, 0):
                            direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                            direction = (1, 0)
                        elif event.key == pygame.K_ESCAPE:
                            pause_menu()

                # Move snake
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])
                snake.insert(0, new_head)

                # Check if food is eaten
                if new_head == food:
                    score += 10
                    while True:
                        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        if food not in snake:
                            break
                else:
                    snake.pop()

                # Collision detection
                x, y = new_head
                if (
                    x < 0 or x >= GRID_WIDTH or
                    y < 0 or y >= GRID_HEIGHT or
                    new_head in snake[1:]
                ):
                    break

                # Draw everything
                win.fill(BLACK)
                draw_grid()
                for segment in snake:
                    pygame.draw.rect(win, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(win, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                draw_text(f"Score: {score}", WHITE, 10, 10)
                draw_text(f"Highscore: {max(score, load_highscore())}", WHITE, 10, 40)
                pygame.display.update()
                clock.tick(speed)

            death_screen(score)
        except Exception as e:
            if str(e) == "restart":
                continue
            elif str(e) == "title":
                title_screen()

if __name__ == "__main__":
    title_screen()
    game_loop()

