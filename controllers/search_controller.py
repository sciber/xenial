from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr


class SearchScreen(Screen):
    search_results = []
    search_query = ''
    search_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.search_input.bind(on_text_validate=self.search_articles)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Search')
        self.search_intput_hint_text = tr.translate('Search active guide articles')
        self.search_results_title = tr.translate('{0} results for [b]"{1}"[/b]'.
                                                 format(len(self.search_results), self.search_query))

    def search_articles(self, *args):
        self.search_query = self.search_input.text
        self.search_input.text = ''
        self.search_results_title = tr.translate('{0} results for [b]"{1}"[/b]'.
                                                 format(len(self.search_results), self.search_query))
        print(self.search_query, self.search_results_title)

