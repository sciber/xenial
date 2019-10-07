import kivy

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.garden.navigationdrawer import NavigationDrawer

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


class ApplicationRoot(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavigationDrawer, self).__init__(**kwargs)


class XenialApp(App):
    def build(self):
        return ApplicationRoot()

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
