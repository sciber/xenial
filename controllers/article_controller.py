import kivy

from kivy.uix.screenmanager import Screen

from models import guides, articles

from controllers.components.articlesmenu_controller import ArticlesMenu

kivy.require('1.11.1')


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
