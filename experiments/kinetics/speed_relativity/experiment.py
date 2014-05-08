# -*- coding: utf-8 -*-
import math
from kivy.atlas import CoreImage
from kivy.core.text import Label

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import BooleanProperty

from core.widgets.controls.sliderControl import SliderControl
from core.widgets.experimentWindow import ExperimentWindow
from core.widgets.physicsObject import PhysicsObject


Builder.load_string('''
<MyExperimentWindow>:

    Label:
        size: root.size
        pos: root.pos
        halign:'center'
        valign:'middle'
        text_size: self.size
        text: "Speed: {:.2f}".format(root.boat_speed.value)
''')
RIVERSIDE_SIZE = sp(40)
BOAT_WIDTH = sp(30)
BOAT_HEIGHT = sp(60)


class Boat(PhysicsObject):
    boat_speed = 0.0
    river_speed = 0.0
    boat_angle = 0.0
    total_speed = 0.0

    def __init__(self, **kwargs):
        self.show_trajectory = True
        self.size = (BOAT_WIDTH, BOAT_HEIGHT)
        super(Boat, self).__init__(**kwargs)

    def update(self, dt):
        super(Boat, self).update(dt)
        self.angle = self.boat_angle
        self.update_vector('boat_speed', self.boat_speed, self.boat_angle)
        self.update_vector('river_speed', self.river_speed, 90.0)

        total_speed_x = self.boat_speed * math.sin(self.boat_angle * math.pi / 180.0) + self.river_speed
        total_speed_y = self.boat_speed * math.cos(self.boat_angle * math.pi / 180.0)
        total_speed_angle = math.atan2(total_speed_x, total_speed_y) * 180.0 / math.pi
        total_speed_length = math.sqrt(total_speed_x * total_speed_x + total_speed_y * total_speed_y)
        self.total_speed = total_speed_length
        self.update_vector('speed', total_speed_length, total_speed_angle)

        self.x += total_speed_x * dt
        self.y += total_speed_y * dt
        max_size = max(self.width, self.height) / 2
        if self.x < 0.0 + max_size:
            self.x = 0.0 + max_size
        if self.y < RIVERSIDE_SIZE + max_size:
            self.y = RIVERSIDE_SIZE + max_size
        if self.x > self.parent.width - max_size:
            self.x = self.parent.width - max_size
        if self.y > self.parent.height - RIVERSIDE_SIZE - max_size:
            self.y = self.parent.height - RIVERSIDE_SIZE - max_size

    pass


class MyExperimentWindow(ExperimentWindow):
    boat_speed = SliderControl(label="Boat speed",
                               description="Speed value of the boat",
                               min=1, max=40, value=5.0, dim=' m/s')
    river_speed = SliderControl(label="River speed",
                                description="Speed of the river flow",
                                min=-40, max=40, value=5.0, dim=' m/s')
    boat_angle = SliderControl(label="Angle of the boat",
                               description="Control your boat",
                               min=-180.0, max=180.0, value=0.0, dim=u' \u00b0')

    boat = None
    river_offset = 0.0
    use_timeline = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MyExperimentWindow, self).__init__(**kwargs)
        self.boat = Boat()
        self.boat_inited = False
        self.boat.source = 'experiments/kinetics/speed_relativity/data/boat.png'
        self.boat.color = [194 / 255.0, 56 / 255.0, 8 / 255.0, 1.0]
        self.boat.add_vector('boat_speed', 'Vb', self.boat_speed.value, self.boat_angle.value, (1, 0.4, 1, 1))
        self.boat.add_vector('river_speed', 'Vr', self.river_speed.value, 90.0, (0.4, 1, 1, 1))
        self.boat.add_vector('speed', 'V', self.boat_speed.value, self.boat_angle.value)
        self.boat_angle.bind(on_value_changed=self.update)
        self.boat_speed.bind(on_value_changed=self.update)
        self.river_speed.bind(on_value_changed=self.update)
        self.add_widget(self.boat)

        self.speed_label = Label(text='0.0 m/s', font_size=16, bold=True)
        self.speed_label.refresh()

    def reset(self, *largs):
        self.boat_speed.value = 5.0
        self.river_speed.value = 5.0
        self.boat_angle.value = 0.0
        self.boat.x = sp(100)
        self.boat.y = sp(RIVERSIDE_SIZE + BOAT_HEIGHT / 2)
        self.boat.init()


    def update(self, *largs):
        try:
            dt = float(largs[0])
        except:
            dt = 0.0
        self.boat.boat_speed = self.boat_speed.value
        self.boat.boat_angle = self.boat_angle.value
        self.boat.river_speed = self.river_speed.value
        self.river_offset += dt * self.river_speed.value / 100.0
        if self.river_offset > 1.0:
            self.river_offset = 0
        if self.river_offset < 0:
            self.river_offset = 1.0
        self.boat.update(dt)
        self.speed_label.text = "Boat combined speed: {:.2f} m/s".format(self.boat.total_speed)
        self.speed_label.refresh()
        self.river_texture = CoreImage.load(
            'experiments/kinetics/speed_relativity/data/river.png').texture
        self.riverside_texture = CoreImage.load(
            'experiments/kinetics/speed_relativity/data/riverside.png').texture
        self.river_texture.wrap = 'repeat'
        self.riverside_texture.wrap = 'repeat'
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Riversides
            Color(70 / 255.0, 204 / 255.0, 41 / 255.0, 1)
            rsu = 0.0
            rsv = 0.0
            rsw = self.width / self.riverside_texture.width * 2
            rsh = -RIVERSIDE_SIZE / self.riverside_texture.height * 2
            Rectangle(pos=self.pos, size=(self.size[0], RIVERSIDE_SIZE), texture=self.riverside_texture,
                      tex_coords=[
                          rsu, rsv,
                          rsu + rsw, rsv,
                          rsv + rsw, rsv + rsh,
                          rsu, rsv + rsh
                      ])
            Rectangle(pos=(self.pos[0], self.pos[1] + self.height - RIVERSIDE_SIZE),
                      size=(self.size[0], RIVERSIDE_SIZE), texture=self.riverside_texture,
                      tex_coords=[
                          rsu, rsv,
                          rsu + rsw, rsv,
                          rsv + rsw, rsv + rsh,
                          rsu, rsv + rsh
                      ])

            Color(30 / 255.0, 215 / 255.0, 1, 1)
            o = -self.river_offset
            u = 0.0
            v = 0.0
            w = self.width / self.river_texture.width
            h = -self.height / self.river_texture.height
            Rectangle(pos=(self.pos[0], self.pos[1] + RIVERSIDE_SIZE),
                      size=(self.size[0], self.size[1] - 2 * RIVERSIDE_SIZE),
                      texture=self.river_texture,
                      tex_coords=[
                          o + u, v,
                          o + u + w, v,
                          o + v + w, v + h,
                          o + u, v + h
                      ])
            Color(1, 1, 1, 1)
            Rectangle(
                pos=(10, 10),
                size=self.speed_label.texture.size,
                texture=self.speed_label.texture
            )

        self.boat.draw(self.canvas)

    def on_size(self, *largs):
        if self.height > 250 and not self.boat_inited:
            self.boat.init()
            self.boat_inited = True
        self.update(0)


    def on_time(self, *largs):
        pass
        #self.boat_pos_x = self.time * self.river_speed.value
        #self.boat_pos_y = self.time * self.boat_speed.value
        #       self.boat.pos = (self.boat_pos_x, self.boat_pos_y)


def load_experiment():
    main_widget = MyExperimentWindow()
    return main_widget



