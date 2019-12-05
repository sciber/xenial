import os

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader

from kivy.garden.navigationdrawer import NavigationDrawer

from models import guides, articles, bookmarks

from controllers.guide_controller import GuidesMenuScreen, GuideScreen, GuideLoadFailedWarning
from controllers.tag_controller import TagsMenuScreen, TagScreen
from controllers.category_controller import CategoriesMenuScreen, CategoryScreen
from controllers.article_controller import ArticlesMenuScreen
from controllers.bookmark_controller import BookmarksMenuScreen
from controllers.search_controller import SearchScreen
from controllers.settings_controller import SettingsScreen

kivy.require('1.11.1')

Config.set('kivy', 'default_font',
           '''["Noto Sans", 
               "assets/fonts/NotoSans-Regular.ttf",
               "assets/fonts/NotoSans-Italic.ttf",
               "assets/fonts/NotoSans-Bold.ttf",
               "assets/fonts/NotoSans-BoldItalic.ttf"
              ]''')

# Views components
Builder.load_file('views/components/navigationpanel.kv')
Builder.load_file('views/components/screentitlebar.kv')
Builder.load_file('views/components/tagslist.kv')
Builder.load_file('views/components/categoriesmenu.kv')
Builder.load_file('views/components/articlesmenu.kv')

# Screens views
Builder.load_file('views/screens/guidesmenu_screen.kv')
Builder.load_file('views/screens/guide_screen.kv')
Builder.load_file('views/screens/tagsmenu_screen.kv')
Builder.load_file('views/screens/tag_screen.kv')
Builder.load_file('views/screens/articlesmenu_screen.kv')
Builder.load_file('views/screens/categoriesmenu_screen.kv')
Builder.load_file('views/screens/category_screen.kv')
Builder.load_file('views/screens/bookmarksmenu_screen.kv')

Builder.load_file('views/screens/article_screen.kv')
Builder.load_file('views/screens/search_screen.kv')
Builder.load_file('views/screens/settings_screen.kv')

# Application root view
Builder.load_string('''
<ApplicationRoot>:
    anim_type: 'slide_above_simple'
    NavigationPanel:
        is_active_guide: root.is_active_guide
    ScreenManager:
        id: manager
''')


class ArticleAssignedTag(Button):
    pass


class ArticleAssignedTagsList(StackLayout):
    def __init__(self, tags, **kwargs):
        super(ArticleAssignedTagsList, self).__init__(**kwargs)
        for tag in tags:
            tag_button = ArticleAssignedTag(text=tag)
            self.add_widget(tag_button)


class ArticleSubtitle(Label):
    pass


class ArticleParagraph(Label):
    pass


class ArticleImage(BoxLayout):
    def __init__(self, image, caption, **kwargs):
        super(ArticleImage, self).__init__(**kwargs)
        self.image = image
        self.caption = caption


class ArticleAudio(BoxLayout):
    slider_value = NumericProperty()
    manual_sound_stop = False

    def _update_sound_track_pos(self, dt):
        self.sound_track_pos = self.sound.get_pos()
        self.slider_value = round(self.sound_track_pos / self.sound.length * 100)

    def _on_sound_stop(self):
        self.sound_track_timer.cancel()
        if not self.manual_sound_stop:
            self.sound_track_pos = 0
            self.slider_value = 0
            self.ids.toggle_button.state = 'normal'
        self.manual_sound_stop = False

    def __init__(self, audio_source, caption, **kwargs):
        super(ArticleAudio, self).__init__(**kwargs)
        self.audio_source = audio_source
        self.caption = caption

        self.sound = SoundLoader.load(audio_source)
        self.sound.on_stop = self._on_sound_stop

        self.sound_track_length = self.sound.length
        self.sound_track_timer = None
        self.sound_track_pos = 0

    def toggle_audio_play(self, state):
        if state == 'down':
            if self.sound is not None and self.sound.state == 'play':
                return

            if self.sound is not None and self.sound.state == 'stop':
                self.sound.play()
                self.sound_track_timer = Clock.schedule_interval(self._update_sound_track_pos, .1)
                self.sound.seek(self.sound_track_pos)

            if self.sound is None:
                self.sound.play()
                self.sound_track_timer = Clock.schedule_interval(self._update_sound_track_pos, .1)
        else:
            if self.sound is None or self.sound.state == 'stop':
                return
            self.manual_sound_stop = True
            self.sound.stop()

    def on_slider_value_change(self, slider_value):
        if self.slider_value != slider_value:
            self.slider_value = slider_value
            self.sound_track_pos = (slider_value / 100) * self.sound.length
            if self.sound.state == 'play':
                self.sound.seek(self.sound_track_pos)


class ArticleVideo(BoxLayout):
    video_player = ObjectProperty()
    slider_value = NumericProperty()

    def _on_position_change(self, instance, value):
        self.slider_value = round(value / self.video_player.duration * 100)

    def _on_duration_change(self, instance, value):
        self.video_track_length = value

    def _on_state_change(self, instance, value):
        if value == 'stop':
            self.video_player.position = 0
            self.video_track_pos = 0
            self.slider_value = 0
            instance.state = 'pause'
            self.ids.toggle_button.state = 'normal'

    def __init__(self, video_source, cover_image_source, caption, **kwargs):
        super(ArticleVideo, self).__init__(**kwargs)
        self.video_source = video_source
        self.cover_image_source = cover_image_source
        self.caption = caption
        self.video_player.source = video_source
        self.video_player.bind(position=self._on_position_change,
                               duration=self._on_duration_change,
                               state=self._on_state_change)
        self.video_track_timer = None
        self.video_track_length = 0

    def toggle_video_play(self, state):
        if state == 'down':
            self.video_player.state = 'play'
        else:
            self.video_player.state = 'pause'

    def _on_unloaded_video_slider_value_change(self, dt):
        self.video_player.state = 'pause'

    def on_slider_value_change(self, slider_value):
        if not self.video_player.loaded:
            self.video_player.state = 'play'
            Clock.schedule_once(self._on_unloaded_video_slider_value_change)

        if self.slider_value != slider_value:
            self.video_player.seek(slider_value / 100, True)
            self.slider_value = self.video_player.position / self.video_track_length * 100


class ArticleContent(BoxLayout):
    items_container: ObjectProperty()

    def __init__(self, content, **kwargs):
        super(ArticleContent, self).__init__(**kwargs)
        self.items_container = self

        for content_item in content:

            if content_item['type'] == 'subtitle':
                item_widget = ArticleSubtitle(text=content_item['text'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'paragraph':
                item_widget = ArticleParagraph(text=content_item['text'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'image':
                image = os.path.join(guides.active_guide_path, 'content', 'media', 'image', content_item['source'])
                item_widget = ArticleImage(image=image,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'audio':
                audio_source = os.path.join(guides.active_guide_path,
                                            'content', 'media', 'audio',
                                            content_item['source'])
                item_widget = ArticleAudio(audio_source=audio_source,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'video':
                video_source = os.path.join(guides.active_guide_path,
                                            'content', 'media', 'video',
                                            content_item['source'])
                cover_image_source = os.path.join(guides.active_guide_path,
                                                  'content', 'media', 'video',
                                                  content_item['screenshot'])
                item_widget = ArticleVideo(video_source=video_source,
                                           cover_image_source=cover_image_source,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue


class ArticleRelatedArticlesMenuItem(Button):
    def __init__(self, icon, name, title, synopsis, **kwargs):
        super(ArticleRelatedArticlesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name
        self.title = title
        self.synopsis = synopsis


class ArticleRelatedArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(ArticleRelatedArticlesMenu, self).__init__(**kwargs)
        for article in articles:
            icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
            menu_item = ArticleRelatedArticlesMenuItem(icon=icon,
                                                       name=article['name'],
                                                       title=article['title'],
                                                       synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class ArticleRelatedCategoriesMenuItem(Button):
    def __init__(self, icon, name, **kwargs):
        super(ArticleRelatedCategoriesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name


class ArticleRelatedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(ArticleRelatedCategoriesMenu, self).__init__(**kwargs)
        for category in categories:
            icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
            menu_item = ArticleRelatedCategoriesMenuItem(icon=icon,
                                                         name=category['name'])
            self.items_container.add_widget(menu_item)


class ArticleScreen(Screen):
    def __init__(self, article_name, **kwargs):
        super(ArticleScreen, self).__init__(**kwargs)
        article = articles.by_name(article_name)
        self.article_name = article_name
        self.article_icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
        self.article_title = article['title']
        self.article_assigned_tags = article['tags']
        self.article_content = article['content']
        self.is_bookmarked = bookmarks.is_article_bookmarked(article_name)
        self.article_related_categories = articles.related_categories(article_name)
        self.article_related_articles = articles.related_articles(article_name)

        article_container = self.ids.container
        article_assigned_tags_list = ArticleAssignedTagsList(tags=self.article_assigned_tags)
        article_container.add_widget(article_assigned_tags_list)

        article_content_wrapper = ArticleContent(content=self.article_content)
        article_container.add_widget(article_content_wrapper)

        if len(self.article_related_articles) > 0:
            article_related_articles_menu = ArticleRelatedArticlesMenu(articles=self.article_related_articles)
            article_container.add_widget(article_related_articles_menu)

        article_related_categories_menu = ArticleRelatedCategoriesMenu(categories=self.article_related_categories)
        article_container.add_widget(article_related_categories_menu)

    def toggle_bookmark(self):
        if self.is_bookmarked:
            bookmarks.remove(self.article_name)
        else:
            bookmarks.add(self.article_name)
        self.is_bookmarked = not self.is_bookmarked


class ApplicationRoot(NavigationDrawer):
    is_active_guide = BooleanProperty()

    def __init__(self, **kwargs):
        super(ApplicationRoot, self).__init__(**kwargs)
        self.sm = self.ids.manager

        self.categoriesmenu_screen = CategoriesMenuScreen()
        self.sm.add_widget(self.categoriesmenu_screen)

        self.category_screen = CategoryScreen()
        self.sm.add_widget(self.category_screen)

        self.guidesmenu_screen = GuidesMenuScreen()
        self.sm.add_widget(self.guidesmenu_screen)

        self.guide_screen = GuideScreen()
        self.sm.add_widget(self.guide_screen)

        self.tagsmenu_screen = TagsMenuScreen()
        self.sm.add_widget(self.tagsmenu_screen)

        self.tag_screen = TagScreen()
        self.sm.add_widget(self.tag_screen)

        self.articlesmenu_screen = ArticlesMenuScreen()
        self.sm.add_widget(self.articlesmenu_screen)

        self.bookmarksmenu_screen = BookmarksMenuScreen()
        self.sm.add_widget(self.bookmarksmenu_screen)

        self.search_screen = SearchScreen()
        self.sm.add_widget(self.search_screen)

        self.settings_screen = SettingsScreen()
        self.sm.add_widget(self.settings_screen)

        if guides.active_guide_name:
            self.show_categoriesmenu_screen()
        else:
            self.show_guidesmenu_screen()

        self.is_active_guide = bool(guides.active_guide_name)

    def show_guidesmenu_screen(self):
        self.sm.current = 'guidesmenu'

    def load_guide(self, guide_archive_paths):
        if guides.load(guide_archive_paths[0]):
            self.guidesmenu_screen.update_guidesmenu_items()
        else:
            guide_archive_name = os.path.basename(guide_archive_paths[0])
            GuideLoadFailedWarning('"[b]{}[/b]"\n guide load failed!'.format(guide_archive_name)).open()
        self.is_active_guide = bool(guides.active_guide_name)

    def show_guide_screen(self, guide_name):
        if self.guide_screen.guide_name != guide_name:
            prev_guide_screen = self.guide_screen
            prev_guide_screen.name = 'prev_guide'
            new_guide_screen = GuideScreen(name='guide')
            new_guide_screen.update_guide_screen_items(guide_name)
            self.sm.add_widget(new_guide_screen)
            self.guide_screen = new_guide_screen
            self.sm.remove_widget(prev_guide_screen)
        self.sm.current = 'guide'

    def unload_guide(self, guide_name):
        guides.unload(guide_name)
        self.guidesmenu_screen.update_guidesmenu_items()
        self.show_guidesmenu_screen()
        self.is_active_guide = bool(guides.active_guide_name)

    def show_tagsmenu_screen(self):
        if guides.active_guide_name and self.tagsmenu_screen.from_guide_name != guides.active_guide_name:
            self.tagsmenu_screen.update_tagsmenu_items()
            self.tagsmenu_screen.tagsmenu_widget.parent.scroll_y = 1
        self.sm.current = 'tagsmenu'

    def show_tag_screen(self, tag_name):
        if self.tag_screen.from_guide_name != guides.active_guide_name or self.tag_screen.tag_name != tag_name:
            prev_tag_screen = self.tag_screen
            prev_tag_screen.name = 'prev_tag'
            new_tag_screen = TagScreen(name='tag')
            new_tag_screen.update_tag_screen_items(tag_name)
            self.sm.add_widget(new_tag_screen)
            self.tag_screen = new_tag_screen
            self.sm.remove_widget(prev_tag_screen)
        self.sm.current = 'tag'

    def show_categoriesmenu_screen(self):
        if guides.active_guide_name and self.categoriesmenu_screen.from_guide_name != guides.active_guide_name:
            self.categoriesmenu_screen.update_categoriesmenu_items()
            self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
        self.sm.current = 'categoriesmenu'

    def show_category_screen(self, category_name):
        print(category_name)
        if (self.category_screen.from_guide_name != guides.active_guide_name
                or self.category_screen.category_name != category_name):
            print('is either not from this guide or it si new category')
            prev_category_screen = self.category_screen
            prev_category_screen.name = 'prev_category'
            new_category_screen = CategoryScreen(name='category')
            new_category_screen.update_category_screen_items(category_name)
            self.sm.add_widget(new_category_screen)
            self.category_screen = new_category_screen
            self.sm.remove_widget(prev_category_screen)
        self.sm.current = 'category'

    def show_articlesmenu_screen(self):
        if guides.active_guide_name and self.articlesmenu_screen.from_guide_name != guides.active_guide_name:
            self.articlesmenu_screen.update_articlesmenu_items()
            self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
        self.sm.current = 'articlesmenu'

    def show_bookmarksmenu_screen(self):
        if guides.active_guide_name and self.bookmarksmenu_screen.from_guide_name != guides.active_guide_name:
            self.bookmarksmenu_screen.update_bookmarksmenu_items()
            self.bookmarksmenu_screen.ids.bookmarksmenu_widget.parent.scroll_y = 1
        self.sm.current = 'bookmarksmenu'

    def add_bookmark(self, article_name):
        bookmarks.add(article_name)
        self.bookmarksmenu_screen.updatebookmarks_menu_items()

    def remove_bookmark(self, article_name):
        bookmarks.remove(article_name)
        self.bookmarksmenu_screen.update_bookmarksmenu_items()

    def show_search_screen(self):
        self.sm.current = 'search'

    def show_settings_screen(self):
        self.sm.current = 'settings'

########################################

    def show_article_screen(self, article_name):
        screen_manager = self.ids.manager
        screen_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Article: ' + str(article_name)
        if screen_name not in screen_names:
            article_screen = ArticleScreen(name=screen_name,
                                           article_name=article_name)
            screen_manager.add_widget(article_screen)

        screen_manager.current = screen_name

    def bookmark_article(self, article_name):
        if not bookmarks.is_article_bookmarked(article_name):
            bookmarks.add(article_name)
            self.bookmarks_screen.update_bookmarks_menu_items()

    def unbookmark_article(self, article_name):
        pass


class XenialApp(App):
    GUIDES_DIR = guides.GUIDES_DIR

    def build(self):
        self.root = ApplicationRoot()
        return self.root

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
