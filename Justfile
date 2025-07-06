continue:
    uv run presentation.py --continue

present:
    uv run presentation.py # --disable-footer

help:
    uv run presentation.py --help

sync:
    uv sync

ruff:
    uvx ruff check --fix presentation.py dynamic_slides/*.py clippt/*.py
    uvx ruff format presentation.py slides/*.py dynamic_slides/*.py clippt/*.py

qr:
    qrencode -t utf8i https://github.com/janpipek/terminal-data-talk

download-un:
    curl -o data/countries.csv https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/un_basic.csv

download-cities:
    curl -o data/cities.parquet https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/worldcities.parquet

download-weather:
    curl -o data/weather.parquet https://raw.githubusercontent.com/janpipek/eda-polars-way/refs/heads/main/data/prague-meteostat.parquet
