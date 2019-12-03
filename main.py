import os

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader

from kivy.garden.navigationdrawer import NavigationDrawer

from models import guides, tags, categories, articles, bookmarks

from controllers.guide_controller import GuidesMenuScreen, GuideScreen, GuideLoadFailedWarning
from controllers.tag_controller import TagsMenuScreen
from controllers.category_controller import CategoriesMenuScreen
from controllers.article_controller import ArticlesMenuScreen

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
Builder.load_file('views/components/articlesmenu.kv')
Builder.load_file('views/components/categoriesmenu.kv')

# Screens views
Builder.load_file('views/screens/guidesmenu_screen.kv')
Builder.load_file('views/screens/guide_screen.kv')
Builder.load_file('views/screens/tagsmenu_screen.kv')
Builder.load_file('views/screens/articlesmenu_screen.kv')
Builder.load_file('views/screens/categoriesmenu_screen.kv')
Builder.load_file('views/screens/bookmarksmenu_screen.kv')

Builder.load_file('views/screens/tag_screen.kv')
Builder.load_file('views/screens/category_screen.kv')
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


# class ArticlesScreen(Screen):
#     from_guide_name = ''
#     articles_menu_items = ListProperty()
#
#     def update_articles_menu_items(self):
#         self.from_guide_name = guides.active_guide_name
#         item_keys = ('icon', 'name', 'title', 'synopsis')
#         self.articles_menu_items = [
#             {('article_' + key): item[key] for key in item_keys} for item in articles.all()
#         ]


class BookmarksScreen(Screen):
    from_guide_name = ''
    bookmarks_menu_items = ListProperty()
    is_model_modified = False

    def update_bookmarks_menu_items(self):
        self.from_guide_name = guides.active_guide_name
        item_keys = ('icon', 'name', 'title', 'synopsis')
        self.bookmarks_menu_items = [
            {('article_' + key): item[key] for key in item_keys} for item in bookmarks.bookmarked_articles()
        ]


class SearchScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


#################################################################################

class CategoryAssignedTag(Button):
    pass


class CategoryAssignedTagsList(StackLayout):
    def __init__(self, tags, **kwargs):
        super(CategoryAssignedTagsList, self).__init__(**kwargs)
        for tag in tags:
            tag_button = CategoryAssignedTag(text=tag)
            self.add_widget(tag_button)


class CategoryRelatedCategoriesMenuItem(Button):
    def __init__(self, icon, name, **kwargs):
        super(CategoryRelatedCategoriesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name


class CategoryRelatedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(CategoryRelatedCategoriesMenu, self).__init__(**kwargs)

        for category in categories:
            icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
            menu_item = CategoryRelatedCategoriesMenuItem(icon=icon,
                                                          name=category['name'])
            self.items_container.add_widget(menu_item)


class CategoryArticlesMenuItem(Button):
    def __init__(self, icon, title, synopsis, **kwargs):
        super(CategoryArticlesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.title = title
        self.synopsis = synopsis


class CategoryArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(CategoryArticlesMenu, self).__init__(**kwargs)
        self.items_container = self
        for article in articles:
            icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
            menu_item = CategoryArticlesMenuItem(icon=icon,
                                                 title=article['title'],
                                                 synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class CategoryScreen(Screen):
    def __init__(self, category_name, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        category = categories.by_name(category_name)
        self.category_icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
        self.category_name = category_name
        self.category_assigned_tags = category['tags']
        self.category_related_categories = categories.related_categories(category_name)
        self.category_articles = categories.related_articles(category_name)
        category_container = self.ids.container
        category_assigned_tags_list = CategoryAssignedTagsList(tags=self.category_assigned_tags)
        category_container.add_widget(category_assigned_tags_list)
        if len(self.category_related_categories) > 0:
            category_related_categories_menu = CategoryRelatedCategoriesMenu(categories=self.category_related_categories)
            category_container.add_widget(category_related_categories_menu)
        if len(self.category_articles) > 0:
            category_articles_menu = CategoryArticlesMenu(articles=self.category_articles)
            category_container.add_widget(category_articles_menu)


class TaggedCategoriesMenuItem(Button):
    def __init__(self, icon, name, **kwargs):
        super(TaggedCategoriesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name


class TaggedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(TaggedCategoriesMenu, self).__init__(**kwargs)
        for category in categories:
            icon = os.path.join(guides.active_guide_path, 'icons', 'categories', category['icon'])
            menu_item = TaggedCategoriesMenuItem(icon=icon,
                                                 name=category['name'])
            self.items_container.add_widget(menu_item)


class TaggedArticlesMenuItem(Button):
    def __init__(self, icon, name, title, synopsis, **kwargs):
        super(TaggedArticlesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name
        self.title = title
        self.synopsis = synopsis


class TaggedArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(TaggedArticlesMenu, self).__init__(**kwargs)
        for article in articles:
            icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
            menu_item = TaggedArticlesMenuItem(icon=icon,
                                               name=article['name'],
                                               title=article['title'],
                                               synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class TagScreen(Screen):
    def __init__(self, tag_name, **kwargs):
        super(TagScreen, self).__init__(**kwargs)
        self.tag_name = tag_name
        self.tagged_categories = tags.tagged_categories(tag_name)
        self.tagged_articles = tags.tagged_articles(tag_name)

        tag_container = self.ids.container
        if len(self.tagged_categories) > 0:
            tagged_categories_menu = TaggedCategoriesMenu(categories=self.tagged_categories)
            tag_container.add_widget(tagged_categories_menu)
        if len(self.tagged_articles) > 0:
            tagged_articles_menu = TaggedArticlesMenu(articles=self.tagged_articles)
            tag_container.add_widget(tagged_articles_menu)


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
                audio_source = os.path.join(guides.active_guide_path, 'content', 'media', 'audio', content_item['source'])
                item_widget = ArticleAudio(audio_source=audio_source,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'video':
                video_source = os.path.join(guides.active_guide_path, 'content', 'media', 'video', content_item['source'])
                cover_image_source = os.path.join(guides.active_guide_path, 'content', 'media', 'video', content_item['screenshot'])
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

        self.guidesmenu_screen = GuidesMenuScreen()
        self.sm.add_widget(self.guidesmenu_screen)

        self.tagsmenu_screen = TagsMenuScreen()
        self.sm.add_widget(self.tagsmenu_screen)

        self.articlesmenu_screen = ArticlesMenuScreen()
        self.sm.add_widget(self.articlesmenu_screen)

        self.bookmarks_screen = BookmarksScreen()
        self.sm.add_widget(self.bookmarks_screen)

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
        self.sm.current = 'guides'

    def load_guide(self, guide_archive_paths):
        if guides.load(guide_archive_paths[0]):
            self.guidesmenu_screen.update_guidesmenu_items()
        else:
            guide_archive_name = os.path.basename(guide_archive_paths[0])
            GuideLoadFailedWarning('"[b]{}[/b]"\n guide load failed!'.format(guide_archive_name)).open()
        self.is_active_guide = bool(guides.active_guide_name)

    def unload_guide(self, guide_name):
        guides.unload(guide_name)
        self.guidesmenu_screen.update_guidesmenu_items()
        self.show_guidesmenu_screen()
        self.is_active_guide = bool(guides.active_guide_name)

    def show_tagsmenu_screen(self):
        if guides.active_guide_name and self.tagsmenu_screen.from_guide_name != guides.active_guide_name:
            self.tagsmenu_screen.update_tagsmenu_items()
            self.tagsmenu_screen.tagsmenu_widget.parent.scroll_y = 1
        self.sm.current = 'tags'

    def show_categoriesmenu_screen(self):
        if guides.active_guide_name and self.categoriesmenu_screen.from_guide_name != guides.active_guide_name:
            self.categoriesmenu_screen.update_categoriesmenu_items()
            self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
        self.sm.current = 'categories'

    def show_articlesmenu_screen(self):
        if guides.active_guide_name and self.articlesmenu_screen.from_guide_name != guides.active_guide_name:
            self.articlesmenu_screen.update_articlesmenu_items()
            self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
        self.sm.current = 'articles'

    def show_bookmarks_screen(self):
        if guides.active_guide_name and self.bookmarks_screen.from_guide_name != guides.active_guide_name:
            self.bookmarks_screen.update_bookmarks_menu_items()
            self.bookmarks_screen.ids.recycleview.scroll_y = 1
        self.sm.current = 'bookmarks'

    def add_bookmark(self, article_name):
        bookmarks.add(article_name)
        self.bookmarks_screen.update_bookmarks_menu_items()

    def remove_bookmark(self, article_name):
        bookmarks.remove(article_name)
        self.bookmarks_screen.update_bookmarks_menu_items()

    def show_search_screen(self):
        self.sm.current = 'search'

    def show_settings_screen(self):
        self.sm.current = 'settings'

########################################

    def show_tag_screen(self, tag_name):
        screens_names = [screen.name for screen in self.sm.screens]
        screen_name = '{{"{0}":{{"tag": "{1}"}}}}'.format(guides.active_guide_name, tag_name)
        if screen_name not in screens_names:
            tag_screen = TagScreen(name=screen_name,
                                   tag_name=tag_name)
            self.sm.add_widget(tag_screen)
        self.sm.current = screen_name

    def show_category_screen(self, category_name):
        screens_names = [screen.name for screen in self.sm.screens]
        screen_name = '{{"{0}":{{"category": "{1}"}}}}'.format(guides.active_guide_name, category_name)
        if screen_name not in screens_names:
            category_screen = CategoryScreen(name=screen_name,
                                             category_name=category_name)
            self.sm.add_widget(category_screen)
        self.sm.current = screen_name

    def show_article_screen(self, article_name):
        screen_manager = self.ids.manager
        screen_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Article: ' + str(article_name)
        if screen_name not in screen_names:
            article_screen = ArticleScreen(name=screen_name,
                                           article_name=article_name)
            screen_manager.add_widget(article_screen)

        screen_manager.current = screen_name

    def show_guide_screen(self, guide_name):
        screen_manager = self.ids.manager
        screen_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Guide: ' + guide_name
        if screen_name not in screen_names:
            guide_screen = GuideScreen(name=screen_name,
                                       guide_name=guide_name)
            screen_manager.add_widget(guide_screen)

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
