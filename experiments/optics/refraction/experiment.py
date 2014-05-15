# -*- coding: utf-8 -*-
import math

from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.utils import boundary

from core.widgets.controls.sliderControl import SliderControl
from core.widgets.experimentWindow import ExperimentWindow
from core.widgets.lineWidget import LineWidget
from core.widgets.physicsObject import PhysicsObject
from core.widgets.texturedWidget import TexturedWidget


GLASS_WIDTH = 128

class RefractionExperimentWindow(ExperimentWindow):
    in_angle = SliderControl(label="Input angle",
                             description="Angle of the input ray",
                             min=-85.0, max=85.0, value=0.0, dim=u' \u00b0')
    refractive_index = SliderControl(label="Refractive index",
                                     description="of the glass",
                                     min=1, max=5, value=1.52, dim='')
    reflectivity = SliderControl(label="Reflectivity",
                                 description="of the glass",
                                 min=0, max=1, value=0.0, dim='')

    boat = ObjectProperty()
    scale = NumericProperty(1.0)
    can_change_speed = True

    def load(self, *largs):
        self.torch = PhysicsObject(source=self.get_file('data/torch.png'), draggable=True)
        self.torch.bind(on_drag=self.set_ray_angle)
        self.glass = TexturedWidget(source=self.get_file('data/glass.png'), scale=GLASS_WIDTH / 256.0)
        self.line_in = LineWidget(width=3.0)
        self.line_glass = LineWidget(width=3.0)
        self.line_out = LineWidget(width=3.0)
        self.line_reflection = LineWidget(width=3.0, color=[1, 1, 1, 0.0])

        self.add_widget(self.line_in)
        self.add_widget(self.line_glass)
        self.add_widget(self.line_out)
        self.add_widget(self.line_reflection)
        self.add_widget(self.glass)
        self.add_widget(self.torch)


    def reset(self, *largs):
        self.update()


    def update(self, *largs):
        try:
            dt = float(largs[0])
        except:
            dt = 0.0

        cx = (self.size[1] / 2.2) * math.sin((90 - self.in_angle.value) * math.pi / 180.0)
        cy = (self.size[1] / 2.2) * math.cos((90 - self.in_angle.value) * math.pi / 180.0)
        self.line_in.start = (self.line_in.end[0] - cx, self.line_in.end[1] - cy)

        self.torch.pos = self.line_in.start
        self.torch.angle = -self.in_angle.value
        self.line_reflection.end = (self.line_in.end[0] - cx * 10.0, self.line_in.end[1] + cy * 10.0)
        self.line_reflection.color = [1, 1, 0.7, self.reflectivity.value]
        self.line_out.color = [0.7, 1, 0.7, 1.0 - self.reflectivity.value]
        self.line_glass.color = [0.7, 1, 0.7, 1.0 - self.reflectivity.value]

        sina = math.sin(self.in_angle.value * math.pi / 180.0)
        siny = sina / self.refractive_index.value
        cosy = math.sqrt(1 - siny * siny)
        l = math.sqrt(GLASS_WIDTH * GLASS_WIDTH + math.pow(GLASS_WIDTH / math.tan(math.atan2(cosy, siny)), 2))
        self.line_glass.end = (self.line_glass.start[0] + l * cosy, self.line_glass.start[1] + l * siny)

        cosy = math.sqrt(1 - sina * sina)
        l = self.size[0]
        self.line_out.start = self.line_glass.end
        self.line_out.end = (self.line_out.start[0] + l * cosy, self.line_out.start[1] + l * sina)

    def set_ray_angle(self, widget, touch):
        touch_x, touch_y = touch.x, touch.y
        angle = math.atan2(touch_y - self.line_in.end_y, touch_x - self.line_in.end_x)
        angle = angle * 180 / math.pi + 180
        if (angle > 180):
            angle -= 360
        angle = boundary(angle, -85.0, 85.0)
        self.in_angle.value = angle
        self.update()


    def on_size(self, *largs):
        self.glass.pos = (self.pos[0] + self.size[0] / 2.0, self.pos[1])
        self.glass.size = (128, self.size[1])

        self.line_in.end = (self.pos[0] + self.size[0] / 2.0, self.pos[0] + self.size[1] / 2.0)
        self.line_glass.start = self.line_in.end
        self.line_out.start = self.line_glass.end
        self.line_out.end = (self.pos[0] + self.size[0], self.pos[0])
        self.line_reflection.start = self.line_in.end

        self.update()


def load_experiment():
    main_widget = RefractionExperimentWindow()
    return main_widget



