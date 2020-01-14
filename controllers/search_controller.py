from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Search')
        self.search_intput_hint_text = tr.translate('Search active guide articles')
        self.no_results_text = tr.translate('Your search did not match any articles')
