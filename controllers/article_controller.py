import os

from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr
from models import guides

from controllers.components.tagslist_controller import TagsList
from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu
from controllers.components.articlecontent_controller import ArticleContent

from connector import audio, video


class ArticlesMenuScreen(Screen):
    from_guide_name = ''

    def __init__(self, **kwargs):
        super(ArticlesMenuScreen, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self.translate_ui)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        ev.bind(on_active_guide=self.set_articlesmenu_items)
        self.set_articlesmenu_items()

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Articles')

    def set_articlesmenu_items(self, *args):
        if guides.active_guide is not None:
            self.articlesmenu_widget.articlesmenu_items = guides.active_guide.articles_list()
        else:
            self.articlesmenu_widget.articlesmenu_items = []


class ArticleScreen(Screen):
    article_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ArticleScreen, self).__init__(**kwargs)
        self.tagslist_widget = TagsList()
        self.ids.tagslist_container.add_widget(self.tagslist_widget)
        self.categoriesmenu_widget = CategoriesMenu()
        self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
        self.articlesmenu_widget = ArticlesMenu()
        self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
        self.articlecontent_widget = ArticleContent()
        self.ids.articlecontent_container.add_widget(self.articlecontent_widget)
        ev.bind(on_ui_lang_code=self.translate_ui)
        ev.bind(on_add_bookmark=self.on_toggle_bookmark)
        ev.bind(on_delete_bookmark=self.on_toggle_bookmark)

    def translate_ui(self, *args):
        self.screen_title = tr.translate('Article')
        self.related_categories_subtitle = tr.translate('Related categories')
        self.related_articles_subtitle = tr.translate('Related articles')

    def clear_article_screen_items(self, *args):
        if self.article_id:
            self.article_id = 0

    def on_article_id(self, *args):
        if self.article_id:
            article = guides.active_guide.article_by_id(self.article_id)
            self.article_name = article.article_name
            self.article_icon = article.article_icon
            self.article_title = article.article_title
            self.article_synopsis = article.article_synopsis
            self.tagslist_widget.tagslist_items = article.tags_list()
            self.categoriesmenu_widget.categoriesmenu_items = article.categories_list()
            self.article_has_categories = bool(self.categoriesmenu_widget.categoriesmenu_items)
            self.articlesmenu_widget.articlesmenu_items = article.related_articles_list()
            self.article_has_related_articles = bool(self.articlesmenu_widget.articlesmenu_items)
            self.articlecontent_widget.articlecontent_blocks = []
            self.article_is_bookmarked = article.bookmark() is not None
        else:
            self.article_name = ''
            self.article_icon = ''
            self.article_title = ''
            self.article_synopsis = ''
            self.tagslist_widget.tagslist_items = []
            self.categoriesmenu_widget.categoriesmenu_items = []
            self.articlesmenu_widget.articlesmenu_items = []
            self.articlecontent_widget.articlecontent_items = []
            self.article_is_bookmarked = False

    def on_enter(self):
        article = guides.active_guide.article_by_id(self.article_id)
        self.articlecontent_widget.articlecontent_blocks = article.content_blocks_list()

    @staticmethod
    def on_pre_leave():
        audio.stop()
        video.stop()

    def toggle_article_bookmark(self):
        if not self.article_id:
            return
        article = guides.active_guide.article_by_id(self.article_id)
        article_bookmark = article.bookmark()
        if article_bookmark is not None:
            guides.active_guide.delete_bookmark(article_bookmark['bookmark_id'])
            ev.dispatch('on_delete_bookmark', self.article_id)
        else:
            guides.active_guide.add_bookmark(self.article_id)
            ev.dispatch('on_add_bookmark', self.article_id)

    def on_toggle_bookmark(self, instance, article_id):
        if not self.article_id or self.article_id != article_id:
            return
        article = guides.active_guide.article_by_id(self.article_id)
        article_bookmark = article.bookmark()
        self.article_is_bookmarked = article_bookmark is not None

    # def on_delete_bookmark(self, instance, article_id):
    #     print('on_delete_bookmark - article_id', self.article_id)
    #     if not self.article_id:
    #         return
    #     article = guides.active_guide.article_by_id(self.article_id)
    #     print('on_delete_bookmark - article', article)
    #     article_bookmark = article.bookmark()
    #     print('on_delete_bookmark - article_bookmark', article_bookmark)
    #     if article_bookmark['bookmark_id'] == bookmark_id:
    #         self.article_is_bookmarked = False

    # def update_article_screen_items(self, article_name):
    #     self.from_guide_name = guides.active_guide_name
    #     article = articles.by_name(article_name)
    #     self.article_icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
    #     self.article_name = article_name
    #     self.article_title = article['title']
    #     self.article_synopsis = article['synopsis']
    #     self.article_is_bookmarked = bookmarks.is_article_bookmarked(article_name)
    #     self.article_assigned_tags = article['tags']
    #     self.tagslist_widget.tagslist_items = self.article_assigned_tags
    #     self.article_content = articles.content(article_name)
    #     self.articlecontent_widget.content_items = self.article_content
    #     self.article_related_categories = articles.related_categories(article_name)
    #     category_item_keys = ('icon', 'name')
    #     self.categoriesmenu_widget.menu_items = [
    #         {'category_' + key: item[key] for key in category_item_keys} for item in self.article_related_categories
    #     ]
    #     self.article_related_articles = articles.related_articles(article_name)
    #     article_item_keys = ('icon', 'name', 'title', 'synopsis')
    #     self.articlesmenu_widget.menu_items = [
    #         {'article_' + key: item[key] for key in article_item_keys} for item in self.article_related_articles
    #     ]

    #     if not bookmarks.is_article_bookmarked(self.article_name):
    #         bookmarks.add(self.article_name)
    #         self.article_is_bookmarked = True
    #     else:
    #         bookmarks.remove(self.article_name)
    #         self.article_is_bookmarked = False
