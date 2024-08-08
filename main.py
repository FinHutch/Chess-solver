# main.py
import pygame
import os
import copy

from boardtree import BoardNode
pygame.init()

# Define constants
INITIAL_WIDTH, INITIAL_HEIGHT = 600, 600
ROWS, COLS = 8, 8

# Set up the display with resizable window
WIN = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Load and scale piece images
def load_and_scale_image(file_name, square_size):
    image = pygame.image.load(os.path.join('assets', file_name))
    orig_width, orig_height = image.get_size()
    if orig_width > orig_height:
        new_width = square_size
        new_height = int((square_size / orig_width) * orig_height)
    else:
        new_height = square_size
        new_width = int((square_size / orig_height) * orig_width)
    return pygame.transform.scale(image, (new_width, new_height))


def load_pieces(square_size):
    return {
        'wP': load_and_scale_image('whitepawn.png', square_size),
        'bP': load_and_scale_image('blackpawn.png', square_size),
        'wR': load_and_scale_image('whiterook.png', square_size),
        'bR': load_and_scale_image('blackrook.png', square_size),
        'wN': load_and_scale_image('whiteknight.png', square_size),
        'bN': load_and_scale_image('blackknight.png', square_size),
        'wB': load_and_scale_image('whitebishop.png', square_size),
        'bB': load_and_scale_image('blackbishop.png', square_size),
        'wQ': load_and_scale_image('whitequeen.png', square_size),
        'bQ': load_and_scale_image('blackqueen.png', square_size),
        'wK': load_and_scale_image('whiteking.png', square_size),
        'bK': load_and_scale_image('blackking.png', square_size)
    }


# Initialize piece positions
startBoard = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
         ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]


def draw_board(win):
    win.fill(WHITE)
    width, height = win.get_size()
    square_size = min(width // COLS, height // ROWS)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, BLACK, (col * square_size, row * square_size, square_size, square_size))
    return square_size


def draw_pieces(win, board, piece_images, square_size):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != '':
                win.blit(piece_images[board[row][col]], (col * square_size + square_size * 0.3, row * square_size))


def is_valid_move(piece, start_pos, end_pos, board):
    return True


def main():
    selected_piece = None
    start_pos = None
    boardNode = BoardNode([], startBoard, 'w')
    run = True
    while run:
        square_size = draw_board(WIN)
        piece_images = load_pieces(square_size)
        draw_pieces(WIN, boardNode.board, piece_images, square_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // square_size, y // square_size
                if boardNode.board[row][col] != '':
                    selected_piece = boardNode.board[row][col]
                    start_pos = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                col, row = x // square_size, y // square_size
                if start_pos is not None:
                    # Create a hypothetical board state by copying the current board
                    if start_pos != (row, col):
                        new_board = [row.copy() for row in boardNode.board]

                        # Make the move on the hypothetical board
                        new_board[row][col] = selected_piece
                        new_board[start_pos[0]][start_pos[1]] = ''
                        boardNode.find_board_moves()
                        # Check if the hypothetical board is in the list of allowed future boards
                        if new_board in boardNode.moves:
                            boardNode.history.append(copy.deepcopy(boardNode.board))
                            boardNode.board[row][col] = selected_piece
                            boardNode.board[start_pos[0]][start_pos[1]] = ''
                            if boardNode.player_to_move == 'w':
                                boardNode.player_to_move = 'b'
                            else:
                                boardNode.player_to_move = 'w'
                        elif selected_piece == 'wK' or selected_piece == 'bK':
                            if start_pos == (7, 4) or (row, col) == (0, 4):
                                for castle_check in boardNode.moves:
                                    if castle_check[row][col] == selected_piece:
                                        boardNode.board = copy.deepcopy(castle_check)
                                        if boardNode.player_to_move == 'w':
                                            boardNode.player_to_move = 'b'
                                        else:
                                            boardNode.player_to_move = 'w'
                                        break

                    # Reset the selected piece and start position
                    selected_piece = None
                    start_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    x, y = event.pos
                    WIN.fill(WHITE)  # Clear the screen to redraw
                    square_size = draw_board(WIN)
                    draw_pieces(WIN, boardNode.board, piece_images, square_size)
                    piece_image = piece_images[selected_piece]
                    WIN.blit(piece_image, (x - square_size // 2, y - square_size // 2))  # Draw piece at cursor
                    pygame.display.update()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
