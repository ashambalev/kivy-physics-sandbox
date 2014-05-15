# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'


class SliderControl(BaseControl):
    label = StringProperty('')
    description = StringProperty('')
    value = NumericProperty(50)
    min = NumericProperty(0)
    max = NumericProperty(100)
    dim = StringProperty(' m')
    format = StringProperty("{:.2f} ")
    slider = ObjectProperty()

    def __init__(self, **kwargs):
        super(SliderControl, self).__init__(**kwargs)
        self.register_event_type('on_value_changed')
        self.slider.value = self.value
        self.slider.min = self.min
        self.slider.max = self.max


    def on_value_changed(self, value):
        pass

    def update_value(self, *largs):
        self.value = self.slider.value
        self.dispatch('on_value_changed', self.value)

    pass
