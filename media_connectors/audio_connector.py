"""
Audio connector
===============
Provides single shared instance of AudioConnector class which manages playback of articles audio content.
"""

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import media_connectors.video_connector as video_connector


class AudioConnector:
    """
    Manages playback of articles audio content.
    """

    def __init__(self):
        self.sound = None
        self.widget = None
        self.play_timer = None

    def toggle_play(self, widget):
        """ Toggles playback from the widget of an audio component view. """

        if self.widget is None or self.widget is not widget:
            self._load(widget)
        if self.sound.state == 'play':
            self.stop()
        else:
            self._play()

    def change_pos(self, widget, slider_value):
        """ Changes playback position when set from the widget of an audio component view. """

        audio_pos = slider_value / 100 * widget.audio_length
        widget.audio_pos = audio_pos
        widget.slider_value = slider_value
        if self.widget is widget:
            self.sound.seek(audio_pos)

    def stop(self):
        """ Stops audio playback; is invoked externally when article's screen is left. """

        if self.sound and self.sound.state == 'play':
            self.play_timer.cancel()
            self.sound.stop()
            self.widget.audio_state = 'stop'

    def _play(self):
        video_connector.video.stop()
        self.sound.play()
        self.sound.seek(self.widget.audio_pos)
        self.widget.audio_state = 'play'
        self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def _load(self, widget):
        if self.widget is not None:
            if self.widget.audio_state == 'play':
                self.play_timer.cancel()
                self.widget.audio_state = 'stop'
            self.sound.unload()
        self.widget = widget
        self.sound = SoundLoader.load(self.widget.source)
        self.widget.audio_length = self.sound.length
        self.sound.seek(self.widget.audio_pos)

    def _update_widget_controls(self, dt):
        if self.sound.state == 'stop':
            self.widget.audio_state = 'stop'
            self.widget.audio_pos = 0
            self.widget.slider_value = 0
            self.play_timer.cancel()
        else:
            self.widget.audio_pos = self.sound.get_pos()
            pos_percent = 0 if not self.widget.audio_length else self.widget.audio_pos / self.widget.audio_length * 100
            self.widget.slider_value = round(pos_percent)


audio = AudioConnector()
