from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget


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
