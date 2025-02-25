📂 ChessRangerSolver  
```
│── main.py          # File chính
│── move.py          # Xử lý nước đi  
│── config.py        # Cấu hình main  
│── getTest.py       # Lấy testcase từ https://www.puzzle-chess.com/  
│── log.txt          # Lời của tất cả testcase tạo bằng main.py  
│── testcases/       # Chứa các file tests từ 4 đến 11 quân cờ, mỗi file chứa 100 testcases  
│── assets/          # Ảnh bàn cờ, quân cờ & âm thanh  
│── dfs-sample.py    # File nháp  

  ```
Chạy chương trình:  
`python main.py`  
  
*Thay đổi số quân cờ bằng biến SIZE trong config.py*
  
Hỗ trợ:  
- Nạp puzzle ngẫu nhiên từ bộ testcases.
- Kéo thả để giải puzzle.
- Giải puzzle bằng DFS, A*.
- Lấy thêm testcase lưu vào tests/ (ancap từ web):     
   `python getTest.py --size <số quân cờ (4-11)> --num_test <số lượng testcase>`
