from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from events import ev
from translator import tr
from models import guides

# from controllers.components.categoriesmenu_controller import CategoriesMenu
# from controllers.components.articlesmenu_controller import ArticlesMenu


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


# class TagScreen(Screen):
#     from_guide_name = ''
#
#     def __init__(self, **kwargs):
#         super(TagScreen, self).__init__(**kwargs)
#         self.tag_name = ''
#         self.tagged_categories = []
#         self.categoriesmenu_widget = CategoriesMenu()
#         self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
#         self.tagged_articles = []
#         self.articlesmenu_widget = ArticlesMenu()
#         self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
#
#     def update_tag_screen_items(self, tag_name):
#         self.from_guide_name = guides.active_guide_name
#         self.tag_name = tag_name
#         self.tagged_categories = tags.tagged_categories(tag_name)
#         category_item_keys = ('icon', 'name')
#         self.categoriesmenu_widget.menu_items = [
#             {'category_' + key: item[key] for key in category_item_keys} for item in self.tagged_categories
#         ]
#         self.tagged_articles = tags.tagged_articles(tag_name)
#         article_item_keys = ('icon', 'name', 'title', 'synopsis')
#         self.articlesmenu_widget.menu_items = [
#             {'article_' + key: item[key] for key in article_item_keys} for item in self.tagged_articles
#         ]
