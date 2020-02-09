"""
Navigation panel presenter
==========================

"""

from kivy.uix.scrollview import ScrollView

from events import ev
from translator import tr
from models.guides_model import guides


class NavigationPanel(ScrollView):
    """

    """

    def __init__(self, **kwargs):
        super(NavigationPanel, self).__init__(**kwargs)
        self.set_has_active_guide()
        ev.bind(on_active_guide=self._set_has_active_guide)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def _set_has_active_guide(self, *args):
        self.has_active_guide = bool(guides.active_guide is not None)

    def _translate_ui(self, *args):
        self.search_button_title = tr.translate('Search')
        self.categories_button_title = tr.translate('Categories')
        self.tags_button_title = tr.translate('Tags')
        self.articles_button_title = tr.translate('Articles')
        self.bookmarks_button_title = tr.translate('Bookmarks')
        self.guides_button_title = tr.translate('Guides')
        self.settings_button_title = tr.translate('Settings')
