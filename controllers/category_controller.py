import os

from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr
from models import guides


# from controllers.components.tagslist_controller import TagsList
from controllers.components.categoriesmenu_controller import CategoriesMenu
# from controllers.components.articlesmenu_controller import ArticlesMenu


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

    def set_categoriesmenu_items(self):
        if guides.active_guide is not None:
            categoriesmenu_items = guides.active_guide.categories_list()
        else:
            categoriesmenu_items = []
        self.categoriesmenu_widget.menu_items = categoriesmenu_items


# class CategoryScreen(Screen):
#     from_guide_name = ''
#
#     def __init__(self, **kwargs):
#         super(CategoryScreen, self).__init__(**kwargs)
#         self.category_icon = ''
#         self.category_name = ''
#         self.category_description = ''
#         self.category_assigned_tags = []
#         self.tagslist_widget = TagsList(self.category_assigned_tags)
#         self.ids.tagslist_container.add_widget(self.tagslist_widget)
#         self.category_related_categories = []
#         self.categoriesmenu_widget = CategoriesMenu()
#         self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
#         self.category_articles = []
#         self.articlesmenu_widget = ArticlesMenu()
#         self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
#
#     def update_category_screen_items(self, category_name):
#         self.from_guide_name = guides.active_guide_name
#         category = categories.by_name(category_name)
#         self.category_icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
#         self.category_name = category_name
#         self.category_assigned_tags = category['tags']
#         self.tagslist_widget.tagslist_items = self.category_assigned_tags
#         self.category_related_categories = categories.related_categories(category_name)
#         category_item_keys = ('icon', 'name')
#         self.categoriesmenu_widget.menu_items = [
#             {'category_' + key: item[key] for key in category_item_keys} for item in self.category_related_categories
#         ]
#         self.category_articles = categories.related_articles(category_name)
#         article_item_keys = ('icon', 'name', 'title', 'synopsis')
#         self.articlesmenu_widget.menu_items = [
#             {'article_' + key: item[key] for key in article_item_keys} for item in self.category_articles
#         ]
