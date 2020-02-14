"""
Categories menu component presenter
===================================
Contains CategoriesMenu class presenting data to the 'categoriesmenu.kv' component view.
"""

from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout


class CategoriesMenuItem(AnchorLayout):
    """
    Presents data to the Categories menu item view component.
    """

    def __init__(self, category_id, category_name, category_icon, **kwargs):
        super(CategoriesMenuItem, self).__init__(**kwargs)
        self.category_id = category_id
        self.category_name = category_name
        self.category_icon = category_icon


class CategoriesMenu(GridLayout):
    """
     Presents data to the Categories menu component 'categoriesmenu.kv' view.
    """

    categoriesmenu_items = ListProperty([])

    def on_categoriesmenu_items(self, instance, categoriesmenu_items):
        """ Updates the object attributes according to `categoriesmenu_items` attribute/argument. """

        self.clear_widgets()
        for item in categoriesmenu_items:
            item_widget = CategoriesMenuItem(item['category_id'], item['category_name'], item['category_icon'])
            self.add_widget(item_widget)
