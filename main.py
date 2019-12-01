import os

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader

from kivy.garden.navigationdrawer import NavigationDrawer

from models import guides, tags, categories, articles, bookmarks


Config.set('kivy', 'default_font',
           '''["Noto Sans", 
               "assets/fonts/NotoSans-Regular.ttf",
               "assets/fonts/NotoSans-Italic.ttf",
               "assets/fonts/NotoSans-Bold.ttf",
               "assets/fonts/NotoSans-BoldItalic.ttf"
              ]''')

Builder.load_file('ui-components.kv')
Builder.load_file('search.kv')

# Views components
Builder.load_file('views/components/categories_menu.kv')
Builder.load_file('views/components/articles_menu.kv')

# Screens views
Builder.load_file('views/screens/guides_screen.kv')
Builder.load_file('views/screens/tags_screen.kv')
Builder.load_file('views/screens/categories_screen.kv')
Builder.load_file('views/screens/articles_screen.kv')
Builder.load_file('views/screens/bookmarks_screen.kv')

Builder.load_file('category.kv')
Builder.load_file('tag.kv')
Builder.load_file('article.kv')
Builder.load_file('settings.kv')
Builder.load_file('guide.kv')

kivy.require('1.11.1')


class GuidesScreen(Screen):
    guides_menu_items = ListProperty()

    def __init__(self, **kwargs):
        super(GuidesScreen, self).__init__(**kwargs)
        self.update_guides_menu_items()

    def update_guides_menu_items(self):
        item_keys = ('icon', 'name', 'title', 'lang', 'from_place', 'to_place', 'is_active')
        self.guides_menu_items = [
            {('guide_' + key): item[key] for key in item_keys} for item in guides.all()
        ]


class TagsScreen(Screen):
    from_guide_name = ''
    tags_screen_menu_items = ListProperty()

    def __init__(self, **kwargs):
        super(TagsScreen, self).__init__(**kwargs)
        self.update_tags_screen_menu_items()

    def update_tags_screen_menu_items(self):
        self.from_guide_name = guides.active_guide['name']
        self.tags_screen_menu_items = [{
            'tag_name': tag_name,
            'num_tagged_categories': len(tags.tagged_categories(tag_name)),
            'num_tagged_articles': len(tags.tagged_articles(tag_name))
        } for tag_name in tags.all()]


class CategoriesScreen(Screen):
    from_guide_name = ''
    categories_menu_items = ListProperty()

    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs)
        self.update_categories_menu_items()

    def update_categories_menu_items(self):
        self.from_guide_name = guides.active_guide['name']
        item_keys = ('icon', 'name')
        self.categories_menu_items = [
            {('category_' + key): item[key] for key in item_keys} for item in categories.all()
        ]


class ArticlesScreen(Screen):
    from_guide_name = ''
    articles_menu_items = ListProperty()

    def __init__(self, **kwargs):
        super(ArticlesScreen, self).__init__(**kwargs)
        self.update_articles_menu_items()

    def update_articles_menu_items(self):
        self.from_guide_name = guides.active_guide['name']
        item_keys = ('icon', 'name', 'title', 'synopsis')
        self.articles_menu_items = [
            {('article_' + key): item[key] for key in item_keys} for item in articles.all()
        ]


class BookmarksScreen(Screen):
    from_guide_name = ''
    bookmarks_menu_items = ListProperty()
    is_model_modified = False

    def __init__(self, **kwargs):
        super(BookmarksScreen, self).__init__(**kwargs)
        self.update_bookmarks_menu_items()

    def update_bookmarks_menu_items(self):
        self.from_guide_name = guides.active_guide['name']
        item_keys = ('icon', 'name', 'title', 'synopsis')
        self.bookmarks_menu_items = [
            {('article_' + key): item[key] for key in item_keys} for item in bookmarks.bookmarked_articles()
        ]

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


class GuideAssignedTag(Button):
    pass


class GuideAssignedTagsList(StackLayout):
    def __init__(self, tags, **kwargs):
        super(GuideAssignedTagsList, self).__init__(**kwargs)
        for tag in tags:
            tag_button = GuideAssignedTag(text=tag)
            self.add_widget(tag_button)


class GuideScreen(Screen):
    def __init__(self, guide_name, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        guide = guides.by_name(guide_name)
        self.guide_name = guide_name
        self.guide_icon = os.path.join(guides.GUIDES_DIR, guide['name'], 'icons', 'guide', guide['icon'])
        self.guide_title = guide['title']
        self.guide_assigned_tags = guide['tags']
        self.guide_description = guide['description']
        self.guide_lang = guide['lang']
        self.guide_from_place = guide['from_place']
        self.guide_to_place = guide['to_place']
        guide_container = self.ids.container
        guide_assigned_tags_list = GuideAssignedTagsList(tags=guide['tags'])
        guide_container.add_widget(guide_assigned_tags_list)


class GuideLoadFailedWarning(Popup):
    def __init__(self, message, **kwargs):
        super(GuideLoadFailedWarning, self).__init__(**kwargs)
        self.message = message


class UnloadGuideWarningPopup(Popup):
    def __init__(self, guide_name, guide_title, **kwargs):
        super(UnloadGuideWarningPopup, self).__init__(**kwargs)
        self.guide_name = guide_name
        self.guide_title = guide_title


class ApplicationRoot(NavigationDrawer):
    def __init__(self, **kwargs):
        super(ApplicationRoot, self).__init__(**kwargs)
        self.sm = self.ids.manager

        self.categories_screen = CategoriesScreen()
        self.sm.add_widget(self.categories_screen)

        self.guides_screen = GuidesScreen()
        self.sm.add_widget(self.guides_screen)

        self.tags_screen = TagsScreen()
        self.sm.add_widget(self.tags_screen)

        self.articles_screen = ArticlesScreen()
        self.sm.add_widget(self.articles_screen)

        self.bookmarks_screen = BookmarksScreen()
        self.sm.add_widget(self.bookmarks_screen)

        self.sm.current = 'categories'

    def show_guides_screen(self):
        self.sm.current = 'guides'

    @staticmethod
    def change_active_guide(guide_name):
        guides.activate(guide_name)

    def show_tags_screen(self):
        if guides.active_guide and self.tags_screen.from_guide_name != guides.active_guide['name']:
            self.tags_screen.update_tags_screen_menu_items()
        self.sm.current = 'tags'

    def show_categories_screen(self):
        if guides.active_guide and self.categories_screen.from_guide_name != guides.active_guide['name']:
            self.categories_screen.update_categories_menu_items()
        self.sm.current = 'categories'

    def show_articles_screen(self):
        if guides.active_guide and self.articles_screen.from_guide_name != guides.active_guide['name']:
            self.articles_screen.update_articles_menu_items()
        self.sm.current = 'articles'

    def show_bookmarks_screen(self):
        if guides.active_guide and self.bookmarks_screen.from_guide_name != guides.active_guide['name']:
            self.bookmarks_screen.update_bookmarks_menu_items()
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

    def show_tag_screen(self, tag_name):
        screens_names = [screen.name for screen in self.sm.screens]
        screen_name = '{{"{0}":{{"tag": "{1}"}}}}'.format(guides.active_guide['name'], tag_name)
        if screen_name not in screens_names:
            tag_screen = TagScreen(name=screen_name,
                                   tag_name=tag_name)
            self.sm.add_widget(tag_screen)
        self.sm.current = screen_name

    def show_category_screen(self, category_name):
        screens_names = [screen.name for screen in self.sm.screens]
        screen_name = '{{"{0}":{{"category": "{1}"}}}}'.format(guides.active_guide['name'], category_name)
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

    def load_guide(self, guide_archive_paths):
        if guides.load(guide_archive_paths[0]):
            self.guides_screen.update_guides_menu_items()
        else:
            guide_archive_name = os.path.basename(guide_archive_paths[0])
            GuideLoadFailedWarning('"[b]{}[/b]"\n guide load failed!'.format(guide_archive_name)).open()

    def unload_guide(self, guide_name):
        guides.unload(guide_name)
        if guides.active_guide is None:
            app.is_active_guide = False
        screen_manager = self.ids.manager
        screen_manager.current = 'guides'


class XenialApp(App):
    GUIDES_DIR = guides.GUIDES_DIR

    def _switch_to_guides(self, dt):
        self.root.ids.manager.current = 'guides'

    def __init__(self, **kwargs):
        super(XenialApp, self).__init__(**kwargs)

        if guides.active_guide is None:
            Clock.schedule_once(self._switch_to_guides)  # Temporary hack
            self.is_active_guide = False
        else:
            self.is_active_guide = True

    def build(self):
        self.root = ApplicationRoot()
        return self.root

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
