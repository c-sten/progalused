import pygame
import tkinter as tk
from tkinter import messagebox
pygame.init()

LAIUS, KORGUS = 640, 480
SUURUS = 40
VALGE = (255, 255, 255)
MUST = (0, 0, 0)
HALL = (128, 128, 128)
PLAYER_COLOR = (0, 128, 255)
BOX_COLOR = (255, 165, 0)
TARGET_COLOR = (0, 255, 0)
COMPLETED_BOX_COLOR = (0, 128, 0)

levels = [
    [
        "################",
        "#@      $     . ",
        "# ###########  #",
        "#         $    #",
        "#  #############",
        "#  #########  .#",
        "#.    $        #",
        "#############  #",
        "#.      $      #",
        "#   ############",
        "#            $.#",
        "################",
    ],
    [
        "################",
        "################",
        "#######  #######",
        "###### * #######",
        "###### *$ ######",
        "###### .  ######",
        "###### # #######",
        "###### @ #######",
        "################",
        "################",
        "################",
        "################",
    ],
    [
        "################",
        "################",
        "########  ######",
        "########$ ######",
        "######  *  #####",
        "######  * @#####",
        "######  * ######",
        "########* ######",
        "########.#######",
        "################",
        "################",
        "################",
    ],
]

lv = 0
player_pos = [0, 0]
boxes = []
targets = []

game_start_time = pygame.time.get_ticks()

def load_level(level_index):
    global player_pos, boxes, targets
    boxes = []
    targets = []
    level = levels[level_index]
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            if cell == "@":
                player_pos = [x, y]
            elif cell == "$":
                boxes.append([x, y])
            elif cell == ".":
                targets.append([x, y])
            elif cell == "*":
                boxes.append([x, y])
                targets.append([x, y])

def kontrolli():
    for box in boxes:
        if box not in targets:
            return False
    return True

def move(dx, dy):
    global player_pos
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if levels[lv][new_y][new_x] == "#":
        return
    if [new_x, new_y] in boxes:
        box_new_x = new_x + dx
        box_new_y = new_y + dy
        if levels[lv][box_new_y][box_new_x] == "#" or [box_new_x, box_new_y] in boxes:
            return
        boxes[boxes.index([new_x, new_y])] = [box_new_x, box_new_y]
    player_pos[0] = new_x
    player_pos[1] = new_y

def restart_level():
    load_level(lv)

screen = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("Sokoban")
clock = pygame.time.Clock()
load_level(lv)

running = True
while running:
    screen.fill(VALGE)
    elapsed_game_time_ms = pygame.time.get_ticks() - game_start_time
    elapsed_game_time_s = elapsed_game_time_ms // 1000
    minutes = elapsed_game_time_s // 60
    seconds = elapsed_game_time_s % 60
    pygame.display.set_caption(f"Sokoban - Aeg: {minutes}:{seconds:02d}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(0, -1)
            elif event.key == pygame.K_DOWN:
                move(0, 1)
            elif event.key == pygame.K_LEFT:
                move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move(1, 0)
            elif event.key == pygame.K_r:
                restart_level()
            if kontrolli():
                if lv < len(levels) - 1:
                    lv += 1
                    load_level(lv)
                else:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo("Õnnitlused!", f"Lõpetasite mängu ajaga: {minutes}:{seconds:02d}!")
                    running = False

    for y, row in enumerate(levels[lv]):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * SUURUS, y * SUURUS, SUURUS, SUURUS)
            pygame.draw.rect(screen, HALL if cell == "#" else VALGE, rect)
            pygame.draw.rect(screen, MUST, rect, 1)

    for target in targets:
        rect = pygame.Rect(target[0] * SUURUS, target[1] * SUURUS, SUURUS, SUURUS)
        pygame.draw.rect(screen, TARGET_COLOR, rect)

    for box in boxes:
        rect = pygame.Rect(box[0] * SUURUS, box[1] * SUURUS, SUURUS, SUURUS)
        color = COMPLETED_BOX_COLOR if box in targets else BOX_COLOR
        pygame.draw.rect(screen, color, rect)

    player_rect = pygame.Rect(player_pos[0] * SUURUS, player_pos[1] * SUURUS, SUURUS, SUURUS)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    pygame.display.flip()

pygame.quit()
