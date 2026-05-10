from clippt.slides import FuncSlide
from textual.app import App
from textualeffects.effects import EffectType
from textualeffects.widgets import EffectLabel


text = ("Hello World! " * 5 + "\n") * 10
effect: EffectType = "Spotlights"
config = {
    "search_duration": 500,
    "spotlight_count": 3,
}


def spotlights_f(app: App):
    label = EffectLabel(text, effect=effect, config=config)
    return label


spotlights = FuncSlide(f=spotlights_f)
