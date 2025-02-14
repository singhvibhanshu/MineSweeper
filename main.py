import tkinter as tk
import random
from tkinter import messagebox

class Cell:
    def __init__(self, master, game, x, y):
        self.master = master
        self.game = game
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

        self.button = tk.Button(master, width=3, height=1, command=self.reveal)
        self.button.grid(row=x, column=y)
        self.button.bind('<Button-3>', self.toggle_flag)

    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return

        self.is_revealed = True
        if self.is_mine:
            self.button.config(text="💣", bg="red")
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.game.end_game(False)
        else:
            self.button.config(text=str(self.neighbor_mines) if self.neighbor_mines > 0 else "", bg="lightgrey")
            if self.neighbor_mines == 0:
                self.game.reveal_neighbors(self.x, self.y)

    def toggle_flag(self, event):
        if self.is_revealed:
            return
        self.is_flagged = not self.is_flagged
        self.button.config(text="🚩" if self.is_flagged else "")

class Minesweeper:
    def __init__(self, root, size, mines):
        self.root = root
        self.size = size
        self.mines = mines
        self.cells = [[Cell(root, self, x, y) for y in range(size)] for x in range(size)]
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

    def end_game(self, won):
        messagebox.showinfo("Game Over", "You Win!" if won else "You Lost!")
        self.root.quit()

def main_menu():
    def start_game(size, mines):
        menu.destroy()
        root = tk.Tk()
        root.title("Minesweeper")
        Minesweeper(root, size, mines)
        root.mainloop()

    menu = tk.Tk()
    menu.title("Minesweeper - Select Difficulty")
    
    tk.Label(menu, text="Select Difficulty", font=("Arial", 14)).pack()

    tk.Button(menu, text="Easy (8x8, 10 Mines)", command=lambda: start_game(8, 10)).pack()
    tk.Button(menu, text="Medium (10x10, 15 Mines)", command=lambda: start_game(10, 15)).pack()
    tk.Button(menu, text="Hard (15x15, 30 Mines)", command=lambda: start_game(15, 30)).pack()

    menu.mainloop()

if __name__ == "__main__":
    main_menu()
