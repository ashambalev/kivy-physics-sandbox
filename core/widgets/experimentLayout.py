# -*- coding: utf-8 -*-
import imp
import json
import os
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import SpinnerOption

__author__ = 'gipzo'

Builder.load_string('''
<SpeedButton>:
    background_normal: 'data/button_normal.png'
    background_down: 'data/button_down.png'


<ExperimentLayout>:
    container: container
    controls: controls
    time_slider:time_slider
    tabs_area: tabs_area
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'

            RelativeLayout:
                size_hint: 1, 1

                id: container

            Widget:
                id: tabs_area
                size_hint: None, 1
                width: sp(312)*root.tabs_pos
        Widget:
            size_hint: 1, None
            height: sp(64+16)*root.timeline_pos

    TabbedPanel:
        size_hint: None, None
        width: sp(312)
        background_color: 1,1,1,0
        tab_height:30
        height: root.tabs_area.height
        pos: root.tabs_area.pos[0], root.tabs_area.pos[1]
        do_default_tab: False
        TabbedPanelItem:
            text: 'Info'
            background_normal: 'data/tab_bg.png'
            background_down: 'data/tab_bg_down.png'
            StackLayout:
                padding: '12sp'
                RstDocument:
                    document_root: root.experiment_path
                    source: root.description_rst
        TabbedPanelItem:
            text: 'Controls'
            background_color: 1,1,1,1
            background_normal: 'data/tab_bg.png'
            background_down: 'data/tab_bg_down.png'
            border: 14,14,14,14
            ScrollView:
                GridLayout:
                    size_hint: 1.0, None
                    height: self.minimum_height
                    cols: 1
                    id: controls
                    spacing: '12sp'
                    padding: '12sp'


    BoxLayout:
        size_hint: 1, None
        padding:'8sp'
        pos: 0, sp(-64-16)*(1.0-root.timeline_pos)
        height: sp(64+16)
        spacing:8
        orientation: 'horizontal'


        ToggleButton:
            size_hint: None, 1
            size: '64sp', '64sp'
            border: 3,3,3,3
            background_down: 'data/play_down.png'
            background_normal: 'data/play_normal.png'
            text: ''
            on_state: root.toggle_time(self.state)
        Button:
            size_hint: None, 1
            size: '64sp', '64sp'
            border: 3,3,3,3
            background_down: 'data/reset.png'
            background_normal: 'data/reset.png'
            text: ''
            on_state: root.reset()

        Label:
            size_hint: None, 1
            size: '64sp', '64sp'
            font_size: '16sp'
            text: "{:.2f} s".format(root.time)
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        Slider:
            id: time_slider
            padding: '24sp'
            opacity: 1.0 if root.experiment and root.experiment.use_timeline else 0.0
            on_value: root.change_time(self.value)

        Spinner:
            size_hint: None, 1.0
            size: '64sp', '64sp'
            text: '1x'
            border: 22, 22, 22, 22
            background_down: 'data/spinner_down.png'
            background_normal: 'data/spinner_normal.png'
            values: '1x', '2x', '5x'
            option_cls: 'SpeedButton'
            on_text: root.change_speed(self.text)

''')


class SpeedButton(SpinnerOption):
    pass


Factory.register('SpeedButton', cls=SpeedButton)


def load_module(category, experiment, name):
    tmp = imp.find_module(name, ["experiments/{}/{}/".format(category, experiment)])
    try:
        module = imp.load_module(name, tmp[0], "path", tmp[2])
    finally:
        tmp[0].close()
    return module


class ExperimentLayout(Screen):
    name = StringProperty('experiment')
    title = StringProperty('Experiment')
    description = StringProperty('')
    description_rst = StringProperty()
    experiment_path = StringProperty()
    category = ''
    experiment_name = ''
    controls = ObjectProperty()
    container = ObjectProperty()
    tabs_area = ObjectProperty()
    time_slider = ObjectProperty()
    show_timeline = BooleanProperty(True)
    tabs_pos = NumericProperty(1.0)
    tabs_target = 1.0
    timeline_pos = NumericProperty(1.0)
    timeline_target = 1.0
    time = NumericProperty(0.0)
    max_time = NumericProperty(30.0)
    time_speed = NumericProperty(1.0)
    experiment = ObjectProperty(allownone=True)
    experiment_info = None

    def __init__(self, **kwargs):
        super(ExperimentLayout, self).__init__(**kwargs)
        self.bind(on_leave=self.unload)

    def load_experiment(self, category, experiment):
        self.experiment_name = experiment
        self.category = category
        self.experiment_path = os.path.join("experiments/", category, experiment)
        self.description_rst = os.path.join(self.experiment_path, "description.rst")
        self.experiment_info = json.load(open(os.path.join(self.experiment_path, "experiment.json")))
        exp_module = load_module(category, experiment, "experiment")
        self.experiment = exp_module.load_experiment()
        self.experiment.build_controls(self.controls)
        self.container.add_widget(self.experiment)
        self.time_slider.min = 0
        self.time_slider.max = self.max_time

        self.title = self.experiment_info['title']
        self.description = self.experiment_info['description']

    def unload(self, *largs):
        self.container.remove_widget(self.experiment)
        self.controls.clear_widgets()
        self.experiment = None

    def update_time(self, dt):
        self.time += dt * self.time_speed
        self.time_slider.value = self.time
        if self.time > self.max_time:
            self.time = 0
        self.experiment.time = self.time
        self.experiment.update(dt * self.time_speed)

    def change_time(self, value):
        self.time = value
        self.experiment.time = self.time

    def change_speed(self, value):
        self.time_speed = float(value.replace('x', ''))

    def toggle_time(self, state):
        if state == 'down':
            Clock.schedule_interval(self.update_time, 1 / 30.0)
        else:
            Clock.unschedule(self.update_time)

    def reset(self, *largs):
        self.experiment.reset()

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