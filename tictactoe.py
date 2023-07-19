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
    for col in range(3):
        for row in range(3):
            if board[col][row] is EMPTY:
                actions.add((col, row))
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
    for row in range(3):
        if board[row][0] is not EMPTY and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]

    # Check winner column by column
    for col in range(3):    
        if board[0][col] is not EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]  
                    
    # No winner
    return None


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
    def max_value(board, absolute_max, absolute_min):
        if terminal(board):
            return [utility(board)]
        move = None        
        local_max = -math.inf
        for action in actions(board):
            _ = min_value(result(board, action), absolute_max, absolute_min)[0]           
            absolute_max = max(absolute_max, _)
            if _ > local_max:
                local_max = _
                move = action
            if absolute_max >= absolute_min:
                break
        return [local_max, move]

    # Find minimum
    def min_value(board, absolute_max, absolute_min):
        if terminal(board):
            return [utility(board)]
        move = None        
        local_min = math.inf
        for action in actions(board):
            _ = max_value(result(board, action), absolute_max, absolute_min)[0]
            absolute_min = min(absolute_min, _)
            if local_min > _:
                local_min = _
                move = action
            if absolute_max >= absolute_min:
                break
        return [local_min, move]
    
    # Determine best move
    absolute_max = -math.inf
    absolute_min = math.inf
    if player(board) == X:
        best_move = max_value(board, absolute_max, absolute_min)
    else:
        best_move = min_value(board, absolute_max, absolute_min)
    return best_move[1]

