import numpy as np
from typing import Optional, List

BDAME = -2
WDAME = 2
BLACK = -1
WHITE = 1


class BoardState:
    moves = []
    to_eat = [[], [], [], []]

    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

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
            i = 2
            if y + i < 8 and x + i < 8 and self.board[y + 1, x + 1] * self.current_player < 0 and self.board[
                y + 2, x + 2] == 0:
                self.moves.append([y + 2, x + 2])
                self.to_eat[0] = [y + 1, x + 1]
            elif y - i > -1 and x + i < 8 and self.board[y - 1, x + 1] * self.current_player < 0 and self.board[
                y - 2, x + 2] == 0:
                self.moves.append([y - 2, x + 2])
                self.to_eat[1] = [y - 1, x + 1]
            elif y + i < 8 and x - i > -1 and self.board[y + 1, x - 1] * self.current_player < 0 and self.board[
                y + 2, x - 2] == 0:
                self.moves.append([y + 2, x - 2])
                self.to_eat[3] = [y + 1, x - 1]
            elif y - i > -1 and x - i > -1 and self.board[y - 1, x - 1] * self.current_player < 0 and self.board[
                y - 2, x - 2] == 0:
                self.moves.append([y - 2, x - 2])
                self.to_eat[2] = [y - 1, x - 1]
        else:
            i = 1
            while y + i < 8 and x + i < 8 and self.board[y + i, x + i] * self.current_player >= 0 and self.board[
                y + i, x + i] == 0:
                i += 1
            if y + i < 7 and x + i < 7 and self.board[y + i, x + i] * self.current_player < 0 and self.board[
                y + i + 1, x + i + 1] == 0:
                self.moves.append([y + i + 1, x + i + 1])
                self.to_eat[0] = [y + i, x + i]
            i = 1
            while y - i > -1 and x + i < 8 and self.board[y - i, x + i] * self.current_player >= 0 and self.board[
                y - i, x + i] == 0:
                i += 1
            if y - i > 0 and x + i < 7 and self.board[y - i, x + i] * self.current_player < 0 and self.board[
                y - i - 1, x + i + 1] == 0:
                self.moves.append([y - i - 1, x + i + 1])
                self.to_eat[1] = [y - i, x + i]
            i = 1
            while y + i < 8 and x - i > -1 and self.board[y + i, x - i] * self.current_player >= 0 and self.board[
                y + i, x - i] == 0:
                i += 1
            if y + i < 7 and x - i > 0 and self.board[y + i, x - i] * self.current_player < 0 and self.board[
                y + i + 1, x - i - 1] == 0:
                self.moves.append([y + i + 1, x - i - 1])
                self.to_eat[3] = [y + i, x - i]
            i = 1
            while y - i > -1 and x - i > -1 and self.board[y - i, x - i] * self.current_player >= 0 and self.board[
                y - i, x - i] == 0:
                i += 1
            if y - i > 0 and x - i > 0 and self.board[y - i, x - i] * self.current_player < 0 and self.board[
                y - i - 1, x - i - 1]:
                self.moves.append([y - i - 1, x - i - 1])
                self.to_eat[2] = [y - i, x - i]

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
            if from_y < to_y and from_x < to_x:
                x, y = from_x, from_y
                while x != to_x:
                    x += 1
                    y += 1
                    if self.board[y, x] != 0:
                        return None
            if from_y > to_y and from_x < to_x:
                x, y = from_x, from_y
                while x != to_x:
                    x += 1
                    y -= 1
                    if self.board[y, x] != 0:
                        return None
            if from_y < to_y and from_x > to_x:
                x, y = from_x, from_y
                while x != to_x:
                    x -= 1
                    y += 1
                    if self.board[y, x] != 0:
                        return None
            if from_y > to_y and from_x > to_x:
                x, y = from_x, from_y
                while x != to_x:
                    x -= 1
                    y -= 1
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

    def ai_move(self, x, y):
        just_moves = []
        if self.board[y, x] == BLACK and self.current_player == -1:
            if x + 1 < 8 and y + 1 < 8 and self.board[y + 1, x + 1] == 0:
                state = self.copy()
                state.board[y + 1, x + 1] = state.board[y, x]
                if y == 6:
                    state.board[y + 1, x + 1] -= 1
                state.board[y, x] = 0
                just_moves.append(state)
            if x - 1 > -1 and y + 1 < 8 and self.board[y + 1, x - 1] == 0:
                state = self.copy()
                state.board[y + 1, x - 1] = state.board[y, x]
                if y == 6:
                    state.board[y + 1, x - 1] -= 1
                state.board[y, x] = 0
                just_moves.append(state)
        if self.board[y, x] == WHITE and self.current_player == 1:
            if x + 1 < 8 and y - 1 > -1 and self.board[y - 1, x + 1] == 0:
                state = self.copy()
                state.board[y - 1, x + 1] = state.board[y, x]
                if y == 1:
                    state.board[y - 1, x + 1] += 1
                state.board[y, x] = 0
                just_moves.append(state)
            if x - 1 > -1 and y - 1 > -1 and self.board[y - 1, x - 1] == 0:
                state = self.copy()
                state.board[y - 1, x - 1] = state.board[y, x]
                if y == 1:
                    state.board[y - 1, x - 1] += 1
                state.board[y, x] = 0
                just_moves.append(state)
        if (self.board[y, x] == WDAME and self.current_player == 1) or (
                self.board[y, x] == BDAME and self.current_player == -1):
            x1 = x
            y1 = y
            while x1 + 1 < 8 and y1 + 1 < 8 and self.board[y1 + 1, x1 + 1] == 0:
                x1 += 1
                y1 += 1
                state = self.copy()
                state.board[y1, x1] = state.board[y, x]
                state.board[y, x] = 0
                just_moves.append(state)
            while x1 - 1 > -1 and y1 + 1 < 8 and self.board[y1 + 1, x1 - 1] == 0:
                x1 -= 1
                y1 += 1
                state = self.copy()
                state.board[y1, x1] = state.board[y, x]
                state.board[y, x] = 0
                just_moves.append(state)
            while x1 + 1 < 8 and y1 - 1 > -1 and self.board[y1 - 1, x1 + 1] == 0:
                x1 += 1
                y1 -= 1
                state = self.copy()
                state.board[y1, x1] = state.board[y, x]
                state.board[y, x] = 0
                just_moves.append(state)
            while x1 - 1 > -1 and y1 - 1 > -1 and self.board[y1 - 1, x1 - 1] == 0:
                x1 -= 1
                y1 -= 1
                state = self.copy()
                state.board[y1, x1] = state.board[y, x]
                state.board[y, x] = 0
                just_moves.append(state)
        return just_moves

    def ai_eat(self, x, y, ai_bites, n=0):
        if (self.board[y, x] == WHITE and self.current_player == 1) or (
                self.board[y, x] == BLACK and self.current_player == -1):
            m = True
            if x + 2 < 8 and y + 2 < 8 and self.board[y + 1, x + 1] * self.current_player < 0 and self.board[
                y + 2, x + 2] == 0:
                m = False
                self.board[y + 2, x + 2] = self.board[y, x]
                self.board[y, x] = 0
                k = self.board[y + 1, x + 1]
                self.board[y + 1, x + 1] = 0
                if y + 2 == 7 and k == WHITE:
                    self.board[y + 2, x + 2] -= 1
                self.ai_eat(x + 2, y + 2, ai_bites, n + 1)
                self.board[y, x] = self.board[y + 2, x + 2]
                self.board[y + 1, x + 1] = k
                self.board[y + 2, x + 2] = 0
            if x + 2 < 8 and y - 2 > -1 and self.board[y - 1, x + 1] * self.current_player < 0 and self.board[
                y - 2, x + 2] == 0:
                m = False
                self.board[y - 2, x + 2] = self.board[y, x]
                self.board[y, x] = 0
                k = self.board[y - 1, x + 1]
                self.board[y - 1, x + 1] = 0
                if y - 2 == 0 and k == BLACK:
                    self.board[y - 2, x + 2] += 1
                self.ai_eat(x + 2, y - 2, ai_bites, n + 1)
                self.board[y - 1, x + 1] = k
                self.board[y, x] = self.board[y - 2, x + 2]
                self.board[y - 2, x + 2] = 0
            if x - 2 > -1 and y + 2 < 8 and self.board[y + 1, x - 1] * self.current_player < 0 and self.board[
                y + 2, x - 2] == 0:
                m = False
                self.board[y + 2, x - 2] = self.board[y, x]
                self.board[y, x] = 0
                k = self.board[y + 1, x - 1]
                self.board[y + 1, x - 1] = 0
                if y + 2 == 7 and k == WHITE:
                    self.board[y + 2, x - 2] -= 1
                self.ai_eat(x - 2, y + 2, ai_bites, n + 1)
                self.board[y + 1, x - 1] = k
                self.board[y, x] = self.board[y + 2, x - 2]
                self.board[y + 2, x - 2] = 0
            if x - 2 > -1 and y - 2 > -1 and self.board[y - 1, x - 1] * self.current_player < 0 and self.board[
                y - 2, x - 2] == 0:
                m = False
                self.board[y - 2, x - 2] = self.board[y, x]
                self.board[y, x] = 0
                k = self.board[y - 1, x - 1]
                self.board[y - 1, x - 1] = 0
                if y - 2 == 0 and k == BLACK:
                    self.board[y - 2, x - 2] += 1
                self.ai_eat(x - 2, y - 2, ai_bites, n + 1)
                self.board[y - 1, x - 1] = k
                self.board[y, x] = self.board[y - 2, x - 2]
                self.board[y - 2, x - 2] = 0
            if m and n > 0:
                ai_bites.append(self.copy())
        if (self.board[y, x] == WDAME and self.current_player == 1) or (
                self.board[y, x] == BDAME and self.current_player == -1):
            m = True
            i = 1
            while x + i < 8 and y + i < 8 and self.board[y + i, x + i] == 0:
                i += 1
            if x + i < 7 and y + i < 7 and self.board[y + i, x + i] * self.current_player < 0:
                if self.board[y + i + 1, x + i + 1] == 0:
                    m = False
                    self.board[y + i + 1, x + i + 1] = self.board[y, x]
                    self.board[y, x] = 0
                    k = self.board[y + i, x + i]
                    self.board[y + i, x + i] = 0
                    self.ai_eat(x + i + 1, y + i + 1, ai_bites, n + 1)
                    self.board[y, x] = self.board[y + i + 1, x + i + 1]
                    self.board[y + i, x + i] = k
                    self.board[y + i + 1, x + i + 1] = 0
            i = 1
            while x - i > -1 and y + i < 8 and self.board[y + i, x - i] == 0:
                i += 1
            if x - i > 0 and y + i < 7 and self.board[y + i, x - i] * self.current_player < 0:
                if self.board[y + i + 1, x - i - 1] == 0:
                    m = False
                    self.board[y + i + 1, x - i - 1] = self.board[y, x]
                    self.board[y, x] = 0
                    k = self.board[y + i, x - i]
                    self.board[y + i, x - i] = 0
                    self.ai_eat(x - i - 1, y + i + 1, ai_bites, n + 1)
                    self.board[y, x] = self.board[y + i + 1, x - i - 1]
                    self.board[y + i, x - i] = k
                    self.board[y + i + 1, x - i - 1] = 0
            i = 1
            while x + i < 8 and y - i > -1 and self.board[y - i, x + i] == 0:
                i += 1
            if x + i < 7 and y - i > 0 and self.board[y - i, x + i] * self.current_player < 0:
                if self.board[y - i - 1, x + i + 1] == 0:
                    m = False
                    self.board[y - i - 1, x + i + 1] = self.board[y, x]
                    self.board[y, x] = 0
                    k = self.board[y - i, x + i]
                    self.board[y - i, x + i] = 0
                    self.ai_eat(x + i + 1, y - i - 1,  ai_bites, n + 1)
                    self.board[y, x] = self.board[y - i - 1, x + i + 1]
                    self.board[y - i, x + i] = k
                    self.board[y - i - 1, x + i + 1] = 0
            i = 1
            while x - i > -1 and y - i > -1 and self.board[y - i, x - i] == 0:
                i += 1
            if x - i > 0 and y - i > 0 and self.board[y - i, x - i] * self.current_player < 0:
                if self.board[y - i - 1, x - i - 1] == 0:
                    m = False
                    self.board[y - i - 1, x - i - 1] = self.board[y, x]
                    self.board[y, x] = 0
                    k = self.board[y - i, x - i]
                    self.board[y - i, x - i] = 0
                    self.ai_eat(x - i - 1, y - i - 1, ai_bites, n + 1)
                    self.board[y, x] = self.board[y - i - 1, x - i - 1]
                    self.board[y - i, x - i] = k
                    self.board[y - i - 1, x - i - 1] = 0
            if m and n > 0:
                ai_bites.append(self.copy())

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
        #self.ai_eat(7, 2, ai_bites)
        if len(ai_bites) != 0:
            return ai_bites
        return just_moves

    @property
    def is_game_finished(self) -> bool:
        res = False
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
        # дамка = 2, шашка = 1, черные = -1
        for i in range(7, 4, -1):
            for j in range((i + 1) % 2, 8, 2):
                board[i, j] = 1

        for i in range(2, -1, -1):
            for j in range((i + 1) % 2, 8, 2):
                board[i, j] = -1

        return BoardState(board, 1)
