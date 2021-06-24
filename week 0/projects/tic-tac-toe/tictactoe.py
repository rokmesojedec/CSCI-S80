"""
Tic Tac Toe Player
"""

import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_count = 0
    # Counts number of empty cells
    # If number of empty cells is even then it's X's turn
    # otherwise it's O's turn
    for row in board:
        for cell in row:
            if cell is EMPTY:
                empty_count += 1

    return (X, O)[empty_count % 2 == 0]


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell is EMPTY:
                possible_actions.add((row_index, cell_index))
    return possible_actions


def is_valid_action(action):
    if len(action) != 2:
        return False
    else:
        row = action[0]
        cell = action[1]
        return row >= 0 and row < 3 and \
            cell >= 0 and cell < 3
    return False


def is_full_board(board):
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if is_valid_action(action):
        new_board = []
        action_row = action[0]
        action_cell = action[1]
        for row_index, row in enumerate(board):
            new_row = []
            new_board.append(new_row)
            for cell_index, cell in enumerate(row):
                if row_index == action_row and cell_index == action_cell:
                    if cell is not EMPTY:
                        raise Exception("Cell is not Empty")
                    new_row.append(player(board))
                else:
                    new_row.append(board[row_index][cell_index])
        return new_board
    else:
        raise Exception("Invalid Action")
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check top-left-bottom-right diagonal
    if board[0][0] is not EMPTY and \
            board[0][0] == board[1][1] and \
            board[0][0] == board[2][2]:
        return board[0][0]

    # check top-right-bottom-left diagonal
    if board[0][2] is not EMPTY and \
            board[0][2] == board[1][1] and \
            board[0][2] == board[2][0]:
        return board[0][2]

    board_length = len(board)

    # check for horizontal (column) winner
    for row in range(board_length):
        cell_matching = None
        for cell in range(board_length):
            if board[row][cell] is EMPTY:
                break
            if cell_matching is None:
                cell_matching = board[row][cell]
            elif cell_matching != board[row][cell]:
                cell_matching = None
                break
            if cell == board_length - 1 and cell_matching is not None:
                return cell_matching

    # check for vertical (row) winner
    for cell in range(board_length):
        row_matching = None
        for row in range(board_length):
            if board[row][cell] is EMPTY:
                break
            if row_matching is None:
                row_matching = board[row][cell]
            elif row_matching != board[row][cell]:
                row_matching = None
                break
            if row == board_length - 1 and row_matching is not None:
                return row_matching

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return is_full_board(board) and winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    if winner(board) is O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    is_X = player(board) == X
    possible_actions = list(map(lambda action: (
        action, utility(result(board, action))), actions(board)))
    best_utility = (math.inf, -math.inf)[is_X]

    for action in possible_actions:
        print(action)
        if is_X:
            if best_utility < action[1]:
                best_utility = action[1]
        else:
            if best_utility > action[1]:
                best_utility = action[1]

    best_utility_possible_actions = list(
        filter(
            lambda action: action[1] == best_utility,
            possible_actions))
    print(best_utility_possible_actions)
    return random.choice(best_utility_possible_actions)[0]
