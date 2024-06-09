"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # if game state is initial, X gets the first move
    if all(row.count(EMPTY) == len(row) for row in board):
        return X

    countX = 0
    countO = 0
    for row in board:
        for item in row:
            if item == X:
                countX += 1
            elif item == O:
                countO += 1

    return O if countO < countX else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i, inner_list in enumerate(board):
        for j, _ in enumerate(inner_list):
            if board[i][j] == EMPTY:
                possible.add((i, j))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)

    currentPlayer = player(boardCopy)
    possibleActions = actions(boardCopy)

    if action not in possibleActions:
        raise NameError("Not a valide action")

    if currentPlayer == X:
        boardCopy[action[0]][action[1]] = X
    else:
        boardCopy[action[0]][action[1]] = O

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for line in lines(board):
        if len(set(line)) == 1 and line[0] is not EMPTY:
            return line[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not any(EMPTY in row for row in board) or winner(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    currentPlayer = player(board)

    if currentPlayer == X:
        optimalAction = maxValue(board)["optimalAction"]
    else:
        optimalAction = minValue(board)["optimalAction"]

    return optimalAction


def _rows_and_diagonal(board):
    yield from board  # the rows
    yield [board[i][i] for i in range(len(board))]  # one of the diagonals


def lines(board):
    yield from _rows_and_diagonal(board)
    # rotate the board 90 degrees to get the columns and the other diagonal
    yield from _rows_and_diagonal(list(zip(*reversed(board))))


def maxValue(board):
    v = -100000

    if terminal(board):
        return {"v": utility(board), "optimalAction": None}

    optimalAction = None

    for action in actions(board):
        minValueResult = minValue(result(board, action))
        if minValueResult["v"] > v:
            v = minValueResult["v"]
            optimalAction = action

    return {"v": v, "optimalAction": optimalAction}


def minValue(board):
    v = 100000

    if terminal(board):
        return {"v": utility(board), "optimalAction": None}

    optimalAction = None

    for action in actions(board):
        maxValueResult = maxValue(result(board, action))
        if maxValueResult["v"] < v:
            v = maxValueResult["v"]
            optimalAction = action

    return {"v": v, "optimalAction": optimalAction}
