import os

from io import BytesIO

from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.video import Video
from kivy.clock import Clock


class AudioMeter:
    @staticmethod
    def get_audio_length(audio_source):
        sound = SoundLoader.load(audio_source)
        audio_length = sound.length
        sound.unload()
        return audio_length


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
    video_sources = []
    video_metrics = {}
    dbname = ''
    current_processed_video_source = ''
    frame_count = 0
    callback = None
    volume = 0

    def get_videos_lengths_and_covers(self, video_sources, callback, dbname):
        self.video_sources = video_sources
        self.callback = callback
        self.dbname = dbname
        self.video_metrics = {}
        if self.video_sources:
            self.current_processed_video_source = self.video_sources.pop()
            self._start_video_processing(self.current_processed_video_source)

    def _start_video_processing(self, source):
        self.source = source
        self.state = 'play'

    def _on_video_frame(self, *largs):
        super(VideoMeter, self)._on_video_frame(*largs)
        if self.current_processed_video_source == self.source:
            if self.frame_count == 5:
                video_cover_source = os.path.splitext(self.current_processed_video_source)[0] + '.png'
                im = CoreImage(self.texture)
                im.save(video_cover_source)
                self.video_metrics[self.current_processed_video_source] = {
                    'video_length': self.duration,
                    'video_cover_source': video_cover_source
                }
                self.state = 'stop'
                self.unload()
                if self.video_sources:
                    self.current_processed_video_source = self.video_sources.pop()
                    self._start_video_processing(self.current_processed_video_source)
                    self.frame_count = 0
                else:
                    self.callback(self.video_metrics, self.dbname)
            else:
                self.frame_count += 1


class VideoConnector(Video):
    def __init__(self, **kwargs):
        super(VideoConnector, self).__init__(**kwargs)
        self.eos = False
        self.widget = None
        self.widget_video_container = None
        self.play_timer = None

    def toggle_play(self, widget):
        print('toggle_play - self.widget:', self.widget, '; widget:', widget)
        if self.widget is widget:
            print('self.widget is widget')
            if self.state == 'play':
                self.stop()
            else:
                self._play()
        else:
            print('self.widget is NOT widget')
            if self.widget is not None:
                print('self.widget is not None')
                if self.state == 'play':
                    print("self.state == 'play'")
                    self.stop()
                self.widget_video_container.remove_widget(self)
                self._store_current_video_frame()
                self.texture = None
                self.unload()
            self.widget = widget
            self.widget_video_container = self.widget.ids.video_container
            if self.widget_video_container.children:
                print(self.widget_video_container.children)
                self.texture = self.widget_video_container.children[0].texture
                self.widget_video_container.clear_widgets()
            self.widget_video_container.add_widget(self)
            self.source = self.widget.video_source
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
        self.texture = self.widget.video_cover_image.texture

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
