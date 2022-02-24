"""
@author: Gabriel Castillo, Marcelo Alvarez
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
from timeit import repeat
from turtle import heading, width
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(width, height):
    """returns a grid of width x height random values"""
    return np.random.choice(vals, width*height, p=[0.2, 0.8]).reshape(width, height)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def read_TXT():
    print("\n\n You've chosen to input a file.")
    file = open("C:\\Users\\mache\\Documents\\Universidad\\8vo Semestre\\Simulation and Visualization\\com139-class-master\\GoL\\1_Con.txt", "r")
    text = file.read().split("\n")
    width = int(text[0].split(" ")[0])
    height = int(text[0].split(" ")[1])
    frames = int(text[1])
    grid = np.zeros(width * height).reshape(width, height)
    
    for line in text[2:]:
        x = int(line.split(" ")[0])
        y = int(line.split(" ")[1])
        grid[x, y] = ON
    
    file.close()

    return grid, width, height, frames 

def input_config():
    print("\n\n You've chosen to input the data here. Please, enter your values below.")
    width = int(input("Width: ") or 50)
    height = int(input("Height: ") or 50)
    frames = int(input("Frames: ") or 200)

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    grid = randomGrid(width, height)
    return grid, width, height, frames

def update(frameNum, img, grid, width, height, frames):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    #print("pre grid: ", grid)
    newGrid = grid.copy()
    #print("new grid: ", newGrid)
    # Implement the rules of Conway's Game of Life
    for row in range(width):
        for col in range(height):
            num_alive = check_neighbors(grid, row, col, width, height)
            if newGrid[row, col] == ON:
                if num_alive < 2 or num_alive > 3:
                    newGrid[row, col] = OFF
            if newGrid[row, col] == OFF:
                if num_alive == 3:
                    newGrid[row, col] = ON

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    #print("grid_up", grid)
    return img,

def check_neighbors(grid, row, col, width, height):
    x = row
    y = col
    alive = 0
    for i in range(x - 1, x + 2):
        if i >= 0 and i < width:
            for j in range(y - 1, y + 2):
                if j >= 0 and j < height:
                    if not (x == i and y == j) and grid[i, j] == ON:
                        alive += 1
    return alive

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")

    print(" Welcome to the Game of Life Simulation.")
    print(" Please, select your way of introducing data: \n")
    print(" 1.- Use a .txt file with the configurations")
    print(" 2.- Enter your own configuration in the terminal")
    option = int(input("Select your option: "))
    if option == 1:
        grid, width, height, frames = read_TXT()
    if option == 2:
        grid, width, height, frames = input_config()

    # set animation update interval
    updateInterval = 50

    # Uncomment lines to see the "glider" demo
    #grid = np.zeros(N*N).reshape(N, N)
    #addGlider(1, 1, grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='gray')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, width, height, frames, ),
                                  frames = frames,
                                  interval = updateInterval,
                                  save_count = 50, 
                                  repeat = False)

    plt.show()

# call main
if __name__ == '__main__':
    main()