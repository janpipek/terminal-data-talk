# Data wrangling in a modern terminal

This is a live presentation in terminal which I gave at PyData Prague in 2025.
The presentation itself is a Python app that uses [Textual](https://textual.textualize.io/) to drive the display
of Markdown slides and run code snippets in a terminal window.

## Install & run

As a first step, clone the repository:

```shell
git clone https://github.com/janpipek/terminal-data-talk
```

### uv & just

If you have [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just) on your system, you don't have to install anything to run the presentation.
Just run:

```shell
just present
```

### Otherwise

Just do (ideally in a virtual environment)

```shell
pip install -e .
python presentation.py
```

## Links

### Tools

- [bat](https://github.com/sharkdp/bat)
- [xan](https://github.com/medialab/xan)
- [visidata](https://www.visidata.org/)

### Libraries

- [plotille](https://github.com/tammoippen/plotille)
- [plotext](https://github.com/piccolomo/plotext)
- [rich](https://github.com/Textualize/rich)
- [textual](https://textual.textualize.io/)
- [textual-plotext](https://github.com/Textualize/textual-plotext)
- [textual-plot](https://github.com/davidfokkema/textual-plot)
- [textual-fastdatatable](https://github.com/tconbeer/textual-fastdatatable)

### Other recommendations

- [click]() - argument parsing
- [typer]() - argument parsing based on type annotations
- [prompt_toolkit]() - input handling
