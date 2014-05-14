# -*- coding: utf-8 -*-
import os
from kivy.lang import Builder
from kivy.metrics import Metrics
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.widget import Widget

Builder.load_string('''
<ExperimentWindow>:
    size_hint: 1, 1
''')


class ExperimentWindow(Widget):
    time = NumericProperty()
    experiment_path = StringProperty()
    live = BooleanProperty(False)
    can_change_speed = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(ExperimentWindow, self).__init__(**kwargs)

        self.scale = Metrics.density

    def reset(self, *largs):
        pass

    def get_file(self, file):
        return os.path.join(self.experiment_path, file)

    def build_controls(self, controls):
        for name in dir(self):
            if hasattr(getattr(self, name), '__class__'):
                if getattr(self, name).__class__.__name__ in ["SliderControl", "CheckControl"]:
                    controls.add_widget(getattr(self, name))

                    getattr(self, name).bind(on_value_changed=self.update)

