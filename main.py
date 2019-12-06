import os

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty

from kivy.garden.navigationdrawer import NavigationDrawer

from models import guides, bookmarks

from controllers.guide_controller import GuidesMenuScreen, GuideScreen, GuideLoadFailedWarning
from controllers.tag_controller import TagsMenuScreen, TagScreen
from controllers.category_controller import CategoriesMenuScreen, CategoryScreen
from controllers.article_controller import ArticlesMenuScreen, ArticleScreen
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
Builder.load_file('views/components/articlecontent.kv')

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

        self.article_screen = ArticleScreen()
        self.sm.add_widget(self.article_screen)

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
        if self.tagsmenu_screen.from_guide_name != guides.active_guide_name:
            self.tagsmenu_screen.update_tagsmenu_items()
            self.tagsmenu_screen.tagsmenu_widget.parent.scroll_y = 1
        self.sm.current = 'tagsmenu'

    def show_tag_screen(self, tag_name):
        if (self.tag_screen.from_guide_name != guides.active_guide_name
                or self.tag_screen.tag_name != tag_name):
            prev_tag_screen = self.tag_screen
            prev_tag_screen.name = 'prev_tag'
            new_tag_screen = TagScreen(name='tag')
            new_tag_screen.update_tag_screen_items(tag_name)
            self.sm.add_widget(new_tag_screen)
            self.tag_screen = new_tag_screen
            self.sm.remove_widget(prev_tag_screen)
        self.sm.current = 'tag'

    def show_categoriesmenu_screen(self):
        if self.categoriesmenu_screen.from_guide_name != guides.active_guide_name:
            self.categoriesmenu_screen.update_categoriesmenu_items()
            self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
        self.sm.current = 'categoriesmenu'

    def show_category_screen(self, category_name):
        if (self.category_screen.from_guide_name != guides.active_guide_name
                or self.category_screen.category_name != category_name):
            prev_category_screen = self.category_screen
            prev_category_screen.name = 'prev_category'
            new_category_screen = CategoryScreen(name='category')
            new_category_screen.update_category_screen_items(category_name)
            self.sm.add_widget(new_category_screen)
            self.category_screen = new_category_screen
            self.sm.remove_widget(prev_category_screen)
        self.sm.current = 'category'

    def show_articlesmenu_screen(self):
        if self.articlesmenu_screen.from_guide_name != guides.active_guide_name:
            self.articlesmenu_screen.update_articlesmenu_items()
            self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
        self.sm.current = 'articlesmenu'

    def show_article_screen(self, article_name):
        if (self.article_screen.from_guide_name != guides.active_guide_name
                or self.article_screen.article_name != article_name):
            prev_article_screen = self.article_screen
            prev_article_screen.name = 'prev_article'
            new_article_screen = ArticleScreen(name='article')
            new_article_screen.update_article_screen_items(article_name)
            self.sm.add_widget(new_article_screen)
            self.article_screen = new_article_screen
            self.sm.remove_widget(prev_article_screen)
        self.sm.current = 'article'

    def show_bookmarksmenu_screen(self):
        self.bookmarksmenu_screen.update_bookmarksmenu_items()
        self.bookmarksmenu_screen.ids.bookmarksmenu_widget.parent.scroll_y = 1
        self.sm.current = 'bookmarksmenu'

    def remove_bookmark(self, article_name):
        bookmarks.remove(article_name)
        self.bookmarksmenu_screen.update_bookmarksmenu_items()

    def show_search_screen(self):
        self.sm.current = 'search'

    def show_settings_screen(self):
        self.sm.current = 'settings'


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
