from typing import Optional

from .boardstate import BoardState


class PositionEvaluation:
    def evaluate(self, board):
        value = 0
        for x in range(8):
            for y in range(8):
                value += board.board[y, x]
                if abs(board.board[y, x]) == 2:
                    value += (board.board[y, x] // 2)
        return value

    def __call__(self, board: BoardState, depth: int, color) -> float:
        value = 0
        if depth == 0:
            return self.evaluate(board)
        else:
            b = board.copy()
            b.current_player *= -1
            moves = b.get_possible_moves()
            if color == board.current_player:
                value = 64
            for i in moves:
                cur = self.evaluate(i)
                if color == board.current_player:
                    value = min(value, self.__call__(i, depth - 1, color))
                else:
                    value = max(value, self.__call__(i, depth - 1, color))
            return value




class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int, color : int):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.depth: int = search_depth
        self.color: int = color

    def next_move(self, board: BoardState) -> Optional[BoardState]:
        moves = board.get_possible_moves()
        if len(moves) == 0:
            return None
        best_move = moves[0]
        #return BoardState(best_move, board.current_player)
        return max(moves, key=lambda b: self.position_evaluation(b, self.depth, self.color) * b.current_player)
