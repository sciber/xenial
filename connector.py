from io import BytesIO

import kivy

from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.video import Video
from kivy.clock import Clock

kivy.require('1.11.1')


class AudioMeter:
    @staticmethod
    def set_audio_length(audio_widget):
        sound = SoundLoader.load(audio_widget.source)
        audio_widget.audio_length = sound.length
        sound.unload()


class AudioConnector:
    def __init__(self):
        self.sound = None
        self.widget = None
        self.play_timer = None

    def toggle_play(self, widget):
        if self.widget is None or self.widget is not widget:
            self._load(widget)
        if self.sound.state == 'play':
            self.stop()
        else:
            self._play()

    def change_pos(self, widget, slider_value):
        audio_pos = slider_value / 100 * widget.audio_length
        widget.audio_pos = audio_pos
        widget.slider_value = slider_value
        if self.widget is widget:
            self.sound.seek(audio_pos)

    def _update_widget_controls(self, dt):
        if self.sound.state == 'stop':
            self.widget.audio_state = 'stop'
            self.widget.audio_pos = 0
            self.widget.slider_value = 0
            self.play_timer.cancel()
        else:
            self.widget.audio_pos = self.sound.get_pos()
            self.widget.slider_value = round(self.widget.audio_pos / self.widget.audio_length * 100)

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

    def _play(self):
        video.stop()
        self.sound.play()
        self.sound.seek(self.widget.audio_pos)
        self.widget.audio_state = 'play'
        self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def stop(self):
        if self.sound and self.sound.state == 'play':
            self.play_timer.cancel()
            self.sound.stop()
            self.widget.audio_state = 'stop'


class VideoMeter(Video):
    video_widgets = []
    processed_widget_frame_num = 0
    processed_widget = None
    volume = 0

    def set_video_attrs(self, video_widget):
        if self.processed_widget:
            self.video_widgets.append(video_widget)
        else:
            self.processed_widget = video_widget
            self.source = video_widget.source
            self.state = 'play'

    def _on_video_frame(self, *largs):
        super(VideoMeter, self)._on_video_frame(*largs)
        if not self.processed_widget_frame_num:
            self.processed_widget_frame_num = 1
            return
        else:
            self.processed_widget_frame_num = 0
        if self.processed_widget is not None:
            self.processed_widget.video_length = self.duration
            self.processed_widget.video_aspect_ratio = self.texture.size
        self.unload()
        if self.video_widgets:
            self.processed_widget = self.video_widgets.pop(0)
            self.source = self.processed_widget.source
            self.state = 'play'
        else:
            self.processed_widget = None


class VideoConnector(Video):
    def __init__(self, **kwargs):
        super(VideoConnector, self).__init__(**kwargs)
        self.eos = False
        self.widget = None
        self.widget_video_container = None
        self.play_timer = None

    def toggle_play(self, widget):
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
                self.unload()
            self.widget = widget
            self.widget_video_container = self.widget.ids.video_container
            if self.widget_video_container.children:
                self.texture = self.widget_video_container.children[0].texture
                self.widget_video_container.clear_widgets()
            self.widget_video_container.add_widget(self)
            self.source = self.widget.source
            self._play()

    def _play(self):
        audio.stop()
        self.state = 'play'
        if self.loaded:
            self.seek(self.widget.video_pos / self.duration, precise=True)
            self.widget.video_state = 'play'
            self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def _on_load(self, *largs):
        super(VideoConnector, self)._on_load(*largs)
        self.seek(self.widget.video_pos / self.widget.video_length, precise=True)
        self.widget.video_state = 'play'
        self.play_timer = Clock.schedule_interval(self._update_widget_controls, .1)

    def _on_eos(self, *largs):
        super(VideoConnector, self)._on_eos(*largs)
        self.play_timer.cancel()
        self.widget.video_state = 'stop'
        self.widget.video_pos = 0
        self.widget.slider_value = 0

    def stop(self):
        self.state = 'pause'
        if self.play_timer is not None:
            self.play_timer.cancel()
        if self.widget is not None:
            self.widget.video_state = 'stop'

    def change_pos(self, widget, slider_value):
        video_pos = slider_value / 100 * widget.video_length
        widget.video_pos = video_pos
        widget.slider_value = slider_value
        if self.widget is widget:
            self.seek(slider_value / 100, precise=True)

    def _update_widget_controls(self, dt):
        self.widget.video_pos = self.position
        self.widget.slider_value = round(self.widget.video_pos / self.widget.video_length * 100)

    def _store_current_video_frame(self):
        data = BytesIO()
        core_image = CoreImage(self.texture)
        core_image.save(data, fmt='png')
        frame_image = Image()
        frame_image.texture = CoreImage(data, ext='png').texture
        self.widget_video_container.add_widget(frame_image)


audio_meter = AudioMeter()
audio = AudioConnector()

video_meter = VideoMeter()
video = VideoConnector()
