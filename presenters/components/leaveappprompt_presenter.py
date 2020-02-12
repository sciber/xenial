"""
Leave app prompt
================
Contains LeaveAppPromt class which presents data to the 'leaveappprompt.kv' component view.
"""

from kivy.uix.popup import Popup

from events.global_events import ev
from translations.translator import transl


class LeaveAppPrompt(Popup):
    """
    Presents data to the 'leaveappprompt.kv' component view.
    """

    def __init__(self, **kwargs):
        super(LeaveAppPrompt, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self._translate_ui()

    def _translate_ui(self, *args):
        self.title = transl.translate('Warning')
        self.prompt_text = transl.translate('Do you want to leave the app?')
        self.cancel_button_text = transl.translate('Cancel')
        self.quit_button_text = transl.translate('Quit')

    def _handle_keyboard(self, window, key, *largs):
        super(LeaveAppPrompt, self)._handle_keyboard(window, key, *largs)
        if key == 27:
            self.dismiss()
            return True
