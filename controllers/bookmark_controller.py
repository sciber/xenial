from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from events import ev
from translator import tr
from models import guides


class BookmarksMenuItem(BoxLayout):
    def __init__(self, bookmark_id, bookmark_article_id, bookmark_article_icon,
                 bookmark_article_title, bookmark_article_synopsis, **kwargs):
        super(BookmarksMenuItem, self).__init__(**kwargs)
        self.bookmark_id = bookmark_id
        self.bookmark_article_id = bookmark_article_id
        self.bookmark_article_icon = bookmark_article_icon
        self.bookmark_article_title = bookmark_article_title
        self.bookmark_article_synopsis = bookmark_article_synopsis

    def delete_bookmark(self, bookmark_id):
        guides.active_guide.delete_bookmark(bookmark_id)
        ev.dispatch('on_delete_bookmark', self.bookmark_article_id)


class BookmarksMenuScreen(Screen):
    bookmarksmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.bookmarksmenu_widget = self.ids.bookmarksmenu_widget
        ev.bind(on_active_guide=self.set_bookmarksmenu_items)
        ev.bind(on_add_bookmark=self.set_bookmarksmenu_items)
        ev.bind(on_delete_bookmark=self.set_bookmarksmenu_items)
        self.set_bookmarksmenu_items()

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Bookmarks')

    def on_bookmarksmenu_items(self, *args):
        self.bookmarksmenu_widget.clear_widgets()
        for item in self.bookmarksmenu_items:
            item_widget = BookmarksMenuItem(item['bookmark_id'], item['bookmark_article_id'],
                                            item['bookmark_article_icon'], item['bookmark_article_title'],
                                            item['bookmark_article_synopsis'])
            self.bookmarksmenu_widget.add_widget(item_widget)

    def set_bookmarksmenu_items(self, *args):
        if guides.active_guide is not None:
            self.bookmarksmenu_items = guides.active_guide.bookmarks_list()
        else:
            self.bookmarksmenu_items = []
