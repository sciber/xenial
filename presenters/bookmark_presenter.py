"""
Bookmark presenter
===================
Contains BookmarksMenuScreen class presenting data to the 'bookmarksmenu_screen.kv' screen view.
"""

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from events import ev
from translations.translator import transl
from models.guides_model import guides


class BookmarksMenuItem(BoxLayout):
    """
    Presents data to the Bookmarks menu item view component (defined in 'bookmarksmenu_screen.kv').
    """

    def __init__(self, bookmark_id, bookmark_article_id, bookmark_article_icon,
                 bookmark_article_title, bookmark_article_synopsis, **kwargs):
        super(BookmarksMenuItem, self).__init__(**kwargs)
        self.bookmark_id = bookmark_id
        self.bookmark_article_id = bookmark_article_id
        self.bookmark_article_icon = bookmark_article_icon
        self.bookmark_article_title = bookmark_article_title
        self.bookmark_article_synopsis = bookmark_article_synopsis

    def remove_bookmark(self, bookmark_id):
        """ Removes article's bookmark from data model. """

        guides.active_guide.delete_bookmark(bookmark_id)
        ev.dispatch('on_remove_bookmark', self.bookmark_article_id)


class BookmarksMenuScreen(Screen):
    """
    Presents data to the Bookmarks menu 'bookmarksmenu_screen.kv' screen view.
    """

    bookmarksmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        self.bookmarksmenu_widget = self.ids.bookmarksmenu_widget
        ev.bind(on_active_guide=self._set_bookmarksmenu_items)
        ev.bind(on_add_bookmark=self._set_bookmarksmenu_items)
        ev.bind(on_remove_bookmark=self._set_bookmarksmenu_items)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self._set_bookmarksmenu_items()

    def on_bookmarksmenu_items(self, instance, bookmarksmenu_items):
        """ Updates the object attributes according to `bookmarksmenu_items` attribute/argument. """

        self.bookmarksmenu_widget.clear_widgets()
        for item in bookmarksmenu_items:
            item_widget = BookmarksMenuItem(item['bookmark_id'], item['bookmark_article_id'],
                                            item['bookmark_article_icon'], item['bookmark_article_title'],
                                            item['bookmark_article_synopsis'])
            self.bookmarksmenu_widget.add_widget(item_widget)

    def _set_bookmarksmenu_items(self, *args):
        if guides.active_guide is not None:
            self.bookmarksmenu_items = guides.active_guide.bookmarks_list()
        else:
            self.bookmarksmenu_items = []

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Bookmarks')
