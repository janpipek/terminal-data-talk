# Data wrangling in a modern terminal 

This is a live presentation in terminal which I gave at PyData Prague in 2025.
The presentation itself is a Python app that uses [Textual](https://textual.textualize.io/) to drive the display
of Markdown slides and run code snippets in a terminal window.

## Install & run

As a first step, clone the repository:

```
git clone https://github.com/janpipek/terminal-data-talk
```

### uv & just

If you have [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just) on your system, you don't have to install anything to run the presentation.
Just run:

```sh
just present
```

### Otherwise

Just do (ideally in a virtual environment)

```
pip install -e .
python presentation.py
```

## Links

### Tools

- [bat]()
- [xan]()
- [visidata]()

### Libraries

- 
- [textual]()