import os

import kivy

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models import guides

from connector import audio_meter, audio, video_meter, video

kivy.require('1.11.1')


class ArticleSubtitle(Label):
    pass


class ArticleParagraph(Label):
    pass


class ArticleImage(BoxLayout):
    def __init__(self, source, caption, **kwargs):
        super(ArticleImage, self).__init__(**kwargs)
        self.source = os.path.join(guides.active_guide_path, 'content', 'media', 'image', source)
        self.caption = caption


class ArticleAudio(BoxLayout):
    def __init__(self, source, caption, **kwargs):
        super(ArticleAudio, self).__init__(**kwargs)
        self.source = os.path.join(guides.active_guide_path, 'content', 'media', 'audio', source)
        self.caption = caption
        self.audio_state = 'stop'
        self.audio_pos = 0
        self.audio_length = 0
        self.slider_value = 0
        audio_meter.set_audio_length(self)

    def toggle_audio_play(self):
        audio.toggle_play(self)

    def slider_changed(self, slider_value):
        if self.slider_value != slider_value:
            audio.change_pos(self, slider_value)


class ArticleVideo(BoxLayout):
    def __init__(self, source, caption, **kwargs):
        super(ArticleVideo, self).__init__(**kwargs)
        self.source = os.path.join(guides.active_guide_path, 'content', 'media', 'video', source)
        self.caption = caption
        self.video_state = 'stop'
        self.video_pos = 0
        self.video_length = 0
        self.slider_value = 0
        self.video_aspect_ratio = (16, 1)
        self.video_track_timer = None
        video_meter.set_video_attrs(self)

    def toggle_video_play(self):
        video.toggle_play(self)

    def slider_changed(self, slider_value):
        if self.slider_value != slider_value:
            video.change_pos(self, slider_value)


class ArticleContent(BoxLayout):
    content_items = ListProperty([])

    def on_content_items(self, instance, value):
        self.clear_widgets()
        for content_item in self.content_items:
            if content_item['type'] == 'subtitle':
                item_widget = ArticleSubtitle(text=content_item['text'])
            elif content_item['type'] == 'paragraph':
                item_widget = ArticleParagraph(text=content_item['text'])
            elif content_item['type'] == 'image':
                item_widget = ArticleImage(source=content_item['source'],
                                           caption=content_item['caption'])
            elif content_item['type'] == 'audio':
                item_widget = ArticleAudio(source=content_item['source'],
                                           caption=content_item['caption'])
            elif content_item['type'] == 'video':
                item_widget = ArticleVideo(source=content_item['source'],
                                           caption=content_item['caption'])
            else:
                continue
            self.add_widget(item_widget)
