import numpy as np
import random as r

class Tile:
    def __init__(self,x:int,y:int,bombs_nearby,is_mine=False,is_clicked=False,is_flagged=False):
        self.x = x
        self.y = y
        self.isMine = is_mine
        self.isClicked = is_clicked
        self.isFlagged = is_flagged
        self.bombs_nearby = bombs_nearby

    def __str__(self):
        return str((self.x,self.y))

class Board:
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
    def bomb_clicked(self,bomb_cord:tuple):
        print(f"Game over there was a bomb at {bomb_cord}")

    def propagate_tiles(self, tile_clicked:tuple):
        self.player_facing_board[tile_clicked[0],tile_clicked[1]] = self.board[tile_clicked[0],tile_clicked[1]]

    def click(self,tile_cords:tuple):
        if self.turn_number == 0:
            self._gen_board(tile_cords)
            self.propagate_tiles(tile_cords)
            self.turn_number += 1
        else:
            ...

    @staticmethod
    def bombs_nearby(bomb_cords:list, cord_of_tile:tuple):

        bombs_nearby = 0
        for dir in Board.directions:
            tile_in_dir = (cord_of_tile[0] + dir[0], cord_of_tile[1] + dir[1])
            if -1 in tile_in_dir:
                continue
            if tile_in_dir in bomb_cords:
                bombs_nearby += 1
        return bombs_nearby

    def _gen_board(self,click_cords:tuple) :
        bomb_pos = []
        forbidden_tiles = [click_cords]
        for dir in Board.directions:
            tile_in_dir = (click_cords[0] + dir[0],click_cords[1] + dir[1])
            if -1 in tile_in_dir or self.rows - 1 in tile_in_dir:
                continue
            forbidden_tiles.append(tile_in_dir)
        if self.difficulty == 1:
            for i in range(7):
                pos = (r.randint(0,7),r.randint(0,7))
                while pos in bomb_pos or pos in forbidden_tiles:
                    pos = (r.randint(0, 7), r.randint(0, 7))
                bomb_pos.append(pos)
        elif self.difficulty == 2:
            for i in range(30):
                pos = (r.randint(0,13),r.randint(0,13))
                while pos in bomb_pos or pos in forbidden_tiles:
                    pos = (r.randint(0, 13), r.randint(0, 13))
                bomb_pos.append(pos)

        elif self.difficulty == 3:
            for i in range(82):
                pos = (r.randint(0,17),r.randint(0,17))
                while pos in bomb_pos or pos in forbidden_tiles:
                    pos = (r.randint(0, 17), r.randint(0, 17))
                bomb_pos.append(pos)

        board_lists = []
        for row in range(self.rows):
            row_list = []
            for col in range(self.cols):
                if (row,col) in bomb_pos:
                    row_list.append(Tile(col, row,-1))
                else:
                    bombs_nearby = Board.bombs_nearby(bomb_pos, (row, col))
                    row_list.append(Tile(col,row,bombs_nearby))

            board_lists.append(row_list)

        board = np.array(board_lists)
        self.board = board
        self.bomb_pos = bomb_pos

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
        self.board = None

        def gen_player_facing_board():
            player_board_list = []
            for x in range(self.rows - 1):
                row_list = []
                for y in range(self.cols - 1):
                    row_list.append("~")
                player_board_list.append(row_list)
            return np.array(player_board_list)

        self.player_facing_board = gen_player_facing_board()
        self.bomb_pos = None
        self.turn_number = 0

    def board_to_string(self,mode:int):
        board_list = []
        if mode == 1:
            return str(self.player_facing_board)
        elif mode == 2:
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

    def __str__(self):
        return self.board_to_string(1)
board1 = Board(1)
board1.click((1,1))
# print(board1)
print(board1.board_to_string(1))
print(board1.board_to_string(2))