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


def display_terminal_message(win, message):
    # Define the dimensions for the modal dialog
    width, height = win.get_size()
    dialog_width, dialog_height = width // 2, height // 2
    dialog_x, dialog_y = (width - dialog_width) // 2, (height - dialog_height) // 2

    # Draw the dialog background
    pygame.draw.rect(win, (200, 200, 200), (dialog_x, dialog_y, dialog_width, dialog_height))
    pygame.draw.rect(win, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

    # Render the message text
    font = pygame.font.Font(None, 36)
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + dialog_height // 3))
    win.blit(text_surface, text_rect)

    # Draw the restart button
    button_width, button_height = dialog_width // 3, dialog_height // 6
    button_x, button_y = (width - button_width) // 2, dialog_y + dialog_height // 2
    pygame.draw.rect(win, (100, 100, 100), (button_x, button_y, button_width, button_height))
    pygame.draw.rect(win, BLACK, (button_x, button_y, button_width, button_height), 2)

    # Render the button text
    button_text = font.render("Restart", True, WHITE)
    button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    win.blit(button_text, button_text_rect)

    pygame.display.update()

    return (button_x, button_y, button_width, button_height)  # Return the button's rect for event handling
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

            if boardNode.terminal:
                message = boardNode.game_state  # Assuming this stores the game state like "Checkmate" or "Draw"
                button_rect = display_terminal_message(WIN, message)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if (button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and
                        button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]):
                        # Restart the game
                        boardNode = BoardNode([], startBoard, 'w')
                        selected_piece = None
                        start_pos = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not boardNode.terminal:
                    x, y = event.pos
                    col, row = x // square_size, y // square_size
                    if boardNode.board[row][col] != '':
                        selected_piece = boardNode.board[row][col]
                        start_pos = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                if not boardNode.terminal:
                    x, y = event.pos
                    col, row = x // square_size, y // square_size

                    if start_pos is not None:
                        if start_pos != (row, col):
                            new_board = [row.copy() for row in boardNode.board]
                            new_board[row][col] = selected_piece
                            new_board[start_pos[0]][start_pos[1]] = ''

                            valid_move_found = False

                            for future_board in boardNode.moves:
                                if selected_piece in ['wR', 'bR']:
                                    if new_board == future_board:
                                        valid_move_found = True
                                        break
                                elif (future_board[row][col] == selected_piece and
                                      future_board[start_pos[0]][start_pos[1]] == '' and
                                      future_board[row][col] == new_board[row][col] and
                                      future_board[start_pos[0]][start_pos[1]] == new_board[start_pos[0]][start_pos[1]]):
                                    valid_move_found = True
                                    break

                            if valid_move_found:
                                boardNode.player_to_move = 'b' if boardNode.player_to_move == 'w' else 'w'
                                boardNode.history.append(boardNode.board)
                                boardNode = BoardNode(boardNode.history, copy.deepcopy(future_board), boardNode.player_to_move, boardNode.move_number + 0.5)


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
