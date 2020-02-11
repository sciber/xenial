"""
Tag presenter
=============
Contains TagsMenuScreen and TagScreen classes which present data to the 'tagsmenu_screen.kv' and 'tag_screen.kv'
screens views, respectively.
"""

from kivy.properties import NumericProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from events.global_events import ev
from translations.translator import transl
from models.guides_model import guides

from presenters.components.categoriesmenu_presenter import CategoriesMenu
from presenters.components.articlesmenu_presenter import ArticlesMenu


class TagsMenuItem(Button):
    """
    Presents data to the Tags menu item view component (defined in 'tagsmenu_screen.kv').
    """

    def __init__(self, tag_id, tag_name, tag_count_categories, tag_count_articles, **kwargs):
        super(TagsMenuItem, self).__init__(**kwargs)
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.tag_count_categories = tag_count_categories
        self.tag_count_articles = tag_count_articles


class TagsMenuScreen(Screen):
    """
    Presents data to the Tags menu 'tagsmenu_screen.kv' screen view.
    """

    tagsmenu_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TagsMenuScreen, self).__init__(**kwargs)
        self.tagsmenu_widget = self.ids.tagsmenu_widget
        ev.bind(on_active_guide=self._set_tagsmenu_items)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self._set_tagsmenu_items()

    def on_tagsmenu_items(self, instance, tagsmenu_items):
        """ Updates the object attributes according to `tagsmenu_items` attribute/argument. """

        self.tagsmenu_widget.clear_widgets()
        for item in tagsmenu_items:
            item_widget = TagsMenuItem(item['tag_id'], item['tag_name'],
                                       item['tag_count_categories'], item['tag_count_articles'])
            self.tagsmenu_widget.add_widget(item_widget)

    def _set_tagsmenu_items(self, *args):
        if guides.active_guide is not None:
            self.tagsmenu_items = guides.active_guide.tags_list()
        else:
            self.tagsmenu_items = []

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Tags')


class TagScreen(Screen):
    """
    Presents data to the Tag 'tag_screen.kv' screen view.
    """

    tag_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TagScreen, self).__init__(**kwargs)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        ev.bind(on_active_guide=self._clear_tag_screen_items)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def on_tag_id(self, instance, tag_id):
        """" Updates object attributes according to `tag_id` attribute/argument. """

        if tag_id:
            tag = guides.active_guide.tag_by_id(tag_id)
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

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Tag')
        self.tagged_categories_subtitle = transl.translate('Tagged categories')
        self.tagged_articles_subtitle = transl.translate('Tagged articles')

    def _clear_tag_screen_items(self, *args):
        if self.tag_id:
            self.tag_id = 0
