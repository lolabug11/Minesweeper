import numpy as np
import random as r

class Tile:
    def __init__(self,x:int,y:int,bombs_nearby:int,is_mine=False,is_clicked=False,is_flagged=False):
        self.x = x
        self.y = y
        self.isMine = is_mine
        self.isClicked = is_clicked
        self.isFlagged = is_flagged
        self.bombs_nearby = bombs_nearby

    def __str__(self):
        return str((self.x,self.y))

class Board:
    @staticmethod
    def bombs_nearby(bomb_cords:list, cord_of_tile:tuple):
        directions = [
            (-1,1),#  up left
            (0,1), #  up
            (1,1), #  up right
            (-1,0),#  left
            (1,0), #  right
            (-1,-1),# down left
            (0,-1),#  down
            (1,-1) #  down right
        ]
        bombs_nearby = 0
        for dir in directions:
            tile_in_dir = (cord_of_tile[0] + dir[0], cord_of_tile[1] + dir[1])
            if -1 in tile_in_dir:
                continue
            if tile_in_dir in bomb_cords:
                bombs_nearby += 1
        return bombs_nearby

    def _gen_board(self,rows:int,cols:int) :
        bomb_pos = []
        if self.difficulty == 1:
            for i in range(7):
                pos = (r.randint(0,7),r.randint(0,7))
                while pos in bomb_pos:
                    pos = (r.randint(0, 7), r.randint(0, 7))
                bomb_pos.append(pos)
        elif self.difficulty == 2:
            for i in range(30):
                pos = (r.randint(0,13),r.randint(0,13))
                while pos in bomb_pos:
                    pos = (r.randint(0, 13), r.randint(0, 13))
                bomb_pos.append(pos)

        elif self.difficulty == 3:
            for i in range(82):
                pos = (r.randint(0,17),r.randint(0,17))
                while pos in bomb_pos:
                    pos = (r.randint(0, 17), r.randint(0, 17))
                bomb_pos.append(pos)

        board_lists = []
        for row in range(rows):
            row_list = []
            for col in range(cols):
                if (row,col) in bomb_pos:
                    row_list.append(Tile(col, row,-1))
                else:
                    bombs_nearby = Board.bombs_nearby(bomb_pos, (row, col))
                    row_list.append(Tile(col,row,bombs_nearby))

            board_lists.append(row_list)

        board = np.array(board_lists)
        return board,bomb_pos

    def rearrange_board_after_click(self, click_cords:tuple):
        directions = [
            (-1, 1),  # up left
            (0, 1),  # up
            (1, 1),  # up right
            (-1, 0),  # left
            (1, 0),  # right
            (-1, -1),  # down left
            (0, -1),  # down
            (1, -1)  # down right
        ]
        bombs_to_move = []
        cords_around_click = []
        for dir in directions:
            cord_in_dir = (click_cords[0] + dir[0], click_cords[1] + dir[1])
            if cord_in_dir in self.bomb_pos:
                cords_around_click.append(cord_in_dir)
        if click_cords in self.bomb_pos:
            bombs_to_move.append(click_cords)
        for cord in cords_around_click:
            if cord in self.bomb_pos:
                bombs_to_move.append(cord)

        for bomb in bombs_to_move:
            if self.difficulty == 1:
                new_pos = (r.randint(0,7),r.randint(0,7))
                while new_pos in cords_around_click:
                    new_pos = (r.randint(0, 7), r.randint(0, 7))
                self.board[new_pos[0],new_pos[1]] = -1
            elif self.difficulty == 2:
                new_pos = (r.randint(0, 13), r.randint(0, 13))
                while new_pos in cords_around_click:
                    new_pos = (r.randint(0, 13), r.randint(0, 13))
                self.board[new_pos[0], new_pos[1]] = -1
            elif self.difficulty == 3:
                new_pos = (r.randint(0, 17), r.randint(0, 17))
                while new_pos in cords_around_click:
                    new_pos = (r.randint(0, 17), r.randint(0, 17))
                self.board[new_pos[0], new_pos[1]] = -1

        for row in range(self.rows):
            for col in range(self.cols):
                if (row,col) in self.bomb_pos:
                    continue
                print(row,col)
                tile = self.board[row,col]
                print(type(tile))
                tile.bombs_nearby = Board.bombs_nearby(self.bomb_pos,(row,col))

    def __init__(self,difficulty:int):
        self.difficulty = difficulty
        if difficulty == 1:
            self.cols = 8
            self.rows = 8
        elif difficulty == 2:
            self.cols = 14
            self.rows = 14
        elif difficulty == 3:
            self.cols = 18
            self.rows = 18
        self.board,self.bomb_pos = self._gen_board(self.rows,self.cols)

    def __str__(self):
        return_list = []
        for row in self.board:
            row_list = []
            for tile in row:
                if tile.isClicked:
                    row_list.append(tile.distance_from_bomb)
                elif tile.isFlagged:
                    row_list.append("⚐")
                else:
                    row_list.append(tile.bombs_nearby)
            return_list.append(row_list)
        return_array = np.array(return_list)
        return str(return_array)


board1 = Board(1)
print(board1)
board1.rearrange_board_after_click((0,0))
print(board1)