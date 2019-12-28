import kivy

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from translator import translator, translations

kivy.require('1.11.1')


class LanguageSettingsMenuItem(BoxLayout):
    def __init__(self, lang, **kwargs):
        super(LanguageSettingsMenuItem, self).__init__(**kwargs)
        self.lang = lang


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.screen_title = 'Settings'
        self.items_container = self.ids.container
        for lang in translator.LANGUAGES:
            menuitem_widget = LanguageSettingsMenuItem(lang)
            self.items_container.add_widget(menuitem_widget)
