import os

import kivy

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from connector import audio, video

kivy.require('1.11.1')


class ArticleSubtitle(Label):
    def __init__(self, subtitle_text, **kwargs):
        super(ArticleSubtitle, self).__init__(**kwargs)
        self.subtitle_text = subtitle_text


class ArticleParagraph(Label):
    def __init__(self, paragraph_text, **kwargs):
        super(ArticleParagraph, self).__init__(**kwargs)
        self.paragraph_text = paragraph_text


class ArticleImage(BoxLayout):
    def __init__(self, image_source, image_caption_text, **kwargs):
        super(ArticleImage, self).__init__(**kwargs)
        self.image_source = image_source
        self.image_caption_text = image_caption_text


class ArticleAudio(BoxLayout):
    def __init__(self, audio_source, audio_length, audio_caption_text, **kwargs):
        super(ArticleAudio, self).__init__(**kwargs)
        self.source = audio_source
        self.audio_length = audio_length
        self.audio_caption_text = audio_caption_text
        self.audio_state = 'stop'
        self.audio_pos = 0
        self.slider_value = 0

    def toggle_audio_play(self):
        audio.toggle_play(self)

    def slider_changed(self, slider_value):
        if self.slider_value != slider_value:
            audio.change_pos(self, slider_value)


class VideoCoverImage(Image):
    def __init__(self, source, **kwargs):
        super(VideoCoverImage, self).__init__(**kwargs)
        self.source = source


class ArticleVideo(BoxLayout):
    def __init__(self, video_source, video_length, video_cover_source, video_caption_text, **kwargs):
        super(ArticleVideo, self).__init__(**kwargs)
        self.video_source = video_source
        self.video_length = video_length
        self.video_cover_source = video_cover_source
        self.video_cover_image = VideoCoverImage(video_cover_source)
        self.ids.video_container.add_widget(self.video_cover_image)
        self.video_caption_text = video_caption_text
        self.video_state = 'stop'
        self.video_pos = 0
        self.slider_value = 0
        self.video_track_timer = None

    def toggle_video_play(self):
        video.toggle_play(self)

    def slider_changed(self, slider_value):
        if self.slider_value != slider_value:
            video.change_pos(self, slider_value)


class ArticleContent(BoxLayout):
    articlecontent_blocks = ListProperty([])

    def on_articlecontent_blocks(self, *args):
        self.clear_widgets()
        for content_block in self.articlecontent_blocks:
            if content_block['block_type'] == 'subtitle':
                item_widget = ArticleSubtitle(subtitle_text=content_block['subtitle_text'])
            elif content_block['block_type'] == 'paragraph':
                item_widget = ArticleParagraph(paragraph_text=content_block['paragraph_text'])
            elif content_block['block_type'] == 'image':
                item_widget = ArticleImage(image_source=content_block['image_source'],
                                           image_caption_text=content_block['image_caption_text'])
            elif content_block['block_type'] == 'audio':
                item_widget = ArticleAudio(audio_source=content_block['audio_source'],
                                           audio_length=content_block['audio_length'],
                                           audio_caption_text=content_block['audio_caption_text'])
            elif content_block['block_type'] == 'video':
                print(content_block)
                item_widget = ArticleVideo(video_source=content_block['video_source'],
                                           video_length=content_block['video_length'],
                                           video_cover_source=content_block['video_cover_source'],
                                           video_caption_text=content_block['video_caption_text'])
            else:
                continue
            self.add_widget(item_widget)
