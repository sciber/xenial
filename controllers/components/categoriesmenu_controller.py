import kivy

from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

kivy.require('1.11.1')


class CategoriesMenuItem(Button):
    def __init__(self, category_icon, category_name, **kwargs):
        super(CategoriesMenuItem, self).__init__(**kwargs)
        self.category_icon = category_icon
        self.category_name = category_name


class CategoriesMenu(GridLayout):
    menu_items = ListProperty([])

    def on_menu_items(self, instance, value):
        self.clear_widgets()
        for item in self.menu_items:
            item_widget = CategoriesMenuItem(**item)
            self.add_widget(item_widget)
