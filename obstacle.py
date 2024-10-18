import pygame
from settings import OBSTACLE_SPEED

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Размер препятствия 50x50 пикселей
        self.color = (255, 0, 0)  # Красный цвет препятствия

    def update(self):
        # Движение препятствия вниз
        self.rect.y += OBSTACLE_SPEED

    def draw(self, screen):
        # Отрисовка препятствия на экране
        pygame.draw.rect(screen, self.color, self.rect)
