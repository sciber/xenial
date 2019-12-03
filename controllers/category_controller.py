import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from models import guides, categories

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


class CategoriesMenuScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(CategoriesMenuScreen, self).__init__(**kwargs)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)

    def update_categoriesmenu_items(self):
        self.from_guide_name = guides.active_guide_name
        item_keys = ('icon', 'name')
        categoriesmenu_items = [
            {('category_' + key): item[key] for key in item_keys} for item in categories.all()
        ]
        self.categoriesmenu_widget.menu_items = categoriesmenu_items
