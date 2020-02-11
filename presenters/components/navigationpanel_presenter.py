"""
Navigation panel presenter
==========================
Contains NavigationPanel class which presents data to Navigation panel 'navigationpanel.kv' view.
"""

from kivy.uix.scrollview import ScrollView

from events import ev
from translations.translator import transl
from models.guides_model import guides


class NavigationPanel(ScrollView):
    """
    Presents data to the Navigation panel 'navigationpanel.kv' view component.
    """

    def __init__(self, **kwargs):
        super(NavigationPanel, self).__init__(**kwargs)
        self._set_has_active_guide()
        ev.bind(on_active_guide=self._set_has_active_guide)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def _set_has_active_guide(self, *args):
        self.has_active_guide = bool(guides.active_guide is not None)

    def _translate_ui(self, *args):
        self.search_button_title = transl.translate('Search')
        self.categories_button_title = transl.translate('Categories')
        self.tags_button_title = transl.translate('Tags')
        self.articles_button_title = transl.translate('Articles')
        self.bookmarks_button_title = transl.translate('Bookmarks')
        self.guides_button_title = transl.translate('Guides')
        self.settings_button_title = transl.translate('Settings')
