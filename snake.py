import pygame
from pygame.locals import *
from random import randint


# DIRECTIONS
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def random_position():
    x = randint(0, 500 // 20)
    y = randint(0, 700 // 20)
    return (x * 20, y * 20)

def random_position_list(size):
    position = []
    for p in range(size):
        position.append(random_position())
    return position

def random_apple_position(stones):
    apple_position = random_position()
    while True:
        for item in stones:
            if apple_position == item:
                apple_position = random_position()
            else:
                return apple_position

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
screen_width = 500
screen_height = 700
screen_center = (screen_width // 2, screen_height // 2)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')
all_image = pygame.image.load('./assets/snake-graphics.png')

life = 3
score = 0
myfont = pygame.font.SysFont("monospace", 16)
snake = [(280, 340), (260, 340), (240, 340)]
snake_direction = RIGHT

snake_head_up = all_image.subsurface(pygame.Rect(60, 0, 20, 20))
snake_head_down = all_image.subsurface(pygame.Rect(80, 20, 20, 20))
snake_head_left = all_image.subsurface(pygame.Rect(60, 20, 20, 20))
snake_head_right = all_image.subsurface(pygame.Rect(80, 0, 20, 20))

snake_tail_up = all_image.subsurface(pygame.Rect(60, 40, 20, 20))
snake_tail_down = all_image.subsurface(pygame.Rect(80, 60, 20, 20))
snake_tail_left = all_image.subsurface(pygame.Rect(60, 60, 20, 20))
snake_tail_right = all_image.subsurface(pygame.Rect(80, 40, 20, 20))

snake_body_hor = all_image.subsurface(pygame.Rect(20, 0, 20, 20))
snake_body_ver = all_image.subsurface(pygame.Rect(40, 20, 20, 20))

snake_body_top_left = all_image.subsurface(pygame.Rect(0, 0, 20, 20))
snake_body_top_right = all_image.subsurface(pygame.Rect(40, 0, 20, 20))
snake_body_bottom_left = all_image.subsurface(pygame.Rect(0, 20, 20, 20))
snake_body_bottom_right = all_image.subsurface(pygame.Rect(40, 40, 20, 20))

clock = pygame.time.Clock()

stones_position = random_position_list(10)
stone_image = all_image.subsurface(pygame.Rect(20, 60, 20, 20))

apple_position = random_apple_position(stones_position)
apple_image = all_image.subsurface(pygame.Rect(0, 60, 20, 20))


def add_score():
    global score
    score += 10


def snake_decrease_life():
    global life, snake, snake_direction
    life -= 1
    snake = [(280, 340), (260, 340), (240, 340)]
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
    clock.tick(7)

    if controls() == False:
        break

    tail = snake.pop()

    if snake_direction == RIGHT:
        tail = (snake[0][0] + 20, snake[0][1])
    if snake_direction == LEFT:
        tail = (snake[0][0] - 20, snake[0][1])
    if snake_direction == UP:
        tail = (snake[0][0], snake[0][1] - 20)
    if snake_direction == DOWN:
        tail = (snake[0][0], snake[0][1] + 20)

    snake.insert(0, tail)


    if collision_list(snake[0], stones_position):
        snake_decrease_life()

    if (snake[0][0] < 0 or snake[0][0] > screen_width - 20) or (snake[0][1] < 0 or snake[0][1] > screen_height - 20):
        snake_decrease_life()

    if snake_collision(snake) == False:
        snake_decrease_life()

    if collision(snake[0], apple_position):
        apple_position = random_apple_position(stones_position)
        snake.append(snake[-1])
        add_score()

    if life == 0:
        break

    screen.fill(BLACK)
    screen.blit(apple_image, apple_position)
    for i, pos in enumerate(snake):
        if i == 0:
            if snake_direction == RIGHT:
                screen.blit(snake_head_right, pos)
            if snake_direction == LEFT:
                screen.blit(snake_head_left, pos)
            if snake_direction == UP:
                screen.blit(snake_head_up, pos)
            if snake_direction == DOWN:
                screen.blit(snake_head_down, pos)
        elif i == len(snake)-1:
            tail = snake[i]
            last_body = snake[i - 1]
            if last_body == tail:
                last_body = snake[i - 2]
            if last_body[0] < tail[0]:
                screen.blit(snake_tail_left, pos)
            if last_body[0] > tail[0]:
                screen.blit(snake_tail_right, pos)
            if last_body[1] < tail[1]:
                screen.blit(snake_tail_up, pos)
            if last_body[1] > tail[1]:
                screen.blit(snake_tail_down, pos)
        else:
            mid_body = snake[i]
            next_body = snake[i + 1]
            prev_body = snake[i - 1]
            tail = snake[-1]
            mx = mid_body[0]
            my = mid_body[1]
            px = prev_body[0]
            py = prev_body[1]
            nx = next_body[0]
            ny = next_body[1]
            if mid_body == tail:
                continue
            elif prev_body[1] == next_body[1]:
                screen.blit(snake_body_hor, pos)
            elif prev_body[0] == next_body[0]:
                screen.blit(snake_body_ver, pos)
            elif (my == ny and mx > nx and mx == px and my < py) or (my == py and mx > px and mx == nx and my < ny):
                screen.blit(snake_body_top_right, pos)
            elif (my == ny and mx < nx and mx == px and my < py) or (my == py and mx < px and mx == nx and my < ny):
                screen.blit(snake_body_top_left, pos)
            elif (mx == nx and my > ny and my == py and mx > px) or (mx == px and my > py and my == ny and mx > nx):
                screen.blit(snake_body_bottom_right, pos)
            else:
                screen.blit(snake_body_bottom_left, pos)


    for pos in stones_position:
        screen.blit(stone_image, pos)


    scoretext = myfont.render('SCORE:'+str(score), 1, (255, 255, 255))
    screen.blit(scoretext, (10, 10))
    lifetext = myfont.render('LIFE:'+str(life), 1, (255, 255, 255))
    screen.blit(lifetext, (screen_width - 300, 10))
    quittext = myfont.render('ESC PARA SAIR', 1, (255, 255, 255))
    screen.blit(quittext, (screen_width - 140, 10))

    pygame.display.update()


pygame.quit()
