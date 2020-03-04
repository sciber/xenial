from ffpyplayer.player import MediaPlayer

from kivy.clock import Clock

import plugins.video


class AudioPlayer:
    def __init__(self):
        self._widget = None
        self._player = None
        self._timer = None

    def toggle_playback(self, widget):
        if self._widget == widget:
            if self._player.get_pause():
                plugins.video.video_player.pause_playback()
                self._player.set_pause(False)
                self._widget.audio_state = 'play'
                self._timer = Clock.schedule_interval(self._playback_update, .1)
            else:
                self.pause_playback()
        else:
            plugins.video.video_player.pause_playback()
            if self._widget is not None:
                self.pause_playback()
            self._widget = widget
            self._widget.audio_state = 'play'
            self._player = MediaPlayer(filename=self._widget.audio_source,
                                       ff_opts={'paused': True, 'ss': self._widget.audio_pos})
            Clock.schedule_interval(self._start_playback, .1)

    def _start_playback(self, dt):
        if self._player.get_metadata()['duration'] is not None:
            self._player.set_pause(False)
            self._timer = Clock.schedule_interval(self._playback_update, .1)
            return False

    def pause_playback(self):
        if self._timer is not None:
            self._timer.cancel()
        if self._player is not None and not self._player.get_pause():
            self._player.set_pause(True)
        if self._widget is not None:
            self._widget.audio_state = 'pause'

    def _playback_update(self, dt):
        pts = self._player.get_pts()
        if pts >= self._widget.audio_length:
            self._player.set_pause(True)
            self._player.seek(pts=0, relative=False, accurate=True)
            self._widget.audio_state = 'pause'
            self._widget.audio_pos = 0
            return False
        self._widget.audio_pos = pts

    def update_audio_pos(self, widget, pts):
        if self._widget == widget and self._player is not None:
            self._player.seek(pts=pts, relative=False, accurate=True)
        widget.audio_pos = pts


audio_player = AudioPlayer()
