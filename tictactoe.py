"""
Tic Tac Toe Player
"""

import math
import copy
from sre_parse import State

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

    # Count moves played
    moves = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is not EMPTY:
                moves += 1
    
    # Determine who's turn it is
    if moves % 2 == 0: 
        return X 
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Return set of EMPTY cells
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Check if action is valid
    if action not in actions(board):
        raise ValueError
    
    # Make new board
    new_board = copy.deepcopy(board)    
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check winner diagonal 1
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]  
    
    # Check winner diagonal 2
    elif board[2][0] is not EMPTY and board[2][0] == board[1][1] == board[0][2]:  
        return board[2][0]       
    
    # Check winner row by row  
    for i in range(3):
        if board[i][0] is not EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    # Check winner column by column
    for i in range(3):    
        if board[0][i] is not EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]  
                    
    # No winner
    return


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if there is a winner
    if winner(board) is not EMPTY:
        return True
    
    # Check for EMPTY space
    for row in board:
        if EMPTY in row:
            return False
    
    # Out of space
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    # Determin winner
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # Find maximum
    def max_value(board, Max, Min):
        if terminal(board):
            return [utility(board), None];
        move = None        
        v = -math.inf
        for action in actions(board):
            v2 = min_value(result(board, action), Max, Min)[0]
            Max = max(Max, v2)
            if v2 > v:
                v = v2
                move = action
            if Max >= Min:
                break
        return [v, move]

    # Find minimum
    def min_value(board, Max, Min):
        if terminal(board):
            return [utility(board), None];
        move = None        
        v = math.inf
        for action in actions(board):
            v2 = max_value(result(board, action), Max, Min)[0]
            Min = min(Min, v2)
            if v > v2:
                v = v2
                move = action
            if Max >= Min:
                break
        return [v, move]
    
    # Check for terminal board
    if terminal(board):
        return
    
    # Find optimal move
    Max = -math.inf
    Min = math.inf
    if player(board) == X:
        optimum = max_value(board, Max, Min)
    else:
        optimum = min_value(board, Max, Min)
    return optimum[1]
