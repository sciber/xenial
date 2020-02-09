"""
Tags list component presenter
=============================
Contains TagsList class presenting data to the 'tagslist.kv' component view.
"""

from kivy.properties import ListProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button


class TagsListItem(Button):
    """
    Presents data to Tags list item component view.
    """

    def __init__(self, tag_id, tag_name, **kwargs):
        super(TagsListItem, self).__init__(**kwargs)
        self.tag_id = tag_id
        self.tag_name = tag_name


class TagsList(StackLayout):
    """
    Presents data to the Tags list component 'tagslist.kv' view.
    """

    tagslist_items = ListProperty([])

    def on_tagslist_items(self, instance, tagslist_items):
        """ Updates object attributes according to `tagslist_items` attribute/argument. """

        self.clear_widgets()
        for item in tagslist_items:
            item_widget = TagsListItem(item['tag_id'], item['tag_name'])
            self.add_widget(item_widget)
