import pygame
import random
import time
import sys
import os

from entities import Orb
from pathlib import Path

# Just a function so that PyInstaller doesn't end up becoming annoying
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # This shows a warning in VSCode because sys._MEIPASS DOESN'T exist.
        # But it does exist when the program is a EXE file, so we can ignore it.
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_save_path(filename):
    save_dir = Path.home() / ".avoid_the_orbs"

    save_dir.mkdir(exist_ok=True)

    return os.path.join(save_dir, filename)

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    try:
        with open(HIGHSCORE_FILE, "w") as file:
            file.write(str(score))
    except Exception as e:
        return 0


HIGHSCORE_FILE = get_save_path("highscore.txt")
high_score = load_high_score()
pygame.init()
pygame.mixer.init()

GAME_WIDTH = 640
GAME_HEIGHT = 640
theme = input("Choose a theme (dark/light): ").lower()

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Avoid the Orbs!")

# Set up cursor based on theming.
if theme == "dark":
    cursor_img = pygame.image.load(resource_path("assets/mouse_cursor_light.png")).convert_alpha()
elif theme == "light":
    cursor_img = pygame.image.load(resource_path("assets/mouse_cursor_dark.png")).convert_alpha()

pygame.mouse.set_visible(False)

# Background music
pygame.mixer.music.load(resource_path("assets/The Last Encounter Medium Loop.wav"))
pygame.mixer.music.set_volume(0.3)

canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

# Text types
font = pygame.font.Font(None, size=60)
font2 = pygame.font.Font(None, size=30)
score_font = pygame.font.Font(None, size=36)

# Buttons
start_game_button = pygame.Rect(200, 300, 250, 60)
quit_game_button = pygame.Rect(200, 400, 250, 60)



mpos_list = []
orbs = []

current_score = 0
game_start_time = 0

game_state = "PLAYING"
running = True

game_state = "MENU"
start_time = time.time()
while running:
    # Whenever the screen updates we need to check the new window size in case of scaling.
    # Also scaling the mouse inputs to our 640x640 space.
    screenW, screenH = screen.get_size()
    raw_mpos = pygame.mouse.get_pos()
    mpos = (
        int(raw_mpos[0] * (GAME_WIDTH / screenW)),
        int(raw_mpos[1] * (GAME_HEIGHT / screenH))
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "MENU":
                if start_game_button.collidepoint(mpos):
                    game_state = "READY"
                    start_time = time.time()
                elif quit_game_button.collidepoint(mpos):
                    running = False
                    sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if game_state == "GAME OVER":
                if event.key == pygame.K_SPACE:
                    game_state = "READY"
                    start_time = time.time()
                    current_score = 0


    if theme == "dark":
        canvas.fill((0, 0, 0))
    elif theme == "light":
        canvas.fill((255, 255, 255))

    if len(mpos_list) == 10:
        mpos_list.pop(0)
    else:
        mpos_list.append([mpos[0], mpos[1]])

    if game_state == "MENU":
        if theme == "dark":
            menu_text = font.render("Avoid the Orbs!", True, (255, 255, 255))
            start_text = font.render("Start Game", True, (255, 255, 255))
            quit_text = font.render("Quit Game", True, (255, 255, 255))
        elif theme == "light":
            menu_text = font.render("Avoid the Orbs!", True, (0, 0, 0))
            start_text = font.render("Start Game", True, (255, 255, 255))
            quit_text = font.render("Quit Game", True, (255, 255, 255))

        pygame.draw.rect(canvas, (100, 100, 100), start_game_button)
        pygame.draw.rect(canvas, (100, 100, 100), quit_game_button)
        text_rect = menu_text.get_rect(center=(320, 200))
        canvas.blit(menu_text, text_rect)

        canvas.blit(start_text, start_text.get_rect(center=start_game_button.center))
        canvas.blit(quit_text, quit_text.get_rect(center=quit_game_button.center))

    # In the first loop, give the player some time to get ready.
    # This was the biggest problem I saw while testing with friends 
    if game_state == "READY":
        elapsed = time.time() - start_time

        if elapsed < 2:
            if theme == "dark":
                text_surf = font.render("Ready...?", True, (255, 255, 255))
            elif theme == "light":
                text_surf = font.render("Ready...?", True, (0, 0, 0))
        elif elapsed < 3:
            if theme == "dark":
                text_surf = font.render("GO!", True, (255, 255, 255))
            elif theme == "light":
                text_surf = font.render("GO!", True, (0, 0, 0))
        else:
            game_state = "PLAYING"
            text_surf = None
            game_start_time = time.time()
            pygame.mixer.music.play(-1)

        if text_surf:
            text_rect = text_surf.get_rect(center=(320, 320))
            canvas.blit(text_surf, text_rect)

    if game_state != "MENU":
        for i in range(len(mpos_list) - 1):
            if theme == "dark":
                pygame.draw.line(canvas, (255, 255, 255), mpos_list[i], mpos_list[i+1], 2)
            elif theme == "light":
                pygame.draw.line(canvas, (0, 0, 0), mpos_list[i], mpos_list[i+1], 2)


    if game_state == "PLAYING":
        current_score = int((time.time() - game_start_time) * 100)

        if random.random() < 0.25:
            edge = random.randint(1, 4)
            if edge == 1:
                orbs.append(Orb(random.randint(0, 640), 0))
            elif edge == 2:
                orbs.append(Orb(random.randint(0, 640), 640))
            elif edge == 3:
                orbs.append(Orb(0, random.randint(0, 640)))
            else:
                orbs.append(Orb(640, random.randint(0, 640)))


    elif game_state == "GAME OVER":
        if theme == "dark":
            text = font.render("Game Over!", True, (255, 255, 255))
            score_summary = score_font.render(f"Score: {current_score} | High Score: {high_score}", True, score_color)
            try_again = font2.render("(Press space to try again!)", True, (255, 255, 255))
        elif theme == "light":
            text = font.render("Game Over!", True, (0, 0, 0))
            score_summary = score_font.render(f"Score: {current_score} | High Score: {high_score}", True, score_color)
            try_again = font2.render("(Press space to try again!)", True, (0, 0, 0))

        text_rect2 = try_again.get_rect(center=(320, 355))
        text_rect = text.get_rect(center=(320, 320))
        score_rect = score_summary.get_rect(center=(180,20))
        
        canvas.blit(text, text_rect)
        canvas.blit(try_again, text_rect2)
        canvas.blit(score_summary, score_rect)

    if game_state == "PLAYING":
        for orb in orbs:
            orb.update()
            if orb.check_collision(mpos):
                game_state = "GAME OVER"
                orbs.clear()
                pygame.mixer.music.stop()

                if current_score > high_score:
                    high_score = current_score
                    save_high_score(high_score)

            orb.draw(canvas)

        if theme == "dark":
            score_color = (255, 255, 255)
        else:
            score_color = (0, 0, 0)

        score_surf = score_font.render(f"Score: {current_score}", True, score_color)
        canvas.blit(score_surf, (15, 15))
    
    scaled_canvas = pygame.transform.scale(canvas, (screenW, screenH))
    screen.blit(scaled_canvas, (0, 0))
    screen.blit(cursor_img, raw_mpos)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()