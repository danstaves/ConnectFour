# Dan Staves
# Project 3 - Adversarial Search: Connect 4

from enum import IntEnum, auto
from typing import List, Self
import time

class EndState(IntEnum):
    Win = 1
    Lose = -1
    Tie = 0

class Direction(IntEnum):
    North = auto()
    NorthEast = auto()
    East = auto()
    SouthEast = auto()
    South = auto()
    SouthWest = auto()
    West = auto()
    NorthWest = auto()

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
    
    def __repr__(self):
        return self.__str__()
    
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
            
    def get_valid_indices(self)->List[int]:
        def get_column_index(column)->bool:
            for index in range(column, self.columns * self.rows, self.columns):
                if self.grid[index] is None: return index

        return [index for c in range(self.columns) if (index:=get_column_index(c)) is not None]
    
    def get_valid_moves(self)->List[int]:
        def is_column_available(column)->bool:
            for index in range(column, self.columns * self.rows, self.columns):
                if self.grid[index] is None: return True
                
            return False
        
        return [col for col in range(self.columns) if is_column_available(col)]

    def get_longest_run(self, token)->int:
        """Return the number and length of runs"""

        #Get the index of the top token in each column
        def get_top_index(col):
            for index in range(col, self.rows*self.columns, self.columns):
                if self.grid[index] is not None: yield index

        available_indices = [col_index[-1] for col in range(self.columns) if len(col_index:=[i for i in get_top_index(col)]) > 0 ]

        neighbor_count = 0
        for index in available_indices:
            if self.grid[index] != token: continue
            # Check diagonals, vertical, and horizontal for 4 in a row
            cur_x, cur_y = self.get_coord(index)


            # Check North West
            nw_count = 0
            for check_x, check_y in [(x,y) for d in range(1, min(cur_x, self.rows-cur_y)+1) if (x:=cur_x-d)>=0 and (y:=cur_y+d)<self.rows]:
                check_index = self.get_index(check_x, check_y)
                if self.grid[check_index] == token: nw_count += 1
                else: break

            # Check West
            w_count = 0
            for check_x in range(cur_x-1, -1, -1):
                check_index = self.get_index(check_x, cur_y)
                if self.grid[check_index] == token: w_count += 1
                else: break

            # Check South West
            sw_count = 0
            for check_x, check_y in [(x,y) for d in range(1, min(cur_x, cur_y)+1) if (x:=cur_x-d)>=0 and (y:=cur_y-d)>=0]:
                check_index = self.get_index(check_x, check_y)
                if self.grid[check_index] == token: sw_count += 1
                else: break

            # Check South
            s_count = 0
            for check_y in range(cur_y-1, -1, -1):
                check_index = self.get_index(cur_x, check_y)
                if self.grid[check_index] == token: s_count += 1
                else: break

            # Check South East
            se_count = 0
            for check_x, check_y in [(x,y) for d in range(1, min(self.columns-cur_x, cur_y)+1) if (x:=cur_x+d)<self.columns and (y:=cur_y-d)>=0]:
                check_index = self.get_index(check_x, check_y)
                if self.grid[check_index] == token: se_count += 1
                else: break

            # Check East
            e_count = 0
            for check_x in range(cur_x+1, self.columns, 1):
                check_index = self.get_index(check_x, cur_y)
                if self.grid[check_index] == token: e_count += 1
                else: break

            # Check North East
            ne_count = 0
            for check_x, check_y in [(x,y) for d in range(1, min(self.columns-cur_x, self.rows-cur_y)+1) if (x:=cur_x+d)<self.columns and (y:=cur_y+d)<self.rows]:
                check_index = self.get_index(check_x, check_y)
                if self.grid[check_index] == token: ne_count += 1
                else: break 

            longest_run = max(w_count+e_count, sw_count+ne_count, s_count, se_count+nw_count)
            if longest_run > neighbor_count: neighbor_count = longest_run

        return neighbor_count
    
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
                next_states = [parent.drop_token(possible_move, current_token) for possible_move in parent.get_valid_moves()]
                sorted_states = sorted(next_states, key=lambda s: s.get_longest_run(current_token), reverse=True)
                for state in sorted_states:
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
        sorted_states = sorted(next_states, key=lambda s: s.get_longest_run(self.token), reverse=True)
        for state in sorted_states:
            num = state.get_longest_run(self.token)
            if time.time() - start_time <= 10:
                utility, max_level = calculate_utility(state, 0)
                deepest_search = max(deepest_search, max_level)
                if best_score is None or utility > best_score:
                    best_score = utility
                    best_move = state
        
        print(f"Max Level: {deepest_search}")
        return best_move

                    
                    
            