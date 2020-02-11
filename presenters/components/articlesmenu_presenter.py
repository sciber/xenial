"""
Articles menu component presenter
===================================
Contains ArticlesMenu class presenting data to the 'articlesmenu.kv' component view.
"""

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ArticlesMenuItem(Button):
    """
    Present data to the Articles menu item view component.
    """
    def __init__(self, article_id, article_name, article_icon, article_title, article_synopsis, **kwargs):
        super(ArticlesMenuItem, self).__init__(**kwargs)
        self.article_id = article_id
        self.article_icon = article_icon
        self.article_name = article_name
        self.article_title = article_title
        self.article_synopsis = article_synopsis


class ArticlesMenu(BoxLayout):
    """
     Presents data to the Articles menu component 'articlesmenu.kv' view.
    """

    articlesmenu_items = ListProperty([])

    def on_articlesmenu_items(self, *args):
        """ Updates the object attributes according to `articlesmenu_items` attribute/argument. """

        self.clear_widgets()
        for item in self.articlesmenu_items:
            item_widget = ArticlesMenuItem(item['article_id'], item['article_name'], item['article_icon'],
                                           item['article_title'], item['article_synopsis'])
            self.add_widget(item_widget)
