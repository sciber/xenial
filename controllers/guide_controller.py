import os

import kivy

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from models import guides

from controllers.components.tagslist_controller import TagsList

kivy.require('1.11.1')


class GuidesMenuItem(BoxLayout):
    def __init__(self, item_data, **kwargs):
        super(GuidesMenuItem, self).__init__(**kwargs)
        for key in item_data:
            setattr(self, key, item_data[key])


class GuidesMenuScreen(Screen):
    guidesmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(GuidesMenuScreen, self).__init__(**kwargs)
        if guides.active_guide_name:
            self.update_guidesmenu_items()

    def update_guidesmenu_items(self):
        item_keys = ('icon', 'name', 'title', 'lang', 'from_place', 'to_place', 'is_active')
        self.guidesmenu_items = [
            {('guide_' + key): item[key] for key in item_keys} for item in guides.all()
        ]

    def on_guidesmenu_items(self, instance, value):
        guidesmenu = self.ids.guidesmenu
        guidesmenu.clear_widgets()
        for item in self.guidesmenu_items:
            item_widget = GuidesMenuItem(item)
            guidesmenu.add_widget(item_widget)


class GuideLoadFailedWarning(Popup):
    def __init__(self, message, **kwargs):
        super(GuideLoadFailedWarning, self).__init__(**kwargs)
        self.message = message


class GuideScreen(Screen):
    def __init__(self, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        self.guide_name = ''
        self.guide_icon = ''
        self.guide_title = ''
        self.guide_assigned_tags = []
        self.guide_description = ''
        self.guide_lang = ('', '')
        self.guide_from_place = ''
        self.guide_to_place = ''
        self.tagslist_widget = TagsList(self.guide_tags)
        self.ids.tagslist_container.add_widget(self.tagslist_widget)

    def update_guide_screen_items(self, guide_name):
        guide = guides.by_name(guide_name)
        self.guide_name = guide_name
        self.guide_icon = os.path.join(guides.GUIDES_DIR, guide['name'], 'icons', 'guide', guide['icon'])
        self.guide_title = guide['title']
        self.guide_assigned_tags = guide['tags']
        self.guide_description = guide['description']
        self.guide_lang = guide['lang']
        self.guide_from_place = guide['from_place']
        self.guide_to_place = guide['to_place']
        self.tagslist_widget.tagslist_items = self.guide_assigned_tags


class UnloadGuideWarningPopup(Popup):
    def __init__(self, guide_name, guide_title, **kwargs):
        super(UnloadGuideWarningPopup, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.guide_title = guide_title
