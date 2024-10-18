import pygame
import random
from player import Player
from obstacle import Obstacle
from database import Database
from settings import WIDTH, HEIGHT, WHITE, FPS, OBSTACLE_SPAWN_RATE
import time

# Инициализация pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game")

# Шрифт
font = pygame.font.Font(None, 36)

# ФПС
clock = pygame.time.Clock()

# Подключение к базе данных
db = Database("game_scores.db")

# Функция для запроса имени игрока
def get_player_name():
    name = ""
    input_active = True
    input_box = pygame.Rect(WIDTH // 3, HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        screen.fill(WHITE)
        txt_surface = font.render(name, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(FPS)
    return name

# Запрос имени игрока перед началом игры
player_name = get_player_name()

# Создание игрока
player = Player(player_name, WIDTH // 2, HEIGHT - 60)

# Список препятствий
obstacles = []

# Время для создания новых препятствий и отслеживание времени выживания
obstacle_timer = 0
start_time = time.time()  # Время начала игры

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем состояние клавиш
    keys = pygame.key.get_pressed()

    # Обновляем состояние игрока
    player.update(keys)

    # Спавн препятствий
    obstacle_timer += 1
    if obstacle_timer > OBSTACLE_SPAWN_RATE:
        obstacle_timer = 0
        # Создаем новое препятствие в случайной позиции по оси X
        obstacle = Obstacle(random.randint(0, WIDTH - 50), -50)
        obstacles.append(obstacle)

    # Обновляем положение всех препятствий
    for obstacle in obstacles:
        obstacle.update()
        # Проверяем на столкновение с игроком
        if obstacle.rect.colliderect(player.rect):
            end_time = time.time()  # Время окончания игры
            survival_time = round(end_time - start_time, 2)  # Вычисление времени выживания
            print("Game Over!")
            running = False  # Останавливаем игру при столкновении
            db.save_score(player_name, survival_time)  # Сохранение результата

    # Удаляем препятствия, которые вышли за нижнюю границу экрана
    obstacles = [obstacle for obstacle in obstacles if obstacle.rect.y < HEIGHT]

    # Обновление экрана
    screen.fill(WHITE)

    # Отрисовка игрока
    player.draw(screen)

    # Отрисовка препятствий
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Обновление дисплея
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(FPS)

# Показать топ-5 игроков после окончания игры
top_scores = db.get_top_scores(5)
screen.fill(WHITE)
y_offset = 100
screen.blit(font.render(f"Game Over! {player_name}'s score: {survival_time}s", True, (0, 0, 0)), (100, 50))
screen.blit(font.render("Top 5 Players:", True, (0, 0, 0)), (100, y_offset))
for i, (name, score) in enumerate(top_scores):
    y_offset += 50
    screen.blit(font.render(f"{i + 1}. {name} - {score}s", True, (0, 0, 0)), (100, y_offset))

pygame.display.flip()
pygame.time.wait(5000)  # Пауза на 5 секунд перед закрытием

# Закрытие базы данных и завершение Pygame
db.close()
pygame.quit()
