import os

from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from events import ev
from translator import tr
from models import guides

from controllers.components.tagslist_controller import TagsList


class GuidesMenuItem(BoxLayout):
    def __init__(self, guide_name, guide_icon, guide_title, guide_description,
                 guide_lang, guide_from_place, guide_to_place, **kwargs):
        super(GuidesMenuItem, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.guide_icon = guide_icon
        self.guide_title = guide_title
        self.guide_description = guide_description
        self.guide_lang = guide_lang
        self.guide_from_place = guide_from_place
        self.guide_to_place = guide_to_place
        ev.bind(on_ui_lang_code=self.translate_ui)

    def translate_ui(self, *args):
        self.guide_from_place_label = (tr.translate('From') + ': [b]{}[/b]').format(self.guide_from_place)
        self.guide_to_place_label = (tr.translate('To') + ': [b]{}[/b]').format(self.guide_to_place)

    def activate_guide(self):
        guides.set_active_guide(self.guide_name)
        ev.dispatch('on_active_guide')


class GuidesMenuScreen(Screen):
    guidesmenu_items = ListProperty()

    def __init__(self, **kwargs):
        super(GuidesMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.guidesmenu_widget = self.ids.guidesmenu_widget
        ev.bind(on_import_guide=self.set_guidesmenu_items)
        ev.bind(on_remove_guide=self.set_guidesmenu_items)
        self.set_guidesmenu_items()

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Guides')
        self.import_button_text = tr.translate('Import guide')

    def on_guidesmenu_items(self, instance, value):
        self.guidesmenu_widget.clear_widgets()
        for item in self.guidesmenu_items:
            item_widget = GuidesMenuItem(item['guide_name'], item['guide_icon'], item['guide_title'],
                                         item['guide_description'], item['guide_lang'],
                                         item['guide_from_place'], item['guide_to_place'])
            self.guidesmenu_widget.add_widget(item_widget)

    def set_guidesmenu_items(self, *args):
        self.guidesmenu_items = guides.guides_list


class LoadGuidePopup(Popup):
    def __init__(self, **kwargs):
        super(LoadGuidePopup, self).__init__(**kwargs)
        self.title = tr.translate('Select guide (zip) archive file')
        self.cancel_button_text = tr.translate('Cancel')
        self.load_button_text = tr.translate('Load')

    @staticmethod
    def import_guide(archive):
        guides_list_item = guides.import_from_archive(archive)
        if guides_list_item:
            ev.dispatch('on_import_guide')
            if guides_list_item['guide_name'] == guides.active_guide.guide_name:
                ev.dispatch('on_active_guide')
        else:
            GuideLoadFailedWarning(os.path.basename(archive)).open()


class GuideLoadFailedWarning(Popup):
    def __init__(self, archive, **kwargs):
        super(GuideLoadFailedWarning, self).__init__(**kwargs)
        self.message = tr.translate('"[b]{}[/b]"\n guide load failed!').format(os.path.basename(archive))
        self.title = tr.translate('Error')
        self.ok_button_text = tr.translate('OK')


class GuideScreen(Screen):
    guide_name = StringProperty('')

    def __init__(self, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        self.guide_lang = ('', '')
        self.guide_from_place = ''
        self.guide_to_place = ''
        self.tagslist_widget = TagsList()
        self.ids.tagslist_container.add_widget(self.tagslist_widget)
        ev.bind(on_ui_lang_code=self.translate_ui)
        ev.bind(on_remove_guide=self.remove_guide)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Guide')
        self.lang_name_label = tr.translate('Language') + ': [b]{}[/b]'.format(self.guide_lang[0])
        self.from_place_label = tr.translate('From') + ': [b]{}[/b]'.format(self.guide_from_place)
        self.to_place_label = tr.translate('To') + ': [b]{}[/b]'.format(self.guide_to_place)
        self.delete_guide_button_text = tr.translate('Delete guide')

    def clear_guide_screen_items(self, *args):
        if self.guide_name:
            self.guide_name = ''

    def on_guide_name(self, *args):
        if self.guide_name:
            guide = guides.guide_by_name(self.guide_name)
            self.guide_icon = guide.guide_icon
            self.guide_title = guide.guide_title
            self.guide_description = guide.guide_description
            self.guide_lang = guide.guide_lang
            self.guide_from_place = guide.guide_from_place
            self.guide_to_place = guide.guide_to_place
            self.tagslist_widget.tagslist_items = guide.tags_list()
        else:
            self.guide_icon = ''
            self.guide_title = ''
            self.guide_description = ''
            self.guide_lang = ('', '')
            self.guide_from_place = ''
            self.guide_to_place = ''
            self.tagslist_widget.tagslist_items = []
        self.translate_ui()

    def remove_guide(self, instance, guide_name):
        if guide_name != self.guide_name:
            return
        before_active_guide_name = guides.active_guide.guide_name
        guides.remove_guide(self.guide_name)
        if before_active_guide_name != guides.active_guide.guide_name:
            ev.dispatch('on_active_guide')


class UnloadGuideWarningPopup(Popup):
    def __init__(self, guide_name, guide_title, **kwargs):
        super(UnloadGuideWarningPopup, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.title = tr.translate('Warning')
        self.message = (tr.translate('Delete guide') + '\n"[b]{}[/b]"?').format(guide_title)
        self.cancel_button_text = tr.translate('Cancel')
