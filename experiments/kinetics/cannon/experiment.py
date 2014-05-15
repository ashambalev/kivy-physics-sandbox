# -*- coding: utf-8 -*-
import math
from kivy.metrics import sp, Metrics
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.utils import boundary

from core.widgets.controls.sliderControl import SliderControl
from core.widgets.experimentWindow import ExperimentWindow
from core.widgets.physicsObject import PhysicsObject
from core.widgets.texturedWidget import TexturedWidget


GROUND_SIZE = sp(128)
CANNONBALL_SIZE = sp(20)
BALL_INIT_POS = (sp(100), GROUND_SIZE + sp(16))


class CannonBall(PhysicsObject):
    ball_speed = 0.0
    cannon_angle = 0.0
    wind_speed = 0.0
    gravity = 0.0
    mass = 0.0
    time_in_air = 0.0
    max_height = 0.0
    max_length = 0.0
    init_pos_x = 0.0
    init_pos_y = 0.0

    def __init__(self, **kwargs):
        self.show_trajectory = True
        super(CannonBall, self).__init__(**kwargs)

    def update(self, dt):
        super(CannonBall, self).update(dt)
        self.update_vector('ball_speed', self.ball_speed / 20.0, self.cannon_angle)
        self.update_vector('wind_speed', self.wind_speed)
        self.update_vector('gravity', self.gravity * self.mass)
        total_speed_x = self.ball_speed * math.sin(self.cannon_angle * math.pi / 180.0)
        total_speed_x += self.wind_speed
        total_speed_y = self.ball_speed * math.cos(self.cannon_angle * math.pi / 180.0)
        total_speed_y -= self.gravity * self.mass

        total_speed_angle = math.atan2(total_speed_x, total_speed_y) * 180.0 / math.pi
        total_speed_length = math.sqrt(total_speed_x * total_speed_x + total_speed_y * total_speed_y)
        new_y = self.y + total_speed_y * dt * self.scale

        if self.y > GROUND_SIZE:
            self.time_in_air += dt
            self.ball_speed = total_speed_length
            self.cannon_angle = total_speed_angle
            self.y = new_y
            self.x += total_speed_x * dt * self.scale
            self.max_height = max(self.max_height, math.fabs(self.y - self.init_pos_y))
            self.max_length = max(self.max_length, math.fabs(self.x - self.init_pos_x))


class CannonExperimentWindow(ExperimentWindow):
    ball_speed = SliderControl(label="Initial speed",
                               description="of the cannonball",
                               min=250, max=500, value=320.0, dim=' m/s')
    cannon_angle = SliderControl(label="Angle of the cannon",
                                 description="",
                                 min=-90.0, max=90.0, value=45.0, dim=u' \u00b0')
    wind_speed = SliderControl(label="Wind speed",
                               description="Speed value of the wind",
                               min=-20, max=20, value=0.0, dim=' m/s')
    gravity = SliderControl(label="Gravity",
                            description="",
                            min=1, max=20, value=9.8, dim=' m/s2')

    mass = SliderControl(label="Ball mass",
                         description="",
                         min=0.1, max=5, value=1.0, dim=' kg')

    ball = None
    info_label = None
    ground = None
    cannon_base = None
    cannon = None
    can_change_speed = False

    def load(self, *largs):
        self.ball = CannonBall(scale=self.scale,
                               source=self.get_file('data/cannon_ball.png'),
                               color=[1, 1, 1, 1],
                               size=(CANNONBALL_SIZE, CANNONBALL_SIZE),
                               show_trajectory=True,
                               constraint_x=False,
                               pos=BALL_INIT_POS)

        self.ball.add_vector('ball_speed', 'Vb',
                             self.ball_speed.value,
                             self.cannon_angle.value,
                             (1, 0.4, 1, 1))

        self.ball.add_vector('wind_speed', 'Vw',
                             self.wind_speed.value,
                             90.0,
                             (0.4, 1, 1, 1))

        self.ball.add_vector('gravity', 'g',
                             self.gravity.value,
                             180)

        self.info_label = Label(text='Length: 0.0 m  Height: 0.0 m  Time in air: 0.0 s',
                                font_size=sp(16),
                                bold=True,
                                halign='center',
                                valign='middle')

        self.ground = TexturedWidget(source=self.get_file('data/ground.png'), scale=0.25 * Metrics.density)

        self.cannon_base = Image(source=self.get_file('data/cannon_base.png'),
                                 size=(64 * Metrics.density, 64 * Metrics.density))
        self.cannon = PhysicsObject(source=self.get_file('data/cannon.png'),
                                    size=(64 * Metrics.density, 64 * Metrics.density))

        self.add_widget(self.ground)
        self.add_widget(self.info_label)
        self.add_widget(self.cannon_base)
        self.add_widget(self.ball)
        self.add_widget(self.cannon)
        self.bind(on_drag=self.update_angle)

    def update_angle(self, widget, touch):
        touch_x, touch_y = touch.x, touch.y
        angle = math.atan2(touch_y - self.cannon.y, touch_x - self.cannon.y)
        angle = 90 - angle * 180 / math.pi
        angle = boundary(angle, -85.0, 85.0)
        self.cannon_angle.value = angle
        self.update()

    def reset(self, *largs):
        super(CannonExperimentWindow, self).reset(*largs)
        self.ball.x, self.ball.y = sp(100), GROUND_SIZE + sp(16)
        self.ball.init_pos_x, self.ball.init_pos_y = self.ball.x, self.ball.y
        self.ball.init()
        self.ball.time_in_air = 0.0
        self.ball.max_height = 0.0
        self.ball.max_length = 0.0
        self.update_ball_params()
        self.update()

    def update_ball_params(self):
        self.ball.constraints = [0, self.width, GROUND_SIZE - sp(10), self.height]
        if not self.live:
            self.ball.ball_speed = self.ball_speed.value
            self.ball.cannon_angle = self.cannon_angle.value
            self.cannon.angle = self.cannon_angle.value
        self.ball.wind_speed = self.wind_speed.value
        self.ball.gravity = self.gravity.value
        self.ball.mass = self.mass.value

    def update(self, *largs):
        try:
            dt = float(largs[0])
        except:
            dt = 0.0
        self.update_ball_params()
        self.ball.update(dt)
        self.ball.after_update(dt)

        self.info_label.text = \
            "Length: {:.2f} m \
            Height: {:.2f} m \
            Time in air: {:.2f} s".format(self.ball.max_length,
                                          self.ball.max_height,
                                          self.ball.time_in_air)

    def on_size(self, *largs):
        self.ball.constraints = [0, self.width, GROUND_SIZE - sp(10), self.height]
        self.ground.pos = self.pos
        self.ground.size = (self.size[0], GROUND_SIZE)
        self.info_label.pos = self.pos
        self.info_label.size = (self.size[0], GROUND_SIZE)
        self.cannon_base.pos = (
            BALL_INIT_POS[0] - self.cannon_base.width / 2, BALL_INIT_POS[1] - self.cannon_base.height / 2)
        self.cannon.pos = BALL_INIT_POS


def load_experiment():
    main_widget = CannonExperimentWindow()
    return main_widget
