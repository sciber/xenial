from kivy.properties import ListProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button


class TagsListItem(Button):
    def __init__(self, tag_id, tag_name, **kwargs):
        super(TagsListItem, self).__init__(**kwargs)
        self.tag_id = tag_id
        self.tag_name = tag_name


class TagsList(StackLayout):
    tagslist_items = ListProperty([])

    def on_tagslist_items(self, *args):
        self.clear_widgets()
        for item in self.tagslist_items:
            item_widget = TagsListItem(item['tag_id'], item['tag_name'])
            self.add_widget(item_widget)
