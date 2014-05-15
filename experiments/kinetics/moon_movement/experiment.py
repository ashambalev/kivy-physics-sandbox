# -*- coding: utf-8 -*-
import math

from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.uix.label import Label

from core.widgets.controls.checkControl import CheckControl
from core.widgets.controls.sliderControl import SliderControl
from core.widgets.experimentWindow import ExperimentWindow
from core.widgets.physicsObject import PhysicsObject
from core.widgets.texturedWidget import TexturedWidget


class Moon(PhysicsObject):
    mass = 1.0
    earth_mass = 1.0
    total_speed = 1.0
    total_speed_x = 1.0
    total_speed_y = 0.0
    earth_pos = (0, 0)

    def update(self, dt):
        super(Moon, self).update(dt)

        earth_vector = (self.x - self.earth_pos[0], self.y - self.earth_pos[1])
        r2 = math.pow(earth_vector[0], 2) + math.pow(earth_vector[1], 2)
        G = 6.67545 * 5000
        r = math.sqrt(r2)
        earth_vector = (earth_vector[0] / r, earth_vector[1] / r)
        Vg = -G * self.earth_mass / r2
        Vg_x = earth_vector[0] * Vg
        Vg_y = earth_vector[1] * Vg
        self.total_speed_x += Vg_x*dt
        self.total_speed_y += Vg_y*dt
        self.total_speed = math.sqrt(self.total_speed_x * self.total_speed_x + self.total_speed_y * self.total_speed_y)

        self.update_vector('moon_speed', self.total_speed/4.0,
                           90 - math.atan2(self.total_speed_y, self.total_speed_x) * 180.0 / math.pi)
        self.update_vector('gravity', self.mass * self.earth_mass / 10.0 + 2.0,
                           90 - math.atan2(Vg_y, Vg_x) * 180.0 / math.pi)
        self.x += self.total_speed_x * dt
        self.y += self.total_speed_y * dt


class MoonMovementExperimentWindow(ExperimentWindow):
    moon_distance = SliderControl(label="Moon orbit",
                                  description="Distance from Earth",
                                  min=100, max=500, value=384.0, dim=',000 km', format='{:.0f}')
    start_speed = SliderControl(label="Start speed",
                                description="Speed of the moon",
                                min=1000, max=10000, value=3623, dim=' km/h')
    earth_mass = SliderControl(label="Earth mass",
                               description="",
                               min=0.1, max=9.9, value=5.972, dim=u'x 10\u00B2\u2074 kg')
    moon_mass = SliderControl(label="Moon mass",
                              description="",
                              min=0.1, max=9.9, value=7.3477, dim=u'x 10\u00B2\u00B2 kg')
    show_trajectory = CheckControl(label="Show moon trajectory",
                                   description="",
                                   value=True, )

    scale = NumericProperty(1.0)

    def load(self, *largs):

        self.stars = TexturedWidget(source=self.get_file('data/stars.png'),
                                    color=[1, 1, 1, 1])
        self.earth = PhysicsObject(source=self.get_file('data/earth.png'),
                                   size=(128, 128))
        self.moon = Moon(source=self.get_file('data/moon.png'),
                         size=(64, 64), scale=0.5,
                         show_trajectory=True)

        self.moon.add_vector('moon_speed', 'V', self.start_speed.value / 200 + 2, 90, (1, 1, 1, 1))
        self.moon.add_vector('gravity', 'g', self.moon_mass.value, 180, (1, 1, 1, 1))

        self.info_label = Label(text='Moon speed: 0.0 m/s', font_size=sp(16), bold=True, halign='center',
                                valign='middle')

        self.add_widget(self.stars)
        self.add_widget(self.earth)
        self.add_widget(self.moon)
        self.add_widget(self.info_label)


    def reset(self, *largs):
        self.moon.clear_trajectory()

        self.update()


    def update(self, *largs):
        try:
            dt = float(largs[0])
        except:
            dt = 0.0
        self.moon.mass = self.moon_mass.value
        self.moon.earth_mass = self.earth_mass.value

        if not self.live:
            self.moon.pos = (self.size[0] / 2, self.size[1] / 2 + self.moon_distance.value / 5 + 64)
            self.moon.total_speed_x = self.start_speed.value / 100 + 2.0
            self.moon.total_speed_y = 0
            self.moon.earth_pos = self.earth.pos
        self.info_label.text = "Moon speed: {:.0f},000 km/h".format(100.0 * (self.moon.total_speed - 2))
        self.moon.update(dt)

    def on_size(self, *largs):
        self.stars.size = self.size
        self.info_label.pos = self.pos
        self.info_label.size = (self.width, 100)
        self.info_label.text_size = self.size
        if not self.live:
            self.earth.pos = (self.size[0] / 2, self.size[1] / 2)
            self.moon.pos = (self.size[0] / 2, self.size[1] / 2 + self.moon_distance.value / 2 + 64)
            self.moon.clear_trajectory()
        self.update()


def load_experiment():
    main_widget = MoonMovementExperimentWindow()
    return main_widget



