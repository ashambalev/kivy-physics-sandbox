# -*- coding: utf-8 -*-
import json
import os
from kivy.core.image import Image
from kivy.metrics import sp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

__author__ = 'gipzo'


class CatalogItem(ButtonBehavior, Widget):
    name = StringProperty()
    title = StringProperty()
    icon = StringProperty()
    text_padding = NumericProperty(sp(8))
    text_height = NumericProperty(sp(32))
    icon_texture = ObjectProperty()

    def load(self, path, file):
        category_info = json.load(open(os.path.join(path, file), 'r'))
        self.name = os.path.split(path)[1]
        self.title = category_info['title']
        self.icon = category_info['icon']
        self.icon_texture = Image(os.path.join(path, self.icon)).texture
