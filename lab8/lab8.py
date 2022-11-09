import pygame
from pygame.draw import *
from random import randint, sample

pygame.init()

FPS = 200
screen = pygame.display.set_mode((1200, 900))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
x = 100
y = 100
r = 50
dx = 1
dy = 1
last_ticks = 0
inp = True
clock = pygame.time.Clock()
finished = False
points = 0
circles = [(x, y, r, dx, dy)]
name = ""
down = False
loose = False


def draw_text(name: str):
    """Функция отрисосвывает текст на экране ввода имени.

           Args:
               name: Введенное с клавиатуры имя.
    """
    text = pygame.font.Font(None, 100).render('Ваше имя:',
                                              True, (255, 255, 255))
    screen.blit(text, (80, 300))
    text = pygame.font.Font(None, 100).render(name,
                                              True, (255, 255, 255))
    screen.blit(text, (80, 500))


def write_to_leaderboard(name: str, points: int):
    """Функция записывает в файл данные для таблицы leaderboard.txt.

               Args:
                   name: Введенное с клавиатуры имя.
                   points: Количество очков
    """
    with open('leaderboard.txt', 'rt', encoding='utf-8') as f:
        opener = f.readline()
        leaderboard = list(map(lambda a: [a[0], int(a[1])],
                               [i.split() for i in f.readlines()]))
    leaderboard.append([name if name else 'bahtovar', points])
    with open('leaderboard.txt', 'wt', encoding='utf-8') as f:
        opener += '\n'.join(map(lambda a: a[0].ljust(10, ' ') + '\t' + str(a[1]),
                                sorted(leaderboard, key=lambda a: a[1], reverse=True)))
        f.write(opener)


def balls_move(circles: list):
    """Функция отрисовывает шарики и задает взаимодействие с краями экрана.

         Args:
            circles: Массив, содеражщий информацию о всей созданных шариках(координаты, радиус, скорости).
    """
    for i in range(len(circles)):
        xi, yi, ri, dxi, dyi = circles[i]
        xi += dxi
        yi += dyi
        circle(screen, sample(COLORS, 1)[0], (xi, yi), ri)
        if xi >= 1150 or xi < 50:
            if xi > 1150:
                xi = 1150
            if xi < 50:
                xi = 50
            v = dxi ** 2 + dyi ** 2
            dxi = randint(1, int(v ** 0.5 * 100) - 1) * 0.01 * (abs(dxi) / dxi) * -1
            dyi = (v - dxi ** 2) ** 0.5 * (abs(dyi) / dyi)
        if yi >= 850 or yi < 50:
            if yi > 850:
                yi = 850
            if yi < 50:
                yi = 50
            v = dxi ** 2 + dyi ** 2
            dyi = randint(1, int(v ** 0.5 * 100) - 1) * 0.01 * (abs(dyi) / dyi) * -1
            dxi = (v - dyi ** 2) ** 0.5 * (abs(dxi) / dxi)
        circles[i] = [xi, yi, ri, dxi, dyi]


while not finished:
    clock.tick(FPS)
    if loose:
        text = pygame.font.Font(None, 100).render('Вы проиграли, ваш счет: ' + str(points),
                                                  True, (255, 255, 255))
        screen.blit(text, (200, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                write_to_leaderboard(name, points)
    else:
        if inp:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.KEYDOWN:
                    if 97 <= event.key <= 122 and len(name) < 10:
                        name += chr(event.key)
                    elif event.key == 8 and name:
                        down = True
                    elif event.key == 13:
                        inp = False
                elif event.type == pygame.KEYUP:
                    if event.key == 8:
                        down = False
            if down:
                cur_ticks = pygame.time.get_ticks()
                if cur_ticks - last_ticks >= 125:
                    name = name[:-1]
                    last_ticks = cur_ticks
            draw_text(name)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                    write_to_leaderboard(name, points)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x1, y1 = pygame.mouse.get_pos()
                    for i in range(len(circles)):
                        xc, yc, rc = circles[i][:3]
                        if ((x1 - xc) ** 2 + (y1 - yc) ** 2) ** 0.5 <= r:
                            del circles[i]
                            points += 1
                            break
                        else:
                            pass
            cur_ticks = pygame.time.get_ticks()
            if cur_ticks - last_ticks >= 2000:
                if len(circles) == 4:
                    loose = True
                dy += randint(1, 10) * 0.1 * (dy / abs(dy))
                dx += randint(1, 10) * 0.1 * (dx / abs(dx))
                dx *= sample([-1, 1], 1)[0]
                dy *= sample([-1, 1], 1)[0]
                circles.append([randint(100, 1100), randint(100, 800), 50, dx, dy])
                last_ticks = cur_ticks
            balls_move(circles)
            text = pygame.font.Font(None, 100).render('Счёт:' + str(points),
                                                      True, (255, 255, 255))
            screen.blit(text, (80, 300))
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
print('Количество очков', points)
