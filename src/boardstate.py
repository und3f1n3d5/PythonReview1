import numpy as np
from typing import Optional, List

BDAME = -2
WDAME = 2
BLACK = -1
WHITE = 1
desk = {'0': 0, '1': 1, '2': 2, '3': -1, '4': -2}
desk1 = {0: '0', 1: '1', 2: '2', -1: '3', -2: '4'}


class BoardState:
    moves = []
    to_eat = [[], [], [], []]

    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def save(self):
        f = open("src/board.txt", 'w')
        for y in range(8):
            for x in range(8):
                f.write(desk1[self.board[y, x]])
            f.write('\n')
        f.close()

    def load(self):
        f = open("src/board.txt", 'r')

        import os
        if os.path.getsize('src/board.txt') == 0:
            self.initial_state()
        else:
            for y in range(8):
                s = f.readline()
                for x in range(8):
                    self.board[y, x] = desk[s[x]]
        f.close()

    def change_player(self):
        self.current_player *= -1

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def get_moves(self, x, y):
        self.moves = []
        self.to_eat = [[], [], [], []]
        if abs(self.board[y, x]) == 1:
            mvs = [[0, 2, 2], [1, -2, 2], [2, -2, -2], [3, 2, -2]]
            for k, i, j in mvs:
                if y + i < 8 and x + j < 8 and self.board[y + i // 2, x + j // 2] \
                        * self.current_player < 0 and self.board[y + i, x + j] == 0:
                    self.moves.append([y + i, x + j])
                    self.to_eat[k] = [y + i // 2, x + i // 2]
        else:
            mvs = [[0, 1, 1], [1, -1, 1], [2, 1, -1], [3, -1, -1]]
            for k, dx, dy in mvs:
                i = 1
                while y + dy * i < 8 and x + dx * i < 8 and self.board[y + dy * i, x + dx * i] \
                        * self.current_player >= 0 and self.board[y + dy * i, x + dx * i] == 0:
                    i += 1
                if y + i * dy < 7 and x + i * dx < 7 and self.board[y + i * dy, x + i * dx] \
                        * self.current_player < 0 and self.board[y + (i + 1) * dy, x + (i + 1) * dx] == 0:
                    self.moves.append([y + (i + 1) * dy, x + (i + 1) * dx])
                    self.to_eat[0] = [y + i * dy, x + i * dx]

    def eat_up(self, from_x, from_y, to_x, to_y):
        if [to_y, to_x] in self.moves:
            result = self.copy()
            result.board[to_y, to_x] = result.board[from_y, from_x]
            if self.board[from_y, from_x] == WHITE and to_y == 0:
                result.board[to_y, to_x] += 1
            if self.board[from_y, from_x] == BLACK and to_y == 7:
                result.board[to_y, to_x] -= 1
            result.board[from_y, from_x] = 0
            if from_y < to_y and from_x < to_x:
                result.board[self.to_eat[0][0], self.to_eat[0][1]] = 0
            if from_y > to_y and from_x < to_x:
                result.board[self.to_eat[1][0], self.to_eat[1][1]] = 0
            if from_y < to_y and from_x > to_x:
                result.board[self.to_eat[3][0], self.to_eat[3][1]] = 0
            if from_y > to_y and from_x > to_x:
                result.board[self.to_eat[2][0], self.to_eat[2][1]] = 0
            return result
        else:
            return None

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:

        if from_x == to_x and from_y == to_y:
            return None  # invalid move

        if (to_x + to_y) % 2 == 0:
            return None

        if self.board[to_y, to_x] != 0:
            return None

        if self.board[from_y, from_x] == WDAME or self.board[from_y, from_x] == BDAME:
            result = self.copy()
            dx = 1 if to_x > from_x else -1
            dy = 1 if to_y > from_y else -1
            x, y = from_x, from_y
            while x != to_x:
                x += dx
                y += dy
                if self.board[y, x] != 0:
                    return None
            result.board[to_y, to_x] = result.board[from_y, from_x]
            result.board[from_y, from_x] = 0
        else:
            if self.board[from_y, from_x] == WHITE and self.current_player == 1:
                if to_y == from_y - 1 and abs(to_x - from_x) <= 1:
                    result = self.copy()
                    result.board[to_y, to_x] = result.board[from_y, from_x]
                    if to_y == 0:
                        result.board[to_y, to_x] += 1
                    result.board[from_y, from_x] = 0
                else:
                    return None
            elif self.board[from_y, from_x] == BLACK and self.current_player == -1:
                if to_y == from_y + 1 and abs(to_x - from_x) <= 1:
                    result = self.copy()
                    result.board[to_y, to_x] = result.board[from_y, from_x]
                    if to_y == 7:
                        result.board[to_y, to_x] -= 1
                    result.board[from_y, from_x] = 0
                else:
                    return None
            else:
                return None
        return result

    def move_white(self, x, y, just_moves):
        for dx in (-1, 1):
            if 8 > x + dx > -1 and y - 1 > -1 and self.board[y - 1, x + dx] == 0:
                state = self.copy()
                state.board[y - 1, x + dx] = state.board[y, x]
                if y == 1:
                    state.board[y - 1, x + dx] += 1
                state.board[y, x] = 0
                just_moves.append(state)

    def move_black(self, x, y, just_moves):
        for dx in (-1, 1):
            if 8 > x + dx > -1 and y + 1 < 8 and self.board[y + 1, x + dx] == 0:
                state = self.copy()
                state.board[y + 1, x + dx] = state.board[y, x]
                if y == 6:
                    state.board[y + 1, x + dx] += 1
                state.board[y, x] = 0
                just_moves.append(state)

    def move_with_dame(self, x, y, just_moves):
        mv = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        for dx, dy in mv:
            x1 = x
            y1 = y
            while -1 < x1 + dx < 8 and -1 < y1 + dy < 8 and self.board[y1 + dy, x1 + dx] == 0:
                x1 += dx
                y1 += dy
                state = self.copy()
                state.board[y1, x1] = state.board[y, x]
                state.board[y, x] = 0
                just_moves.append(state)

    def ai_move(self, x, y):
        just_moves = []
        if self.board[y, x] == BLACK and self.current_player == -1:
            self.move_black(x, y, just_moves)
        if self.board[y, x] == WHITE and self.current_player == 1:
            self.move_white(x, y, just_moves)
        if (self.board[y, x] == WDAME and self.current_player == 1) or (
                self.board[y, x] == BDAME and self.current_player == -1):
            self.move_with_dame(x, y, just_moves)
        return just_moves

    def eat_with_usual(self, x, y, ai_bites, n):
        m = True
        mv = [[2, 2], [-2, -2], [-2, 2], [2, -2]]
        for dx, dy in mv:
            if -1 < x + dx < 8 and -1 < y + dy < 8 and self.board[y + dy/2, x + dx/2]\
                    * self.current_player < 0 and self.board[y + dy, x + dx] == 0:
                m = False
                self.board[y + dy, x + dx] = self.board[y, x]
                self.board[y, x] = 0
                k = self.board[y + dy/2, x + dx/2]
                self.board[y + dy/2, x + dx/2] = 0
                if y + dy == 7 and k == WHITE:
                    self.board[y + dy, x + dx] -= 1
                if y + dy == 0 and k == BLACK:
                    self.board[y + dy, x + dx] += 1
                self.ai_eat(y + dy, x + dx, ai_bites, n + 1)
                self.board[y, x] = self.board[y + 2, x + 2]
                self.board[y + dy/2, x + dx/2] = k
                self.board[y + dy, x + dx] = 0
        if m and n > 0:
            ai_bites.append(self.copy())

    def eat_with_dame(self, x, y, ai_bites, n):
        m = True
        mv = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        for dx, dy in mv:
            i = 1
            while -1 < x + dx*i < 8 and -1 < y + dy*i < 8 and self.board[y + dy*i, x + dx*i] == 0:
                i += 1
            if 0 < x + dx*i < 7 and 0 < y + dy*i < 7 and self.board[y + dy*i, x + dx*i] * self.current_player < 0:
                if self.board[y + dy*(i + 1), x + dx*(i + 1)] == 0:
                    m = False
                    self.board[y + dy*(i + 1), x + dx*(i + 1)] = self.board[y, x]
                    self.board[y, x] = 0
                    k = self.board[y + dy*i, x + dx*i]
                    self.board[y + dy*i, x + dx*i] = 0
                    self.ai_eat(x + dx*(i + 1), y + dy*(i + 1), ai_bites, n + 1)
                    self.board[y, x] = self.board[y + dy*(i + 1), x + dx*(i + 1)]
                    self.board[y + dy*i, x + dx*i] = k
                    self.board[y + dy*i, x + dx*i] = 0
        if m and n > 0:
            ai_bites.append(self.copy())

    def ai_eat(self, x, y, ai_bites, n=0):
        if (self.board[y, x] == WHITE and self.current_player == 1) or (
                self.board[y, x] == BLACK and self.current_player == -1):
            self.eat_with_usual(x, y, ai_bites, n)
        if (self.board[y, x] == WDAME and self.current_player == 1) or (
                self.board[y, x] == BDAME and self.current_player == -1):
            self.eat_with_dame(x, y, ai_bites, n)

    def get_possible_moves(self) -> List['BoardState']:
        just_moves = []
        ai_bites = []
        for x in range(8):
            for y in range(8):
                if self.board[y, x] != 0:
                    self.ai_eat(x, y, ai_bites)
                    if len(ai_bites) == 0:
                        j_moves = self.ai_move(x, y)
                        for i in j_moves:
                            just_moves.append(i)
        # self.ai_eat(7, 2, ai_bites)
        if len(ai_bites) != 0:
            return ai_bites
        return just_moves

    @property
    def is_game_finished(self) -> bool:
        k = self.get_possible_moves()
        res = (len(k) == 0)
        if not res:
            self.current_player *= -1
            res = (len(self.get_possible_moves()) == 0)
            self.current_player *= -1
        return res

    @property
    def get_winner(self) -> Optional[int]:
        res = (len(self.get_possible_moves()) == 0)
        if res:
            return self.current_player * -1
        return self.current_player

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)
        # дамка = 2, шашка = 1, черные = -1 и -2
        for i in range(7, 4, -1):
            for j in range((i + 1) % 2, 8, 2):
                board[i, j] = 1

        for i in range(2, -1, -1):
            for j in range((i + 1) % 2, 8, 2):
                board[i, j] = -1

        return BoardState(board, 1)
