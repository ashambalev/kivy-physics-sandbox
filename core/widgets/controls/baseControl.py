# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget

__author__ = 'gipzo'

Builder.load_string('''
<BaseControl>:
    canvas:
        Color:
            rgba: 0,0,0,0.2
        Rectangle:
            pos: root.pos
            size: root.size[0], root.size[1]+sp(10)


''')


class BaseControl(Widget):
    def __init__(self, **kwargs):
        super(BaseControl, self).__init__(**kwargs)

