# -*- coding: utf-8 -*-
import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from core.widgets.catalogItem import CatalogItem

__author__ = 'gipzo'

Builder.load_string('''
<MainScreen>:
    name: 'main'
    grid: grid
    ScrollView:
        size_hint: 1, 1
        StackLayout:
            id: grid

            padding: '32sp'
            spacing: '16sp'
            size_hint_y: None
            height: self.minimum_height

''')

EXPERIMENTS_DIR = './experiments/'

class MainScreen(Screen):
    grid = ObjectProperty()
    mainLayout = ObjectProperty()
    title = StringProperty('Kivy physics sandbox')
    description = StringProperty('Please select category')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def load_categories(self):
        for category in os.listdir(EXPERIMENTS_DIR):
            category_dir = os.path.join(EXPERIMENTS_DIR, category)
            if os.path.isdir(category_dir):
                if os.path.isfile(os.path.join(category_dir, 'category.json')):
                    button = CatalogItem()
                    button.load(category_dir, 'category.json')
                    button.bind(on_press=self.on_category)
                    self.grid.add_widget(button)

    def on_category(self, *largs):
        widget = largs[0]
        self.mainLayout.select_category(widget.name)

    pass