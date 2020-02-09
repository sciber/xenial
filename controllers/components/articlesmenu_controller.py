from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ArticlesMenuItem(Button):
    def __init__(self, article_id, article_name, article_icon, article_title, article_synopsis, **kwargs):
        super(ArticlesMenuItem, self).__init__(**kwargs)
        self.article_id = article_id
        self.article_icon = article_icon
        self.article_name = article_name
        self.article_title = article_title
        self.article_synopsis = article_synopsis


class ArticlesMenu(BoxLayout):
    articlesmenu_items = ListProperty([])

    def on_articlesmenu_items(self, *args):
        self.clear_widgets()
        for item in self.articlesmenu_items:
            item_widget = ArticlesMenuItem(item['article_id'], item['article_name'], item['article_icon'],
                                           item['article_title'], item['article_synopsis'])
            self.add_widget(item_widget)
