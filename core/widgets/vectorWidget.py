from kivy.core.text import Label
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.uix.widget import Widget

Builder.load_string('''
#:import math math
<VectorWidget>:
    opacity: 1.0 if math.fabs(self.length)>0.01 else 0.01
    canvas:
        PushMatrix
        Translate:
            xy: self.pos[0], self.pos[1]
        Rotate:
            angle: -self.angle
            axis: 0, 0, 1
        Color:
            rgba: self.color
        Line:
            points: 0, 0,\
                    0, self.length * self._scale,\
                    -self.arrow_size, self.length * self._scale - self.arrow_size * math.copysign(1, self.length),\
                    self.arrow_size, self.length * self._scale - self.arrow_size * math.copysign(1, self.length),\
                    0, self.length * self._scale,\
                    0, 0
            width: 1.5
        Translate:
            xy: 0, self.length*self._scale/2.0
        Rotate:
            angle: self.angle
            axis: 0,0,1
        Color:
            rgba: 0,0,0,0.6
        Rectangle:
            pos: -5, -5
            size: root.label.size
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: -5, -5
            texture: root.label.texture if root.label else None
            size: root.label.size
        PopMatrix
''')


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