#!/usr/bin/kivy
import kivy
from kivy.lang import Builder
from kivy.uix.slider import Slider
from core.mainLayout import MainLayout

kivy.require('1.4.2')
import os
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'height', '600')
from kivy.app import App

CATALOG_ROOT = os.path.dirname(__file__)
Builder.unbind_widget(Slider.uid)
Builder.load_string('''
<Slider>:
    canvas:
        Clear
        Color:
            rgb: 1, 1, 1
        BorderImage:
            border: (0, 18, 0, 18) if self.orientation == 'horizontal' else (18, 0, 18, 0)
            pos: (self.x + self.padding, self.center_y - sp(18)) if self.orientation == 'horizontal' else (self.center_x - 18, self.y + self.padding)
            size: (self.width - self.padding * 2, sp(36)) if self.orientation == 'horizontal' else (sp(36), self.height - self.padding * 2)
            source: 'data/slider_bg.png'
        Rectangle:
            pos: (self.value_pos[0] - sp(16), self.center_y - sp(14)) if self.orientation == 'horizontal' else (self.center_x - (16), self.value_pos[1] - sp(16))
            size: (sp(32), sp(32))
            source: 'data/slider_handle.png'

''')


class KivyPhysicsSandboxApp(App):
    use_kivy_settings = False
    title = 'Kivy Physics Sandbox'
    icon = 'data/icon.png'

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    KivyPhysicsSandboxApp().run()
