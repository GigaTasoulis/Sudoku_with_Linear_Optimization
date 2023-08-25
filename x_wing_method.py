import numpy as np
import matplotlib.pyplot as plt
import time


def apply_x_wing(board):
   
      for num in range(1, 10):
          # Check X-Wing pattern in rows
          for row in range(9):
              candidate_cols = []
              for col in range(9):
                  if board[row][col] == num:
                      candidate_cols.append(col)
              if len(candidate_cols) == 2:
                  col1, col2 = candidate_cols
                  # Check if the same two columns appear in another row
                  for other_row in range(row + 1, 9):
                      if board[other_row][col1] == num and board[other_row][col2] == num:
                          # Eliminate num from other cells in the same columns
                          for eliminate_row in range(9):
                              if eliminate_row != row and eliminate_row != other_row:
                                  if board[eliminate_row][col1] == num:
                                      board[eliminate_row][col1] = 0
                                  if board[eliminate_row][col2] == num:
                                      board[eliminate_row][col2] = 0

          # Check X-Wing pattern in columns
          for col in range(9):
              candidate_rows = []
              for row in range(9):
                  if board[row][col] == num:
                      candidate_rows.append(row)
              if len(candidate_rows) == 2:
                  row1, row2 = candidate_rows
                  # Check if the same two rows appear in another column
                  for other_col in range(col + 1, 9):
                      if board[row1][other_col] == num and board[row2][other_col] == num:
                          # Eliminate num from other cells in the same rows
                          for eliminate_col in range(9):
                              if eliminate_col != col and eliminate_col != other_col:
                                  if board[row1][eliminate_col] == num:
                                      board[row1][eliminate_col] = 0
                                  if board[row2][eliminate_col] == num:
                                      board[row2][eliminate_col] = 0

def is_valid(board, row, col, num):
    # Check if the current number placement is valid in the given row
    for c in range(9):
        if board[row][c] == num:
            return False

    # Check if the current number placement is valid in the given column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check if the current number placement is valid in the corresponding 3x3 grid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Undo the current placement if it leads to an invalid solution
                return False
    return True


def plot_sudoku(grid):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(grid, cmap='binary', vmin=0, vmax=9)
    ax.set_xticks(np.arange(-.5, 9, 1))
    ax.set_yticks(np.arange(-.5, 9, 1))
    ax.grid(color='black', linestyle='-', linewidth=2)
    ax.tick_params(axis='both', length=0)

    for i in range(0, 10, 3):
        ax.axhline(i-0.5, color='purple', linewidth=3)
        ax.axvline(i-0.5, color='purple', linewidth=3)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j, i, grid[i][j], color='blue', fontsize=16, ha='center', va='center')
            else:
              ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='black', linewidth=2))
    plt.axis('off')
    plt.show()


normal_sudoku = [
                    [0,0,6, 7,0,0, 0,8,1],
                    [0,4,0, 0,0,0, 9,0,0],
                    [0,8,0, 0,0,3, 0,0,0],
                # ------------------
                    [0,5,0, 0,7,0, 0,0,0],
                    [0,0,3, 5,0,6, 7,0,0],
                    [0,0,0, 0,3,0, 0,5,0],
                # ------------------
                    [0,0,0, 8,0,0, 0,6,0],
                    [0,0,2, 0,0,0, 0,9,0],
                    [5,6,0, 0,0,9, 3,0,0]
                ]

# Start measuring time
start_time = time.time()

apply_x_wing(normal_sudoku)
solve_sudoku(normal_sudoku)

# Stop measuring time
end_time = time.time()
solving_time = end_time - start_time
print("Sudoku solved succesfully!")
print(f"Solving time: {solving_time} seconds")

plot_sudoku(normal_sudoku)