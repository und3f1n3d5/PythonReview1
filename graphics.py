import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
RED = (230, 50, 130)


def draw_board():
    pygame.init()
    f = open("labirynth.txt", "r")
    labirinth = f.readlines()
    screen = pygame.display.set_mode((900, 900))
    height = 800 // len(labirinth)
    length = 800 // len(labirinth[0])
    x = 10
    y = 10
    for line in labirinth:
        for j in range(len(line)):
            i = line[j]
            if i == "_":
                pygame.draw.aaline(screen, WHITE, [x - length, y + height], [min(800, x + 2 * length), y + height])
            if i == "|":
                if j < len(line) - 1 and line[j + 1] == '|':
                    pygame.draw.aaline(screen, WHITE, [x, y + height], [min(800, x + length), y + height])
                    pygame.draw.aaline(screen, WHITE, [x, y], [min(800, x + length), y])
                if j == len(line) - 2:
                    pygame.draw.aaline(screen, WHITE, [x + length, y], [x + length, y + height])
                else:
                    pygame.draw.aaline(screen, WHITE, [x, y], [x, y + height])
            if i == "#":
                pygame.draw.circle(screen, GREEN, (x, y + height // 2), 2 * length // 3)
            if i == "!":
                pygame.draw.circle(screen, RED, (x, y + height // 2), 2 * length // 3, length // 4)
            if i == "*":
                pygame.draw.circle(screen, YELLOW, (x - length // 3, y + height // 2), length // 5)
            if i == "\u0332":
                pygame.draw.aaline(screen, WHITE, [x - length, y + height], [min(800, x + 2*length), y + height])
                x -= length
            x += length
        x = 10
        y += height
    pygame.display.update()

