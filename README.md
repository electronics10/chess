# Chess

A two-player chess game with a clickable graphical board, written in pure Python
with `tkinter`. No external libraries required — just Python itself.

This was my first-ever Python project, so the code is kept as-is; this README and
the launcher scripts just make it easier for anyone to start a game.

## Quick start

### macOS / Linux

Double-click `run.sh`, or from a terminal in this folder:

```bash
./run.sh
```

(If it won't run, first do `chmod +x run.sh`.)

### Windows

Double-click `run.bat`, or from a terminal in this folder:

```bat
run.bat
```

The launcher uses [uv](https://docs.astral.sh/uv/) if it's installed, and
otherwise falls back to a regular `python` install.

## Running it manually

If you'd rather start it yourself:

```bash
python main.py
```

Requires **Python 3.12+**. If you use `uv`, run `uv run main.py` instead.

## Requirements

- **Python 3.12 or newer.**
- **tkinter** — Python's built-in GUI toolkit.
  - It ships with the official installers from [python.org](https://www.python.org/downloads/) and on Windows.
  - On macOS with Homebrew Python: `brew install python-tk`
  - On Debian/Ubuntu: `sudo apt install python3-tk`

To check that tkinter is available:

```bash
python -c "import tkinter; print('tkinter is ready')"
```

## How to play

The board opens with White at the bottom. Two people share the keyboard/mouse and
take turns — White moves first.

To make a move:

1. **Click the piece** you want to move. (Its legal squares can be highlighted —
   see *Show Moves* below.)
2. **Click the destination square.**

That's one move. The turn then passes to the other player automatically.

When a pawn reaches the far rank, the game asks you to promote it: type
`Queen`, `Rook`, `Knight`, or `Bishop` into the text box on the right and press
**submit**. Castling and en passant are supported — just move the king two
squares toward the rook to castle.

The text panel on the right logs each click and move, plus check, checkmate,
stalemate, and draw messages.

## Button guide

| Button | What it does |
|--------|--------------|
| **retract** | Undo the last move. |
| **Quit** | Close the game. |
| **New** | Start a fresh game. |
| **SAM** | *Show Available Moves* — toggle highlighting of a selected piece's legal squares. |
| **T90°** | Rotate the board 90° (press repeatedly to cycle through all four orientations). |
| **submit** | Confirm a pawn-promotion choice typed in the text box. |

Enjoy the game!
