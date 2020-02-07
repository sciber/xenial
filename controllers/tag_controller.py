from kivy.properties import NumericProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from events import ev
from translator import tr
from models.guides_model import guides

from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu


class TagsMenuItem(Button):
    def __init__(self, tag_id, tag_name, tag_count_categories, tag_count_articles, **kwargs):
        super(TagsMenuItem, self).__init__(**kwargs)
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.tag_count_categories = tag_count_categories
        self.tag_count_articles = tag_count_articles


class TagsMenuScreen(Screen):
    tagsmenu_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TagsMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.tagsmenu_widget = self.ids.tagsmenu_widget
        ev.bind(on_active_guide=self.set_tagsmenu_items)
        self.set_tagsmenu_items()

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Tags')

    def on_tagsmenu_items(self, instance, value):
        self.tagsmenu_widget.clear_widgets()
        for item in self.tagsmenu_items:
            item_widget = TagsMenuItem(item['tag_id'], item['tag_name'],
                                       item['tag_count_categories'], item['tag_count_articles'])
            self.tagsmenu_widget.add_widget(item_widget)

    def set_tagsmenu_items(self, *args):
        if guides.active_guide is not None:
            self.tagsmenu_items = guides.active_guide.tags_list()
        else:
            self.tagsmenu_items = []


class TagScreen(Screen):
    tag_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TagScreen, self).__init__(**kwargs)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        ev.bind(on_active_guide=self.clear_tag_screen_items)
        ev.bind(on_ui_lang_code=self.translate_ui)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Tag')
        self.tagged_categories_subtitle = tr.translate('Tagged categories')
        self.tagged_articles_subtitle = tr.translate('Tagged articles')

    def clear_tag_screen_items(self, *args):
        if self.tag_id:
            self.tag_id = 0

    def on_tag_id(self, *args):
        if self.tag_id:
            tag = guides.active_guide.tag_by_id(self.tag_id)
            self.tag_name = tag.tag_name
            self.categoriesmenu_widget.categoriesmenu_items = tag.tagged_categories_list()
            self.tag_has_tagged_categories = bool(self.categoriesmenu_widget.categoriesmenu_items)
            self.articlesmenu_widget.articlesmenu_items = tag.tagged_articles_list()
            self.tag_has_tagged_articles = bool(self.articlesmenu_widget.articlesmenu_items)
        else:
            self.tag_name = ''
            self.categoriesmenu_widget.categoriesmenu_items = []
            self.tag_has_tagged_categories = False
            self.articlesmenu_widget.articlesmenu_items = []
            self.tag_has_tagged_articles = False
