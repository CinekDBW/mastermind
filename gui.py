import random

import pygame
import main

SCREEN_WIDTH = 660
SCREEN_HEIGHT = 660

TILE_SIZE = 110

GRID_WIDTH = int(SCREEN_WIDTH / TILE_SIZE)
GRID_HEIGHT = int(SCREEN_HEIGHT / TILE_SIZE)

# Define some colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 125, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (125, 125, 25)
BLACK = (0, 0, 0)
BLUE_LAGOON = (0, 98, 111)
PURPLE = (255, 0, 255)


COLOR = {}
COLOR[0] = BLUE
COLOR[1] = GREEN
COLOR[2] = YELLOW
COLOR[3] = ORANGE
COLOR[4] = PURPLE
COLOR[5] = BLUE_LAGOON


def drawAttempts(n):
    pygame.font.init()

    font = pygame.font.SysFont(None, 80)

    text_surface = font.render(str(n), False, WHITE)

    window.blit(text_surface, (SCREEN_WIDTH-140,10))


def drawOriginalPattern(pattern):
    r = TILE_SIZE / 3

    x_pos = SCREEN_WIDTH/2 - 3 * r
    y_pos = TILE_SIZE/2
    pygame.draw.circle(window, COLOR[pattern[0]], (x_pos, y_pos), r)

    x_pos = SCREEN_WIDTH/2 - 1 * r
    y_pos = TILE_SIZE/2
    pygame.draw.circle(window, COLOR[pattern[1]], (x_pos, y_pos), r)

    x_pos = SCREEN_WIDTH/2 + 1 * r
    y_pos = TILE_SIZE/2
    pygame.draw.circle(window, COLOR[pattern[2]], (x_pos, y_pos), r)

    x_pos = SCREEN_WIDTH/2  + 3 * r
    y_pos = TILE_SIZE/2
    pygame.draw.circle(window, COLOR[pattern[3]], (x_pos, y_pos), r)

def drawScoreCircles(current_y, current_score):

    colors = [BLACK]*4

    for i in range(4):
        if i < current_score[0]:
            colors[i] = RED
        elif i < current_score[0] + current_score[1]:
            colors[i] = WHITE

    # lewy gorny
    s_c_x_pos = 4 * TILE_SIZE + TILE_SIZE / 4 + TILE_SIZE / 2
    s_c_y_pos = SCREEN_HEIGHT - current_y * TILE_SIZE - TILE_SIZE / 4 - TILE_SIZE / 2
    pygame.draw.circle(window, colors[0], (s_c_x_pos, s_c_y_pos), TILE_SIZE / 4 - 10)

    # prawy gorny
    s_c_x_pos = 4 * TILE_SIZE + TILE_SIZE / 4 + TILE_SIZE
    s_c_y_pos = SCREEN_HEIGHT - current_y * TILE_SIZE - TILE_SIZE / 4 - TILE_SIZE / 2
    pygame.draw.circle(window, colors[1], (s_c_x_pos, s_c_y_pos), TILE_SIZE / 4 - 10)

    # lewe dolne
    s_c_x_pos = 4 * TILE_SIZE + TILE_SIZE / 4 + TILE_SIZE/2
    s_c_y_pos = SCREEN_HEIGHT - current_y * TILE_SIZE - TILE_SIZE / 4
    pygame.draw.circle(window, colors[2], (s_c_x_pos, s_c_y_pos), TILE_SIZE / 4 - 10)

    #prawy dolny
    s_c_x_pos = 4 * TILE_SIZE + TILE_SIZE / 4 + TILE_SIZE
    s_c_y_pos = SCREEN_HEIGHT - current_y * TILE_SIZE - TILE_SIZE / 4
    pygame.draw.circle(window, colors[3], (s_c_x_pos, s_c_y_pos), TILE_SIZE / 4 - 10)




pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

main.init_all()
# guess_list, score_list, original_pattern = main.play_gui(main.knuth)
guess_list, score_list, original_pattern = main.play_gui(main.rng)

jump_size = 1
if(len(guess_list) > 20):
    jump_size = int(len(guess_list)/15)

clock = pygame.time.Clock()

has_reached_end = False

queue = []
curr_index = len(guess_list) - 1
queue.append(guess_list[-1])

while running:
    window.fill(BLACK)
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    for i in range(5):
        pygame.draw.line(window, COLOR[random.randint(0,5)], (0, (i + 1) * TILE_SIZE), (SCREEN_WIDTH, (i + 1) * TILE_SIZE))
    drawOriginalPattern(original_pattern)
    for i in range(len(queue)):
        for j in range(len(queue[i])): # tymczasowo zawsze 4
            circle_x_pos = int(j * TILE_SIZE + 0.5 * TILE_SIZE)
            circle_y_pos = int(SCREEN_HEIGHT - i * TILE_SIZE - 0.5 * TILE_SIZE)
            pygame.draw.circle(window, COLOR[guess_list[curr_index + jump_size * i][j]], (circle_x_pos, circle_y_pos), (TILE_SIZE/2)-10)

        drawScoreCircles(i, score_list[curr_index + jump_size * i])

    drawAttempts(len(guess_list) - curr_index)

    pygame.display.update()
    if not has_reached_end:
        if len(queue) >= 5:
            queue.pop()
        curr_index -= jump_size
        if curr_index <= 0:
            has_reached_end = True
            curr_index = 0
        queue.insert(0, guess_list[curr_index])

pygame.quit()