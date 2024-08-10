import math
from boardtree import BoardNode

recursion_count = 0

def minimax(node, depth, alpha, beta, maximizingPlayer, max_depth):
   # Check for terminal state
    capture_cost = 3
    reg_cost = 5
    global recursion_count
    recursion_count += 1
    if recursion_count %1000 == 0:
        print(recursion_count)
    if depth <= 0 or node.terminal:
        if node.terminal == 'black':
            return -math.inf, None
        elif node.terminal == 'white':
            return math.inf, None
        elif node.terminal == 'draw':  # Handle draw scenario
            return 0, None
        else:
            return node.board_score, None

    best_move = None
    node.find_board_moves()
    if maximizingPlayer:
        maxEval = -math.inf
        for child_board in node.moves:
            child_node = BoardNode(node.history + [node.board], child_board,
                                   'b' if node.player_to_move == 'w' else 'w',
                                   node.move_number + 0.5)

            is_capture = child_node.piece_count(child_node.board) != node.piece_count(node.board)
            is_check = child_node.is_in_check(child_node.board, child_node.player_to_move)

            new_depth = depth - (capture_cost if is_capture or is_check else reg_cost)

            eval, child_best_move = minimax(child_node, new_depth, alpha, beta, False, max_depth)
            if eval > maxEval:
                maxEval = eval
                if depth == max_depth:
                    best_move = child_board  # Record the board state of the best move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = math.inf
        for child_board in node.moves:
            child_node = BoardNode(node.history + [node.board], child_board,
                                   'b' if node.player_to_move == 'w' else 'w',
                                   node.move_number + 1)

            is_capture = child_node.piece_count(child_node.board) != node.piece_count(node.board)
            is_check = child_node.is_in_check(child_node.board,child_node.player_to_move)# Assume this method exists

            new_depth = depth - (capture_cost if is_capture or is_check else reg_cost)

            eval, child_best_move = minimax(child_node, new_depth, alpha, beta, True, max_depth)
            if eval < minEval:
                minEval = eval
                if depth == max_depth:
                    best_move = child_board  # Record the board state of the best move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move

# Example usage
# best_eval, best_move = minimax(root_node, depth=3, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, max_depth=3)
