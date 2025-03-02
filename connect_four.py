# Dan Staves
# Project 3 - Adversarial Search: Connect 4

from enum import Enum
from typing import List, Self

class EndState(Enum):
    Win = 1
    Lose = -1
    Tie = 0

class Grid:
    def __init__(self, rows:int, cols:int):
        self.rows = rows
        self.columns = cols
        self.grid = [None] * rows * cols

    def __str__(self)->str:
        board = ' '.join([str(x) for x in range(self.columns)])
        for i in range(self.rows)[::-1]:
            row_start = i * self.columns
            row_end = row_start + self.columns
            row = self.grid[row_start:row_end]

            board += '\n' + '|'.join([" " if x is None else str(x) for x in row])
        return board

    def drop_token(self, column, token)->bool:
        """Drop a token in a specified column.
        Return True is successful, False if the column is full"""
        for index in range(column,self.rows*self.columns, self.columns):
            if not self.grid[index]:
                self.grid[index]=token
                return True
            
        return False
    
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
    









# board = ["o","o","x","o","x","o","x","x","o","x","o","o","o","x","o","x","x","o","o","x","o","o","o","x","o","o","x","o","o","o"]
# calc_score(board,'x')


