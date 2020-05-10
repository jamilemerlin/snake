import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_RIGHT, K_LEFT)
from random import randint


# DIRECTIONS
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (120, 120, 120)


def random_position():
    x = randint(0, 590)
    y = randint(0, 790)
    return (x//10 * 10, y//10 * 10)


def random_position_list(size):
    position = []
    for p in range(size):
        position.append(random_position())
    return position


def collision(cell1, cell2):
    return cell1[0] == cell2[0] and cell1[1] == cell2[1]


def collision_list(cell, list):
    for item in list:
        if collision(cell, item):
            return True
    return False


def snake_collision(snake):
    for position in snake[1:]:
        if collision(snake[0], position):
            return False


pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Snake')

life = 3
score = 0
myfont = pygame.font.SysFont("monospace", 16)
snake = [(320, 400), (310, 400), (300, 400)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill(WHITE)
snake_direction = RIGHT

apple = pygame.Surface((10, 10))
apple.fill(RED)
apple_position = random_position()

stone = pygame.Surface((10, 10))
stone.fill(GRAY)
stones_position = random_position_list(10)

clock = pygame.time.Clock()

def add_score():
    global score
    score += 10


def snake_decrease_life():
    global life, snake, snake_direction
    life -= 1
    snake = [(320, 400), (310, 400), (300, 400)]
    snake_direction = RIGHT


def controls():
    global snake_direction
    for event in pygame.event.get():
        if event.type == QUIT:
            return False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            if event.key == K_UP:
                snake_direction = UP
            if event.key == K_DOWN:
                snake_direction = DOWN
            if event.key == K_RIGHT:
                snake_direction = RIGHT
            if event.key == K_LEFT:
                snake_direction = LEFT


while True:
    clock.tick(10)

    if controls() == False:
        break

    tail = snake.pop()

    if snake_direction == RIGHT:
        tail = (snake[0][0] + 10, snake[0][1])
    if snake_direction == LEFT:
        tail = (snake[0][0] - 10, snake[0][1])
    if snake_direction == UP:
        tail = (snake[0][0], snake[0][1] - 10)
    if snake_direction == DOWN:
        tail = (snake[0][0], snake[0][1] + 10)

    snake.insert(0, tail)

    if collision(snake[0], apple_position):
        apple_position = random_position()
        snake.append(snake[-1])
        add_score()

    if collision_list(snake[0], stones_position):
        snake_decrease_life()

    if (snake[0][0] < 0 or snake[0][0] > 590) or (snake[0][1] < 0 or snake[0][1] > 790):
        snake_decrease_life()

    if snake_collision(snake) == False:
        snake_decrease_life()

    if life == 0:
        break

    screen.fill(BLACK)
    screen.blit(apple, apple_position)

    for pos in snake:
        screen.blit(snake_skin, pos)
    for pos in stones_position:
        screen.blit(stone, pos)
    scoretext = myfont.render('SCORE:'+str(score), 1, (255, 255, 255))
    screen.blit(scoretext, (10, 10))
    lifetext = myfont.render('LIFE:'+str(life), 1, (255, 255, 255))
    screen.blit(lifetext, (520, 10))

    pygame.display.update()


pygame.quit()
