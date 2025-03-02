from connect_four import Grid

COLUMNS = 6
ROWS = 5

tokens = ['x','o']
turn = 0
board = Grid(ROWS, COLUMNS)

while not board.check_endgame(tokens[turn%2]):

    print(board)
    inputSuccess = False
    while not inputSuccess:
        col_choice = input(f"Turn {turn}: Which Column do you want to play? (Enter Number between 0 and {COLUMNS - 1}: ")
        inputSuccess = board.drop_token(int(col_choice), tokens[turn%2])

    turn+=1

print(board)
print(board.check_endgame(tokens[0]))