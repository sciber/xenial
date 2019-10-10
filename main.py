import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
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


class ArticleScreen(Screen):
    def toggle_bookmark(self):
        print('Article (un)bookmarked!')


class BookmarksMenuItem(BoxLayout):
    def __init__(self, bookmark, **kwargs):
        super(BookmarksMenuItem, self).__init__(**kwargs)
        article = next(a for a in app.guide['articles'] if a['id'] == bookmark['article_id'])
        self.icon = 'guides/dummy/icons/articles/' + article['icon']
        self.title = article['content'][0]['text']
        self.synopsis = article['content'][1]['text']
        self.bookmark = bookmark

    def delete_bookmark(self):
        app.guide['bookmarks'].remove(self.bookmark)
        self.parent.remove_widget(self)


class BookmarksMenuScreen(Screen):
    bookmarks_container = ObjectProperty()

    def _post_init(self, dt):
        for bookmark in app.guide['bookmarks']:
            bookmarks_menu_item = BookmarksMenuItem(bookmark=bookmark)
            self.bookmarks_container.add_widget(bookmarks_menu_item)

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


class ApplicationRoot(NavigationDrawer):
    pass


class XenialApp(App):
    from guides.dummy.guide import guide

    def build(self):
        return ApplicationRoot()

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
