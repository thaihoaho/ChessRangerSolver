def pawn_moves(col, row):
    moves = []
    if row == 0:
        return
    if col > 0:
        moves.append((col - 1, row - 1))
    if col < 7:
        moves.append((col + 1, row - 1))
    return moves

def rook_moves(col, row):
    moves = []
    for i in range(8):
        moves.append((i, row))
    for i in range(8):
        moves.append((col, i))
    return moves

def bishop_moves(col, row):
    moves = []
    for i in range(8):
        if row - col + i < 0 or row - col + i > 7:
            continue
        moves.append((i, row - col + i))
    for i in range(8):
        if row + col - i < 0 or row + col - i > 7:
            continue
        moves.append((i, row + col - i))
    return moves

def queen_moves(col, row):
    return rook_moves(col, row) + bishop_moves(col, row)

def king_moves(col, row):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_col <= 7 and 0 <= new_row <= 7:
            moves.append((new_col, new_row))
    
    return moves

def knight_moves(col, row):
    moves = []
    directions = [(-2, 1), (-2, -1), (2, -1), (2, 1),
                  (-1, -2), (1, 2), (-1, 2), (1, -2)]
    
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_col <= 7 and 0 <= new_row <= 7: 
            moves.append((new_col, new_row))
    return moves

switch = {
    'p': pawn_moves,
    'r': rook_moves,
    'b': bishop_moves,
    'k': king_moves,
    'n': knight_moves,
    'q': queen_moves
}

def legal_move(piece, col, row):
    return switch[piece](col, row)

legal_move('b', 5, 3)
