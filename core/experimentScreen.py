# -*- coding: utf-8 -*-
import imp
import json
import os
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import SpinnerOption

__author__ = 'gipzo'


class SpeedButton(SpinnerOption):
    pass


Factory.register('SpeedButton', cls=SpeedButton)


def load_experiment(category, experiment):
    name = "experiments.{}.{}.experiment".format(category, experiment)
    mod = __import__(name,
                     globals=globals(),
                     locals=locals(),
                     fromlist=['experiment'], level=0)
    f = getattr(mod, 'load_experiment')
    return f()

class ExperimentScreen(Screen):
    name = StringProperty('experiment')
    title = StringProperty('Experiment')
    description = StringProperty('')
    description_rst = StringProperty()
    experiment_path = StringProperty()
    category = ''
    experiment_name = ''
    controls = ObjectProperty()
    container = ObjectProperty()
    play_button = ObjectProperty()
    tabs_area = ObjectProperty()
    show_timeline = BooleanProperty(True)
    tabs_pos = NumericProperty(1.0)
    tabs_target = 1.0
    timeline_pos = NumericProperty(1.0)
    timeline_target = 1.0
    time = NumericProperty(0.0)
    max_time = NumericProperty(999.0)
    time_speed = NumericProperty(1.0)
    experiment = ObjectProperty(allownone=True)
    experiment_info = None

    def __init__(self, **kwargs):
        super(ExperimentScreen, self).__init__(**kwargs)
        self.bind(on_leave=self.unload)

    def load_experiment(self, category, experiment):
        self.experiment_name = experiment
        self.category = category
        self.experiment_path = os.path.join("experiments/", category, experiment)
        self.description_rst = open(os.path.join(self.experiment_path, "description.rst"), 'r').read()
        self.experiment_info = json.load(open(os.path.join(self.experiment_path, "experiment.json")))
        self.experiment = load_experiment(category, experiment)
        self.experiment.experiment_path = self.experiment_path
        self.experiment.load()
        self.experiment.build_controls(self.controls)
        self.container.add_widget(self.experiment)
        self.experiment.reset()
        self.title = self.experiment_info['title']
        self.description = self.experiment_info['description']

    def unload(self, *largs):
        self.experiment.clear_widgets()
        self.container.remove_widget(self.experiment)
        self.controls.clear_widgets()
        self.experiment = None

    def update_time(self, dt):
        self.time += dt * self.time_speed
        if self.time > self.max_time:
            self.time = 0.0
        if self.experiment is not None:
            self.experiment.time = self.time
            self.experiment.update(dt * self.time_speed)

    def change_speed(self, value):
        self.time_speed = float(value.replace('x', ''))

    def toggle_time(self, state):
        if state == 'down':
            self.experiment.live = True
            Clock.schedule_interval(self.update_time, 1 / 30.0)
        else:
            self.experiment.live = False
            Clock.unschedule(self.update_time)

    def reset(self, *largs):
        self.play_button.state = 'normal'
        self.time = 0.0
        self.experiment.reset()

    def on_enter(self, *args):
        self.reset()

    def on_pre_enter(self, *args):
        self.tabs_target = 1.0
        self.tabs_pos = 1.0
        self.timeline_target = 1.0
        self.timeline_pos = 1.0

    def on_pre_leave(self, *args):
        self.reset()

    def toggle_tabs(self, *largs):
        if self.tabs_target == 1.0:
            self.tabs_target = 0.0
        else:
            self.tabs_target = 1.0
        Animation.stop_all(self, 'tabs_pos')
        tabs_anim = Animation(tabs_pos=self.tabs_target, t='out_quad', d=0.4)
        tabs_anim.start(self)

    def toggle_timeline(self, *largs):
        if self.timeline_target == 1.0:
            self.timeline_target = 0.0
        else:
            self.timeline_target = 1.0
        Animation.stop_all(self, 'timeline_pos')
        timeline_anim = Animation(timeline_pos=self.timeline_target, t='out_quad', d=0.4)
        timeline_anim.start(self)