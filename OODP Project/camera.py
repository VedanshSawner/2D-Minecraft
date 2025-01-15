import pygame
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2()

    def update(self, player):
        self.offset.x = player.rect.centerx - self.width // 2
        self.offset.y = player.rect.centery - self.height // 2