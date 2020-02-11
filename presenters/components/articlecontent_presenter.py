"""
Article content presenter
=========================
Contains ArticleContent, ArticleSubtitle, ArticleParagraph, ArticleImage, ArticleAudio and ArticleVideo
classes which presents data to the 'articlecontent.kv' components views.
"""

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from media_connectors.audio_connector import audio
from media_connectors.video_connector import video


class ArticleSubtitle(Label):
    """
    Presents data to the article's subtitle view component.
    :attr `subtitle_text` is the label text.
    """

    def __init__(self, subtitle_text, **kwargs):
        super(ArticleSubtitle, self).__init__(**kwargs)
        self.subtitle_text = subtitle_text


class ArticleParagraph(Label):
    """
    Presents data to the article's paragraph view component.
    :attr `paragraph_text` is the label text.
    """

    def __init__(self, paragraph_text, **kwargs):
        super(ArticleParagraph, self).__init__(**kwargs)
        self.paragraph_text = paragraph_text


class ArticleImage(BoxLayout):
    """
    Presents data to the article's image view component.
    :attr `image_source` is uri of the image source file.
    :attr `image_caption_text` is text of caption assigned to the image.
    """

    def __init__(self, image_source, image_caption_text, **kwargs):
        super(ArticleImage, self).__init__(**kwargs)
        self.image_source = image_source
        self.image_caption_text = image_caption_text


class ArticleAudio(BoxLayout):
    """
    Presents data to the article's audio view component.
    :attr `audio_source` is uri of the audio source file.
    :attr `audio_length` is length of the audio in seconds.
    :attr `audio_caption_text` is text of caption assigned to the audio.
    """

    def __init__(self, audio_source, audio_length, audio_caption_text, **kwargs):
        super(ArticleAudio, self).__init__(**kwargs)
        self.source = audio_source
        self.audio_length = audio_length
        self.audio_caption_text = audio_caption_text
        self.audio_state = 'stop'
        self.audio_pos = 0
        self.slider_value = 0

    def toggle_audio_play(self):
        """ Toggles state of the audio playback. When turning the audio play on, any other media playback is turned off.
            The method is called from the corresponding article audio component view. """

        audio.toggle_play(self)

    def slider_changed(self, slider_value):
        """ Updates audio position upon changed slider position in corresponding audio component view. """

        if self.slider_value != slider_value:
            audio.change_pos(self, slider_value)


class VideoCoverImage(Image):
    """
    Presents uri of video cover image to the corresponding component view.
    """

    def __init__(self, source, **kwargs):
        super(VideoCoverImage, self).__init__(**kwargs)
        self.source = source


class ArticleVideo(BoxLayout):
    """
    Presents data to the article's video component view.
    :attr `video_source` is uri of the video source file.
    :attr `video_length` is length of the video in seconds.
    :attr `video_cover_source` is uri of the video cover image.
    :attr `video_caption_text` is text of caption assigned to the video.
    """

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
        """ Toggles state of the video playback. When turning the video play on, any other media playback is turned off.
            The method is called from the corresponding article video component view. """

        video.toggle_play(self)

    def slider_changed(self, slider_value):
        """ Updates video position upon changed slider position in corresponding video component view. """

        if self.slider_value != slider_value:
            video.change_pos(self, slider_value)


class ArticleContent(BoxLayout):
    """
    Presents data to the Article content 'articlecontent.kv' component view.
    """

    articlecontent_blocks = ListProperty([])

    def on_articlecontent_blocks(self, instance, articlecontent_blocks):
        """ Updates the article's instance content blocks according to `articlecontent_blocks` attribute/argument. """

        self.clear_widgets()
        for content_block in articlecontent_blocks:
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
                item_widget = ArticleVideo(video_source=content_block['video_source'],
                                           video_length=content_block['video_length'],
                                           video_cover_source=content_block['video_cover_source'],
                                           video_caption_text=content_block['video_caption_text'])
            else:
                continue
            self.add_widget(item_widget)
