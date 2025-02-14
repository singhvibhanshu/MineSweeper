# Minesweeper

A Python implementation of the classic Minesweeper game using the `tkinter` library for the graphical user interface.

## Features

- **Difficulty Levels**: Choose from Easy, Medium, or Hard modes, each with varying grid sizes and mine counts.
- **Intuitive Controls**:
  - **Left-Click**: Reveal a cell.
  - **Right-Click**: Flag or unflag a cell as a potential mine.
- **Automatic Cell Reveal**: Uncover all adjacent non-mine cells when a cell with zero neighboring mines is revealed.
- **Game Over Detection**: Alerts when a mine is uncovered or when all non-mine cells are successfully revealed.

## Requirements

- Python 3.x
- `tkinter` library (usually included with standard Python installations)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/singhvibhanshu/MineSweeper.git
   cd MineSweeper
   ```

2. **Run the Game**:
   ```bash
   python minesweeper.py
   ```

## How to Play

1. **Launch the Game**: Run the `minesweeper.py` script.
2. **Select Difficulty**: Choose your desired difficulty level from the main menu.
3. **Gameplay**:
   - **Reveal Cells**: Left-click on cells to uncover them.
   - **Flag Mines**: Right-click on cells to mark or unmark them as potential mines.
4. **Winning the Game**: Successfully reveal all non-mine cells without triggering any mines.
5. **Losing the Game**: Uncovering a cell containing a mine will end the game.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the game.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by the classic Minesweeper game.
- Developed using Python and the `tkinter` library for GUI components.

