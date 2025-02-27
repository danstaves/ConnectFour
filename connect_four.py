# Dan Staves
# Project 3 - Adversarial Search: Connect 4

COLUMNS = 6
ROWS = 5

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
    for i in range(ROWS)[::-1]:
        row_start = i * COLUMNS
        row_end = row_start + COLUMNS
        row = board[row_start:row_end]

        print('|'.join([" " if x is None else str(x) for x in row]))

def calc_score(board, token)->int:
    """Calculate the score of the game
    1: win, 0: draw, -1: lose"""
    for index, value in enumerate(board):
        if value:
            # Check diagonals, vertical, and horizontal for 4 in a row
            cur_x, cur_y = get_coord(index)

            if cur_x >= 3 and cur_y <= ROWS-4:
                # Check Left-Diagonal
                indices = [get_index(cur_x-d, cur_y+d) for d in range(1,4)]
                values = [board[i] for i in indices]
                is_win = all([x == value for x in values])
                if is_win:
                    return 1 if value == token else -1
            
            if cur_y <= ROWS-4:
                # Check Vertical
                indices = [get_index(cur_x, cur_y+d) for d in range(1,4)]
                values = [board[i] for i in indices]
                is_win = all([x == value for x in values])
                if is_win:
                    return 1 if value == token else -1

            if cur_x <= COLUMNS - 4 and cur_y <= ROWS-4:
                # Check Right-Diagonal
                indices = [get_index(cur_x+d, cur_y+d) for d in range(1,4)]
                values = [board[i] for i in indices]
                is_win = all([x == value for x in values])
                if is_win:
                    return 1 if value == token else -1

            if cur_x <= COLUMNS-4:
                # Check Right Horizontal
                indices = [get_index(cur_x+d, cur_y) for d in range(1,4)]
                values = [board[i] for i in indices]
                is_win = all([x == value for x in values])
                if is_win:
                    return 1 if value == token else -1
                
    return 0

board = ["o","o","x","o","x","o","x","x","o","x","o","o","o","x","o","x","x","o","o","x","o","o","o","x","o","o","x","o","o","o"]




print_board(board)
calc_score(board, "o")