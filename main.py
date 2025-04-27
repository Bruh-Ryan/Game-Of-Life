import tkinter as tk
import time

#global variables for grid state and label references
grid_state = []  #to store grid state
labels = []  #to store label widgets for each cell


def create_grid(rows, columns, unit_size):
    
    global grid_state, labels
    
    #initialize grid_state to False (dead) for all cells
    grid_state = [[False for _ in range(columns)] for _ in range(rows)]
    
    
    for r in range(rows):
        row_labels = []
        for c in range(columns):
            label = tk.Label(root, borderwidth=1, relief="solid", width=3, height=5, bg="black")
            label.grid(row=r, column=c, padx=1, pady=1)
            label.row = r  
            label.col = c  
            label.bind("<Button-1>", on_click)  
            row_labels.append(label)
        labels.append(row_labels)

#function to handle clicks on grid cells
def on_click(event):
    label = event.widget
    row, col = label.row, label.col
    
    #toggle the state of the cell between alive and dead
    grid_state[row][col] = not grid_state[row][col]
    if grid_state[row][col]:
        label.config(bg="lightblue")  # Alive
    else:
        label.config(bg="black")  # Dead




# function to count alive neighbors 
def count_alive_neighbors(row, col):
    alive_count = 0
    for i in range(row - 1, row + 2):                   # Check rows 
        for j in range(col - 1, col + 2):  
            if 0 <= i < len(grid_state) and 0 <= j < len(grid_state[0]) and (i != row or j != col):
                if grid_state[i][j]:        # count alive neighbors
                    alive_count += 1
    return alive_count

#   function to update the grid based on conways rules
def update_grid():
    global grid_state
    new_grid_state = [[False for _ in range(len(grid_state[0]))] for _ in range(len(grid_state))]

    for r in range(len(grid_state)):
        for c in range(len(grid_state[0])):
            alive_neighbors = count_alive_neighbors(r, c)
            if grid_state[r][c]:
                # rule 1: a live cell with 2 or 3 neighbors survives
                if alive_neighbors in [2, 3]:
                    new_grid_state[r][c] = True
            else:
                # rule 2: a dead cell with exactly 3 neighbors becomes alive
                if alive_neighbors == 3:
                    new_grid_state[r][c] = True
    
            # ppdate the label based on the new state
            if new_grid_state[r][c]:
                labels[r][c].config(bg="lightblue")
            else:
                labels[r][c].config(bg="black")

    grid_state = new_grid_state  # Update the grid state

#function to start the game loop
def start_game():
    while True:
        update_grid()  # Update the grid to the next generation
        root.update_idletasks()
        root.update()
        time.sleep(0.5)  # Slow down the game loop for better visibility

#main part of the program
root = tk.Tk()
root.title("Conway's Game of Life")

#set the grid size
rows = 10
columns = 10
unit_size = 2 


create_grid(rows, columns, unit_size)


start_button = tk.Button(root, text="Start", command=start_game)
start_button.grid(row=rows, column=0, columnspan=columns, pady=10)

#run the Tkinter main loop
root.mainloop()
