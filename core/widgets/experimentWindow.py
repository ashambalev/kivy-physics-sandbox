# -*- coding: utf-8 -*-
import os
from kivy.metrics import Metrics
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.widget import Widget


class ExperimentWindow(Widget):
    time = NumericProperty()
    experiment_path = StringProperty()
    live = BooleanProperty(False)
    can_change_speed = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_drag')
        super(ExperimentWindow, self).__init__(**kwargs)
        self.scale = Metrics.density

    def load(self, *largs):
        pass

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


    def on_drag(self, touch):
        pass

    def collide_point(self, x, y):
        return self.x < x < self.x + self.size[0] and self.y < y < self.y + self.size[1]

    def on_touch_down(self, touch):
        if super(ExperimentWindow, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.dispatch('on_drag', touch)
            return True
        if super(ExperimentWindow, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(ExperimentWindow, self).on_touch_up(touch)
        touch.ungrab(self)
        return True
