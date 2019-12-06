import os

import kivy

from kivy.uix.screenmanager import Screen

from models import guides, categories

from controllers.components.tagslist_controller import TagsList
from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu

kivy.require('1.11.1')


class CategoriesMenuScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(CategoriesMenuScreen, self).__init__(**kwargs)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)

    def update_categoriesmenu_items(self):
        self.from_guide_name = guides.active_guide_name
        item_keys = ('icon', 'name')
        categoriesmenu_items = [
            {('category_' + key): item[key] for key in item_keys} for item in categories.all()
        ]
        self.categoriesmenu_widget.menu_items = categoriesmenu_items


class CategoryScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.category_icon = ''
        self.category_name = ''
        self.category_description = ''
        self.category_assigned_tags = []
        self.tagslist_widget = TagsList(self.category_assigned_tags)
        self.ids.tagslist_container.add_widget(self.tagslist_widget)
        self.category_related_categories = []
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.category_articles = []
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)

    def update_category_screen_items(self, category_name):
        self.from_guide_name = guides.active_guide_name
        category = categories.by_name(category_name)
        self.category_icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
        self.category_name = category_name
        self.category_assigned_tags = category['tags']
        self.tagslist_widget.tagslist_items = self.category_assigned_tags
        self.category_related_categories = categories.related_categories(category_name)
        category_item_keys = ('icon', 'name')
        self.categoriesmenu_widget.menu_items = [
            {'category_' + key: item[key] for key in category_item_keys} for item in self.category_related_categories
        ]
        self.category_articles = categories.related_articles(category_name)
        article_item_keys = ('icon', 'name', 'title', 'synopsis')
        self.articlesmenu_widget.menu_items = [
            {'article_' + key: item[key] for key in article_item_keys} for item in self.category_articles
        ]
