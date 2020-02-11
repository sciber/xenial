"""
Video connector
===============
Provides single shared instance of VideoConnector class which manages playback of articles video content.
"""

from io import BytesIO

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.video import Video

import media_connectors.audio_connector as audio_connector


class VideoConnector(Video):
    """
    Manages playback of articles video content.
    """

    def __init__(self, **kwargs):
        super(VideoConnector, self).__init__(**kwargs)
        self.eos = False
        self.widget = None
        self.widget_video_container = None
        self.play_timer = None

    def toggle_play(self, widget):
        """ Toggles playback from the widget of a video component view. """

        if self.widget is widget:
            if self.state == 'play':
                self.stop()
            else:
                self._play()
        else:
            if self.widget is not None:
                if self.state == 'play':
                    self.stop()
                self.widget_video_container.remove_widget(self)
                self._store_current_video_frame()
                self.texture = None
                self.source = ''
                self.unload()
            self.widget = widget
            self.widget_video_container = self.widget.ids.video_container
            if self.widget_video_container.children:
                self.texture = self.widget_video_container.children[0].texture
                self.widget_video_container.clear_widgets()
            self.widget_video_container.add_widget(self)
            self.source = self.widget.video_source
            self._play()

    def change_pos(self, widget, slider_value):
        """ Changes playback position when set from the widget of an video component view. """

        video_pos = slider_value / 100 * widget.video_length
        widget.video_pos = video_pos
        widget.slider_value = slider_value
        if self.widget is widget:
            self.seek(slider_value / 100, precise=True)

    def stop(self):
        """ Stops audio playback; is invoked externally when article's screen is left. """

        self.state = 'pause'
        if self.play_timer is not None:
            self.play_timer.cancel()
        if self.widget is not None:
            self.widget.video_state = 'stop'

    def _play(self):
        audio_connector.audio.stop()
        self.state = 'play'
        if self.loaded:
            self.seek(self.widget.video_pos / self.duration, precise=True)
            self.widget.video_state = 'play'
            self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def _on_load(self, *largs):
        super(VideoConnector, self)._on_load(*largs)
        seek_pos = 0 if not self.widget.video_length else self.widget.video_pos / self.widget.video_length
        self.seek(seek_pos, precise=True)
        self.widget.video_state = 'play'
        self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def _update_widget_controls(self, dt):
        self.widget.video_pos = self.position
        pos_percent = 0 if not self.widget.video_length else self.widget.video_pos / self.widget.video_length * 100
        self.widget.slider_value = round(pos_percent)

    def _store_current_video_frame(self):
        data = BytesIO()
        core_image = CoreImage(self.texture)
        core_image.save(data, fmt='png')
        frame_image = Image()
        frame_image.texture = CoreImage(data, ext='png').texture
        self.widget_video_container.add_widget(frame_image)

    def _on_eos(self, *largs):
        super(VideoConnector, self)._on_eos(*largs)
        self.play_timer.cancel()
        self.widget.video_state = 'stop'
        self.widget.video_pos = 0
        self.widget.slider_value = 0
        self.texture = self.widget.video_cover_image.texture


video = VideoConnector()
