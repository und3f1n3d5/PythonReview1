from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState
AI_color = -1
P_color = 1


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    dark = (0, 0, 0)
    white = (200, 200, 200)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else dark
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = 255, 255, 255
        else:
            figure_color = 100, 100, 100
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        if abs(figure) == 2:
            r = 5
            negative_color = [255 - e for e in figure_color]
            pygame.draw.circle(screen, negative_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)


def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // 8
    f = open("src/board.txt", 'r')

    import os
    if os.path.getsize('src/board.txt') == 0:
        board.initial_state()
    else:
        for y in range(8):
            s = f.readline()
            for x in range(8):
                if s[x] == '1':
                    board.board[y, x] = 1
                if s[x] == '2':
                    board.board[y, x] = 2
                if s[x] == '0':
                    board.board[y, x] = 0
                if s[x] == '3':
                    board.board[y, x] = -1
                if s[x] == '4':
                    board.board[y, x] = -2
    f.close()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and board.current_player == P_color:
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]

                k = False
                for x in range(8):
                    for y in range(8):
                        if board.current_player == board.board[y, x]:
                            board.get_moves(x, y)
                            if len(board.moves) > 0:
                                k = True
                                break
                    if k:
                        break
                board.get_moves(old_x, old_y)
                if not k or len(board.moves) > 0:
                    if len(board.moves) > 0:
                        new_board = board.eat_up(old_x, old_y, new_x, new_y)
                        if new_board is not None:
                            board = new_board
                            board.get_moves(new_x, new_y)
                            if len(board.moves) == 0:
                                #print('Change')
                                board.change_player()
                    else:
                        print(board.current_player)
                        new_board = board.do_move(old_x, old_y, new_x, new_y)
                        if new_board is not None:
                            board = new_board
                            #print('here')
                            board.change_player()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 2) % 5 - 2  # change figure

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = board.inverted()

                if event.key == pygame.K_s:
                    f = open("src/board.txt", 'w')
                    for y in range(8):
                        for x in range(8):
                            if board.board[y, x] == 1:
                                f.write('1')
                            if board.board[y, x] == 2:
                                f.write('2')
                            if board.board[y, x] == 0:
                                f.write('0')
                            if board.board[y, x] == -1:
                                f.write('3')
                            if board.board[y, x] == -2:
                                f.write('4')
                        f.write('\n')
                    f.close()
                    return

                if event.key == pygame.K_q:
                    board.initial_state()
                    f = open("src/__init__.py", 'w')
                    for y in range(8):
                        for x in range(8):
                            if board.board[y, x] == 1:
                                f.write('1')
                            if board.board[y, x] == 2:
                                f.write('2')
                            if board.board[y, x] == 0:
                                f.write('0')
                            if board.board[y, x] == -1:
                                f.write('3')
                            if board.board[y, x] == -2:
                                f.write('4')
                        f.write('\n')
                    f.close()

                if event.key == pygame.K_SPACE and board.current_player == AI_color:
                    if board.current_player == AI_color:
                        if board.is_game_finished:
                            board.initial_state()
                            f = open("__init__.py", 'w')
                            for y in range(8):
                                for x in range(8):
                                    f.write(board.board[y, x])
                                f.write('\n')
                            f.close()
                            win = board.get_winner
                            if win == P_color:
                                print("You win!")
                                return
                            else:
                                print("You lose!")
                                return
                        new_board = ai.next_move(board)
                        if new_board is not None:
                            board = new_board
                            print(new_board.board[0])
                            board.change_player()

        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()


pygame.init()

screen: Surface = pygame.display.set_mode([512, 512])
ai = AI(PositionEvaluation(), search_depth=4, color=AI_color)

game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()
