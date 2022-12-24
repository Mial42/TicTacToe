import sys
from collections import deque
board_length = 9
side_length = 3
ghost_board = '012345678'

def print_puzzle(size, board):
    for i in range(0, len(board), size):
        print(board[i: i + size])

def game_over(board): #Represent the board as a 9 character string
    if '.' not in board:
        return True, 0
    for x in range(0, 9, 3):
        row = board[x:x+3]
        if '.' not in row:
            if 'O' not in row:
                return True, 1
            if 'X' not in row:
                return True, -1
    for y in range(0, 3):
        col = board[y::3]
        if '.' not in col:
            if 'O' not in col:
                return True, 1
            if 'X' not in col:
                return True, -1
    diagonal1 = board[0] + board[4] + board[8]
    if '.' not in diagonal1:
        if 'O' not in diagonal1:
            return True, 1
        if 'X' not in diagonal1:
            return True, -1
    diagonal2 = board[2] + board[4] + board[6]
    if '.' not in diagonal2:
        if 'O' not in diagonal2:
            return True, 1
        if 'X' not in diagonal2:
            return True, -1
    return False, -2


def possible_moves(board):
    answer = ''
    for y in range(9):
        if board[y] == '.':
            answer = answer + str(y) + ','
    temp = list(answer)
    temp[-1] = '.'
    return ''.join(temp)


def generate_children(board):
    x_count = board.count('X')
    o_count = board.count('O')
    children = [None] * 9
    if x_count == o_count:
        for y in range(9):
            if board[y] == '.':
                child = list(board)
                child[y] = 'X'
                child = ''.join(child)
                children[y] = child
    else:
        for y in range(9):
            if board[y] == '.':
                child = list(board)
                child[y] = 'O'
                child = ''.join(child)
                children[y] = child
    return children


def maxX(board):
    done, result = game_over(board)
    if done:
        return result
    children = generate_children(board)
    results = []
    for child in children:
        if child is not None:
            results.append(minO(child))
    return max(results)


def minO(board):
    done, result = game_over(board)
    if done:
        return result
    children = generate_children(board)
    results = []
    for child in children:
        if child is not None:
            results.append(maxX(child))
    return min(results)


def place_piece(piece, pos, board):
    temp = list(board)
    temp[pos] = piece
    return ''.join(temp)


def computer_make_moves(board, my_piece, player_piece): #This is not done: I actually need to select the lowest value
    done, result = game_over(board)
    if done:
        #print("DEBUG CPU: " + str(result))
        if result == 0:
            print("We tied!")
        if result == 1 and my_piece == 'X' or result == -1 and my_piece == 'O':
            print("I win!")
        if result == 1 and my_piece == 'O' or result == -1 and my_piece == 'X':
            print("You win!")
        return

    children = generate_children(board)
    temp_dict = {}
    for y in range(9):
        if children[y] is not None:
            if my_piece == 'X':
                temp = minO(children[y])
            if my_piece == 'O':
                temp = maxX(children[y])
            if temp == 0:
                str1 = 'tie.'
                temp_dict[0] = y
            elif temp == 1 and my_piece == 'X' or temp == -1 and my_piece == 'O':
                str1 = 'win.'
                temp_dict[1] = y
            else:
                str1 = 'loss.'
                temp_dict[-1] = y
            print("Moving at " + str(y) + " results in a " + str1)
    print()
    choice = temp_dict[max(temp_dict)]
    print("I choose space " + str(choice) + '.')
    new_board = place_piece(my_piece, choice, board)
    print_current_board(new_board)
    player_make_moves(new_board, player_piece, my_piece)


def player_make_moves(board, player_piece, computer_piece):
    done, result = game_over(board)
    if done:
        #print("DEBUG Player: " + str(result))
        if result == 0:
            print("We tied!")
        if result == 1 and player_piece == 'X' or result == -1 and player_piece == 'O':
            print("You win!")
        if result == 1 and player_piece == 'O' or result == -1 and player_piece == 'X':
            print("I win!")
        return

    print("You can move to any of these spaces: " + possible_moves(board))
    pos = int(input("Your choice?"))
    new_board = place_piece(player_piece, pos, board)
    print_current_board(new_board)
    computer_make_moves(new_board, computer_piece, player_piece)


def print_current_board(board):
    print()
    print("Current board: ")
    for i in range(0, 9, 3):
        print(board[i: i + 3] + "    " + ghost_board[i: i+3])
    print()

my_board = sys.argv[1]
cpu_piece = 'X'
if my_board == '.........':
    cpu_piece = input("Should I be X or O?")
else:
    my_x_count = my_board.count('X')
    my_o_count = my_board.count('O')
    if my_x_count == my_o_count:
        cpu_piece = 'X'
    else:
        cpu_piece = 'O'

print_current_board(my_board)
if cpu_piece == 'X':
    computer_make_moves(my_board, 'X', 'O')
elif my_board == '.........':
    player_make_moves(my_board, 'X', 'O')
else:
    computer_make_moves(my_board, 'O', 'X')
# #print(minO('....OXXOX'))
