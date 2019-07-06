from math import inf as infinity
from random import choice
import platform
import time
from os import system


# Tic Tac Toe


my_gain = +1
opponent_gain = -1
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]


def heuristics(state):
    if victory(state, my_gain):
        score = +1
    elif victory(state, opponent_gain):
        score = -1
    else:
        score = 0

    return score


def victory(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    return victory(state, opponent_gain) or victory(state, my_gain)


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minmax(state, depth, player):
    if player == my_gain:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = heuristics(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minmax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == my_gain:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Meu turno [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minmax(board, depth, my_gain)
        x, y = move[0], move[1]

    set_move(x, y, my_gain)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Seu turno [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Escolha um número de 1 a 9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], opponent_gain)

            if not can_move:
                print('Não pode')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Não pode')
            exit()



def main():
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Jogar com X ou O\nEscolha: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Erro')
            exit()
        except (KeyError, ValueError):
            print('Erro, fechando...')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('Quer começar?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Erro')
            exit()
        except (KeyError, ValueError):
            print('Erro, fechando...')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if victory(board, opponent_gain):
        clean()
        print(f'Seu turno [{h_choice}]')
        render(board, c_choice, h_choice)
        print('VOCE VENCEU!')
    elif victory(board, my_gain):
        clean()
        print(f'Meu turno [{c_choice}]')
        render(board, c_choice, h_choice)
        print('VOCE PERDEU HAHAHA!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('EMPATE!')

    exit()


if __name__ == '__main__':
    main()




