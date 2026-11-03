import pygame
import random

class Orb:
    def __init__(self, x, y):
        center = pygame.Vector2(320 + random.randint(-100, 100), 320 + random.randint(-100, 100))
        self.pos = pygame.Vector2(x, y)
        self.color = (random.randint(100, 255), random.randint(100, 255), 255)

        self.direction = (center - self.pos).normalize()
        self.direction.x = (self.direction.x + (random.random() * 0.4 - 0.2))
        self.direction.y = (self.direction.y + (random.random() * 0.4 - 0.2))
        self.direction = self.direction.normalize()
        
        self.vel = self.direction * random.uniform(1, 3)
        self.radius = random.randint(10, 20)

    def update(self):
        self.pos += self.vel

    def check_collision(self, point):
        distance = self.pos.distance_to(point)
        if distance < self.radius:
            return True
        else:
            return False
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)