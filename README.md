# Data wrangling in a modern terminal

**Note: the presentation app is moved to a separate repo: [clippt](https://github.com/janpipek/clippt)**  

This is a live presentation in terminal which I gave at multiple occasions:
- PyData Prague in 2025 - see [tag:pydata-28](https://github.com/janpipek/terminal-data-talk/releases/tag/pydata-28)
- Pyvo Plzeň in 2026 - see [tag:pyvo-plzen](https://github.com/janpipek/terminal-data-talk/releases/tag/pyvo-plzen)
- EuroPython Kraków in 2026 - see [tag:europython-2026](https://github.com/janpipek/terminal-data-talk/releases/tag/europython-2026)

The presentation itself is based on **[clippt](https://github.com/janpipek/clippt)**, a tool that allows you
to combine Markdown slides withe executable snippets, running fully in the terminal.

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
presentation
```

## Links

### Tools

- [bat](https://github.com/sharkdp/bat)
- [xan](https://github.com/medialab/xan)
- [visidata](https://www.visidata.org/)

### Libraries

- [plotille](https://github.com/tammoippen/plotille)
- [plotext](https://github.com/piccolomo/plotext)
- [matplotlib-backend-kitty](https://github.com/jktr/matplotlib-backend-kitty)
- [rich](https://github.com/Textualize/rich)
- [textual](https://textual.textualize.io/)
- [textual-plotext](https://github.com/Textualize/textual-plotext)
- [textual-plot](https://github.com/davidfokkema/textual-plot)
- [textual-fastdatatable](https://github.com/tconbeer/textual-fastdatatable)

### Other recommendations

- [click](https://click.palletsprojects.com/) - argument parsing
- [typer](https://typer.tiangolo.com/) - argument parsing based on type annotations
- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) - input handling
