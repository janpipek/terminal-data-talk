continue:
    uv run presentation --continue  --disable-footer

present:
    uv run presentation --disable-footer

help:
    uv run presentation --help

sync:
    uv sync

ruff:
    uvx ruff check --fix terminal_data_talk/dynamic_slides/*.py terminal_data_talk/*.py
    uvx ruff format terminal_data_talk/dynamic_slides/*.py terminal_data_talk/*.py

qr:
    qrencode -t utf8i https://github.com/janpipek/terminal-data-talk

download-un:
    curl -o data/countries.csv https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/un_basic.csv

download-cities:
    curl -o data/cities.parquet https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/worldcities.parquet

download-weather:
    curl -o data/weather.parquet https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/prague-meteostat.parquet
