import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6           # Static variables are capitalized
COLUMN_COUNT = 7        # Try reworking code so that board size can be changed?

BLUE = (51, 171, 249)
BLACK = (0, 0, 0)
RED = (216, 31, 52)
YELLOW = (254, 226, 62)
GREEN = (30, 255, 80)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 15)


def create_board():     # Creates the matrix
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, column, piece):
    board[row][column] = piece         # (piece is either defined as 1 or 2 respective to the player)


def is_valid_location(board, column):              # If top row of the matrix != 0, player cant drop piece in the that column.
    return board[ROW_COUNT - 1][column] == 0       # Makes the top row and the selected column


def get_next_open_row(board, column):  # Selects lowest open row after column is selected
    for r in range(ROW_COUNT):
        if board[r][column] == 0:      # ??
            return r


def print_board(board):                 # Flips the matrix, making (0,0) on the bottom left.
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check all horizontal locations for win
    for c in range(COLUMN_COUNT - 3):   # -3, because four in a row can't start past the 4th column.
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # Check all vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):  # -3, because four in a column can't start past the 3rd row.
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Check for positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    # Check for negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):    # Covers 1st to 4th column
        for r in range(3, ROW_COUNT):    # Covers 4th to 7th row
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)  # Takes 3 inputs only!

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

board = create_board()
print_board(board)
game_over = False       # Game is active
turn = 0                # Will be used to dictate which player's turn it is


pygame.init()           # Initializing
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE     # +1 creates top area
size = (width, height)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 50)

draw_board(board)
pygame.display.update()                 # Re-renders the screen


while not game_over:
    for event in pygame.event.get():    # This module runs based off input events.
        if event.type == pygame.QUIT:
            sys.exit()                  # Allows player to properly exit

        if event.type == pygame.MOUSEMOTION:    # Creates top circle tracker thingy
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Erases past circles
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))


            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]     # ??
                column = int(math.floor(posx/SQUARESIZE))  # Rounds down to whole number

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)

                    if winning_move(board, 1):
                        label = myfont.render("PLAYER 1 WINS!", 1, GREEN)
                        screen.blit(label, (140, 40))
                        game_over = True

            # Ask for Player 2 Input
            else:
                posx = event.pos[0]  # ??
                column = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)

                    if winning_move(board, 2):
                        label = myfont.render("PLAYER 2 WINS!", 1, GREEN)
                        screen.blit(label, (140, 40))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2
            # "%" is "mod". it will give the remainder of turn divided by 2.
            # Turn goes from 0 to 1 to 2, where it is divided by 2 to leave a remainder of 0.

            if game_over:
                pygame.time.wait(2000)  # 2000 miliseconds
