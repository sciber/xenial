import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from models import guides, articles

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


class ArticlesMenuScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(ArticlesMenuScreen, self).__init__(**kwargs)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)

    def update_articlesmenu_items(self):
        self.from_guide_name = guides.active_guide_name
        item_keys = ('icon', 'name', 'title', 'synopsis')
        articlesmenu_items = [
            {('article_' + key): item[key] for key in item_keys} for item in articles.all()
        ]
        self.articlesmenu_widget.menu_items = articlesmenu_items
