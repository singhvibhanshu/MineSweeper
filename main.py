import tkinter as tk
import random
from tkinter import messagebox

class Cell:
    def __init__(self, master, x, y, is_mine=False):
        self.master = master
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.button = tk.Button(master, width=2, command=self.reveal)
        self.button.bind('<Button-3>', self.toggle_flag)
        self.button.grid(row=x, column=y)

    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return
        self.is_revealed = True
        if self.is_mine:
            self.button.config(text='*', bg='red')
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.master.quit()
        else:
            self.button.config(text=str(self.neighbor_mines), bg='lightgrey')
            if self.neighbor_mines == 0:
                self.master.reveal_neighbors(self.x, self.y)

    def toggle_flag(self, event):
        if self.is_revealed:
            return
        self.is_flagged = not self.is_flagged
        self.button.config(text='F' if self.is_flagged else '')

class Minesweeper:
    def __init__(self, root, size, mines):
        self.root = root
        self.size = size
        self.mines = mines
        self.cells = [[Cell(self, x, y) for y in range(size)] for x in range(size)]
        self.place_mines()
        self.calculate_neighbors()

    def place_mines(self):
        positions = random.sample([(x, y) for x in range(self.size) for y in range(self.size)], self.mines)
        for x, y in positions:
            self.cells[x][y].is_mine = True

    def calculate_neighbors(self):
        for x in range(self.size):
            for y in range(self.size):
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].neighbor_mines = sum(
                        self.cells[i][j].is_mine
                        for i in range(max(0, x-1), min(self.size, x+2))
                        for j in range(max(0, y-1), min(self.size, y+2))
                    )

    def reveal_neighbors(self, x, y):
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if not self.cells[i][j].is_revealed:
                    self.cells[i][j].reveal()

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root, size=10, mines=15)  # Example: 10x10 grid with 15 mines
    root.mainloop()

if __name__ == "__main__":
    main()
