# Dan Staves
# Project 3 - Adversarial Search: Connect 4

from enum import IntEnum
from typing import List, Self
import time

class EndState(IntEnum):
    Win = 1
    Lose = -1
    Tie = 0

class Grid:
    def __init__(self, rows:int, cols:int):
        self.rows = rows
        self.columns = cols
        self.grid = [None] * rows * cols

    def copy(self)->Self:
        newGrid = Grid(self.rows, self.columns)
        newGrid.grid = self.grid.copy()
        return newGrid

    def __str__(self)->str:
        board = ' '.join([str(x) for x in range(self.columns)])
        for i in range(self.rows)[::-1]:
            row_start = i * self.columns
            row_end = row_start + self.columns
            row = self.grid[row_start:row_end]

            board += '\n' + '|'.join([" " if x is None else str(x) for x in row])
        return board
    
    def __eq__(self, value):
        if len(self.grid) != len(value.grid):
            return False
        
        for index in range(len(self.grid)):
            if self.grid[index] != value.grid[index]:
                return False
            
        return True

    def drop_token(self, column, token)->Self:
        """Drop a token in a specified column.
        Return True is successful, False if the column is full"""
        new_grid = self.copy()
        for index in range(column,self.rows*self.columns, self.columns):
            if not new_grid.grid[index]:
                new_grid.grid[index]=token
                return new_grid
    
    def get_valid_moves(self)->List[int]:
        def is_column_available(column)->bool:
            for index in range(column, self.columns * self.rows, self.columns):
                if self.grid[index] is None: return True
                
            return False
        
        return [col for col in range(self.columns) if is_column_available(col)]

    
    def check_endgame(self, token)->EndState:
        """Return the End State of the game or None if the game is not finished"""
        for index, value in enumerate(self.grid):
            if value:
                # Check diagonals, vertical, and horizontal for 4 in a row
                cur_x, cur_y = self.get_coord(index)

                if cur_x >= 3 and cur_y <= self.rows-4:
                    # Check Left-Diagonal
                    values = self.grid[index::self.columns-1][1:4]
                    is_win = all([x == value for x in values])
                    if is_win:
                        return EndState.Win if value == token else EndState.Lose
                
                if cur_y <= self.rows-4:
                    # Check Vertical
                    values = self.grid[index::self.columns][1:4]
                    is_win = all([x == value for x in values])
                    if is_win:
                        return EndState.Win if value == token else EndState.Lose

                if cur_x <= self.columns - 4 and cur_y <= self.rows-4:
                    # Check Right-Diagonal
                    values = self.grid[index::self.columns+1][1:4]
                    is_win = all([x == value for x in values])
                    if is_win:
                        return EndState.Win if value == token else EndState.Lose

                if cur_x <= self.columns-4:
                    # Check Right Horizontal
                    values = self.grid[index::1][1:4]
                    is_win = all([x == value for x in values])
                    if is_win:
                        return EndState.Win if value == token else EndState.Lose
                    
        return EndState.Tie if self.grid.count(None) == 0 else None

    def get_coord(self,index:int)->tuple[int,int]:
        y = index // self.columns
        x = index % self.columns
        return (x,y)

    def get_index(self, x:int, y:int)->int:
        return y * self.columns + x

tokens = ["o", "x"]
class AI:
    def __init__(self, token:str):
        self.token = token

    def play_turn(self, board:Grid):
        """Play the next move on the input game board"""

        start_time = time.time()

        def calculate_utility(parent:Grid, minimax_level:int) -> tuple[EndState, int]:

            if time.time() - start_time > 10:
                return (EndState.Tie, minimax_level)
            elif (utility := parent.check_endgame(self.token)):
                return (utility, minimax_level)
            else:
                #calculate the utility from children
                best = EndState.Tie
                deepest = 0
                current_player = minimax_level % 2
                current_token = tokens[current_player]
                use_min = current_player == 0
                for possible_move in parent.get_valid_moves():
                    state = parent.drop_token(possible_move, current_token)
                    utility, max_level = calculate_utility(state, minimax_level+1)
                    deepest = max(deepest, max_level)
                    if (use_min and utility < best) or (not use_min and utility > best):
                        best = utility
                        break
                
                return (best, deepest)
            
        # Pick the highest score for each of the children
        
        best_score = None
        best_move = None
        deepest_search = 0
        next_states = [board.drop_token(possible_move, self.token) for possible_move in board.get_valid_moves()]
        for state in next_states:
            if time.time() - start_time <= 10:
                utility, max_level = calculate_utility(state, 0)
                deepest_search = max(deepest_search, max_level)
                if best_score is None or utility > best_score:
                    best_score = utility
                    best_move = state
        
        print(f"Max Level: {deepest_search}")
        return best_move

                    
                    
            