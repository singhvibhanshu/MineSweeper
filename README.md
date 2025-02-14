# Minesweeper

A simple Minesweeper game built using Python and Tkinter.

## Features

- **Customizable Difficulty Levels:** Choose from Easy (8x8, 10 mines), Medium (10x10, 15 mines), Hard (15x15, 30 mines), or define your own custom settings.
- **Intuitive Controls:**
  - Left-click to reveal a cell.
  - Right-click to flag or unflag a cell as a mine.
  - Double-click to reveal surrounding cells if the number of flagged cells matches the number of mines around.
- **Real-Time Statistics:** Track your game statistics, including the number of games played, wins, win rate, and best times for each difficulty level.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/singhvibhanshu/MineSweeper.git
   cd MineSweeper
   ```
2. **Install Dependencies:**
   Ensure you have Python installed on your system. The game uses the Tkinter library, which comes pre-installed with standard Python distributions. If for some reason it's not installed, you can install it using:
   ```bash
   pip install tk
   ```

## Usage

Run the game using the following command:
```bash
python minesweeper.py
```
Upon launching, you'll be presented with a menu to select the difficulty level or define custom game settings.

## How to Play

- **Objective:** Uncover all cells that do not contain mines.
- **Controls:**
  - **Reveal a Cell:** Left-click on the cell.
  - **Flag/Unflag a Cell:** Right-click on the cell to mark it as a potential mine or remove the flag.
  - **Chord:** Double-click on a revealed cell to uncover its neighboring cells if the number of flagged cells around matches the number of mines.

## Statistics

The game maintains statistics for each difficulty level, including:
- Total games played
- Number of wins
- Win rate percentage
- Best completion time

You can view these statistics from the main menu by selecting the "View Statistics" option.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

