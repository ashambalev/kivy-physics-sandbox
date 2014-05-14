from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget

Builder.load_string('''

<LineWidget>:
    canvas:
        Color:
            rgba: self.color
        Line:
            points: self.start_x, self.start_y, self.end_x, self.end_y
            width: self.width

''')

class LineWidget(Widget):
    start_x = NumericProperty(0.0)
    start_y = NumericProperty(0.0)
    start = ReferenceListProperty(start_x, start_y)
    end_x = NumericProperty(100.0)
    end_y = NumericProperty(100.0)
    end = ReferenceListProperty(end_x, end_y)
    width = NumericProperty(1.0)
    color = ListProperty([1, 1, 1, 1])
    pass