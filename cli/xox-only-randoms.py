import random
import os


def print_board(board):
    os.system("cls")
    i = 0
    while i < 9:
        print(board[i], board[i+1], board[i+2])
        i += 3


def get_player_move(board, player):
    if player == "X":
        move = input("Lütfen bir hamle yapınız (1-9): ")
        while move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print_board(board)
            move = input("Lütfen geçerli bir hamle yapınız (1-9): ")
        while board[int(move)-1] != "-":
            print_board(board)
            move = input(
                "O bölüm zaten dolu lütfen geçerli bir hamle yapınız (1-9): ")
        return int(move) - 1
    else:
        move = random.randint(0, 8)
        while board[move] != "-":
            print("ne?")
            move = random.randint(0, 8)
        return move


def make_move(board, player, move):
    board[move] = player


def check_winner(board):
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "-":
            return board[i]
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != "-":
            return board[i * 3]
    if board[0] == board[4] == board[8] != "-":
        return board[0]
    if board[2] == board[4] == board[6] != "-":
        return board[2]
    return None


def is_full(board):
    for cell in board:
        if cell == "-":
            return False
    return True


def main():
    board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    player = "X"
    while True:
        print_board(board)
        move = get_player_move(board, player)
        make_move(board, player, move)
        winner = check_winner(board)
        if winner is not None:
            print_board(board)
            print("Kazandın!" if winner=="X" else "Kaybettin!")
            break
        player = "O" if player == "X" else "X"
        if is_full(board):
            print_board(board)
            print("Berabere!")
            break


if __name__ == "__main__":
    while True:
        main()
        input()
