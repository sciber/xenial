"""
Guide's articles search presenter
=================================
Contains SearchScreen class which presents data to the 'search_screen.kv' screen view.
"""

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label

from models.guides_model import guides
from events import ev
from translations.translator import transl


class BlockSearchResultsItem(Label):
    """
    Presents data to the article's block search results item component view (defined in 'search_screen.kv').
    """

    pass


class ArticleSearchResultsItem(Button):
    """
    Presents data to the article search results item component view (defined in 'search_screen.kv').
    """

    def __init__(self, article_search_results_item, **kwargs):
        super(ArticleSearchResultsItem, self).__init__(**kwargs)
        self.article_search_results_item = article_search_results_item
        self.article_id = self.article_search_results_item[0][0]
        article_list_item = next(item for item in guides.active_guide.articles_list()
                                 if item['article_id'] == self.article_id)
        blocks_search_results = []
        for idx, item in enumerate(self.article_search_results_item):
            if item[2] == 'title':
                article_list_item['article_title'] = item[4]
            elif item[2] == 'synopsis':
                article_list_item['article_synopsis'] = item[4]
            else:
                blocks_search_results.append(item)
        self.article_title = article_list_item['article_title']
        self.article_synopsis = article_list_item['article_synopsis']
        search_results_container = self.ids.search_results_container
        for block_result in blocks_search_results:
            block_result_widget = BlockSearchResultsItem(text=block_result[4])
            search_results_container.add_widget(block_result_widget)


class SearchScreen(Screen):
    """
    Presents data to the Search screen 'search_screen.kv' view.
    """

    articles_search_results = []
    search_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.search_query = ''
        self.search_results_container = self.ids.search_results_container
        self.search_input.bind(on_text_validate=self.search_articles)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def search_articles(self, *args):
        """ Search in articles texts (stored in database 'article_block_search' table) for phrase submitted from
            the screen's text input. """

        self.search_query = self.search_input.text
        self.search_input.text = ''
        self.articles_search_results = []
        self.search_results_container.clear_widgets()
        if self.search_query:
            self.search_input_hint_text = self.search_query
            search_results_rows = guides.active_guide.search_articles(('block_text:({})'.format(self.search_query),))
            articles_ranks_indices = {}
            for row in search_results_rows:
                article_id = row[0]
                if article_id in articles_ranks_indices:
                    article_idx = articles_ranks_indices[article_id]
                    self.articles_search_results[article_idx].append(row)
                else:
                    articles_ranks_indices[article_id] = len(self.articles_search_results)
                    self.articles_search_results.append([row])
            for article_results_item in self.articles_search_results:
                article_results_item.sort(key=lambda row: row[1])
                article_search_results_item_widget = ArticleSearchResultsItem(article_results_item)
                self.search_results_container.add_widget(article_search_results_item_widget)
        else:
            self.search_input_hint_text = transl.translate('Search active guide articles')
        self.search_results_head = transl.translate('{0} results for [b]"{1}"[/b]'.
                                                format(len(self.articles_search_results), self.search_query))

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Search')
        self.search_intput_hint_text = transl.translate('Search active guide articles')
        self.search_results_head = transl.translate('{0} results for [b]"{1}"[/b]'.
                                                format(len(self.articles_search_results), self.search_query))
