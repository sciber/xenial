"""
Category presenter
==================
Contains CategoriesMenuScreen and CategoryScreen classes presenting data to the 'categoriesmenu_screen.kv' and
'category_screen.kv' screens views, respectively.
"""

from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from events.global_events import ev
from translations.translator import transl
from models.guides_model import guides

from presenters.components.tagslist_presenter import TagsList
from presenters.components.categoriesmenu_presenter import CategoriesMenu
from presenters.components.articlesmenu_presenter import ArticlesMenu


class CategoriesMenuScreen(Screen):
    """
    Presents data to the Categories menu 'categoriesmenu_screen.kv' screen view.
    """

    def __init__(self, **kwargs):
        super(CategoriesMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        ev.bind(on_active_guide=self._set_categoriesmenu_items)
        self._set_categoriesmenu_items()

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Categories')

    def _set_categoriesmenu_items(self, *args):
        if guides.active_guide is not None:
            self.categoriesmenu_widget.categoriesmenu_items = guides.active_guide.categories_list()
        else:
            self.categoriesmenu_widget.categoriesmenu_items = []


class CategoryScreen(Screen):
    """
    Presents data to the Category 'category_screen.kv' screen view.
    """

    category_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.tagslist_widget = TagsList()
        self.ids.tagslist_container.add_widget(self.tagslist_widget)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        ev.bind(on_active_guide=self._clear_category_screen_items)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def on_category_id(self, instance, category_id):
        """ Updates object attributes according to `category_id` attribute/argument. """

        if category_id:
            category = guides.active_guide.category_by_id(category_id)
            self.category_name = category.category_name
            self.category_icon = category.category_icon
            self.category_description = category.category_description
            self.tagslist_widget.tagslist_items = category.tags_list()
            self.categoriesmenu_widget.categoriesmenu_items = category.related_categories_list()
            self.category_has_related_categories = bool(self.categoriesmenu_widget.categoriesmenu_items)
            self.articlesmenu_widget.articlesmenu_items = category.articles_list()
            self.category_has_articles = bool(self.articlesmenu_widget.articlesmenu_items)
        else:
            self.category_name = ''
            self.category_icon = ''
            self.category_description = ''
            self.tagslist_widget.tagslist_items = []
            self.categoriesmenu_widget.categoriesmenu_items = []
            self.category_has_related_categories = False
            self.articlesmenu_widget.articlesmenu_items = []
            self.category_has_articles = False

    def _clear_category_screen_items(self, *args):
        if self.category_id:
            self.category_id = 0

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Category')
        self.related_categories_subtitle = transl.translate('Related categories')
        self.related_articles_subtitle = transl.translate('Related articles')
