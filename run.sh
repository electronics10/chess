#!/usr/bin/env bash
# Launch the chess game on macOS / Linux.
# Uses uv if available, otherwise falls back to a system Python.

# Move into the folder this script lives in, so it works no matter where it's run from.
cd "$(dirname "$0")" || exit 1

if command -v uv >/dev/null 2>&1; then
    exec uv run main.py
elif command -v python3 >/dev/null 2>&1; then
    exec python3 main.py
elif command -v python >/dev/null 2>&1; then
    exec python main.py
else
    echo "Python was not found. Please install Python 3.12+ from https://www.python.org/downloads/"
    exit 1
fi
