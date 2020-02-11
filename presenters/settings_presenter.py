"""
Settings presenter
==================
Contains SettingsScreen class which presents data to the 'settings_screen.kv' screen view.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from events import ev
from translator import tr


class LanguageSettingsMenuItem(BoxLayout):
    """
    Presents data to the Language settings menu item component view (defined in 'settings_screen.kv').
    """

    def __init__(self, lang, **kwargs):
        super(LanguageSettingsMenuItem, self).__init__(**kwargs)
        self.lang = lang

    def change_ui_lang_code(self, active):
        """ Changes application's UI language. """

        if active:
            tr.ui_lang_code = self.lang[1]
            ev.dispatch('on_ui_lang_code', self.lang[1])


class SettingsScreen(Screen):
    """
    Presents data to the Settings screen view in 'settings_screen.kv'.
    """

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self.items_container = self.ids.container
        for lang in tr.LANGUAGES:
            menuitem_widget = LanguageSettingsMenuItem(lang)
            self.items_container.add_widget(menuitem_widget)

    def _translate_ui(self, *args):
        self.screen_title = tr.translate('Settings')
        self.app_lang_subtitle = tr.translate('Application language')
