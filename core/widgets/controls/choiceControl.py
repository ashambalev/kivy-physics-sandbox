# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.widget import Widget
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'

Builder.load_string('''
<ChoiceControl>:
    size_hint: 1.0, None
    height: '50sp'
    spinner: spinner

    BoxLayout:
        pos:root.pos
        size:root.size
        orientation: 'horizontal'
        spacing:0
        padding:0
        BoxLayout:
            size_hint: 1.0, 1.0
            orientation: 'vertical'
            spacing:0
            padding:0
            Label:
                size_hint: 1.0, 0.4
                text: root.label
                font_size: '16sp'
                text_size: self.size
                valign: 'middle'
                padding: '-8sp','-2sp'
            Label:
                text: root.description
                size_hint: 1.0, 0.6
                font_size: '12sp'
                text_size: self.size
                valign: 'middle'
                padding: '-8sp', 0
        Spinner:
            id: spinner
            size_hint: None, 0.8
            width: '100sp'
            font_size: '18sp'
            values: root.choices
            text: root.value
            on_text: root.update_value()


''')


class ChoiceControl(BaseControl):
    label = StringProperty('Test')
    description = StringProperty('Description')
    choices = ListProperty(['test', 'test2', 'test3'])
    value = StringProperty('test')
    spinner = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChoiceControl, self).__init__(**kwargs)
        self.spinner.text = self.value

    def update_value(self, *largs):
        self.value = self.spinner.text

    pass
