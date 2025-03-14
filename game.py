from connect_four import Grid, AI

COLUMNS = 6
ROWS = 5

tokens = ['o', 'x']
turn = 0
board = Grid(ROWS, COLUMNS)



#board.grid = [None, "x", "o", "o", "o", None,None, None, "x", "x", None, None,None, None, None, None, None, None,None, None, None, None, None, None,None, None, None, None, None, None]
#board.grid = ["x","x","o","o","x","o","x",None,None,"o",None,None,"x",None,None,None,None,None,"o",None,None,None,None,None,None,None,None,None,None,None]
computer = AI(tokens[1])

while board.check_endgame(tokens[turn%2]) is None:

    print(board)

    col_choice = input(f"Turn {turn}: Which Column do you want to play? (Enter Number between 0 and {COLUMNS - 1}: ")
    board = board.drop_token(int(col_choice), tokens[0])
    board = computer.play_turn(board)

    turn+=1

print(board)
print("You Win!" if board.check_endgame(tokens[0]) == 1 else "You Lose!")