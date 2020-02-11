from kivy.event import EventDispatcher


class AppGlobalEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_ui_lang_code')
        self.register_event_type('on_active_guide')
        self.register_event_type('on_load_guide')
        self.register_event_type('on_change_guides_list')
        self.register_event_type('on_unload_guide')
        self.register_event_type('on_add_bookmark')
        self.register_event_type('on_remove_bookmark')
        super(AppGlobalEventDispatcher, self).__init__(**kwargs)

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


ev = AppGlobalEventDispatcher()
