# -*- coding: utf-8 -*-
import math
from kivy.metrics import sp
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.label import Label
from core.widgets.controls.checkControl import CheckControl

from core.widgets.controls.sliderControl import SliderControl
from core.widgets.experimentWindow import ExperimentWindow
from core.widgets.physicsObject import PhysicsObject
from core.widgets.texturedWidget import TexturedWidget

RIVERSIDE_SIZE = sp(40)
BOAT_WIDTH = sp(30)
BOAT_HEIGHT = sp(60)


class Boat(PhysicsObject):
    boat_speed = 0.0
    river_speed = 0.0
    total_speed = 0.0

    def update(self, dt):
        super(Boat, self).update(dt)
        self.update_vector('boat_speed', self.boat_speed, self.angle)
        self.update_vector('river_speed', self.river_speed, 90.0)

        total_speed_x = self.boat_speed * math.sin(self.angle * math.pi / 180.0) + self.river_speed
        total_speed_y = self.boat_speed * math.cos(self.angle * math.pi / 180.0)
        total_speed_angle = math.atan2(total_speed_x, total_speed_y) * 180.0 / math.pi
        total_speed_length = math.sqrt(total_speed_x * total_speed_x + total_speed_y * total_speed_y)
        self.total_speed = total_speed_length
        self.update_vector('speed', total_speed_length, total_speed_angle)

        self.x += total_speed_x * dt * self.scale
        self.y += total_speed_y * dt * self.scale


class SpeedRelativityExperimentWindow(ExperimentWindow):
    boat_speed = SliderControl(label="Boat speed",
                               description="Speed value of the boat",
                               min=1, max=20, value=5.0, dim=' m/s')
    river_speed = SliderControl(label="River speed",
                                description="Speed of the river flow",
                                min=-15, max=15, value=5.0, dim=' m/s')
    boat_angle = SliderControl(label="Angle of the boat",
                               description="Control your boat",
                               min=-180.0, max=180.0, value=0.0, dim=u' \u00b0')
    show_trajectory = CheckControl(label="Show boat trajectory",
                                   description="",
                                   value=True, )

    boat = ObjectProperty()
    riversize_size = NumericProperty(RIVERSIDE_SIZE)
    scale = NumericProperty(1.0)
    can_change_speed = True

    def load(self, *largs):
        self.boat = Boat(scale=self.scale,
                         source=self.get_file('data/boat.png'),
                         size=(BOAT_WIDTH, BOAT_HEIGHT),
                         show_trajectory=True,
                         pos=(100, 100))
        self.boat.init()
        self.boat.add_vector('boat_speed', 'Vb', self.boat_speed.value, self.boat_angle.value, (1, 0.4, 1, 1))
        self.boat.add_vector('river_speed', 'Vr', self.river_speed.value, 90.0, (0.4, 1, 1, 1))
        self.boat.add_vector('speed', 'V', self.boat_speed.value, self.boat_angle.value)
        self.boat.show_trajectory = self.show_trajectory.value

        self.river = TexturedWidget(source=self.get_file('data/river.png'))
        self.riverside_bottom = TexturedWidget(source=self.get_file('data/riverside.png'))
        self.riverside_top = TexturedWidget(source=self.get_file('data/riverside.png'))
        self.speed_label = Label(text='0.0 m/s', font_size=sp(16),
                                 bold=True, halign='center', valign='middle')

        self.add_widget(self.river)
        self.add_widget(self.riverside_bottom)
        self.add_widget(self.riverside_top)

        self.add_widget(self.boat)

        self.add_widget(self.speed_label)
        self.bind(on_drag=self.update_angle)

    def update_angle(self, widget, touch):
        touch_x, touch_y = touch.x, touch.y
        angle = math.atan2(touch_y - self.boat.y, touch_x - self.boat.x)
        angle = 90 - angle * 180 / math.pi
        if angle > 180:
            angle -= 360
        self.boat_angle.value = angle
        self.update()

    def reset(self, *largs):
        self.boat_speed.value = 5.0
        self.river_speed.value = 5.0
        self.boat_angle.value = 0.0
        self.boat.x, self.boat.y = sp(100), sp(RIVERSIDE_SIZE + BOAT_HEIGHT / 2)
        self.boat.init()
        self.update()

    def update(self, *largs):
        try:
            dt = float(largs[0])
        except:
            dt = 0.0

        self.boat.boat_speed = self.boat_speed.value
        self.boat.angle = self.boat_angle.value
        self.boat.river_speed = self.river_speed.value

        self.boat.show_trajectory = self.show_trajectory.value
        self.boat.update(dt)
        self.boat.after_update(dt)

        self.speed_label.text = "Boat combined speed: {:.2f} m/s".format(self.boat.total_speed)

        self.river.offset_x -= dt * self.river_speed.value / 100.0
        if self.river.offset_x > 1.0:
            self.river.offset_x = 0
        if self.river.offset_x < 0:
            self.river.offset_x = 1.0

    def on_size(self, *largs):
        self.boat.constraints = [0, self.width, RIVERSIDE_SIZE, self.height - RIVERSIDE_SIZE]
        self.river.pos = (self.pos[0], self.pos[1] + RIVERSIDE_SIZE)
        self.river.size = (self.size[0], self.size[1] - RIVERSIDE_SIZE * 2.0)
        self.riverside_top.pos = (self.pos[0], self.pos[1] + self.height - RIVERSIDE_SIZE)
        self.riverside_top.size = (self.size[0], RIVERSIDE_SIZE)
        self.riverside_bottom.pos = self.pos
        self.riverside_bottom.size = (self.size[0], RIVERSIDE_SIZE)
        self.speed_label.pos = self.pos
        self.speed_label.size = (self.width, RIVERSIDE_SIZE)
        self.speed_label.text_size = self.size

        self.update()


def load_experiment():
    main_widget = SpeedRelativityExperimentWindow()
    return main_widget
