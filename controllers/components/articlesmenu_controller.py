import kivy

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

kivy.require('1.11.1')


class ArticlesMenuItem(Button):
    def __init__(self, article_icon, article_name, article_title, article_synopsis, **kwargs):
        super(ArticlesMenuItem, self).__init__(**kwargs)
        self.article_icon = article_icon
        self.article_name = article_name
        self.article_title = article_title
        self.article_synopsis = article_synopsis


class ArticlesMenu(BoxLayout):
    menu_items = ListProperty([])

    def on_menu_items(self, instance, value):
        self.clear_widgets()
        for item in self.menu_items:
            item_widget = ArticlesMenuItem(**item)
            self.add_widget(item_widget)
