from kivy.core.text import Label
from kivy.metrics import sp
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.uix.widget import Widget


class VectorWidget(Widget):
    label = ObjectProperty()
    title = StringProperty()
    length = NumericProperty(10.0)
    angle = NumericProperty()
    mode = StringProperty('object')
    color = ListProperty([1, 1, 1, 1])
    scale = NumericProperty(1.0)
    _scale = NumericProperty(8.5)

    arrow_size = NumericProperty(4.0)

    def __init__(self, **kwargs):
        self.label = Label(text='v', font_size=sp(14), padding=sp(3), valign='middle', halign='center')
        self.label.refresh()
        super(VectorWidget, self).__init__(**kwargs)

    def on_title(self, *largs):
        self.label.text = self.title
        self.label.refresh()

    def on_scale(self, *largs):
        self._scale = self.scale * 10.0
