"""
Global events
=============
Contains GlobalEventBus class which registers and routes application global events.
"""

from kivy.event import EventDispatcher


class GlobalEventBus(EventDispatcher):
    """
    Registers and routes application global events.
    'on_ui_lang_code' event should be dispatched when UI language is changed in 'translations.translator' module;
    'on_active_guide' event should be dispatched when `active_guide` is changed in 'guides_model' module;
    'on_load_guide' and 'on_unload_guide' events should be dispatched upon loading and unloading of guide
        in 'guides_model' module;
    'on_change_guides_list' event is dispatched from 'history' module upon module load or unload;
    'on_add_bookmark' and 'on_remove_bookmark' should be fired when article's bookmark is added or removed via
        'article_model'.
    """

    def __init__(self, **kwargs):
        self.register_event_type('on_ui_lang_code')
        self.register_event_type('on_active_guide')
        self.register_event_type('on_load_guide')
        self.register_event_type('on_unload_guide')
        self.register_event_type('on_change_guides_list')
        self.register_event_type('on_add_bookmark')
        self.register_event_type('on_remove_bookmark')
        super(GlobalEventBus, self).__init__(**kwargs)

    def on_ui_lang_code(self, *args):
        pass

    def on_active_guide(self, *args):
        pass

    def on_load_guide(self, *args):
        pass

    def on_change_guides_list(self, *args):
        pass

    def on_unload_guide(self, *args):
        pass

    def on_add_bookmark(self, *args):
        pass

    def on_remove_bookmark(self, *args):
        pass


ev = GlobalEventBus()
