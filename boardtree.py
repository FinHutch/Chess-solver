class BoardNode:
    def __init__(self, history, board, player_to_move, moves_since_last_capture = 0, castle_white=(True, True), castle_black=(True, True), move_number = 1):
        self.board = board
        self.history = history
        self.player_to_move = player_to_move
        self.game_state = None
        self.check = False
        self.terminal = False
        self.moves = None
        self.moves_since_last_capture = moves_since_last_capture
        # (queen side castle, king side castle)
        self.castle_white = castle_white
        self.castle_black = castle_black
        self.move_number = move_number

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

    def find_board_moves(self):
        board_list = []
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
            if self.castle_white[0]:  # Queen side castle
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
            if self.castle_white[1]:  # King side castle
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
            if self.castle_black[0]:  # Queen side castle
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
            if self.castle_black[1]:  # King side castle
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
