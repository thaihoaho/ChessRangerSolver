import tkinter as tk
from PIL import Image, ImageTk
import random
import copy
from move import legal_move
import time
import config
import vlc  

import heapq


def testcase(num_tests, size):
    print("> Press ENTER to find solution (Should turn off VN-typing)")
    print("> Press SPACE for animation from solution (Should turn off VN-typing)")
    print("> Change number of pieces on board by changing SIZE in config.py")
    print("> Resize window should be done by pulling the CORNER of window to keep it as a square")
    with open("tests/test" + str(size) + ".txt", "r", encoding="utf-8") as file:
        matrices = [eval(line.strip()) for line in file] 
    
    random.seed()  
    for i in range(num_tests):
        number = random.randint(0, 99)
        print('/' * 20, f'Testcase {number}','/' * 20)
        draw_chessboard_with_background_and_pieces(matrices[number])

pieces_on_board = {}
id_to_name = {}
num_to_char_col = {i: chr(97 + i) for i in range(8)}
unformatted_solution=[]

capture_sound = vlc.MediaPlayer("assets/capture.mp3")
solve_sound = vlc.MediaPlayer("assets/solve.mp3")
start_sound = vlc.MediaPlayer("assets/game-start.mp3")
end_sound = vlc.MediaPlayer("assets/game-end.mp3")
dfs_time = None
a_star_time = None

def draw_chessboard_with_background_and_pieces(pieces):
    global unformated_solution
    root = tk.Tk()
    root.title("Chess Ranger")
    # root.after(300, lambda: (start_sound.stop(), start_sound.play()))  

    initial_width, initial_height = 682, 682
    root.geometry(f"{initial_width}x{initial_height}+700+0")
    canvas = tk.Canvas(root, width=initial_width, height=initial_height)
    canvas.pack(fill=tk.BOTH, expand=True)
    board_img_original = Image.open("assets/board_image.png")
    piece_imgs_original = {
        'P': Image.open("assets/black-pawn.png").convert("RGBA"),
        'R': Image.open("assets/black-rook.png").convert("RGBA"),
        'N': Image.open("assets/black-knight.png").convert("RGBA"),
        'B': Image.open("assets/black-bishop.png").convert("RGBA"),
        'Q': Image.open("assets/black-queen.png").convert("RGBA"),
        'K': Image.open("assets/black-king.png").convert("RGBA"),
        'p': Image.open("assets/white-pawn.png").convert("RGBA"),
        'r': Image.open("assets/white-rook.png").convert("RGBA"),
        'n': Image.open("assets/white-knight.png").convert("RGBA"),
        'b': Image.open("assets/white-bishop.png").convert("RGBA"),
        'q': Image.open("assets/white-queen.png").convert("RGBA"),
        'k': Image.open("assets/white-king.png").convert("RGBA"),
    }
    canvas.images = {}
    drag_data = {"piece_id": None, "start_x": 0, "start_y": 0}

    def resize(event):
        id_to_name.clear()
        if canvas.winfo_width() == 0:
            return
        canvas_width = event.width
        canvas_height = event.height
        board_size = min(canvas_width, canvas_height)
        board_img_resized = board_img_original.resize((board_size, board_size), resample=Image.Resampling.LANCZOS)
        
        board_photo = ImageTk.PhotoImage(board_img_resized)
        canvas.delete("all")
        board_x = canvas_width // 2
        board_y = canvas_height // 2
        canvas.create_image(board_x, board_y, image=board_photo, anchor=tk.CENTER)
        canvas.images["board"] = board_photo 
        cell_size = board_size // 8
        for i in range(8):
            for j in range(8):
                piece = pieces[i][j]
                if piece != '.':
                    piece_img_resized = piece_imgs_original[piece].resize((cell_size, cell_size), resample=Image.Resampling.LANCZOS)
                    piece_photo = ImageTk.PhotoImage(piece_img_resized)

                    x = j * cell_size + cell_size // 2
                    y = i * cell_size + cell_size // 2
                    piece_id = canvas.create_image(x, y, image=piece_photo, anchor=tk.CENTER)         
                    piece_coords = canvas.coords(piece_id)
                    col = int((piece_coords[0]) // cell_size)
                    row = int((piece_coords[1]) // cell_size)

                    id_to_name[piece_id] = piece
                    pieces_on_board[(row, col)] = piece_id
                    canvas.images[f"{piece}_{i}_{j}"] = piece_photo
                    canvas.tag_bind(piece_id, "<ButtonPress-1>", on_drag_start)
                    canvas.tag_bind(piece_id, "<B1-Motion>", on_drag_motion)
                    canvas.tag_bind(piece_id, "<ButtonRelease-1>", on_drop)

    def on_drag_start(event):
        drag_data["piece_id"] = event.widget.find_closest(event.x, event.y)[0]
        drag_data["start_x"] = event.x
        drag_data["start_y"] = event.y
        key_to_delete = next((key for key, value in pieces_on_board.items() if value == drag_data["piece_id"]), None)
        if key_to_delete is not None:
            del pieces_on_board[key_to_delete]

    def dfs(pieces, start_time, solution, unformatted_solution, depth=1):
        global dfs_time

        if len(pieces) == 1:
            dfs_time = time.time() - start_time
            solve_sound.stop()
            solve_sound.play()
            return True
        
        for (row, col), piece_id in pieces.items():
            target = filter_moves(row, col, pieces)
            if not target:
                continue
        
            for (target_x, target_y) in target:
                if (target_x, target_y) == (row, col):
                    continue
                child = copy.deepcopy(pieces)
                piece_name = id_to_name[child[(row, col)]].capitalize()
                target_name = id_to_name[child[(target_x, target_y)]].capitalize()
                child[(target_x, target_y)] = child.pop((row, col))
                
                if dfs(child, start_time, solution, unformatted_solution, depth + 1):
                    unformatted_solution.append((row, col, target_x, target_y))
                    solution.append("   " * depth + f"{piece_name}{num_to_char_col[col]}{8-row} x {target_name}{num_to_char_col[target_y]}{8-target_x}")
                    return True     
        return False
    

    def A_star(board, start_time):
        global a_star_time
        open_set = []
        initial_state = frozenset(board.items())  
        heapq.heappush(open_set, (0, initial_state))

        came_from = {}
        g_score = {initial_state: 0}

        while open_set:
            _, current_state = heapq.heappop(open_set)
            
            if len(current_state) == 1:
                a_star_time = time.time() - start_time
                return reconstruct_path(came_from, current_state)

            for (row, col), piece_id in current_state:
                target_positions = filter_moves(row, col, dict(current_state))  

                for (target_x, target_y) in target_positions:
                    tentative_g = g_score[current_state] + 1
                    child = dict(current_state)  
                    
                    piece_name = id_to_name[child[(row, col)]].capitalize()
                    target_name = id_to_name[child[(target_x, target_y)]].capitalize()
                    child[(target_x, target_y)] = child.pop((row, col))  

                    child_state = frozenset(child.items())  

                    if child_state not in g_score:
                        came_from[child_state] = (current_state, f"{piece_name}{num_to_char_col[col]}{8-row} x {target_name}{num_to_char_col[target_y]}{8-target_x}")
                        g_score[child_state] = tentative_g
                        h_score = count_isolated_pieces(child)  
                        f_score = tentative_g + h_score

                        heapq.heappush(open_set, (f_score, child_state))  
        return None

    def reconstruct_path(came_from, state):
        path = []
        while state in came_from:
            path.append(came_from[state][1])
            state = came_from[state][0]
        path.reverse()
        return path
    
    def count_isolated_pieces(board):
        s = 0
        for (row, col), piece_id in board.items():
            if len(filter_moves(row, col, board)) == 0: #khong an duoc quan nao
                is_isolated = True 
                for (other_row, other_col), x in board.items():
                    if (other_row == row) and (other_col == col):
                       continue
                    if (row, col) in filter_moves(other_row, other_col, board): #Co 1 quan nao an duoc
                        is_isolated = False 
                        break
                if is_isolated:
                    s+=1
        return s

    def filter_moves(row, col, board):
        return legal_move(id_to_name[board[(row, col)]], col, row, board)
    
    def on_drag_motion(event):
        delta_x = event.x - drag_data["start_x"]
        delta_y = event.y - drag_data["start_y"]
        canvas.move(drag_data["piece_id"], delta_x, delta_y)
        drag_data["start_x"] = event.x
        drag_data["start_y"] = event.y

    def on_drop(event):
        piece_id = drag_data["piece_id"]
        if piece_id:
            piece_coords = canvas.coords(piece_id)
            cell_size = (canvas.winfo_width() // 8)
            col = int((piece_coords[0]) // cell_size)
            row = int((piece_coords[1]) // cell_size)
            if 0 <= row < 8 and 0 <= col < 8:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                canvas.coords(piece_id, x, y)
                if (row, col) in pieces_on_board:
                    old_piece_id = pieces_on_board[(row, col)]
                    canvas.delete(old_piece_id)
                    capture_sound.stop()
                    capture_sound.play() 

                pieces_on_board[(row, col)] = piece_id

                if len(pieces_on_board) == 1:
                    root.after(200, lambda: (end_sound.stop(), end_sound.play()))  
                    on_close(True)
                    return
                
    def on_key_press(event=None, each=10):
        global dfs_time
        global a_star_time 
        global unformated_solution
        if event and event.keysym != "Return":
            return 
        print("Solving...", flush=True)

        solution = []

        s=0
        for i in range(each):
            solution=[]
            dfs(pieces_on_board, time.time(), solution, unformatted_solution)
            s+=dfs_time
            dfs_time=0
        dfs_time=s/each
        if not solution:
            print("Not found solution")
            return
        print(f"‣ DFS : {dfs_time:.6f} seconds")
        while solution:
            print(f"{solution.pop()}")
        # /print(unformatted_solution)
        
        s=0
        for i in range(each):
            solution=A_star(pieces_on_board, time.time())
            s+=a_star_time
            a_star_time=0
        a_star_time=s/each
        print(f"‣ A* : {a_star_time:.6f} seconds")

        for depth, move in enumerate(solution):
            indent=depth+1
            print(" " * (indent * 3) + move)

    root.bind("<Return>", lambda event: on_key_press(event, each=1))
    root.bind("<space>", lambda event: animate_solution(list(reversed(unformatted_solution))))
    root.bind("<Configure>", resize)
    root.after(500, lambda: on_key_press(None, each=1)) 

    def on_close(wait=False):
        global pieces_on_board, id_to_name, dfs_time, a_star_time, unformated_solution
        pieces_on_board.clear()
        id_to_name.clear()
        unformatted_solution.clear()
        dfs_time = None
        a_star_time = None
        if wait:
            root.after(500, root.destroy)
        else:
            root.destroy()

    def animate_solution(solution, index=0):
        if not solution:
            print("Solving")
            return
        if index >= len(solution):
            solve_sound.stop()
            solve_sound.play()
            on_close()
            return

        move = solution[index]
        start_row, start_col, target_row, target_col = move
        try:
            piece_id = pieces_on_board[(start_row, start_col)]
        except KeyError:
            return
        step_x = (target_col - start_col) * (canvas.winfo_width() / 8 ) / 10
        step_y = (target_row - start_row) * (canvas.winfo_height() / 8 ) / 10

        def step_animation(step=0):
            if step < 10:
                canvas.move(piece_id, step_x, step_y)
                root.after(50, lambda: step_animation(step + 1))
            else:
                capture_sound.stop()
                capture_sound.play()
                pieces_on_board.pop((start_row, start_col))
                old_piece_id = pieces_on_board[(target_row, target_col)]
                canvas.delete(old_piece_id)
                pieces_on_board[(target_row, target_col)] = piece_id
                animate_solution(solution, index + 1)

        step_animation()


    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

testcase(config.NUM_TEST, config.SIZE)
