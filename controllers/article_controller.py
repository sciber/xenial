import os

from kivy.uix.screenmanager import Screen

from events import ev
from translator import tr
from models import guides

# from controllers.components.tagslist_controller import TagsList
# from controllers.components.categoriesmenu_controller import CategoriesMenu
from controllers.components.articlesmenu_controller import ArticlesMenu
# from controllers.components.articlecontent_controller import ArticleContent

# from connector import audio, video, video_meter


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
            self.articlesmenu_widget.menu_items = guides.active_guide.articles_list()
        else:
            self.articlesmenu_widget.menu_items = []


# class ArticleScreen(Screen):
#     from_guide_name = ''
#
#     def __init__(self, **kwargs):
#         super(ArticleScreen, self).__init__(**kwargs)
#         self.article_icon = ''
#         self.article_name = ''
#         self.article_title = ''
#         self.article_synopsis = ''
#         self.article_is_bookmarked = False
#         self.article_assigned_tags = []
#         self.tagslist_widget = TagsList(self.article_assigned_tags)
#         self.ids.tagslist_container.add_widget(self.tagslist_widget)
#         self.article_content = []
#         self.articlecontent_widget = ArticleContent()
#         self.ids.articlecontent_container.add_widget(self.articlecontent_widget)
#         self.article_related_categories = []
#         self.categoriesmenu_widget = CategoriesMenu()
#         self.ids.categoriesmenu_container.add_widget(self.categoriesmenu_widget)
#         self.article_related_articles = []
#         self.articlesmenu_widget = ArticlesMenu()
#         self.ids.articlesmenu_container.add_widget(self.articlesmenu_widget)
#
#         self.on_pre_leave = self._on_pre_leave
#
#     @staticmethod
#     def _on_pre_leave():
#         audio.stop()
#         video.stop()
#
#     def update_article_screen_items(self, article_name):
#         self.from_guide_name = guides.active_guide_name
#         article = articles.by_name(article_name)
#         self.article_icon = os.path.join(guides.active_guide_path, 'icons', 'articles', article['icon'])
#         self.article_name = article_name
#         self.article_title = article['title']
#         self.article_synopsis = article['synopsis']
#         self.article_is_bookmarked = bookmarks.is_article_bookmarked(article_name)
#         self.article_assigned_tags = article['tags']
#         self.tagslist_widget.tagslist_items = self.article_assigned_tags
#         self.article_content = articles.content(article_name)
#         self.articlecontent_widget.content_items = self.article_content
#         self.article_related_categories = articles.related_categories(article_name)
#         category_item_keys = ('icon', 'name')
#         self.categoriesmenu_widget.menu_items = [
#             {'category_' + key: item[key] for key in category_item_keys} for item in self.article_related_categories
#         ]
#         self.article_related_articles = articles.related_articles(article_name)
#         article_item_keys = ('icon', 'name', 'title', 'synopsis')
#         self.articlesmenu_widget.menu_items = [
#             {'article_' + key: item[key] for key in article_item_keys} for item in self.article_related_articles
#         ]
#
#     def toggle_article_bookmark(self):
#         if not bookmarks.is_article_bookmarked(self.article_name):
#             bookmarks.add(self.article_name)
#             self.article_is_bookmarked = True
#         else:
#             bookmarks.remove(self.article_name)
#             self.article_is_bookmarked = False
