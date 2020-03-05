from ffpyplayer.player import MediaPlayer

from kivy.clock import Clock
from kivy.graphics.texture import Texture

import plugins.audio


class VideoPlayer:
    def __init__(self):
        self._widget = None
        self._player = None
        self._timer = None
        self._frame = None
        self._texture = None
        self._trigger = Clock.create_trigger(self._redraw)

    def toggle_playback(self, widget):
        if self._widget == widget:
            if self._player.get_pause():
                plugins.audio.audio_player.pause_playback()
                self._player.set_pause(False)
                self._widget.video_state = 'play'
                Clock.schedule_once(self._next_frame)
            else:
                self.pause_playback()
        else:
            plugins.audio.audio_player.pause_playback()
            if self._widget is not None:
                self.pause_playback()
            self._widget = widget
            self._widget.video_state = 'play'
            self._texture = None
            self._player = MediaPlayer(filename=self._widget.video_source,
                                       ff_opts={'paused': True, 'ss': self._widget.video_pos})
            Clock.schedule_interval(self._start_playback, .1)

    def _start_playback(self, dt):
        if self._player.get_metadata()['duration'] is None:
            return
        if self._player.get_pause():
            self._player.set_pause(False)
        Clock.schedule_once(self._next_frame, 0)
        return False

    def pause_playback(self):
        if self._timer is not None:
            self._timer.cancel()
        if self._player is not None:
            self._player.set_pause(True)
        self._frame = None
        self._texture = None
        if self._widget is not None:
            self._widget.video_state = 'pause'

    def update_video_pos(self, widget, pts):
        if self._widget == widget and self._player is not None:
            self._player.seek(pts=pts, relative=False, accurate=True)
        widget.video_pos = pts

    def _next_frame(self, dt):
        frame, val = self._player.get_frame()
        if val == 'eof':
            self._player.set_pause(True)
            self._player.seek(pts=0, relative=False, accurate=True)
            self._widget.video_image.texture = self._widget.video_cover_image_texture
            self._widget.video_state = 'pause'
            self._widget.video_pos = 0
        elif val == 'paused':
            return
        elif frame is None:
            Clock.schedule_once(self._next_frame, 1/100)
        else:
            val = val if val else 1/30
            self._frame = frame
            self._trigger()
            Clock.schedule_once(self._next_frame, val)

    def _redraw(self, dt):
        if self._player.get_pause() is None or self._frame is None:
            return
        img, pts = self._frame
        if self._texture is None:
            self._texture = Texture.create(size=img.get_size(), colorfmt='rgb')
            self._texture.flip_vertical()
        self._texture.blit_buffer(img.to_memoryview()[0])
        self._widget.video_image.texture = None
        self._widget.video_image.texture = self._texture
        self._widget.video_pos = pts


video_player = VideoPlayer()
