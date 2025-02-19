

# stack = ['A']
# def dfs():
#     while stack:
#         node = stack.pop()
#         print(node, end=" ")
#         for neighbor in reversed(tree[node]):
#             stack.append(neighbor)

# dfs()
# print()
import copy
import time
from move import legal_move

def filter_moves(row, col, board):
    all_legal_move = legal_move(id_to_name[board[(row, col)]], col, row)
    filtered = []
    for (board_row, board_col) in board:
        if all_legal_move is not None and (board_col, board_row) in all_legal_move:
            filtered.append((board_row, board_col))
    return filtered

def solve(pieces, start_time, depth=0):
    if len(pieces) == 1:
        elapsed_time = time.time() - start_time  # Tính thời gian đã trôi qua
        print("         " * depth + f"FOUND - Time: {elapsed_time:.6f} seconds")
        return True
    for (row, col), piece in pieces.items():
        target = filter_moves(row, col, pieces)
        if not target:
            continue
       
        for (target_x, target_y) in target:
            if (target_x, target_y) == (row, col):
                continue
            # Sao chép sâu (deepcopy) để tránh ảnh hưởng đến pieces gốc
            child = copy.deepcopy(pieces)

            # Di chuyển quân cờ trong child
            child[(target_x, target_y)] = child.pop((row, col))

            # In ra với độ sâu phù hợp để thể hiện cây
            print("         " * depth + f"({row}, {col}) -> ({target_x}, {target_y})")
            solve(child, start_time, depth + 1)  # Gọi đệ quy với độ sâu tăng dần

# Gọi hàm solve với dictionary pieces ban đầu
pieces_on_board = {(2, 4): 123, (4, 2): 124, (5, 2): 125, (5.0, 4.0): 126}
id_to_name = {
    123: 'b',
    124: 'p',
    125: 'p',
    126: 'r'
}

start_time = time.time()  # Lưu thời gian bắt đầu
solve(pieces_on_board, start_time)
