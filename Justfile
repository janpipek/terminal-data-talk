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

download-un:
    curl -o data/un_basic.csv https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/un_basic.csv