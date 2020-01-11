from kivy.event import EventDispatcher

from translator import tr

class AppGlobalEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_ui_lang_code')
        self.register_event_type('on_active_guide')
        super(AppGlobalEventDispatcher, self).__init__(**kwargs)

    def on_ui_lang_code(self, *args):
        pass

    def on_active_guide(self, *args):
        pass


ev = AppGlobalEventDispatcher()
