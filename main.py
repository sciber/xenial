import os
import tarfile
import shutil
import json
from functools import reduce
from datetime import datetime

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

Config.set('kivy', 'default_font',
           '''["Noto Sans", 
               "assets/fonts/NotoSans-Regular.ttf",
               "assets/fonts/NotoSans-Italic.ttf",
               "assets/fonts/NotoSans-Bold.ttf",
               "assets/fonts/NotoSans-BoldItalic.ttf"
              ]''')

Builder.load_file('ui-components.kv')
Builder.load_file('search.kv')
Builder.load_file('categories.kv')
Builder.load_file('category.kv')
Builder.load_file('tags.kv')
Builder.load_file('tag.kv')
Builder.load_file('articles.kv')
Builder.load_file('article.kv')
Builder.load_file('bookmarks.kv')
Builder.load_file('settings.kv')
Builder.load_file('guides.kv')

kivy.require('1.11.1')


class CategoriesMenuItem(Button):
    def __init__(self, category, **kwargs):
        super(CategoriesMenuItem, self).__init__(**kwargs)
        self.id_ = category['id']
        self.icon = app.current_guide_dir + '/icons/categories/' + category['icon']
        self.name = category['name']


class CategoriesMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for category in app.current_guide['categories']:
            categories_menu_item = CategoriesMenuItem(category=category)
            self.items_container.add_widget(categories_menu_item)

    def __init__(self, **kwargs):
        super(CategoriesMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


class CategoryAssignedTag(Button):
    pass


class CategoryAssignedTagsList(StackLayout):
    def __init__(self, tags, **kwargs):
        super(CategoryAssignedTagsList, self).__init__(**kwargs)
        for tag in tags:
            tag_button = CategoryAssignedTag(text=tag)
            self.add_widget(tag_button)


class CategoryRelatedCategoriesMenuItem(Button):
    def __init__(self, id_, icon, name, **kwargs):
        super(CategoryRelatedCategoriesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.name = name


class CategoryRelatedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(CategoryRelatedCategoriesMenu, self).__init__(**kwargs)

        for category in categories:
            icon = app.current_guide_dir + '/icons/categories/' + category['icon']
            menu_item = CategoryRelatedCategoriesMenuItem(id_=category['id'],
                                                          icon=icon,
                                                          name=category['name'])
            self.items_container.add_widget(menu_item)


class CategoryArticlesMenuItem(Button):
    def __init__(self, id_, icon, title, synopsis, **kwargs):
        super(CategoryArticlesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.title = title
        self.synopsis = synopsis


class CategoryArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(CategoryArticlesMenu, self).__init__(**kwargs)
        self.items_container = self
        for article in articles:
            icon = app.current_guide_dir + '/icons/articles/' + article['icon']
            menu_item = CategoryArticlesMenuItem(id_=article['id'],
                                                 icon=icon,
                                                 title=article['title'],
                                                 synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class CategoryScreen(Screen):
    def _get_related_categories(self):
        if len(self.category_assigned_tags) == 0:
            return []

        tagged_categories = []
        for category in app.current_guide['categories']:
            if category['id'] == self.category_id:
                continue

            categories_shared_tags = list(set(category['tags']) & set(self.category_assigned_tags))
            if len(categories_shared_tags) > 0:
                tagged_categories.append((category, len(categories_shared_tags)))

        tagged_categories.sort(key=lambda c: c[1], reverse=True)
        related_categories = [item[0] for item in tagged_categories]
        return related_categories

    def _get_articles(self):
        if len(self.category_assigned_tags) == 0:
            return []

        tagged_articles = []
        print('category tags', self.category_assigned_tags)
        for article in app.current_guide['articles']:
            print(article['tags'])
            if len(article['tags']) == 0:
                continue
            if set(article['tags']) > set(self.category_assigned_tags):
                tagged_articles.append(article)

        return tagged_articles

    def __init__(self, category_id, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        category = next(c for c in app.current_guide['categories'] if c['id'] == category_id)
        self.category_id = category_id
        self.category_icon = app.current_guide_dir + '/icons/categories/' + category['icon']
        self.category_name = category['name']
        # self.name = 'Category: ' + self.category_name
        self.category_assigned_tags = category['tags']
        self.category_related_categories = self._get_related_categories()
        self.category_articles = self._get_articles()
        category_container = self.ids.container
        category_assigned_tags_list = CategoryAssignedTagsList(tags=self.category_assigned_tags)
        category_container.add_widget(category_assigned_tags_list)
        if len(self.category_related_categories) > 0:
            category_related_categories_menu = CategoryRelatedCategoriesMenu(categories=self.category_related_categories)
            category_container.add_widget(category_related_categories_menu)
        if len(self.category_articles) > 0:
            category_articles_menu = CategoryArticlesMenu(articles=self.category_articles)
            category_container.add_widget(category_articles_menu)


class TagsMenuItem(Button):
    def _get_num_tagged_articles(self):
        return reduce(lambda x, y: x + 1 if self.name in y['tags'] else x, app.current_guide['articles'], 0)

    def _get_num_tagged_categories(self):
        return reduce(lambda x, y: x + 1 if self.name in y['tags'] else x, app.current_guide['categories'], 0)

    def __init__(self, tag, **kwargs):
        super(TagsMenuItem, self).__init__(**kwargs)
        self.name = tag
        self.num_articles = self._get_num_tagged_articles()
        self.num_categories = self._get_num_tagged_categories()


class TagsMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for tag in app.current_guide['tags']:
            tag_button = TagsMenuItem(tag=tag)
            self.items_container.add_widget(tag_button)

    def __init__(self, **kwargs):
        super(TagsMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


class TaggedCategoriesMenuItem(Button):
    def __init__(self, id_, icon, name, **kwargs):
        super(TaggedCategoriesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.name = name


class TaggedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(TaggedCategoriesMenu, self).__init__(**kwargs)
        for category in categories:
            icon = app.current_guide_dir + '/icons/categories/' + category['icon']
            menu_item = TaggedCategoriesMenuItem(id_=category['id'],
                                                 icon=icon,
                                                 name=category['name'])
            self.items_container.add_widget(menu_item)


class TaggedArticlesMenuItem(Button):
    def __init__(self, id_, icon, title, synopsis, **kwargs):
        super(TaggedArticlesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.title = title
        self.synopsis = synopsis


class TaggedArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(TaggedArticlesMenu, self).__init__(**kwargs)
        for article in articles:
            icon = app.current_guide_dir + '/icons/articles/' + article['icon']
            menu_item = TaggedArticlesMenuItem(id_=article['id'],
                                               icon=icon,
                                               title=article['title'],
                                               synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class TagScreen(Screen):
    def _get_tagged_categories(self):
        tagged_categories = [c for c in app.current_guide['categories'] if self.tag_name in c['tags']]
        return tagged_categories

    def _get_tagged_articles(self):
        tagged_articles = [a for a in app.current_guide['articles'] if self.tag_name in a['tags']]
        return tagged_articles

    def __init__(self, tag_name, **kwargs):
        super(TagScreen, self).__init__(**kwargs)
        self.tag_name = tag_name
        self.tagged_categories = self._get_tagged_categories()
        self.tagged_articles = self._get_tagged_articles()

        tag_container = self.ids.container
        if len(self.tagged_categories) > 0:
            tagged_categories_menu = TaggedCategoriesMenu(categories=self.tagged_categories)
            tag_container.add_widget(tagged_categories_menu)
        if len(self.tagged_articles) > 0:
            tagged_articles_menu = TaggedArticlesMenu(articles=self.tagged_articles)
            tag_container.add_widget(tagged_articles_menu)


class ArticlesMenuItem(Button):
    def __init__(self, article, **kwargs):
        super(ArticlesMenuItem, self).__init__(**kwargs)
        self.id_ = article['id']
        self.icon = app.current_guide_dir + '/icons/articles/' + article['icon']
        self.title = article['title']
        self.synopsis = article['synopsis']


class ArticlesMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for article in app.current_guide['articles']:
            articles_menu_item = ArticlesMenuItem(article=article)
            self.items_container.add_widget(articles_menu_item)

    def __init__(self, **kwargs):
        super(ArticlesMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


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
                image = app.current_guide_dir + '/content/media/image/' + content_item['source']
                item_widget = ArticleImage(image=image,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'audio':
                audio_source = app.current_guide_dir + '/content/media/audio/' + content_item['source']
                item_widget = ArticleAudio(audio_source=audio_source,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue

            if content_item['type'] == 'video':
                video_source = app.current_guide_dir + '/content/media/video/' + content_item['source']
                cover_image_source = app.current_guide_dir + '/content/media/video/' + content_item['screenshot']
                item_widget = ArticleVideo(video_source=video_source,
                                           cover_image_source=cover_image_source,
                                           caption=content_item['caption'])
                self.add_widget(item_widget)
                continue


class ArticleRelatedArticlesMenuItem(Button):
    def __init__(self, id_, icon, title, synopsis, **kwargs):
        super(ArticleRelatedArticlesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.title = title
        self.synopsis = synopsis


class ArticleRelatedArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(ArticleRelatedArticlesMenu, self).__init__(**kwargs)
        for article in articles:
            icon = app.current_guide_dir + '/icons/articles/' + article['icon']
            menu_item = ArticleRelatedArticlesMenuItem(id_=article['id'],
                                                       icon=icon,
                                                       title=article['title'],
                                                       synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class ArticleRelatedCategoriesMenuItem(Button):
    def __init__(self, id_, icon, name, **kwargs):
        super(ArticleRelatedCategoriesMenuItem, self).__init__(**kwargs)
        self.id_ = id_
        self.icon = icon
        self.name = name


class ArticleRelatedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(ArticleRelatedCategoriesMenu, self).__init__(**kwargs)
        for category in categories:
            icon = app.current_guide_dir + '/icons/categories/' + category['icon']
            menu_item = ArticleRelatedCategoriesMenuItem(id_=category['id'],
                                                         icon=icon,
                                                         name=category['name'])
            self.items_container.add_widget(menu_item)


class ArticleScreen(Screen):
    is_bookmarked = BooleanProperty(False)

    def _get_related_categories(self):
        tagged_categories = []
        for category in app.current_guide['categories']:
            article_category_shared_tags = list(set(category['tags']) & set(self.article_assigned_tags))
            if len(article_category_shared_tags) > 0:
                tagged_categories.append((category, len(article_category_shared_tags)))

        tagged_categories.sort(key=lambda c: c[1], reverse=True)
        related_categories = [item[0] for item in tagged_categories]
        return related_categories

    def _get_related_articles(self):
        tagged_articles = []
        for article in app.current_guide['articles']:
            if article['id'] == self.article_id:
                continue

            articles_shared_tags = list(set(article['tags']) & set(self.article_assigned_tags))
            if len(articles_shared_tags) > 0:
                tagged_articles.append((article, len(articles_shared_tags)))

        tagged_articles.sort(key=lambda a: a[1], reverse=True)
        related_articles = [item[0] for item in tagged_articles]
        return related_articles

    def __init__(self, article_id, **kwargs):
        super(ArticleScreen, self).__init__(**kwargs)
        article = next(a for a in app.current_guide['articles'] if a['id'] == article_id)
        self.article_id = article_id
        self.article_icon = app.current_guide_dir + '/icons/articles/' + article['icon']
        self.article_title = article['title']
        self.article_assigned_tags = article['tags']
        self.article_content = article['content']
        self.is_bookmarked = reduce(lambda x, y: x or (y['article_id'] == article_id), app.current_guide['bookmarks'], False)
        self.article_related_categories = self._get_related_categories()
        self.article_related_articles = self._get_related_articles()

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
            bookmark = next(b for b in app.current_guide['bookmarks'] if b['article_id'] == self.article_id)
            app.current_guide['bookmarks'].remove(bookmark)
        else:
            app.current_guide['bookmarks'].append({
                'article_id': self.article_id,
                'created_at': str(datetime.now())
            })

        self.is_bookmarked = not self.is_bookmarked


class BookmarksMenuItem(BoxLayout):
    def __init__(self, bookmark, **kwargs):
        super(BookmarksMenuItem, self).__init__(**kwargs)
        article = next(a for a in app.current_guide['articles'] if a['id'] == bookmark['article_id'])
        self.article_id = article['id']
        self.icon = app.current_guide_dir + '/icons/articles/' + article['icon']
        self.title = article['title']
        self.synopsis = article['synopsis']
        self.bookmark = bookmark

    def delete_bookmark(self):
        app.current_guide['bookmarks'].remove(self.bookmark)
        self.parent.remove_widget(self)


class BookmarksMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for bookmark in app.current_guide['bookmarks']:
            bookmarks_menu_item = BookmarksMenuItem(bookmark=bookmark)
            self.items_container.add_widget(bookmarks_menu_item)

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


class ApplicationRoot(NavigationDrawer):
    def show_category_screen(self, category_id):
        screen_manager = self.ids.manager
        screens_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Category: ' + str(category_id)
        if screen_name not in screens_names:
            category_screen = CategoryScreen(name=screen_name,
                                             category_id=category_id)
            screen_manager.add_widget(category_screen)

        screen_manager.current = screen_name

    def show_tag_screen(self, tag_name):
        screen_manager = self.ids.manager
        screens_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Tag: ' + tag_name
        if screen_name not in screens_names:
            tag_screen = TagScreen(name=screen_name,
                                   tag_name=tag_name)
            screen_manager.add_widget(tag_screen)

        screen_manager.current = screen_name

    def show_article_screen(self, article_id):
        screen_manager = self.ids.manager
        screen_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Article: ' + str(article_id)
        if screen_name not in screen_names:
            article_screen = ArticleScreen(name=screen_name,
                                           article_id=article_id)
            screen_manager.add_widget(article_screen)

        screen_manager.current = screen_name


class XenialApp(App):
    from settings import settings

    GUIDES_DIR = 'guides'
    guides_subdirs = []
    current_guide_dir = None
    current_guide = None

    def _init_guide(self):
        guides_dir_filenames = [os.path.join(self.GUIDES_DIR, fn) for fn in os.listdir(self.GUIDES_DIR)]
        if 'current_guide_name' in self.settings.keys():
            settings_current_guide_dir = os.path.join(self.GUIDES_DIR, self.settings['current_guide_name'])
        else:
            settings_current_guide_dir = None

        for filename in guides_dir_filenames:
            if os.path.isdir(filename):
                self.guides_subdirs.append(filename)

        if settings_current_guide_dir in self.guides_subdirs:
            self.current_guide_dir = settings_current_guide_dir
        elif len(self.guides_subdirs) > 0:
            self.current_guide_dir = self.guides_subdirs[0]

        if self.current_guide_dir is not None:
            with open(os.path.join(self.current_guide_dir, 'guide.json'), 'r') as guide_file:
                self.current_guide = json.load(guide_file)
            with open(os.path.join(self.current_guide_dir, 'categories.json'), 'r') as categories_file:
                self.current_guide['categories'] = json.load(categories_file)
            with open(os.path.join(self.current_guide_dir, 'articles.json'), 'r') as articles_file:
                self.current_guide['articles'] = json.load(articles_file)
            for article in self.current_guide['articles']:
                current_guide_content_dir = os.path.join(self.current_guide_dir, 'content')
                with open(os.path.join(current_guide_content_dir, f'{article["id"]}.json'), 'r') as content_file:
                    article['content'] = json.load(content_file)
            with open(os.path.join(self.current_guide_dir, 'bookmarks.json'), 'r') as bookmarks_file:
                self.current_guide['bookmarks'] = json.load(bookmarks_file)

    def __init__(self, **kwargs):
        super(XenialApp, self).__init__(**kwargs)
        self._init_guide()
        imported_guide_name = input('Name of a guide to be imported (None = Nothing imported):')
        if imported_guide_name != '':
            self.import_guide(os.path.join('guides', imported_guide_name + '.tgz'))

    def import_guide(self, guide_archive):
        guide_name = os.path.basename(guide_archive)[:-4]  # Expects tgz file extension
        guide_dirname = os.path.join(self.GUIDES_DIR, guide_name)
        if guide_dirname in self.guides_subdirs:
            shutil.rmtree(guide_dirname)
        os.mkdir(guide_dirname)
        with tarfile.open(guide_archive, 'r:gz') as tar:
            tar.extractall(guide_dirname)

    def build(self):
        self._init_guide()
        return ApplicationRoot()

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
