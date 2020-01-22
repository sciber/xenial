from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr
from models import guides

from controllers.components.tagslist_controller import TagsList
from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu


class CategoriesMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoriesMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        ev.bind(on_active_guide=self.set_categoriesmenu_items)
        self.set_categoriesmenu_items()

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Categories')

    def set_categoriesmenu_items(self, *args):
        if guides.active_guide is not None:
            self.categoriesmenu_widget.categoriesmenu_items = guides.active_guide.categories_list()
        else:
            self.categoriesmenu_widget.categoriesmenu_items = []


class CategoryScreen(Screen):
    category_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.tagslist_widget = TagsList()
        self.ids.tagslist_container.add_widget(self.tagslist_widget)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        ev.bind(on_active_guide=self.clear_category_screen_items)
        ev.bind(on_ui_lang_code=self.translate_ui)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Category')
        self.related_categories_subtitle = tr.translate('Related categories')
        self.related_articles_subtitle = tr.translate('Related articles')

    def clear_category_screen_items(self, *args):
        if self.category_id:
            self.category_id = 0

    def on_category_id(self, *args):
        if self.category_id:
            category = guides.active_guide.category_by_id(self.category_id)
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