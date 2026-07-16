record:
    asciinema rec --command "just present" --overwrite --title "Data wrangling in a modern terminal" recording.cast

continue:
    uv run presentation --continue  --disable-footer --disable-header

present:
    uv run presentation --disable-footer --disable-header

help:
    uv run presentation --help

sync:
    uv sync

ruff:
    uvx ruff check --fix terminal_data_talk/dynamic_slides/*.py terminal_data_talk/*.py
    uvx ruff format terminal_data_talk/dynamic_slides/*.py terminal_data_talk/*.py

qr:
    qrencode -t utf8i https://github.com/janpipek/terminal-data-talk
