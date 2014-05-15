from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.uix.widget import Widget


class TexturedWidget(Widget):
    source = StringProperty()
    offset_x = NumericProperty(0.0)
    offset_y = NumericProperty(0.0)
    w = NumericProperty(1.0)
    h = NumericProperty(1.0)
    scale = NumericProperty(1.0)
    color = ListProperty([1, 1, 1, 1])
    texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TexturedWidget, self).__init__(**kwargs)

    def _calc_tex_coords(self):
        self.w = float(self.width) / self.texture.width / self.scale if self.texture else 1.0
        self.h = -float(self.height) / self.texture.height / self.scale if self.texture else 1.0

    def on_source(self, *largs):
        self.texture = Image.load(self.source).texture
        self.texture.wrap = 'repeat'
        self._calc_tex_coords()

    def on_size(self, *largs):
        self._calc_tex_coords()

    pass