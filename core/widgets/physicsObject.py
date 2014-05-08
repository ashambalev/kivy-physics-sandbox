# -*- coding: utf-8 -*-
import collections
import math

from kivy.graphics import *
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class Vector(object):
    title = ''
    length = 0.0
    angle = 0.0
    mode = 'object'
    color = (1, 1, 1, 1)

    def __init__(self, title, length, angle, color, mode):
        self.title = title
        self.length = length
        self.angle = angle
        self.color = color
        self.mode = mode


class PhysicsObject(Widget):
    angle = NumericProperty()
    source = StringProperty()
    color = ListProperty([1, 1, 1, 1])
    _vectors = {}
    _vector_labels = {}
    _trajectory = collections.deque()
    _trajectory_points = 80
    _trajectory_resolution = 10
    show_trajectory = False

    def add_vector(self, name, title, length, angle=0.0, color=(1, 1, 1, 1), mode='object'):
        self._vectors[name] = Vector(title, length, angle, color, mode)
        vector_label = Label(text=title)
        self._vector_labels[name] = vector_label
        self.add_widget(vector_label)

    def update(self, dt):
        if len(self._trajectory) == 0:
            self._trajectory.appendleft((self.pos[0], self.pos[1]))
        if math.fabs(self._trajectory[0][0] - self.pos[0]) + \
                math.fabs(self._trajectory[0][1] - self.pos[1]) > self._trajectory_resolution:
            self._trajectory.appendleft((self.pos[0], self.pos[1]))
            if len(self._trajectory) > self._trajectory_points:
                self._trajectory.pop()

    def update_vector(self, name, length, angle):
        vector = self._vectors[name]
        vector.name = name
        vector.length = length
        vector.angle = angle
        self._vectors[name] = vector

    def draw(self, canvas):
        with canvas:
            if self.show_trajectory:
                Color(1, 1, 1, 0.6)
                Line(points=[self.x, self.y] + [x for t in self._trajectory for x in t], width=2)
            Translate(self.x, self.y)
            Rotate(-self.angle, 0, 0, 1)
            Color(self.color[0], self.color[1], self.color[2], self.color[3])
            Rectangle(size=self.size, pos=(-self.width / 2, -self.height / 2), source=self.source)
            Rotate(self.angle, 0, 0, 1)
            self.draw_vectors(canvas)
            Translate(-self.x, -self.y)

    def clear_trajectory(self):
        self._trajectory.clear()

    def init(self, *largs):
        self.update(0)
        self.clear_trajectory()

    def draw_vectors(self, canvas):
        arrow_size = 4
        scale = 8.5
        for vector_name, vector in self._vectors.iteritems():
            Rotate(-vector.angle, 0, 0, 1)
            Color(vector.color[0], vector.color[1], vector.color[2], vector.color[3])
            points = [0, 0,
                      0, vector.length * scale,
                      -arrow_size, vector.length * scale - arrow_size * math.copysign(1, vector.length),
                      arrow_size, vector.length * scale - arrow_size * math.copysign(1, vector.length),
                      0, vector.length * scale,
                      0, 0]
            Line(points=points, width=1.5)

            Translate(0, vector.length / 2 * scale)

            Rotate(vector.angle, 0, 0, 1)

            Color(0, 0, 0, 0.5)
            Rectangle(size=(
            self._vector_labels[vector_name].texture_size[0] + 2, self._vector_labels[vector_name].texture_size[1] + 2),
                      pos=(-1, -1))

            Color(1, 1, 1, 1)
            Rectangle(texture=self._vector_labels[vector_name].texture,
                      size=self._vector_labels[vector_name].texture_size,
                      pos=(0, 0))

            Rotate(-vector.angle, 0, 0, 1)
            Translate(0, -vector.length / 2 * scale)

            Rotate(vector.angle, 0, 0, 1)