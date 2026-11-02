# THIS FILE IS ME FIGURING OUT THINGS IN PYGAME, YOU CAN IGNORE THIS LOL

import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

player_img = pygame.image.load("assets/player_image.png").convert()

player_img = pygame.transform.scale(player_img,
                                    (player_img.get_width() * 1.5,
                                     player_img.get_height() * 1.5)) 

player_img.set_colorkey((0, 0, 0))

running = True
x = 0
clock = pygame.time.Clock()

delta_time = 0.1

font = pygame.font.Font(None, size=30)

while running:
    screen.fill((0, 0, 0))

    screen.blit(player_img, (x, 30))

    hitbox = pygame.Rect(x, 30, player_img.get_width(), player_img.get_height())

    mpos = pygame.mouse.get_pos()

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mpos)
    pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)

    x += 50 * delta_time

    text = font.render("Hello, World!", True, (255, 255, 255))
    screen.blit(text, (300, 300))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()