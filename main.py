import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import random
import copy
from move import legal_move
import time
import config
import vlc  
import sys

def testcase(num_tests, size):
    with open("tests/test" + str(size) + ".txt", "r", encoding="utf-8") as file:
        matrices = [eval(line.strip()) for line in file] 
    
    random.seed()  
    for i in range(num_tests):
        number = random.randint(0, 100)
        print('/' * 20, f'Testcase {number}','/' * 20)
        draw_chessboard_with_background_and_pieces(matrices[number])

pieces_on_board = {}
id_to_name = {}
num_to_char_col = {i: chr(97 + i) for i in range(8)}

capture_sound = vlc.MediaPlayer("assets/capture.mp3")
solve_sound = vlc.MediaPlayer("assets/solve.mp3")
start_sound = vlc.MediaPlayer("assets/game-start.mp3")
end_sound = vlc.MediaPlayer("assets/game-end.mp3")

def draw_chessboard_with_background_and_pieces(pieces):
    root = tk.Tk()
    root.title("Bàn cờ với nền và quân cờ")
    start_sound.stop()
    root.after(300, lambda: (start_sound.stop(), start_sound.play()))  

    initial_width, initial_height = 682, 682
    root.geometry(f"{initial_width}x{initial_height}+0+0")
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

    def solve(pieces, start_time, solution, depth=0):
        if len(pieces) == 1:
            elapsed_time = time.time() - start_time
            print(f"FOUND - Time: {elapsed_time:.6f} seconds")
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
                if solve(child, start_time, solution, depth + 1):
                    solution.append("   " * depth + f"{piece_name}{num_to_char_col[col]}{8-row} x {target_name}{num_to_char_col[target_y]}{8-target_x}")
                    return True     
        return False
                
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
            col = (piece_coords[0]) // cell_size
            row = (piece_coords[1]) // cell_size
            if 0 <= row < 8 and 0 <= col < 8:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                canvas.coords(piece_id, x, y)
                if (row, col) in pieces_on_board:
                    old_piece_id = pieces_on_board[(row, col)]
                    canvas.delete(old_piece_id)
                pieces_on_board[(row, col)] = piece_id

                if len(pieces_on_board) != 1:
                    capture_sound.stop()
                    capture_sound.play()  
                else:
                    end_sound.stop()
                    end_sound.play()
                    pieces_on_board.clear()
                    id_to_name.clear()
                    root.after(500, root.destroy) 
                    return
                
    def on_key_press(event):
        if event.keysym == "Return":
            print("Solving: ",end="")

            solution = []
            solve(pieces_on_board, time.time(), solution)
            while solution:
                print(solution.pop())

    root.bind("<Return>", on_key_press)
    root.bind("<Configure>", resize)
    root.mainloop()

testcase(config.NUM_TEST, config.SIZE)
