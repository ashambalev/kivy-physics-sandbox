# -*- coding: utf-8 -*-
import json
import os
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

__author__ = 'gipzo'

Builder.load_string('''
<CatalogItem>:
    size_hint: None, None
    height: '168sp'
    width: '300sp'

    canvas:
        StencilPush
        Rectangle:
            pos: root.pos
            size: root.size

        StencilUse

        Color:
            rgba: 1,1,1,1
        Rectangle:
            texture: root.icon_texture if root.icon_texture else None
            pos: root.pos[0], root.pos[1]
            size: root.size[0], root.size[0]*root.icon_texture.height/float(root.icon_texture.width) if root.icon_texture else root.size[1]

        StencilUnUse
        Rectangle:
            pos: root.pos
            size: root.size

        StencilPop
        Color:
            rgba: 0, 0, 0, 0.7 if root.state == 'normal' else 0.2
        Rectangle:
            pos: root.pos
            size: root.size[0], root.text_height

    Label:
        text: root.title
        pos: root.pos[0]+root.text_padding, root.pos[1]+root.text_padding
        size: root.size[0]-2*root.text_padding, root.text_height-root.text_padding
        text_size: self.size

''')


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
