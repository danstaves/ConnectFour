from connect_four import Grid, AI

COLUMNS = 6
ROWS = 5

tokens = ['o', 'x']
turn = 0
board = Grid(ROWS, COLUMNS)



#board.grid = [None, "x", "o", "o", "o", None,None, None, "x", "x", None, None,None, None, None, None, None, None,None, None, None, None, None, None,None, None, None, None, None, None]
computer = AI(tokens[1])

while board.check_endgame(tokens[turn%2]) is None:

    print(board)

    col_choice = input(f"Turn {turn}: Which Column do you want to play? (Enter Number between 0 and {COLUMNS - 1}: ")
    board = board.drop_token(int(col_choice), tokens[0])
    board = computer.play_turn(board)

    turn+=1

print(board)
print(board.check_endgame(tokens[0]))