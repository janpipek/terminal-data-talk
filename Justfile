run:
    uv run presentation.py # --disable-footer

help:
    uv run presentation.py --help

sync:
    uv sync

continue:
    uv run presentation.py --continue

format:
    uvx ruff format presentation.py slides/*.py

qr:
    qrencode -t utf8i https://github.com/janpipek/terminal-data-talk