import numpy as np

class Board():
    def __init__(self, n):
        self.n = n
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n
    def __getitem__(self, index):
        return self.pieces[index]
    def get_legal_moves(self):
        moves = set()
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    moves.add((x, y))
        return list(moves)
    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    return True
        return False
    def execute_move(self, move, color):
        (x,y) = move
        assert self[x][y] == 0
        self[x][y] = color

class Gomoku():
    def __init__(self, n=15, nir=5):
        self.n = n
        self.n_in_row = nir
    def get_init_board(self):
        b = Board(self.n)
        return np.array(b.pieces)
    def get_board_size(self):
        return (self.n, self.n)
    def get_action_size(self):
        return self.n * self.n
    def get_next_state(self, board, player, action):
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)
    def get_valid_moves(self, board):
        valids = [0] * self.get_action_size()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves()
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)
    def is_win(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        n = self.n_in_row
        for w in range(self.n):
            for h in range(self.n):
                if (w in range(self.n - n + 1) and board[w][h] != 0 and
                        len(set(board[i][h] for i in range(w, w + n))) == 1):
                    return True
                if (h in range(self.n - n + 1) and board[w][h] != 0 and
                        len(set(board[w][j] for j in range(h, h + n))) == 1):
                    return True
                if (w in range(self.n - n + 1) and h in range(self.n - n + 1) and board[w][h] != 0 and
                        len(set(board[w + k][h + k] for k in range(n))) == 1):
                    return True
                if (w in range(self.n - n + 1) and h in range(n - 1, self.n) and board[w][h] != 0 and
                        len(set(board[w + l][h - l] for l in range(n))) == 1):
                    return True
        return False
    def get_reward_for_player(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        if self.is_win(board, player):
            return 1
        if self.is_win(board, -player):
            return -1
        if b.has_legal_moves():
            return None
        return 0
    def get_canonical_board(self, board, player):
        return player * board

