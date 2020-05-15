import random
from collections import namedtuple
from enum import Enum
import sys
import graphics
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
RED = (230, 50, 130)


class Go(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


Coord = namedtuple('Coord', 'x y')
Element = namedtuple('Element', 'x y direction')
DetailedElement = namedtuple('DetailedElement', 'matrix_element x y direction')
Starter = namedtuple('Starter', 'mode length width')


def mark_start(start):
    start.start()


def mark_finish(last):
    last[0].finish()


def greeting():
    print("Maze generator: start")
    print("Enter its size:")
    print("length: ")
    length = int(input())
    print("width: ")
    width = int(input())
    mode = 1
    starter = Starter(mode=mode, length=length, width=width)
    return starter


class Cell:  # We're drawing labyrinth with cells
    low_string = "_"  # initially each one is "walled"
    left_string = "|"
    right_string = "|"
    is_visited = False
    distance = 0
    UNDERLINED_HASH = "\u0332#"
    UNDERLINED_EXCLAMATION = "\u0332!"
    UNDERLINED_STAR = "\u0332*"

    def __str__(self):
        return self.left_string + self.low_string + self.right_string

    def routeMark(self):  # as part of the route between start and finish
        if self.low_string == self.UNDERLINED_HASH or self.low_string == "#" or \
                self.low_string == self.UNDERLINED_EXCLAMATION or self.low_string == "!":
            pass
        else:
            if self.low_string == "_":
                self.low_string = self.UNDERLINED_STAR
            elif self.low_string == " ":
                self.low_string = "*"

    def start(self):  # marking as start
        self.low_string = self.UNDERLINED_HASH

    def finish(self):  # as finish
        if self.low_string == "_":
            self.low_string = self.UNDERLINED_EXCLAMATION
        else:
            self.low_string = "!"

    def deleteLeft(self):
        self.left_string = " "

    def deleteRight(self):
        self.right_string = " "

    def deleteLower(self):  # crashing particular walls
        if self.low_string == self.UNDERLINED_HASH:
            self.low_string = "#"
        elif self.low_string == self.UNDERLINED_EXCLAMATION:
            self.low_string = "!"
        else:
            self.low_string = " "


def checkBack(matrix, stack):
    cur = stack.pop()
    while visited(getNeighbours(cur, matrix)) and len(stack) > 0:
        cur = stack.pop()
    while not (visited(getNeighbours(cur, matrix))):
        last = cur
        cur = random.choice(
            [el for el in getNeighbours(cur, matrix) if not el[0].is_visited])
        matrix[cur[1]][cur[2]].is_visited = True
        if cur[3] == Go.LEFT:
            last[0].deleteLeft()
            cur[0].deleteRight()
        elif cur[3] == Go.RIGHT:
            last[0].deleteRight()
            cur[0].deleteLeft()
        elif cur[3] == Go.DOWN:
            last[0].deleteLower()
        else:
            cur[0].deleteLower()
        stack.append(cur)


def generateRoute(cur, matrix, stack, way):
    while not (visited(getNeighbours(cur, matrix))):
        last = cur
        cur = random.choice([el for el in getNeighbours(cur, matrix) if not el[0].is_visited])
        matrix[cur[1]][cur[2]].is_visited = True
        if cur[3] == Go.LEFT:
            last[0].deleteLeft()
            cur[0].deleteRight()
        elif cur[3] == Go.RIGHT:
            last[0].deleteRight()
            cur[0].deleteLeft()
        elif cur[3] == Go.DOWN:
            last[0].deleteLower()
        else:
            cur[0].deleteLower()
        stack.append(cur)
        way.append((cur[1], cur[2]))


def getNeighbours(current, matrix):
    x = current[1]
    y = current[2]
    neighbours = []
    if x > 0:
        up_de = DetailedElement(matrix_element=matrix[x - 1][y], x=x - 1, y=y, direction=Go.UP)
        neighbours.append(up_de)
    if x < len(matrix) - 1:
        down_de = DetailedElement(matrix_element=matrix[x + 1][y], x=x + 1, y=y, direction=Go.DOWN)
        neighbours.append(down_de)
    if y > 0:
        left_de = DetailedElement(matrix_element=matrix[x][y - 1], x=x, y=y - 1, direction=Go.LEFT)
        neighbours.append(left_de)
    if y < len(matrix[0]) - 1:
        right_de = DetailedElement(matrix_element=matrix[x][y + 1], x=x, y=y + 1, direction=Go.RIGHT)
        neighbours.append(right_de)
    return neighbours


def visited(neighbours):
    for each in neighbours:
        if not each[0].is_visited:
            return False
    return True


def dfsGenerator(starter):
    matrix = [[Cell() for n in range(starter[2])] for m in range(starter[1])]
    random.seed(version=2)
    matrix[0][0].start()
    current = (matrix[0][0], 0, 0)
    matrix[current[1]][current[2]].is_visited = True
    route_stack = [current]
    way = [(current[1], current[2])]
    while not (visited(getNeighbours(current, matrix))):
        generateRoute(current, matrix, route_stack, way)
    route_stack[len(route_stack) - 1][0].finish()
    while len(route_stack) > 0:
        checkBack(matrix, route_stack)
    print("dfsGenerator: Done")
    return matrix, way


def showRoute(matrix, way):
    for elem in way:
        matrix[elem[0]][elem[1]].routeMark()  # marking the route
    print(" _ " * len(matrix[0]))
    for m in range(len(matrix)):
        for k in range(len(matrix[m])):
            print(matrix[m][k], end="")
        print()


# main

starters = greeting()
labyrinth, route = dfsGenerator(starters)
f = open("labirynth.txt", "w")
std = sys.stdout
f.seek(0)
sys.stdout = f
print(" _ " * len(labyrinth[0]))
for line in labyrinth:
    for elem in line:
        print(elem, end="")
    print()
f.close()
f = open("labirynth.txt", "r")
graphics.draw_board()
f.close()
f = open("labirynth.txt", "w")
sys.stdout = std
print("Show route? yes : no")
if input() == "yes":
    f.seek(0)
    sys.stdout = f
    showRoute(labyrinth, route)
    f.close()
    f = open("labirynth.txt", "r")
    graphics.draw_board()
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
