"""
Guide presenter
===============
Contains GuidesMenuScreen and GuideScreen classes presenting data to the 'guidesmenu_screen.kv' and 'guide_screen.kv'
screens views, respectively.
Contains LoadGuidePopup, GuideLoadFailedWarning and RemoveGuideWarningPopup classes which present data to corresponding
popup components views.
"""

import os

from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from events.global_events import ev
from translations.translator import transl
from models.guides_model import guides


class GuidesMenuItem(BoxLayout):
    """
    Presents data to the Guides menu item component view (defined in 'guidesmenu_screen.kv').
    """

    def __init__(self, guide_name, guide_icon, guide_title, guide_description,
                 guide_lang, guide_from_place, guide_to_place, **kwargs):
        super(GuidesMenuItem, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.guide_icon = guide_icon
        self.guide_title = guide_title
        self.guide_description = guide_description
        self.guide_lang = guide_lang
        self.guide_from_place = guide_from_place
        self.guide_from_place_label = (transl.translate('From') + ': [b]{}[/b]').format(self.guide_from_place)
        self.guide_to_place = guide_to_place
        self.guide_to_place_label = (transl.translate('To') + ': [b]{}[/b]').format(self.guide_to_place)
        self.is_active_guide = (guides.active_guide is not None and self.guide_name == guides.active_guide.guide_name)
        ev.bind(on_active_guide=self._check_is_guide_active)
        ev.bind(on_ui_lang_code=self._translate_ui)

    def activate_guide(self):
        """ Activate guide upon selecting radio checkbox in the corresponding component view. """

        guides.set_active_guide(self.guide_name)
        ev.dispatch('on_active_guide')

    def _check_is_guide_active(self, *args):
        self.is_active_guide = guides.active_guide is not None and self.guide_name == guides.active_guide.guide_name

    def _translate_ui(self, *args):
        self.guide_from_place_label = (transl.translate('From') + ': [b]{}[/b]').format(self.guide_from_place)
        self.guide_to_place_label = (transl.translate('To') + ': [b]{}[/b]').format(self.guide_to_place)


class GuidesMenuScreen(Screen):
    """
     Presents data to the Guides menu screen view in 'guidesmenu_screen.kv'.
    """

    guidesmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(GuidesMenuScreen, self).__init__(**kwargs)
        self.guidesmenu_widget = self.ids.guidesmenu_widget
        ev.bind(on_change_guides_list=self._set_guidesmenu_items)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self._set_guidesmenu_items()

    def on_guidesmenu_items(self, instance, guidesmenu_items):
        """ Updates the object attributes according to `guidesmenu_items` attribute/argument. """

        self.guidesmenu_widget.clear_widgets()
        for item in guidesmenu_items:
            item_widget = GuidesMenuItem(item['guide_name'], item['guide_icon'], item['guide_title'],
                                         item['guide_description'], item['guide_lang'],
                                         item['guide_from_place'], item['guide_to_place'])
            self.guidesmenu_widget.add_widget(item_widget)

    def _set_guidesmenu_items(self, *args):
        self.guidesmenu_items = guides.guides_list

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Guides')
        self.import_button_text = transl.translate('Import guide')


class LoadGuidePopup(Popup):
    """
    Presents data to the guide loading popup component view (in 'guidesmenu_screen.kv') and processes returned
    guide archive name.
    """

    def __init__(self, **kwargs):
        super(LoadGuidePopup, self).__init__(**kwargs)
        self.title = transl.translate('Select guide (zip) archive file')
        self.cancel_button_text = transl.translate('Cancel')
        self.load_button_text = transl.translate('Load')

    @staticmethod
    def load_guide(archive):
        """ Loads guide from selected archive.
            On success returns guide list item (data stored in the corresponding 'guide.json' file);
            otherwise returns None. Opens warning popup when guide import fails. """

        guide_name = os.path.splitext(os.path.basename(archive))[0]
        guides_list_item = guides.load_guide(guide_name)
        if guides_list_item is None:
            GuideLoadFailedWarning(archive).open()
            return
        ev.dispatch('on_load_guide', guides_list_item['guide_name'])

    def _handle_keyboard(self, window, key, *largs):
        super(LoadGuidePopup, self)._handle_keyboard(window, key, *largs)
        if key == 27:
            self.dismiss()
            return True


class GuideLoadFailedWarning(Popup):
    """
    Provides data to the corresponding popup informing about failed guide import (defined in 'guidesmenu_screen.kv')
    and handles Esc/Back button event for the popup dismissal.
    """

    def __init__(self, archive, **kwargs):
        super(GuideLoadFailedWarning, self).__init__(**kwargs)
        self.message = transl.translate('"[b]{}[/b]"\n guide load failed!').format(os.path.basename(archive))
        self.title = transl.translate('Error')
        self.ok_button_text = transl.translate('OK')

    def _handle_keyboard(self, window, key, *largs):
        super(GuideLoadFailedWarning, self)._handle_keyboard(window, key, *largs)
        if key == 27:
            self.dismiss()
            return True


class GuideScreen(Screen):
    """
    Presents data to the Guide screen 'guide_screen.kv' view.
    """

    guide_name = StringProperty('')

    def __init__(self, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        self.guide_lang = ('', '')
        self.guide_from_place = ''
        self.guide_to_place = ''
        self.is_active_guide = False
        ev.bind(on_ui_lang_code=self._translate_ui)
        ev.bind(on_active_guide=self._update_activation_button)

    def on_guide_name(self, instance, guide_name):
        """ Updates object attributes according to `guide_name` attribute/argument. """

        if guide_name:
            guide = guides.guide_by_name(guide_name)
            self.guide_icon = guide.guide_icon
            self.guide_title = guide.guide_title
            self.guide_description = guide.guide_description
            self.guide_lang = guide.guide_lang
            self.guide_from_place = guide.guide_from_place
            self.guide_to_place = guide.guide_to_place
            self._update_activation_button()
        else:
            self.guide_icon = ''
            self.guide_title = ''
            self.guide_description = ''
            self.guide_lang = ('', '')
            self.guide_from_place = ''
            self.guide_to_place = ''
            self.is_active_guide = False
        self._translate_ui()

    def activate_guide(self):
        guides.set_active_guide(self.guide_name)
        ev.dispatch('on_active_guide')

    def _update_activation_button(self, *args):
        self.is_active_guide = guides.active_guide is not None and self.guide_name == guides.active_guide.guide_name

    def _clear_guide_screen_items(self, *args):
        if self.guide_name:
            self.guide_name = ''

    def _translate_ui(self, *args):
        self.screen_title = transl.translate('Guide')
        self.lang_name_label = transl.translate('Language') + ': [b]{}[/b]'.format(self.guide_lang[0])
        self.from_place_label = transl.translate('From') + ': [b]{}[/b]'.format(self.guide_from_place)
        self.to_place_label = transl.translate('To') + ': [b]{}[/b]'.format(self.guide_to_place)
        self.activate_guide_button_text = transl.translate('Activate the guide')
        self.guide_is_active_label_text = transl.translate('The guide is active')
        self.delete_guide_button_text = transl.translate('Delete guide')


class RemoveGuideWarningPopup(Popup):
    """
    Presents data to the popup warning about guide unload (defined in 'guide_screen.kv')
    and process the guide unload upon confirmation action.
    """

    def __init__(self, guide_name, guide_title, **kwargs):
        super(RemoveGuideWarningPopup, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.title = transl.translate('Warning')
        self.message = (transl.translate('Delete guide') + '\n"[b]{}[/b]"?').format(guide_title)
        self.cancel_button_text = transl.translate('Cancel')
        self.delete_button_text = transl.translate('Delete')

    def unload_guide(self):
        """ Unload guide from the application. """

        guides.unload_guide(self.guide_name)
        ev.dispatch('on_unload_guide', self.guide_name)

    def _handle_keyboard(self, window, key, *largs):
        super(RemoveGuideWarningPopup, self)._handle_keyboard(window, key, *largs)
        if key == 27:
            self.dismiss()
            return True
