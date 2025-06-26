from textual.theme import Theme

my_theme = Theme(
    name="my",
    primary="#0000c0",
    secondary="#4040ff",
    accent="#00ff00",
    foreground="#444444",
    background="#ffffff",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#ffffff",
    panel="#ffffff",
    dark=False,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

css_tweaks = """
    Screen {
        align: center middle;
    }
    MarkdownFence {
        max-height: 100;
        background: #ffffff;
    }
 """