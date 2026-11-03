import pygame
import random

from entities import Orb

pygame.init()

GAME_WIDTH = 640
GAME_HEIGHT = 640

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("My Game")

cursor_img = pygame.image.load("assets/mouse_cursor.png").convert_alpha()

pygame.mouse.set_visible(False)

canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.Font(None, size=60)

mpos_list = []
orbs = []

game_state = "PLAYING"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    for i in range(len(mpos_list) - 1):
        pygame.draw.line(canvas, (0, 0, 0), mpos_list[i], mpos_list[i+1], 2)

    if game_state == "PLAYING":
        if random.random() < 0.05:
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