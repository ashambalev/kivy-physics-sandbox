# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'


class CheckControl(BaseControl):
    label = StringProperty('')
    description = StringProperty('')
    value = BooleanProperty(False)
    checkbox = ObjectProperty()

    def __init__(self, **kwargs):
        super(CheckControl, self).__init__(**kwargs)
        self.register_event_type('on_value_changed')
        self.checkbox.active = self.value

    def on_value_changed(self, value):
        pass

    def update_value(self, *largs):
        self.value = self.checkbox.active
        self.dispatch('on_value_changed', self.value)

    pass
