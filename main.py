import pygame
import random
import time
import sys
import os

from entities import Orb

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # This shows a warning in VSCode because sys._MEIPASS DOESN'T exist.
        # But it does exist when the program is a EXE file, so we can ignore it.
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()

GAME_WIDTH = 640
GAME_HEIGHT = 640
theme = input("Choose a theme (dark/light): ").lower()

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Avoid the Orbs!")

if theme == "dark":
    cursor_img = pygame.image.load(resource_path("assets/mouse_cursor_light.png")).convert_alpha()
elif theme == "light":
    cursor_img = pygame.image.load(resource_path("assets/mouse_cursor_dark.png")).convert_alpha()

pygame.mouse.set_visible(False)

canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.Font(None, size=60)

mpos_list = []
orbs = []

game_state = "PLAYING"
running = True

game_state = "READY"
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if theme == "dark":
        canvas.fill((0, 0, 0))
    elif theme == "light":
        canvas.fill((255, 255, 255))

    # Whenever the screen updates we need to check the new window size in case of scaling.
    # Also scaling the mouse inputs to our 640x640 space.
    screenW, screenH = screen.get_size()
    raw_mpos = pygame.mouse.get_pos()
    mpos = (
        int(raw_mpos[0] * (GAME_WIDTH / screenW)),
        int(raw_mpos[1] * (GAME_HEIGHT / screenH))
    )
    if len(mpos_list) == 10:
        mpos_list.pop(0)
    else:
        mpos_list.append([mpos[0], mpos[1]])

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

        if text_surf:
            text_rect = text_surf.get_rect(center=(320, 320))
            canvas.blit(text_surf, text_rect)


    for i in range(len(mpos_list) - 1):
        if theme == "dark":
            pygame.draw.line(canvas, (255, 255, 255), mpos_list[i], mpos_list[i+1], 2)
        elif theme == "light":
            pygame.draw.line(canvas, (0, 0, 0), mpos_list[i], mpos_list[i+1], 2)

    if game_state == "PLAYING":
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
        elif theme == "light":
            text = font.render("Game Over!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(320, 320))
        canvas.blit(text, text_rect)

    if game_state == "PLAYING":
        for orb in orbs:
            orb.update()
            if orb.check_collision(mpos):
                game_state = "GAME OVER"
                orbs.clear()
            orb.draw(canvas)
    
    scaled_canvas = pygame.transform.scale(canvas, (screenW, screenH))
    screen.blit(scaled_canvas, (0, 0))
    screen.blit(cursor_img, raw_mpos)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()