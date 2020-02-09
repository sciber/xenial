from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class CategoriesMenuItem(Button):
    def __init__(self, category_id, category_name, category_icon, **kwargs):
        super(CategoriesMenuItem, self).__init__(**kwargs)
        self.category_id = category_id
        self.category_name = category_name
        self.category_icon = category_icon


class CategoriesMenu(GridLayout):
    categoriesmenu_items = ListProperty([])

    def on_categoriesmenu_items(self, *args):
        self.clear_widgets()
        for item in self.categoriesmenu_items:
            item_widget = CategoriesMenuItem(item['category_id'], item['category_name'], item['category_icon'])
            self.add_widget(item_widget)
