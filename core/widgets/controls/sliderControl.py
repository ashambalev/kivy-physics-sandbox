# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from core.widgets.controls.baseControl import BaseControl

__author__ = 'gipzo'

Builder.load_string('''
<SliderControl>:
    slider: slider
    size_hint: 1.0, None
    height: '80sp'

    BoxLayout:
        orientation: 'vertical'
        pos:root.pos
        size:root.size
        padding:'8sp'
        BoxLayout:
            size_hint: 1.0, None
            height: '55sp'
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
                    valign: 'bottom'
                    padding: '-8sp','-2sp'
                Label:
                    text: root.description
                    size_hint: 1.0, 0.6
                    font_size: '12sp'
                    text_size: self.size
                    valign: 'middle'
                    padding: '-8sp', 0
            Label:
                size_hint: None, 0.8
                width: '100sp'
                font_name: 'data/DejaVuSansCondensed.ttf'
                valign: 'top'
                font_size: '16sp'
                text:  root.format.format(root.value)+root.dim
        Slider:
            id: slider
            size_hint: 1.0, None
            height: '20sp'
            padding:'20sp'
            on_value: root.update_value()



''')


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
