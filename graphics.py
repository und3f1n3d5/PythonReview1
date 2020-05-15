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
    width = 800 // len(labirinth[0])
    x = 10
    y = 10
    for line in labirinth:
        for j in enumerate(line):
            if j[1]== "_":
                pygame.draw.aaline(screen, WHITE, [x - width, y + height], [min(800, x + 2 * width), y + height])
            if j[1]== "|":
                if j[0] < len(line) - 1 and line[j + 1] == '|':
                    pygame.draw.aaline(screen, WHITE, [x, y + height], [min(800, x + width), y + height])
                    pygame.draw.aaline(screen, WHITE, [x, y], [min(800, x + width), y])
                if j[0] == len(line) - 2:
                    pygame.draw.aaline(screen, WHITE, [x + width, y], [x + width, y + height])
                else:
                    pygame.draw.aaline(screen, WHITE, [x, y], [x, y + height])
            if j[1] == "#":
                pygame.draw.circle(screen, GREEN, (x, y + height // 2), 2 * width // 3)
            if j[1] == "!":
                pygame.draw.circle(screen, RED, (x, y + height // 2), 2 * width // 3, width // 4)
            if j[1] == "*":
                pygame.draw.circle(screen, YELLOW, (x - width // 3, y + height // 2), width // 5)
            if j[1] == "\u0332":
                pygame.draw.aaline(screen, WHITE, [x - width, y + height], [min(800, x + 2*width), y + height])
                x -= width
            x += width
        x = 10
        y += height
    pygame.display.update()
