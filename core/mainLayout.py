# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from core.categoryScreen import CategoryScreen
from core.mainScreen import MainScreen
from core.widgets.experimentLayout import ExperimentLayout

Builder.load_string('''
<MainLayout>:
    orientation: 'vertical'
    screen_manager: screen_manager
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            source: 'data/bg.jpg'
            size:root.size
            pos:root.pos
    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1.0, None
        height: '64sp'

        BoxLayout:
            orientation: 'vertical'
            padding: '8sp'

            Label:
                text: root.screen_manager.current_screen.title if root.screen_manager.current_screen else 'Kivy physics sandbox'
                font_size: '20sp'
                bold: True
                halign: 'left'
                text_size: self.size
            Label:
                text: root.screen_manager.current_screen.description if root.screen_manager.current_screen else 'Select category'
                halign: 'left'
                text_size: self.size

        StackLayout:
            orientation: 'rl-tb'
            spacing: '8sp'
            padding: '8sp'
            Button:
                text: ''
                border: 3,3,3,3
                background_down: 'data/home.png'
                background_normal: self.background_down
                size_hint: None, None
                size: sp(64-16), sp(64-16)
                on_press: root.go_main()
            ToggleButton:
                text: ''
                border: 3,3,3,3
                background_down: 'data/timeline_down.png'
                background_normal: 'data/timeline_normal.png'
                background_disabled_normal: 'data/timeline_disabled.png'
                disabled: root.screen_manager.current is not 'experiment'
                size_hint: None, None
                size: sp(64-16), sp(64-16)
                on_press: root.toggle_timeline()

            ToggleButton:
                text: ''
                border: 3,3,3,3
                background_down: 'data/tabs_down.png'
                background_normal: 'data/tabs_normal.png'
                background_disabled_normal: 'data/tabs_disabled.png'
                size_hint: None, None
                disabled: root.screen_manager.current is not 'experiment'
                size: sp(64-16), sp(64-16)
                on_press: root.toggle_tabs()

    ScreenManager:
        id: screen_manager
''')


class MainLayout(BoxLayout):
    title = StringProperty()
    subtitle = StringProperty()
    screen_manager = ObjectProperty()


    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.main_screen = MainScreen(mainLayout=self)
        self.category_screen = CategoryScreen(mainLayout=self)
        self.experiment_layout = ExperimentLayout(mainLayout=self)
        self.main_screen.load_categories()
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.category_screen)
        self.screen_manager.add_widget(self.experiment_layout)
        self.screen_manager.current = 'main'

    def go_main(self, *largs):
        self.screen_manager.current = 'main'

    def toggle_tabs(self, *largs):
        self.experiment_layout.toggle_tabs()

    def toggle_timeline(self, *largs):
        self.experiment_layout.toggle_timeline()

    def select_category(self, name):
        self.category_screen.load_experiments(name)
        self.screen_manager.current = self.category_screen.name

    def open_experiment(self, category, name):
        self.screen_manager.current = self.experiment_layout.name
        self.experiment_layout.load_experiment(category, name)


    pass