import pulp as plp
import matplotlib.pyplot as plt
import numpy as np

def solve_sudoku(input_sudoku):
    # Create the linear programming problem
    prob = plp.LpProblem("Sudoku_Solver")


    # Set the objective function
    # Sudoku works only on the constraints 
    # There is no objective function that we are trying maximize or minimize.
    # Set a dummy objective
    objective = plp.lpSum(0)
    prob.setObjective(objective)

    rows = range(0,9)
    cols = range(0,9)
    grids = range(0,9)
    values = range(1,10)

    # Decision Variable/Target variable
    grid_vars = plp.LpVariable.dicts("grid_value", (rows,cols,values), cat='Binary')
    
    # Fill the prefilled values from input sudoku as constraints
    for row in rows:
        for col in cols:
            if(input_sudoku[row][col] != 0):
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for value in values]),
                                        sense=plp.LpConstraintEQ, 
                                        rhs=input_sudoku[row][col], 
                                        name=f"constraint_prefilled_{row}_{col}"))

    # CONSTRAINT 1: Constraint to ensure only one value is filled for a cell
    for row in rows:
        for col in cols:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value] for value in values]),
                                        sense=plp.LpConstraintEQ, rhs=1, name=f"constraint_sum_{row}_{col}"))


    # CONSTRAINT 2: Constraint to ensure that values from 1 to 9 is filled only once in a row        
    for row in rows:
        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for col in cols]),
                                        sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_row_{row}_{value}"))

    # CONSTRAINT 3: Constraint to ensure that values from 1 to 9 is filled only once in a column        
    for col in cols:
        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for row in rows]),
                                        sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_col_{col}_{value}"))


    # CONSTRAINT 4: Constraint to ensure that values from 1 to 9 is filled only once in the 3x3 grid       
    for grid in grids:
        grid_row  = int(grid/3)
        grid_col  = int(grid%3)

        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[grid_row*3+row][grid_col*3+col][value]*value  for col in range(0,3) for row in range(0,3)]),
                                    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_grid_{grid}_{value}"))

    # Additional constraint to ensure blocks for red colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]] ) == 1         

    # Additional constraint to ensure blocks for purple colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(0,1),(0,4),(0,7),(3,1),(3,4),(3,7),(6,1),(6,4),(6,7)]] ) == 1  
    
    # Additional constraint to ensure blocks for olive colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(0,2),(0,5),(0,8),(3,2),(3,5),(3,8),(6,2),(6,5),(6,8)]] ) == 1  
    
    # Additional constraint to ensure blocks for yellow colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(1,0),(1,3),(1,6),(4,0),(4,3),(4,6),(7,0),(7,3),(7,6)]] ) == 1  
    
    # Additional constraint to ensure blocks for black colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]] ) == 1  
       
    # Additional constraint to ensure blocks for cyan colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(1,2),(1,5),(1,8),(4,2),(4,5),(4,8),(7,2),(7,5),(7,8)]] ) == 1  
    
    # Additional constraint to ensure blocks for blue colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(2,0),(2,3),(2,6),(5,0),(5,3),(5,6),(8,0),(8,3),(8,6)]] ) == 1  
    
    # Additional constraint to ensure blocks for lightgray colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(2,1),(2,4),(2,7),(5,1),(5,4),(5,7),(8,1),(8,4),(8,7)]] ) == 1  
       
    # Additional constraint to ensure blocks for pink colors contain numbers 1:9
    for value in values:
       prob += plp.lpSum([grid_vars[row][col][value] for (row, col) in [(2,2),(2,5),(2,8),(5,2),(5,5),(5,8),(8,2),(8,5),(8,8)]] ) == 1  
    
    # Solve the problem
    prob.solve()               

    print(f'Solution Status = {plp.LpStatus[prob.status]}')

    # Code to extract the final solution grid
    solution = np.zeros((9, 9), dtype=int)
    for row in rows:
        for col in cols:
            for value in values:
                if grid_vars[row][col][value].varValue == 1:
                    solution[row][col] = value
                    
    return solution


       
normal_sudoku = np.array([
                    [0,0,6, 7,0,0, 0,8,1],
                    [0,4,0, 0,0,0, 9,0,0],
                    [0,8,0, 0,0,3, 0,0,0],
                # -------0--0---------
                    [0,5,0, 0,7,0, 0,0,0],
                    [0,0,3, 5,0,6, 7,0,0],
                    [0,0,0, 0,3,0, 0,5,0],
                # -------0--0---------
                    [0,0,0, 8,0,0, 0,6,0],
                    [0,0,2, 0,0,0, 0,9,0],
                    [5,6,0, 0,0,9, 3,0,0]
                ])

solution = solve_sudoku(normal_sudoku)       

# Plot the solved Sudoku grid
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(solution, cmap='binary', vmin=0, vmax=9)
ax.set_xticks(np.arange(-.5, 9, 1))
ax.set_yticks(np.arange(-.5, 9, 1))


# add the boundaries of the 3x3 squares
for i in range(0, 10, 3):
    ax.axhline(i-0.5, color='purple', linewidth=3)
    ax.axvline(i-0.5, color='purple', linewidth=3)


for i in range(9):
    for j in range(9):
        if normal_sudoku[i][j] != 0:
            ax.text(j, i, normal_sudoku[i][j], color='blue', fontsize=16, ha='center', va='center')
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, linewidth=1))
        else:
            ax.text(j, i, int(solution[i][j]), color='green', fontsize=16, ha='center', va='center')
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, linewidth=1))
            
# Coloring every 3 blocks horizontally and vertically to make the constraint visible            
for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        color = "r"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(1, 9, 3):
    for j in range(0, 9, 3):
        color = "y"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(2, 9, 3):
    for j in range(0, 9, 3):
        color = "cyan"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(0, 9, 3):
    for j in range(1, 9, 3):
        color = "m"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(1, 9, 3):
    for j in range(1, 9, 3):
        color = "black"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(2, 9, 3):
    for j in range(1, 9, 3):
        color = "0.8"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(0, 9, 3):
    for j in range(2, 9, 3):
        color = "olive"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(1, 9, 3):
    for j in range(2, 9, 3):
        color = "aquamarine"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
for i in range(2, 9, 3):
    for j in range(2, 9, 3):
        color = "pink"
        ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color=color))
        
plt.axis('off')
plt.show()
