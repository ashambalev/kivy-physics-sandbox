# -*- coding: utf-8 -*-
from kivy import platform
from kivy.base import stopTouchApp
from kivy.core.window import Window, Keyboard
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from core.categoryScreen import CategoryScreen
from core.mainScreen import MainScreen
from core.experimentScreen import ExperimentScreen


class MainLayout(BoxLayout):
    title = StringProperty()
    subtitle = StringProperty()
    screen_manager = ObjectProperty()
    tabs_button = ObjectProperty()
    timeline_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.main_screen = MainScreen(mainLayout=self)
        self.category_screen = CategoryScreen(mainLayout=self)
        self.experiment_layout = ExperimentScreen(mainLayout=self)
        self.main_screen.load_categories()
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.category_screen)
        self.screen_manager.add_widget(self.experiment_layout)
        self.screen_manager.current = 'main'
        if platform == 'android':
            Window.bind(on_keyboard=self.on_keyboard_android)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard_android(self, window, key, scancode, codepoint, modifier):
        if key in (8, 27) or key == Keyboard.keycodes['escape']:  # Backspace or escape
            if self.screen_manager.current == 'main':
                stopTouchApp()
            else:
                self.go_main()
        if self.experiment_layout.experiment is not None:
            if key in (282, 319):
                self.experiment_layout.toggle_tabs()
        return True


    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key in (8, 27) or key == Keyboard.keycodes['escape']:  # Backspace or escape
            if self.screen_manager.current == 'main':
                stopTouchApp()
            else:
                self.go_main()
        if self.experiment_layout.experiment is not None:
            if key == 32:  # Spacebar
                self.experiment_layout.play_button.state = 'normal' if self.experiment_layout.play_button.state == 'down' else 'down'
            if key == 114:  # R
                self.experiment_layout.reset()
            if key in (282, 319):
                self.experiment_layout.toggle_tabs()
        return True

    def go_main(self, *largs):
        self.screen_manager.current = 'main'
        self.timeline_button.state = 'normal'
        self.tabs_button.state = 'normal'

    def toggle_tabs(self, *largs):
        self.experiment_layout.toggle_tabs()

    def toggle_timeline(self, *largs):
        self.experiment_layout.toggle_timeline()

    def select_category(self, name):
        self.category_screen.load_experiments(name)
        self.screen_manager.current = self.category_screen.name

    def open_experiment(self, category, name):
        self.experiment_layout.load_experiment(category, name)
        self.screen_manager.current = self.experiment_layout.name


    pass