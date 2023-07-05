import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
import random

## GLOBALS 
bomb_locations = set()
flag_locations = set()
seconds = 0
#seconds_limit = 100

## FUNCTIONS
def center_window(window, width=300, height=200):
    if (width < 350):
        width = 350
    if (height < 180):
        height = 180
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def create_board_template():
    grid = list()
    for i in range(grid_size):
        row = list()
        for j in range(grid_size):
            # each element has three layers:
            #    0: the button
            #    1: the state: 'hidden', 'flagged' or 'exposed'
            #    2: the contents: number '(0-8)' or 'bomb'
            # state 'hidden' has view 'grass'
            # state 'flagged' has view 'flag'
            # state 'exposed' has view 'number' or 'bomb'
            element = [None, 'hidden', 'nothing']
            row.append(element)
        grid.append(row)
    return grid

def place_bombs(grid):
    global bomb_locations
    bomb_locations = set()
    bomb_number = int(bomb_number_selection.get())

    while len(bomb_locations) < bomb_number:
        rand_col = random.randint(0, grid_size-1)
        rand_row = random.randint(0, grid_size-1)
        if (rand_col, rand_row) in bomb_locations:
            continue
        else:
            bomb_locations.add((rand_col, rand_row))
            grid[rand_col][rand_row][2] = 'bomb'
    print(bomb_locations)

def determine_neighbor_counts(grid):
    for c in range(grid_size):
        for r in range(grid_size):
            if grid[c][r][2] == 'bomb':
                continue
            # check all 8 neighbors; if they don't fall outside the grid
            bomb_neighbors = 0
            cr_offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
            for dc, dr in cr_offsets:
                c_offset = c + dc
                r_offset = r + dr
                if (c_offset >= 0 and c_offset < grid_size) and (r_offset >= 0 and r_offset < grid_size):
                    #print(f'c = {c}; r = {r}; bomb: {grid[c_offset][r_offset][2]}')
                    if grid[c_offset][r_offset][2] == 'bomb':
                        bomb_neighbors += 1
            # for c_offset in [c + o for o in (-1, 0, 1) if c + o > 0 and c + o < grid_size]:
            #     for r_off set in [r + o for o in (-1, 0, 1) if r + o > 0 and r + o < grid_size]:
            #         if grid[c_offset][r_offset][2] == 'bomb':
            #             bomb_neighbors += 1
            grid[c][r][2] = bomb_neighbors

def create_board():
    grid = create_board_template()
    place_bombs(grid)
    determine_neighbor_counts(grid)
    return grid

def process_single_click(event, column, row):
    '''exposes the content and generates resulting action'''
    #print(f"Column {column} and row {row} clicked!")
    if board[column][row][1] == 'hidden':
        board[column][row][1] = 'exposed'
        contents = board[column][row][2]
        board[column][row][0]['image'] = number_imgs[contents]
        if contents == 'bomb':
            play_again = messagebox.showerror(title="You died!", message="You died!")
    # other states do not need an action


def process_right_click(event, column, row):
    '''toggles between flagged and unflagged'''
    #print(f"Column {column} and row {row} right-clicked!")
    loc = (column, row)
    if board[column][row][1] == 'hidden':
        board[column][row][1] = 'flagged'
        board[column][row][0]['image'] = img_flag
        flag_locations.add(loc)

    elif board[column][row][1] == 'flagged':
        board[column][row][1] = 'hidden'
        board[column][row][0]['image'] = img_grass
        flag_locations.remove(loc)
    # exposed does not need an action
    print(flag_locations)
    if flag_locations == bomb_locations:
        messagebox.showerror(title="You won!", message="You won!")
    #print(f'Found all: {flag_locations == bomb_locations}')


def update():
    global seconds
    seconds += 1
    seconds_label.configure(text=seconds)
    root_window.after(1000, update)

    # if seconds < limit:
    #     # schedule next update 1 second later
    #     window.after(1000, update)

def restart():
    global board
    global grid_size
    global tiles_frame

    grid_size = int(grid_size_selection.get())
    center_window(root_window, 100+(grid_size*45), 50+grid_size*50)

    #print(grid_size)
    board = create_board()
    
    tiles_frame.grid_forget()
    tiles_frame.destroy()

    tiles_frame = ttk.Frame(main_frame, padding = 4)
    tiles_frame.grid(column=0, row=2, columnspan = 4)

    ## GAME BOARD SETUP
    for i in range(grid_size**2):
        col = i % grid_size
        row = i // grid_size
        #img = number_imgs[board[col][row][2]]

        btn = tk.Button(tiles_frame, 
                        image=img_grass)
        btn.grid(column=col, row=row)
        btn.bind('<Button-1>', lambda event, clicked_col = col, clicked_row = row: process_single_click(event, clicked_col, clicked_row))
        btn.bind('<Button-2>', lambda event, clicked_col = col, clicked_row = row: process_right_click(event, clicked_col, clicked_row)) 
        btn.bind('<Button-3>', lambda event, clicked_col = col, clicked_row = row: process_right_click(event, clicked_col, clicked_row)) 

        board[col][row][0] = btn

## MAIN WINDOW SETUP
root_window = tk.Tk()
root_window.title('Mine Hunter')

## UI GLOBALS
img_bomb = tk.PhotoImage(file = r"bomb_32.png")
img_grass = tk.PhotoImage(file = r"grass_32.png")
img_flag = tk.PhotoImage(file = r"flag_32.png")

number_imgs = {'bomb': img_bomb, 
               0: tk.PhotoImage(file = r"zero_32.png"), 
               1: tk.PhotoImage(file = r"one_32.png"), 
               2: tk.PhotoImage(file = r"two_32.png"), 
               3: tk.PhotoImage(file = r"three_32.png"), 
               4: tk.PhotoImage(file = r"four_32.png"), 
               5: tk.PhotoImage(file = r"five_32.png"), 
               6: tk.PhotoImage(file = r"six_32.png"), 
               7: tk.PhotoImage(file = r"seven_32.png"), 
               8: tk.PhotoImage(file = r"eight_32.png")}

## WINDOW BUILD
main_frame = ttk.Frame(root_window, padding=10)
main_frame.grid()
#ttk.Label(main_frame, text="Mine Hunter").grid(column=0, row=0)

grid_size_var = StringVar()
grid_size_label = tk.Label(main_frame, textvariable = grid_size_var)
grid_size_var.set("Grid size")
grid_size_label.grid(column=0, row=0)

grid_size_selection = ttk.Spinbox(main_frame, from_ = 5, to = 12, width=5)
grid_size_selection.grid(column=1, row=0)
grid_size_selection.set(6)

bomb_number_var = StringVar()
bomb_number_label = tk.Label(main_frame, textvariable = bomb_number_var)
bomb_number_var.set("Bombs")
bomb_number_label.grid(column=2, row=0)

bomb_number_selection = ttk.Spinbox(main_frame, from_ = 5, to = 25, width=5)
bomb_number_selection.grid(column=3, row=0)
bomb_number_selection.set(9)

elapsed_time_label = tk.Label(main_frame, text="Time")
elapsed_time_label.grid(column=1, row=1)

seconds_label = tk.Label(main_frame, text=seconds)
seconds_label.grid(column=2, row=1)

tiles_frame = ttk.Frame(main_frame, padding = 4)
tiles_frame.grid(column=0, row=2, columnspan = 4)

## START APP
restart()

ttk.Button(master=main_frame, text="Restart", command=restart).grid(column=0, row=3)
ttk.Button(master=main_frame, text="Quit", command=root_window.destroy).grid(column=1, row=3)

root_window.after(1000, update) # start the update 1 second later
root_window.mainloop()

