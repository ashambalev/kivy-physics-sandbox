# -*- coding: utf-8 -*-
import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from core.widgets.catalogItem import CatalogItem

__author__ = 'gipzo'

Builder.load_string('''
<CategoryScreen>:
    name: 'category'
    grid: grid
    ScrollView:
        size_hint: 1, 1
        StackLayout:
            id: grid
            padding: '32sp'
            spacing: '32sp'
            size_hint_y: None
            height: self.minimum_height

''')


class CategoryScreen(Screen):
    grid = ObjectProperty()
    mainLayout = ObjectProperty()
    experiments_dir = StringProperty()
    title = StringProperty('Category')
    description = StringProperty('Please select experiment')

    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)

    def load_experiments(self, category):
        path = os.path.join('./experiments/', category)
        self.experiments_dir = path
        self.grid.clear_widgets()
        for experiment in os.listdir(self.experiments_dir):
            experiment_dir = os.path.join(self.experiments_dir, experiment)
            if os.path.isdir(experiment_dir):
                if os.path.isfile(os.path.join(experiment_dir, 'experiment.json')):
                    button = CatalogItem()
                    button.category = category
                    button.load(experiment_dir, 'experiment.json')
                    self.title = button.title
                    button.bind(on_press=self.open_experiment)
                    self.grid.add_widget(button)

    def open_experiment(self, *largs):
        widget = largs[0]
        self.mainLayout.open_experiment(widget.category, widget.name)

    pass