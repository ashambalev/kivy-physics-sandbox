# -*- coding: utf-8 -*-
import collections
import math

from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.widget import Widget
from core.widgets.vectorWidget import VectorWidget


class PhysicsObject(Widget):
    angle = NumericProperty()
    scale = NumericProperty(1.0)
    source = StringProperty()
    color = ListProperty([1, 1, 1, 1])
    constraints = [0, 100, 0, 100]
    constraint_x = BooleanProperty(True)
    constraint_y = BooleanProperty(True)
    _vectors = {}
    _trajectory = collections.deque()
    _trajectory_points = 100
    _trajectory_resolution = 0.05
    show_trajectory = BooleanProperty(False)
    draggable = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_drag')
        super(PhysicsObject, self).__init__(**kwargs)

    def add_vector(self, name, title, length, angle=0.0, color=(1, 1, 1, 1), mode='object'):
        self._vectors[name] = VectorWidget(title=title, length=length, angle=angle, color=color, mode=mode)
        self.add_widget(self._vectors[name])

    def update(self, dt):
        if len(self._trajectory) == 0:
            self._trajectory.appendleft((self.pos[0], self.pos[1]))
        angle0 = math.atan2(self._trajectory[0][1] - self.pos[1], self._trajectory[0][0] - self.pos[0])
        if len(self._trajectory) > 1:
            angle1 = math.atan2(self._trajectory[1][1] - self._trajectory[0][1],
                                self._trajectory[1][0] - self._trajectory[0][0])
        else:
            angle1 = 0
        if math.fabs(angle0 - angle1) > self._trajectory_resolution:
            self._trajectory.appendleft((self.pos[0], self.pos[1]))
            if len(self._trajectory) > self._trajectory_points:
                self._trajectory.pop()

    def after_update(self, dt):
        max_size = max(self.width, self.height) / 2
        if self.constraint_x:
            if self.x < self.constraints[0] + max_size:
                self.x = self.constraints[0] + max_size
            if self.x > self.constraints[1] - max_size:
                self.x = self.constraints[1] - max_size
        if self.constraint_y:
            if self.y < self.constraints[2] + max_size:
                self.y = self.constraints[2] + max_size
            if self.y > self.constraints[3] - max_size:
                self.y = self.constraints[3] - max_size

    def update_vector(self, name, length, angle=None):
        vector = self._vectors[name]
        vector.name = name
        vector.length = length
        if angle is not None:
            vector.angle = angle

    def on_pos(self, *largs):
        for vector in self._vectors.itervalues():
            vector.pos = self.pos

    def clear_trajectory(self):
        self._trajectory.clear()

    def init(self, *largs):
        self.clear_trajectory()

    def on_drag(self, touch):
        pass

    def collide_point(self, x, y):
        max_size = max(self.width, self.height) / 2
        return self.x - max_size < x < self.x + max_size and self.y - max_size < y < self.y + max_size

    def on_touch_down(self, touch):
        if super(PhysicsObject, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.dispatch('on_drag', touch)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.dispatch('on_drag', touch)
            return True
        if super(PhysicsObject, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(PhysicsObject, self).on_touch_up(touch)
        self.dispatch('on_drag', touch)
        touch.ungrab(self)
        return True
