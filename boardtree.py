class BoardNode:
    def __init__(self, history, board, player_to_move, move_number = 1):
        self.board = board
        self.history = history
        self.player_to_move = player_to_move
        self.game_state = None
        self.check = False
        self.terminal = False
        self.moves = None
        self.board_score = self.get_board_score(self.board)
        # (queen side castle, king side castle)
        self.castle = (True, True)
        self.move_number = move_number
        self.check_for_draw_and_castle()
        self.find_board_moves()
        self.get_board_score(self.board)
        if len(self.moves) == 0:
            if self.is_in_check(self.board, self.player_to_move):
                if player_to_move == 'w':
                    self.terminal = 'black'
                    self.game_state = 'checkmate, black wins'
                    self.board_score = -1000
                else:
                    self.terminal = 'white'
                    self.game_state = 'checkmate, white wins'
                    self.board_score = 1000
            else:
                self.terminal = 'draw'

    def check_for_draw_and_castle(self):

        recent_capture = False
        repetition_count = 1

        # Iterate through history to check draw conditions and update castling rights
        for i in range(len(self.history)):
            index = len(self.history)-i-1
            # Update move count since last capture if not yet found
            if not recent_capture:
                historic_score = self.get_board_score(self.history[index])
                if historic_score != self.board_score:
                    recent_capture = True
            if i >= 99 and not recent_capture:
                self.terminal = 'draw'
                self.game_state = "Draw by 50 move rule"

            # Check if pawns have moved (i.e., if their positions differ)
            current_pawn_positions = [(r, c) for r in range(8) for c in range(8)
                                      if self.board[r][c] and self.board[r][c][1] == 'P']
            previous_pawn_positions = [(r, c) for r in range(8) for c in range(8)
                                       if self.history[index][r][c] and self.history[index][r][c][1] == 'P']
            if current_pawn_positions != previous_pawn_positions:
                break

            # Check for threefold repetition
            if self.board == self.history[index]:
                repetition_count += 1
                if repetition_count == 3:
                    self.terminal = 'draw'
                    self.game_state = 'Draw by repetition'
                    break

        # Update castling rights based on the current and previous board states


        # White king and rooks
        for i in range(len(self.history)):
            index = len(self.history)-i-1
            current_board = self.history[index]
            if self.player_to_move == 'w':
                if current_board[7][4] != 'wK':  # White king moved
                    self.castle = (False, False)
                if current_board[7][0] != 'wR':  # White queen-side rook moved
                    self.castle = (False, self.castle[1])
                if current_board[7][7] != 'wR':  # White king-side rook moved
                    self.castle = (self.castle[0], False)

            # Black king and rooks
            else:
                if current_board[0][4] != 'bK':  # Black king moved
                    self.castle = (False, False)
                if current_board[0][0] != 'bR':  # Black queen-side rook moved
                    self.castle = (False, self.castle[1])
                if current_board[0][7] != 'bR':  # Black king-side rook moved
                    self.castle = (self.castle[0], False)

            # If castling rights are revoked, stop further checks
            if self.castle == (False, False):
                return



    def get_king_position(self, player, board):
        for row in range(8):
            for col in range(8):
                if board[row][col] == player + 'K':
                    return (row, col)
        return None

    def is_in_check(self, board, player):
        return self.is_under_attack(board, player, self.get_king_position(player, board))

    def is_under_attack(self, board, player, attacked_square):
        if not attacked_square:
            return False

        enemy = 'b' if player == 'w' else 'w'

        # Check for threats from all possible directions and from knights
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in directions:
            new_row, new_col = attacked_square[0] + dr, attacked_square[1] + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] != '':
                    if board[new_row][new_col][0] == enemy:
                        piece_type = board[new_row][new_col][1]
                        if piece_type in 'RQ' and (dr == 0 or dc == 0):  # Rook or Queen in a straight line
                            return True
                        if piece_type in 'BQ' and (dr != 0 and dc != 0):  # Bishop or Queen diagonally
                            return True
                        if piece_type == 'K' and abs(new_row - attacked_square[0]) <= 1 and abs(new_col - attacked_square[1]) <= 1:
                            return True
                    break
                new_row += dr
                new_col += dc

        # Check for knight attacks
        for dr, dc in knight_moves:
            new_row, new_col = attacked_square[0] + dr, attacked_square[1] + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == enemy + 'N':
                    return True

        # Check for pawn attacks
        direction = 1 if player == 'b' else -1
        pawn_attacks = [(direction, -1), (direction, 1)]
        for dr, dc in pawn_attacks:
            new_row, new_col = attacked_square[0] + dr, attacked_square[1] + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == enemy + 'P':
                    return True

        return False

    def get_board_score(self, board):
        # Define the piece values
        piece_values = {
            'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1,
        }

        score = 0

        # Iterate through the board
        for row in board:
            for piece in row:
                if piece != '':
                    color = piece[0]  # 'w' or 'b'
                    piece_type = piece[1]  # 'K', 'Q', 'R', etc.
                    value = piece_values[piece_type]

                    if color == 'w':
                        score += value  # Add value for white pieces
                    elif color == 'b':
                        score -= value  # Subtract value for black pieces

        return score

    def get_knight_moves(self, pos, piece):
        row, col = pos
        moves = []
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == '' or self.board[new_row][new_col][0] != piece[0]:
                    moves.append((new_row, new_col))
        return moves

    def get_valid_moves(self, piece, pos):
        row, col = pos
        moves = []

        if piece[1] == 'P':  # Pawn
            direction = -1 if piece[0] == 'w' else 1
            if self.board[row + direction][col] == '':
                moves.append((row + direction, col))
                if (row == 6 and piece[0] == 'w') or (row == 1 and piece[0] == 'b'):
                    if self.board[row + 2 * direction][col] == '':
                        moves.append((row + 2 * direction, col))
            if col - 1 >= 0 and self.board[row + direction][col - 1] != '' and self.board[row + direction][col - 1][
                0] != piece[0]:
                moves.append((row + direction, col - 1))
            if col + 1 < 8 and self.board[row + direction][col + 1] != '' and self.board[row + direction][col + 1][0] != \
                    piece[0]:
                moves.append((row + direction, col + 1))

        elif piece[1] == 'R':  # Rook
            moves.extend(self.get_linear_moves(pos, piece, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)]))

        elif piece[1] == 'N':  # Knight
            moves.extend(self.get_knight_moves(pos, piece))

        elif piece[1] == 'B':  # Bishop
            moves.extend(self.get_linear_moves(pos, piece, directions=[(1, 1), (-1, -1), (1, -1), (-1, 1)]))

        elif piece[1] == 'Q':  # Queen
            moves.extend(self.get_linear_moves(pos, piece, directions=[(1, 0), (-1, 0), (0, 1), (0, -1),
                                                                       (1, 1), (-1, -1), (1, -1), (-1, 1)]))

        elif piece[1] == 'K':  # King
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dr, dc in king_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] == '' or self.board[new_row][new_col][0] != piece[0]:
                        moves.append((new_row, new_col))

        return moves

    def get_linear_moves(self, pos, piece, directions):
        row, col = pos
        moves = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == '':
                    moves.append((new_row, new_col))
                elif self.board[new_row][new_col][0] != piece[0]:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc

        return moves

    def enpassant_and_promotion(self):
        # Get the previous board state from history
        prev_board = self.history[-1] if len(self.history) > 0 else None

        # Initialize a list to hold potential board states after en passant or promotion
        weird_moves = []

        if self.player_to_move == 'w':
            for col in range(8):
                # Check for white pawn on 5th rank (row 3) for en passant
                if self.board[3][col] == 'wP':
                    # Check left and right for en passant
                    if col > 0 and self.board[2][col - 1] == '' and self.board[3][col - 1] == 'bP':
                        if prev_board and prev_board[1][col - 1] == 'bP' and self.board[4][col - 1] == '':
                            new_board = [r[:] for r in self.board]
                            new_board[3][col] = ''
                            new_board[3][col - 1] = ''
                            new_board[2][col - 1] = 'wP'
                            weird_moves.append(new_board)

                    if col < 7 and self.board[2][col + 1] == '' and self.board[3][col + 1] == 'bP':
                        if prev_board and prev_board[1][col + 1] == 'bP' and self.board[4][col + 1] == '':
                            new_board = [r[:] for r in self.board]
                            new_board[3][col] = ''
                            new_board[3][col + 1] = ''
                            new_board[2][col + 1] = 'wP'
                            weird_moves.append(new_board)

                # Check for promotion (white pawn on 7th rank, row 1 for 0-index)
                if self.board[1][col] == 'wP':
                    # Promotion by moving forward into the 8th rank
                    if self.board[0][col] == '':
                        for promotion_piece in ['wQ', 'wR', 'wB', 'wN']:
                            new_board = [r[:] for r in self.board]
                            new_board[1][col] = ''
                            new_board[0][col] = promotion_piece
                            weird_moves.append(new_board)

                    # Promotion by capturing diagonally left
                    if col > 0 and self.board[0][col - 1] != '' and self.board[0][col - 1][0] == 'b':
                        for promotion_piece in ['wQ', 'wR', 'wB', 'wN']:
                            new_board = [r[:] for r in self.board]
                            new_board[1][col] = ''
                            new_board[0][col - 1] = promotion_piece
                            weird_moves.append(new_board)

                    # Promotion by capturing diagonally right
                    if col < 7 and self.board[0][col + 1] != '' and self.board[0][col + 1][0] == 'b':
                        for promotion_piece in ['wQ', 'wR', 'wB', 'wN']:
                            new_board = [r[:] for r in self.board]
                            new_board[1][col] = ''
                            new_board[0][col + 1] = promotion_piece
                            weird_moves.append(new_board)

        elif self.player_to_move == 'b':
            for col in range(8):
                # Check for black pawn on 4th rank (row 4) for en passant
                if self.board[4][col] == 'bP':
                    # Check left and right for en passant
                    if col > 0 and self.board[5][col - 1] == '' and self.board[4][col - 1] == 'wP':
                        if prev_board and prev_board[6][col - 1] == 'wP' and self.board[3][col - 1] == '':
                            new_board = [r[:] for r in self.board]
                            new_board[4][col] = ''
                            new_board[4][col - 1] = ''
                            new_board[5][col - 1] = 'bP'
                            weird_moves.append(new_board)

                    if col < 7 and self.board[5][col + 1] == '' and self.board[4][col + 1] == 'wP':
                        if prev_board and prev_board[6][col + 1] == 'wP' and self.board[3][col + 1] == '':
                            new_board = [r[:] for r in self.board]
                            new_board[4][col] = ''
                            new_board[4][col + 1] = ''
                            new_board[5][col + 1] = 'bP'
                            weird_moves.append(new_board)

                # Check for promotion (black pawn on 2nd rank, row 6 for 0-index)
                if self.board[6][col] == 'bP':
                    # Promotion by moving forward into the 1st rank
                    if self.board[7][col] == '':
                        for promotion_piece in ['bQ', 'bR', 'bB', 'bN']:
                            new_board = [r[:] for r in self.board]
                            new_board[6][col] = ''
                            new_board[7][col] = promotion_piece
                            weird_moves.append(new_board)

                    # Promotion by capturing diagonally left
                    if col > 0 and self.board[7][col - 1] != '' and self.board[7][col - 1][0] == 'w':
                        for promotion_piece in ['bQ', 'bR', 'bB', 'bN']:
                            new_board = [r[:] for r in self.board]
                            new_board[6][col] = ''
                            new_board[7][col - 1] = promotion_piece
                            weird_moves.append(new_board)

                    # Promotion by capturing diagonally right
                    if col < 7 and self.board[7][col + 1] != '' and self.board[7][col + 1][0] == 'w':
                        for promotion_piece in ['bQ', 'bR', 'bB', 'bN']:
                            new_board = [r[:] for r in self.board]
                            new_board[6][col] = ''
                            new_board[7][col + 1] = promotion_piece
                            weird_moves.append(new_board)

        return weird_moves

    def find_board_moves(self):
        board_list = []
        weird_moves = self.enpassant_and_promotion()
        for board in weird_moves:
            if not self.is_in_check(board, self.player_to_move):
                board_list.append(board)
        for row_idx, row in enumerate(self.board):
            for col_idx, piece in enumerate(row):
                if piece and piece[0] == self.player_to_move:
                    valid_moves = self.get_valid_moves(piece, (row_idx, col_idx))
                    for move in valid_moves:
                        new_board = [r[:] for r in self.board]  # Deep copy of the board
                        new_board[move[0]][move[1]] = piece
                        new_board[row_idx][col_idx] = ''  # Clear the original position
                        if not self.is_in_check(new_board, self.player_to_move):
                            board_list.append(new_board)

        # Add castling moves for white

        if self.player_to_move == 'w' and not self.is_in_check(self.board, 'w'):
            if self.castle[0]:  # Queen side castle
                if self.board[7][1] == self.board[7][2] == self.board[7][3] == '' and \
                        not self.is_under_attack(self.board, 'w', (7, 2)) and \
                        not self.is_under_attack(self.board, 'w', (7, 3)):
                        # Perform queen-side castling
                        new_board = [r[:] for r in self.board]  # Deep copy of the board
                        new_board[7][2] = 'wK'
                        new_board[7][3] = 'wR'
                        new_board[7][4] = ''
                        new_board[7][0] = ''
                        board_list.append(new_board)
            if self.castle[1]:  # King side castle
                if self.board[7][5] == self.board[7][6] == '' and \
                        not self.is_under_attack(self.board, 'w', (7, 5)) and \
                        not self.is_under_attack(self.board, 'w', (7, 6)):
                    # Perform king-side castling
                    new_board = [r[:] for r in self.board]  # Deep copy of the board
                    new_board[7][6] = 'wK'
                    new_board[7][5] = 'wR'
                    new_board[7][4] = ''
                    new_board[7][7] = ''
                    board_list.append(new_board)

        # Add castling moves for black
        if self.player_to_move == 'b' and not self.is_in_check(self.board, 'b'):
            if self.castle[0]:  # Queen side castle
                if self.board[0][1] == self.board[0][2] == self.board[0][3] == '' and \
                        not self.is_under_attack(self.board, 'b', (0, 2)) and \
                        not self.is_under_attack(self.board, 'b', (0, 3)):
                    # Perform queen-side castling
                    new_board = [r[:] for r in self.board]  # Deep copy of the board
                    new_board[0][2] = 'bK'
                    new_board[0][3] = 'bR'
                    new_board[0][4] = ''
                    new_board[0][0] = ''
                    board_list.append(new_board)
            if self.castle[1]:  # King side castle
                if self.board[0][5] == self.board[0][6] == '' and \
                        not self.is_under_attack(self.board, 'b', (0, 5)) and \
                        not self.is_under_attack(self.board, 'b', (0, 6)):
                    # Perform king-side castling
                    new_board = [r[:] for r in self.board]  # Deep copy of the board
                    new_board[0][6] = 'bK'
                    new_board[0][5] = 'bR'
                    new_board[0][4] = ''
                    new_board[0][7] = ''
                    board_list.append(new_board)

        self.moves = board_list
        return
