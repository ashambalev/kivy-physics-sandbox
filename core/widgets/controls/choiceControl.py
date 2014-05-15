# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'


class ChoiceControl(BaseControl):
    label = StringProperty('')
    description = StringProperty('')
    choices = ListProperty(['test', 'test2', 'test3'])
    value = StringProperty('test')
    spinner = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChoiceControl, self).__init__(**kwargs)
        self.spinner.text = self.value

    def update_value(self, *largs):
        self.value = self.spinner.text

    pass
