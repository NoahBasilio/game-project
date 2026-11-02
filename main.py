import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

player_img = pygame.image.load("player_image.png").convert()

player_img = pygame.transform.scale(player_img,
                                    (player_img.get_width() * 2,
                                     player_img.get_height() * 2)) 

player_img.set_colorkey((0, 0, 0))

running = True
x = 0
clock = pygame.time.Clock()

delta_time = 0.1
while running:
    screen.fill((0, 0, 0))
    screen.blit(player_img, (x, 30))

    x += 50 * delta_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()