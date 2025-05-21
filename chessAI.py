import chess
import math
import time

class ChessAI:
    def __init__(self):
        self.center_squares = [chess.E4, chess.D4, chess.E5, chess.D5, chess.C3, chess.F3, chess.C6, chess.F6]
        self.extended_center = self.center_squares + [chess.C4, chess.F4, chess.E3, chess.D3, chess.C5, chess.F5, chess.E6, chess.D6]

        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        self.pawnTable = [
            0, 0, 0, 0, 0, 0, 0, 0,
            80, 80, 80, 80, 80, 80, 80, 80,
            20, 20, 30, 40, 40, 30, 20, 20,
            5, 5, 15, 35, 35, 15, 5, 5,
            0, 0, 0, 25, 25, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -30, -30, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.knightTable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 5, 20, 25, 25, 20, 5, -30,
            -30, 5, 15, 25, 25, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        self.bishopTable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 15, 10, 10, 15, 10, -10,
            -10, 0, 15, 20, 20, 15, 0, -10,
            -10, 5, 5, 20, 20, 5, 5, -10,
            -10, 0, 10, 15, 15, 10, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        self.rookTable = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.queenTable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        self.kingTable = [
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]

        self.kingTableEndgame = [
            -50, -40, -30, -20, -20, -30, -40, -50,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -30, 0, 0, 0, 0, -30, -30,
            -50, -30, -30, -30, -30, -30, -30, -50
        ]

    def is_endgame(self, board):
        queens = 0
        minors = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.piece_type == chess.QUEEN:
                    queens += 1
                elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                    minors += 1
        return queens == 0 or (queens == 1 and minors <= 1)

    def position_bonus(self, piece_type, square, is_white, endgame=False):
        tables = {
            chess.PAWN: self.pawnTable,
            chess.KNIGHT: self.knightTable,
            chess.BISHOP: self.bishopTable,
            chess.ROOK: self.rookTable,
            chess.QUEEN: self.queenTable,
            chess.KING: self.kingTableEndgame if endgame else self.kingTable,
        }
        table = tables.get(piece_type)
        if table:
            return table[square] if is_white else table[chess.square_mirror(square)]
        return 0

    def evaluate_board(self, board):
        if board.is_checkmate():
            return -9999 if board.turn == chess.WHITE else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        white_bishops, black_bishops = 0, 0
        mobility_bonus = 5
        endgame = self.is_endgame(board)

        for piece_type in self.piece_values:
            for square in board.pieces(piece_type, chess.WHITE):
                score += self.piece_values[piece_type]
                score += self.position_bonus(piece_type, square, True, endgame)
                if piece_type == chess.BISHOP: white_bishops += 1
                if square in self.center_squares and piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP]:
                    score += 20
            for square in board.pieces(piece_type, chess.BLACK):
                score -= self.piece_values[piece_type]
                score -= self.position_bonus(piece_type, square, False, endgame)
                if piece_type == chess.BISHOP: black_bishops += 1
                if square in self.center_squares and piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP]:
                    score -= 20

        if white_bishops >= 2: score += 30
        if black_bishops >= 2: score -= 30

        score += mobility_bonus * (len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves)))

        for color in [chess.WHITE, chess.BLACK]:
            pawns = board.pieces(chess.PAWN, color)
            pawn_files = [chess.square_file(sq) for sq in pawns]
            for file in range(8):
                if pawn_files.count(file) > 1:
                    score += -25 if color == chess.WHITE else 25
                if file in pawn_files and (file - 1 not in pawn_files and file + 1 not in pawn_files):
                    score += -15 if color == chess.WHITE else 15
            for square in pawns:
                rank = chess.square_rank(square)
                score += (rank * 5) if color == chess.WHITE else -(7 - rank) * 5

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                attackers = board.attackers(not piece.color, square)
                defenders = board.attackers(piece.color, square)
                if attackers and not defenders:
                    score += (-self.piece_values[piece.piece_type] // 2) if piece.color == chess.WHITE else (
                            self.piece_values[piece.piece_type] // 2)

        for color in [chess.WHITE, chess.BLACK]:
            king_sq = board.king(color)
            if king_sq is not None:
                kr = chess.square_rank(king_sq)
                kf = chess.square_file(king_sq)
                shield_squares = [chess.square(f, kr + 1 if color == chess.WHITE else kr - 1)
                                  for f in [kf - 1, kf, kf + 1] if 0 <= f <= 7]
                shield = sum(1 for sq in shield_squares
                             if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color == color)
                score += shield * 15 if color == chess.WHITE else -shield * 15

        return score

    def order_moves(self, board, moves):
        scored_moves = []
        for move in moves:
            score = 0
            if board.is_capture(move):
                victim = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                if victim:
                    v_val = self.piece_values.get(victim.piece_type, 0)
                    a_val = self.piece_values.get(attacker.piece_type if attacker else None, 0)
                    score += 1000 + (v_val - a_val)
                    if victim.piece_type == chess.KNIGHT:
                        score += 200
            if move.promotion: score += 900
            if board.is_castling(move): score += 300
            moving_piece = board.piece_at(move.from_square)
            if moving_piece:
                if moving_piece.piece_type == chess.PAWN and move.to_square in self.extended_center:
                    score += 400
                if moving_piece.piece_type in [chess.KNIGHT, chess.BISHOP] and move.to_square in self.extended_center:
                    score += 100
            scored_moves.append((score, move))
        scored_moves.sort(key=lambda x: -x[0])
        return [m for (_, m) in scored_moves]

    def minimax(self, board, depth, alpha, beta, maximizing, start_time, time_limit):
        if depth == 0 or board.is_game_over() or time.time() - start_time > time_limit:
            return self.evaluate_board(board)

        legal_moves = self.order_moves(board, list(board.legal_moves))
        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False, start_time, time_limit)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True, start_time, time_limit)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

    def best_move(self, board, depth=3, time_limit=10):
        best_move_found = None
        maximizing = board.turn
        best_val = -math.inf if maximizing == chess.WHITE else math.inf
        start_time = time.time()
        legal_moves = self.order_moves(board, list(board.legal_moves))

        for move in legal_moves:
            board.push(move)
            move_val = self.minimax(board, depth - 1, -math.inf, math.inf, maximizing == chess.BLACK, start_time, time_limit)
            board.pop()

            if maximizing == chess.WHITE:
                if move_val > best_val:
                    best_val = move_val
                    best_move_found = move
            else:
                if move_val < best_val:
                    best_val = move_val
                    best_move_found = move

        return best_move_found
