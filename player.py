import pygame
from settings import PLAYER_SPEED

class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 50, 50)  # Размер игрока 50x50 пикселей
        self.color = (0, 128, 255)  # Синий цвет игрока

    def update(self, keys):
        # Движение игрока по осям X и Y
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Ограничиваем движение игрока в пределах экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 750:  # Ширина экрана минус ширина игрока
            self.rect.x = 750
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 550:  # Высота экрана минус высота игрока
            self.rect.y = 550

    def draw(self, screen):
        # Отрисовка игрока на экране
        pygame.draw.rect(screen, self.color, self.rect)
