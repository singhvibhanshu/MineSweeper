import tkinter as tk
import random
import time
import json
import os  # For robust file path handling
from tkinter import messagebox, simpledialog

class Cell:
    def __init__(self, master, game, x, y):
        self.master = master
        self.game = game
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_question_mark = False
        self.neighbor_mines = 0

        self.button = tk.Button(master, width=2, height=1, font=("Arial", 12), relief=tk.RAISED, bd=2, command=self.reveal)
        self.button.grid(row=x, column=y, padx=0, pady=0)
        self.button.bind('<Button-3>', self.toggle_flag)
        self.button.bind('<Double-Button-1>', self.chord)

    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return

        if not self.game.game_started:
            self.game.start_timer()
            self.game.game_started = True

        self.is_revealed = True
        if self.is_mine:
            self.button.config(text="💣", bg="red", relief=tk.SUNKEN)
            self.game.reveal_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.game.end_game(False)
        else:
            self.button.config(text=str(self.neighbor_mines) if self.neighbor_mines > 0 else "",
                               bg="lightgrey", relief=tk.SUNKEN, disabledforeground="black")
            self.button.config(state=tk.DISABLED)

            if self.neighbor_mines == 0:
                self.game.reveal_neighbors(self.x, self.y)
            self.game.check_win_condition()

    def toggle_flag(self, event):
        if self.is_revealed:
            return

        if self.is_question_mark:
            self.is_question_mark = False
            self.is_flagged = False
            self.button.config(text="", fg="black")
        elif self.is_flagged:
            self.is_flagged = False
            self.is_question_mark = True
            self.button.config(text="?", fg="blue")
        else:
            self.is_flagged = True
            self.is_question_mark = False
            self.button.config(text="🚩", fg="red")

        self.game.update_mine_counter()

    def chord(self, event):
        if not self.is_revealed or self.neighbor_mines == 0:
            return

        flagged_neighbors = 0
        unrevealed_neighbors = []
        for i in range(max(0, self.x - 1), min(self.game.size, self.x + 2)):
            for j in range(max(0, self.y - 1), min(self.game.size, self.y + 2)):
                neighbor_cell = self.game.cells[i][j]
                if neighbor_cell != self:
                    if neighbor_cell.is_flagged:
                        flagged_neighbors += 1
                    if not neighbor_cell.is_revealed and not neighbor_cell.is_flagged:
                        unrevealed_neighbors.append(neighbor_cell)

        if flagged_neighbors == self.neighbor_mines:
            for cell in unrevealed_neighbors:
                cell.reveal()

class Minesweeper:
    def __init__(self, root, size, mines, init_grid=True):
        self.root = root
        self.size = size
        self.mines = mines
        self.game_started = False
        self.timer_running = False
        self.start_time = 0
        self.timer_var = tk.StringVar()
        self.mines_remaining_var = tk.StringVar()
        
        if init_grid:
            self.cells = [[Cell(root, self, x, y) for y in range(size)] for x in range(size)]
            self.flags_placed = 0

            self.mine_counter_label = tk.Label(root, textvariable=self.mines_remaining_var, font=("Arial", 12))
            self.mine_counter_label.grid(row=size, column=0, columnspan=size // 2, sticky="w", padx=5, pady=5)

            self.timer_label = tk.Label(root, textvariable=self.timer_var, font=("Arial", 12))
            self.timer_label.grid(row=size, column=size // 2, columnspan=size // 2, sticky="e", padx=5, pady=5)

            self.place_mines()
            self.calculate_neighbors()
            self.update_mine_counter()
            self.update_timer_display()
        else:
            self.cells = []

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
                        for i in range(max(0, x - 1), min(self.size, x + 2))
                        for j in range(max(0, y - 1), min(self.size, y + 2))
                    )

    def reveal_neighbors(self, x, y):
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if not self.cells[i][j].is_revealed and not self.cells[i][j].is_flagged:
                    self.cells[i][j].reveal()

    def reveal_all_mines(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].is_mine:
                    self.cells[x][y].button.config(text="💣", bg="red", relief=tk.SUNKEN, disabledforeground="black")
                    self.cells[x][y].button.config(state=tk.DISABLED)

    def end_game(self, won):
        self.stop_timer()
        if won:
            messagebox.showinfo("Game Over", "You Win! Time: " + self.timer_var.get())
            self.update_stats(won=True)
        else:
            self.update_stats(won=False)
        # Destroy the window to exit the game completely.
        self.root.destroy()

    def check_win_condition(self):
        hidden_cells_count = 0
        for x in range(self.size):
            for y in range(self.size):
                if not self.cells[x][y].is_revealed and not self.cells[x][y].is_mine:
                    hidden_cells_count += 1

        if hidden_cells_count == 0:
            self.reveal_all_mines()
            self.end_game(True)

    def update_mine_counter(self):
        self.flags_placed = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].is_flagged:
                    self.flags_placed += 1
        mines_remaining = max(0, self.mines - self.flags_placed)
        self.mines_remaining_var.set(f"Mines: {mines_remaining}")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_var.set(f"Time: {timer_string}")
            self.root.after(1000, self.update_timer)

    def update_timer_display(self):
        self.timer_var.set("Time: 00:00")

    # --- Statistics Handling ---
    def get_stats_file_path(self):
        stats_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(stats_dir, "minesweeper_stats.json")

    def load_stats(self):
        stats_file = self.get_stats_file_path()
        try:
            with open(stats_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "easy": {"games": 0, "wins": 0, "best_time": None},
                "medium": {"games": 0, "wins": 0, "best_time": None},
                "hard": {"games": 0, "wins": 0, "best_time": None},
                "custom": {"games": 0, "wins": 0, "best_time": None}
            }

    def save_stats(self, stats):
        stats_file = self.get_stats_file_path()
        with open(stats_file, "w") as f:
            json.dump(stats, f)

    def update_stats(self, won):
        stats = self.load_stats()
        difficulty_str = self.get_difficulty_str()
        stats[difficulty_str]["games"] += 1
        if won:
            stats[difficulty_str]["wins"] += 1
            current_time_sec = int(time.time() - self.start_time)
            if stats[difficulty_str]["best_time"] is None or current_time_sec < stats[difficulty_str]["best_time"]:
                stats[difficulty_str]["best_time"] = current_time_sec
        self.save_stats(stats)

    def get_difficulty_str(self):
        if self.size == 8 and self.mines == 10:
            return "easy"
        elif self.size == 10 and self.mines == 15:
            return "medium"
        elif self.size == 15 and self.mines == 30:
            return "hard"
        else:
            return "custom"

    def show_stats_window(self):
        stats = self.load_stats()
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistics")
        stats_text = ""
        difficulties = ["easy", "medium", "hard", "custom"]
        difficulty_names = {"easy": "Easy", "medium": "Medium", "hard": "Hard", "custom": "Custom"}

        for diff in difficulties:
            best_time_str = "N/A"
            if stats[diff]["best_time"] is not None:
                minutes = stats[diff]["best_time"] // 60
                seconds = stats[diff]["best_time"] % 60
                best_time_str = f"{minutes:02d}:{seconds:02d}"

            stats_text += f"{difficulty_names[diff]} Difficulty:\n"
            stats_text += f"  Games Played: {stats[diff]['games']}\n"
            stats_text += f"  Wins: {stats[diff]['wins']}\n"
            win_rate = (f"  Win Rate: {stats[diff]['wins'] / stats[diff]['games'] * 100:.2f}%\n"
                        if stats[diff]['games'] > 0 else "  Win Rate: 0.00%\n")
            stats_text += win_rate
            stats_text += f"  Best Time: {best_time_str}\n\n"

        stats_label = tk.Label(stats_window, text=stats_text, font=("Arial", 10), justify=tk.LEFT)
        stats_label.pack(padx=20, pady=20)

def main_menu():
    def start_game(size, mines):
        menu.destroy()
        root = tk.Tk()
        root.title(f"Minesweeper - {size}x{size}, {mines} Mines")
        minesweeper_game = Minesweeper(root, size, mines)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=lambda: restart_game(minesweeper_game, size, mines))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="Game", menu=filemenu)

        statsmenu = tk.Menu(menubar, tearoff=0)
        statsmenu.add_command(label="View Statistics", command=minesweeper_game.show_stats_window)
        menubar.add_cascade(label="Statistics", menu=statsmenu)

        root.config(menu=menubar)
        root.mainloop()

    def restart_game(game_instance, size, mines):
        game_instance.stop_timer()
        for x in range(size):
            for y in range(size):
                game_instance.cells[x][y].button.destroy()
        game_instance.root.destroy()
        start_game(size, mines)

    def custom_game():
        menu.destroy()
        custom_menu = tk.Tk()
        custom_menu.title("Custom Game")

        tk.Label(custom_menu, text="Grid Size (min 5, max 30):").grid(row=0, column=0, padx=5, pady=5)
        size_entry = tk.Entry(custom_menu)
        size_entry.grid(row=0, column=1, padx=5, pady=5)
        size_entry.insert(0, "15")

        tk.Label(custom_menu, text="Number of Mines:").grid(row=1, column=0, padx=5, pady=5)
        mines_entry = tk.Entry(custom_menu)
        mines_entry.grid(row=1, column=1, padx=5, pady=5)
        mines_entry.insert(0, "30")

        def validate_and_start_custom_game():
            try:
                size_val = int(size_entry.get())
                mines_val = int(mines_entry.get())
                if not 5 <= size_val <= 30:
                    messagebox.showerror("Input Error", "Grid size must be between 5 and 30.")
                    return
                if not 1 <= mines_val < size_val * size_val:
                    messagebox.showerror("Input Error", "Number of mines must be at least 1 and less than total cells.")
                    return
                start_game(size_val, mines_val)
                custom_menu.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Invalid input. Please enter numbers.")

        tk.Button(custom_menu, text="Start Custom Game", command=validate_and_start_custom_game).grid(row=2, columnspan=2, pady=10)
        custom_menu.mainloop()

    menu = tk.Tk()
    menu.title("Minesweeper - Select Difficulty")

    tk.Label(menu, text="Select Difficulty", font=("Arial", 14)).pack(pady=10)
    tk.Button(menu, text="Easy (8x8, 10 Mines)", command=lambda: start_game(8, 10)).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(menu, text="Medium (10x10, 15 Mines)", command=lambda: start_game(10, 15)).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(menu, text="Hard (15x15, 30 Mines)", command=lambda: start_game(15, 30)).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(menu, text="Custom Game", command=custom_game).pack(fill=tk.X, padx=20, pady=5)
    # Use init_grid=False so no grid is created when showing stats.
    tk.Button(menu, text="View Statistics", command=lambda: Minesweeper(menu, 8, 10, init_grid=False).show_stats_window()).pack(fill=tk.X, padx=20, pady=5)

    menu.mainloop()

if __name__ == "__main__":
    main_menu()
