import numpy as np
import matplotlib.pyplot as plt
import time

def solve_sudoku(board):
    """
    Solves a given Sudoku board using backtracking.
    :param board: list of list of integers representing a Sudoku puzzle (0 represents an empty cell)
    :return: True if the board is solvable, False otherwise
    """
    def find_empty_cell():
        # Finds the next empty cell in the board
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_valid(row, col, num):
        # Checks if it's valid to place num at the (row, col) position
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Checks if it's valid to place num in the 3x3 sub-grid
        subgrid_row, subgrid_col = row // 3 * 3, col // 3 * 3
        for i in range(subgrid_row, subgrid_row + 3):
            for j in range(subgrid_col, subgrid_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve():
        # Uses backtracking to solve the Sudoku puzzle
        empty_cell = find_empty_cell()
        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for num in range(1, 10):
            if is_valid(row, col, num):
                board[row][col] = num
                if solve():
                    return True
                board[row][col] = 0

        return False

    # Start measuring time
    start_time = time.time()

    # Solves the Sudoku puzzle using backtracking
    solved = solve()

    # Stop measuring time
    end_time = time.time()

    if solved:
        print("Sudoku solved successfully!")
    else:
        print("Sudoku is unsolvable.")

    # Calculate and print the solving time
    solving_time = end_time - start_time
    print(f"Solving time: {solving_time} seconds")

    return solved

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

solve_sudoku(normal_sudoku)

plot_sudoku(normal_sudoku)