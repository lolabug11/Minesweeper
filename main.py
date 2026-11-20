from mine_class import *

while True:
    diff = int(input("What difficulty do you want? (1: 8x8 board, 2: 14x14 board, 3:18x18 board)\n> "))
    board = Board(diff)
    while not board.game_over:
        if board.turn_number == 0:
            row = int(input("What row do you want to interact with?\n> "))
            col = int(input("What col do you want to interact with?\n> "))
            board.click((row,col))
            print(board)
        else:
            flag = bool(input("Do you want to place a flag? (0: No, 1: Yes)\n> "))
            if not flag:
                board.change_mode()
            row = int(input("What row do you want to interact with?\n> "))
            col = int(input("What col do you want to interact with?\n> "))
            board.click((row,col))
            if not flag:
                board.change_mode()
            print(board)