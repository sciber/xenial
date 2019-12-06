import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from models import guides, bookmarks

kivy.require('1.11.1')


class BookmarksMenuItem(BoxLayout):
    def __init__(self, article_icon, article_name, article_title, article_synopsis, **kwargs):
        super(BookmarksMenuItem, self).__init__(**kwargs)
        self.article_icon = article_icon
        self.article_name = article_name
        self.article_title = article_title
        self.article_synopsis = article_synopsis


class BookmarksMenuScreen(Screen):
    from_guide_name = ''
    bookmarksmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        self.bookmarksmenu_widget = self.ids.bookmarksmenu_widget

    def on_bookmarksmenu_items(self, instance, value):
        self.bookmarksmenu_widget.clear_widgets()
        for item in self.bookmarksmenu_items:
            item_widget = BookmarksMenuItem(**item)
            self.bookmarksmenu_widget.add_widget(item_widget)

    def update_bookmarksmenu_items(self):
        self.from_guide_name = guides.active_guide_name
        item_keys = ('icon', 'name', 'title', 'synopsis')
        self.bookmarksmenu_items = [
            {('article_' + key): item[key] for key in item_keys} for item in bookmarks.bookmarked_articles()
        ]