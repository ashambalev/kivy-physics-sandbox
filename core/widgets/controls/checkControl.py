# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'

Builder.load_string('''
<CheckControl>:
    size_hint: 1.0, None
    height: '60sp'
    checkbox: checkbox

    BoxLayout:
        pos:root.pos
        size:root.size
        orientation: 'horizontal'
        padding:'8sp'
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
        CheckBox:
            id: checkbox
            size_hint: None, 1.0
            width: self.height

            on_active: root.update_value()


''')

class CheckControl(BaseControl):
    label = StringProperty('Test')
    description = StringProperty('Description\n2 lines')
    value = BooleanProperty(False)
    checkbox = ObjectProperty()

    def __init__(self, **kwargs):
        super(CheckControl, self).__init__(**kwargs)
        self.register_event_type('on_value_changed')
        self.checkbox.active = self.value

    def on_value_changed(self, value):
        pass

    def update_value(self, *largs):
        self.value =self.checkbox.active
        self.dispatch('on_value_changed', self.value)
    pass
