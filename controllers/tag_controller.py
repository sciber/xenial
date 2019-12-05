import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from models import guides, tags

from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu

kivy.require('1.11.1')


class TagsMenuItem(Button):
    def __init__(self, tag_name, num_tagged_categories, num_tagged_articles, **kwargs):
        super(TagsMenuItem, self).__init__(**kwargs)
        self.tag_name = tag_name
        self.num_tagged_categories = num_tagged_categories
        self.num_tagged_articles = num_tagged_articles


class TagsMenuScreen(Screen):
    from_guide_name = ''
    tagsmenu_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TagsMenuScreen, self).__init__(**kwargs)
        self.tagsmenu_widget = self.ids.tagsmenu_widget

    def on_tagsmenu_items(self, instance, value):
        self.tagsmenu_widget.clear_widgets()
        for item in self.tagsmenu_items:
            item_widget = TagsMenuItem(**item)
            self.tagsmenu_widget.add_widget(item_widget)

    def update_tagsmenu_items(self):
        self.from_guide_name = guides.active_guide_name
        self.tagsmenu_items = [{
            'tag_name': tag_name,
            'num_tagged_categories': len(tags.tagged_categories(tag_name)),
            'num_tagged_articles': len(tags.tagged_articles(tag_name))
        } for tag_name in tags.all()]


class TagScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(TagScreen, self).__init__(**kwargs)
        self.tag_name = ''
        self.tagged_categories = []
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.tagged_articles = []
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)

    def update_tag_screen_items(self, tag_name):
        self.from_guide_name = guides.active_guide_name
        self.tag_name = tag_name
        self.tagged_categories = tags.tagged_categories(tag_name)
        category_item_keys = ('icon', 'name')
        self.categoriesmenu_widget.menu_items = [
            {'category_' + key: item[key] for key in category_item_keys} for item in self.tagged_categories
        ]
        self.tagged_articles = tags.tagged_articles(tag_name)
        article_item_keys = ('icon', 'name', 'title', 'synopsis')
        self.articlesmenu_widget.menu_items = [
            {'article_' + key: item[key] for key in article_item_keys} for item in self.tagged_articles
        ]
