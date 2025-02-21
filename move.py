def pawn_moves(col, row, board):
    moves = []
    if row == 0:
        return moves
    if col > 0:
        if board.get((row - 1, col - 1)):
            moves.append((row - 1, col - 1))
    if col < 7:
        if board.get((row - 1, col + 1)):
            moves.append((row - 1, col + 1))
    return moves

def rook_moves(col, row, board):
    moves = []
    for c in range(col + 1, 8):
        if board.get((row, c)):
            moves.append((row, c))
            break

    for r in range(row + 1, 8):
        if board.get((r, col)):
            moves.append((r, col))
            break

    for c in range(col - 1, -1, -1):
        if board.get((row, c)):
            moves.append((row, c))
            break

    for r in range(row - 1, -1, -1):
        if board.get((r, col)):
            moves.append((r, col))
            break

    return moves

def bishop_moves(col, row, board):
    moves = []
    for c, r in zip(range(col + 1, 8), range(row + 1, 8)):
        if board.get((r, c)):
            moves.append((r, c))
            break

    for c, r in zip(range(col - 1, -1, -1), range(row - 1, -1, -1)):
        if board.get((r, c)):
            moves.append((r, c))
            break

    for c, r in zip(range(col - 1, -1, -1), range(row + 1, 8)):
        if board.get((r, c)):
            moves.append((r, c))
            break

    for c, r in zip(range(col + 1, 8), range(row - 1, -1, -1)):
        if board.get((r, c)):
            moves.append((r, c))
            break

    return moves

def queen_moves(col, row, board):
    return rook_moves(col, row, board) + bishop_moves(col, row, board)

def king_moves(col, row, board):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_col <= 7 and 0 <= new_row <= 7:
            if board.get((new_row, new_col)):
                moves.append((new_row, new_col))
    return moves

def knight_moves(col, row, board):
    moves = []
    directions = [(-2, 1), (-2, -1), (2, -1), (2, 1),
                  (-1, -2), (1, 2), (-1, 2), (1, -2)]
    
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_col <= 7 and 0 <= new_row <= 7: 
            if board.get((new_row, new_col)):
                moves.append((new_row, new_col))
    return moves

switch = {
    'p': pawn_moves,
    'r': rook_moves,
    'b': bishop_moves,
    'k': king_moves,
    'n': knight_moves,
    'q': queen_moves
}

def legal_move(piece, col, row, board):
    return switch[piece](col, row, board)

# board = {(2, 3): 29, (2, 5): 30, (3, 2): 31, (3, 5): 32, (4, 4): 33, (5, 2): 34, (5, 3): 35, (5, 5): 36}
# print(legal_move('b', 5, 3, board))
