# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

Builder.load_string('''
<ExperimentWindow>:
    size_hint: 1, 1
''')


class ExperimentWindow(Widget):
    time = NumericProperty()

    def __init__(self, **kwargs):
        super(ExperimentWindow, self).__init__(**kwargs)

    def build_controls(self, controls):
        for name in dir(self):
            if hasattr(getattr(self, name), '__class__'):
                if getattr(self, name).__class__.__name__ in ["SliderControl", "CheckControl"]:
                    controls.add_widget(getattr(self, name))

