# Dan Staves
# Project 3 - Adversarial Search: Connect 4

from enum import Enum
from typing import List

COLUMNS = 6
ROWS = 5

class State(Enum):
    Win = 1
    Lose = -1
    Tie = 0
    Playing = 5

# [ | | | | | ]
# [ | | | | | ]
# [ | |x| | | ]
# [ | |x|o| | ]
# [ | |o|x|o| ]

def get_coord(index:int)->tuple[int,int]:
    y = index // COLUMNS
    x = index % COLUMNS
    return (x,y)

def get_index(x:int, y:int)->int:
    return y * COLUMNS + x

def print_board(board):
    print(' '.join([str(x) for x in range(COLUMNS)]))
    for i in range(ROWS)[::-1]:
        row_start = i * COLUMNS
        row_end = row_start + COLUMNS
        row = board[row_start:row_end]

        print('|'.join([" " if x is None else str(x) for x in row]))

def drop_token(board, column, token)->bool:
    """Drop a token in a specified column.
    Return True is successful, False if the column is full"""
    for index in range(column,ROWS*COLUMNS, COLUMNS):
        if not board[index]:
            board[index]=token
            return True
        
    return False

def calc_score(board:List[str], token)->State:
    """Calculate the score of the game
    1: win, 0: draw, -1: lose"""
    for index, value in enumerate(board):
        if value:
            # Check diagonals, vertical, and horizontal for 4 in a row
            cur_x, cur_y = get_coord(index)

            if cur_x >= 3 and cur_y <= ROWS-4:
                # Check Left-Diagonal
                values = board[index::COLUMNS][1:4]
                is_win = all([x == value for x in values])
                if is_win:
                    return State.Win if value == token else State.Lose
            
            if cur_y <= ROWS-4:
                # Check Vertical
                values = board[index::COLUMNS][1:4]
                is_win = all([x == value for x in values])
                if is_win:
                    return State.Win if value == token else State.Lose

            if cur_x <= COLUMNS - 4 and cur_y <= ROWS-4:
                # Check Right-Diagonal
                values = board[index::COLUMNS+1][1:4]
                is_win = all([x == value for x in values])
                if is_win:
                    return State.Win if value == token else State.Lose

            if cur_x <= COLUMNS-4:
                # Check Right Horizontal
                values = board[index::1][1:4]
                is_win = all([x == value for x in values])
                if is_win:
                    return State.Win if value == token else State.Lose
                
    return State.Tie if board.count(None) == 0 else State.Playing

# board = ["o","o","x","o","x","o","x","x","o","x","o","o","o","x","o","x","x","o","o","x","o","o","o","x","o","o","x","o","o","o"]
# calc_score(board,'x')

# Generate an empty game board
board = [None]*ROWS*COLUMNS

tokens = ['x','o']
turn = 0
while calc_score(board,tokens[turn%2]) == State.Playing:

    print_board(board)
    inputSuccess = False
    while not inputSuccess:
        col_choice = input(f"Turn {turn}: Which Column do you want to play? (Enter Number between 0 and {COLUMNS - 1}: ")
        inputSuccess = drop_token(board, int(col_choice), tokens[turn%2])

    turn+=1

print_board(board)
print(calc_score(board, "o"))