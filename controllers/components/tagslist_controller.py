import kivy

from kivy.properties import ListProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button

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

