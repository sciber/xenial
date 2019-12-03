import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button

from models import guides, tags

kivy.require('1.11.1')


class TagsListItem(Button):
    pass


class TagsList(StackLayout):
    tagslist_items = ListProperty()

    def __init__(self, tagslist_items, **kwargs):
        super(TagsList, self).__init__(**kwargs)
        self.tagslist_items = tagslist_items

    def on_tagslist_items(self, instance, value):
        self.clear_widgets()
        for item in self.tagslist_items:
            item_widget = TagsListItem(text=item)
            self.add_widget(item_widget)


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
