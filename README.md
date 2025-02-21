📂 ChessRangerSolver  
```
│── main.py          # File chính  
│── move.py          # Xử lý nước đi  
│── config.py        # Cấu hình main  
│── getTest.py       # Lấy testcase  
│── log.txt          # Giải tất cả testcase bằng main.py  
│── assets/          # Ảnh bàn cờ & quân cờ  
│── testcases/       # Chứa tests từ 4 đến 11 quân cờ  
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
