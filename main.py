import pygame

pygame.init()

GAME_WIDTH = 640
GAME_HEIGHT = 640

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("My Game")

cursor_img = pygame.image.load("assets/mouse_cursor.png").convert_alpha()

pygame.mouse.set_visible(False)

canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

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

    
    scaled_canvas = pygame.transform.scale(canvas, (screenW, screenH))
    screen.blit(scaled_canvas, (0, 0))
    screen.blit(cursor_img, raw_mpos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()