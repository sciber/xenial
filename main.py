"""
Application initialization and the root widget
==============================================
"""

import os
import time

os.environ['KIVY_IMAGE'] = 'pil'
os.environ['KIVY_AUDIO'] = 'ffpyplayer'
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

import kivy

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.base import EventLoop

from kivy.garden.navigationdrawer import NavigationDrawer

from events.global_events import ev
from translations.translator import transl
from settings.settings import app_settings
from history.screens_history import hist

from models.guides_model import guides

from presenters.components.navigationpanel_presenter import NavigationPanel
from presenters.components.leaveappprompt_presenter import LeaveAppPrompt
from presenters.search_presenter import SearchScreen
from presenters.category_presenter import CategoriesMenuScreen, CategoryScreen
from presenters.article_presenter import ArticlesMenuScreen, ArticleScreen
from presenters.bookmark_presenter import BookmarksMenuScreen
from presenters.tag_presenter import TagsMenuScreen, TagScreen
from presenters.guide_presenter import GuidesMenuScreen, GuideScreen
from presenters.settings_presenter import SettingsScreen
from presenters.log_presenter import LogsMenuScreen, LogScreen

kivy.require('1.11.1')

# Views components
Builder.load_file('views/components/navigationpanel.kv')
Builder.load_file('views/components/screentitlebar.kv')
Builder.load_file('views/components/categoriesmenu.kv')
Builder.load_file('views/components/articlesmenu.kv')
Builder.load_file('views/components/articlecontent.kv')
Builder.load_file('views/components/tagslist.kv')
Builder.load_file('views/components/leaveappprompt.kv')

# Screens views
Builder.load_file('views/screens/logsmenu_screen.kv')
Builder.load_file('views/screens/log_screen.kv')
Builder.load_file('views/screens/guidesmenu_screen.kv')
Builder.load_file('views/screens/categoriesmenu_screen.kv')
Builder.load_file('views/screens/category_screen.kv')
Builder.load_file('views/screens/tagsmenu_screen.kv')
Builder.load_file('views/screens/tag_screen.kv')
Builder.load_file('views/screens/articlesmenu_screen.kv')
Builder.load_file('views/screens/article_screen.kv')
Builder.load_file('views/screens/bookmarksmenu_screen.kv')
Builder.load_file('views/screens/search_screen.kv')
Builder.load_file('views/screens/guide_screen.kv')
Builder.load_file('views/screens/settings_screen.kv')

# Application root view
Builder.load_string('''
<ApplicationRoot>:
    anim_type: 'slide_above_simple'
    BoxLayout:
        id: navigation_panel_container
    ScreenManager:
        id: manager
''')


class ApplicationRoot(NavigationDrawer):
    """
    Stores the application's main logic.
    """

    def __init__(self, **kwargs):
        super(ApplicationRoot, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.key_handler)

        self.sm = self.ids.manager

        self.logsmenu_screen = LogsMenuScreen()
        self.sm.add_widget(self.logsmenu_screen)

        self.log_screen = LogScreen()
        self.sm.add_widget(self.log_screen)

        self.search_screen = SearchScreen()
        self.sm.add_widget(self.search_screen)

        self.categoriesmenu_screen = CategoriesMenuScreen()
        self.sm.add_widget(self.categoriesmenu_screen)

        self.category_screen = CategoryScreen(name='category')
        self.sm.add_widget(self.category_screen)
        self.other_category_screen = CategoryScreen(name='other_category')
        self.sm.add_widget(self.other_category_screen)

        self.tagsmenu_screen = TagsMenuScreen()
        self.sm.add_widget(self.tagsmenu_screen)

        self.tag_screen = TagScreen(name='tag')
        self.sm.add_widget(self.tag_screen)
        self.other_tag_screen = TagScreen(name='other_tag')
        self.sm.add_widget(self.other_tag_screen)

        self.articlesmenu_screen = ArticlesMenuScreen()
        self.sm.add_widget(self.articlesmenu_screen)

        self.article_screen = ArticleScreen(name='article')
        self.sm.add_widget(self.article_screen)
        self.other_article_screen = ArticleScreen(name='other_article')
        self.sm.add_widget(self.other_article_screen)

        self.bookmarksmenu_screen = BookmarksMenuScreen()
        self.sm.add_widget(self.bookmarksmenu_screen)

        self.guidesmenu_screen = GuidesMenuScreen()
        self.sm.add_widget(self.guidesmenu_screen)

        self.guide_screen = GuideScreen()
        self.sm.add_widget(self.guide_screen)

        self.navigation_panel_container = self.ids.navigation_panel_container
        self.navigation_panel = NavigationPanel()
        self.navigation_panel_container.add_widget(self.navigation_panel)

        # Settings screen should be initialized last so all the UI of the previous screens is translated automatically
        self.settings_screen = SettingsScreen()
        self.sm.add_widget(self.settings_screen)

        if guides.active_guide is not None:
            self.show_categoriesmenu_screen()
        else:
            self.show_guidesmenu_screen()

    def key_handler(self, window, key, *largs):
        """ Manages showing previous screen after pressing Esc/Back button
            (unless the effect si defined in an underlying widget). """

        if key == 27:  # Esc key/Back button
            prev_screen = hist.pop_screen()
            if prev_screen is None:
                LeaveAppPrompt().open()
                return True
            if prev_screen[0] == 'article':
                self.show_article_screen(prev_screen[1], is_prev_screen=True)
            elif prev_screen[0] == 'category':
                self.show_category_screen(prev_screen[1], is_prev_screen=True)
            elif prev_screen[0] == 'tag':
                self.show_tag_screen(prev_screen[1], is_prev_screen=True)
            return True

    def show_logsmenu_screen(self):
        """ Shows the logs menu screen. """

        self._push_prev_screen_to_history()
        self.logsmenu_screen.ids.logsmenu_items_container.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'logsmenu'

    def show_log_screen(self, log_filename):
        self.log_screen.log_filename = log_filename
        self.sm.transition.direction = 'left'
        self.sm.current = 'log'

    def show_search_screen(self):
        """ Shows the search screen. """

        self._push_prev_screen_to_history()
        self.sm.transition.direction = 'left'
        self.sm.current = 'search'

    def show_categoriesmenu_screen(self):
        """ Shows the category menu screen. """

        self._push_prev_screen_to_history()
        self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'categoriesmenu'

    def show_category_screen(self, category_id, is_prev_screen=False):
        """ Shows screen for a particular category defined by its `category_id` parameter.
            Category screen identifier is stored in the application screens history list
            (if it is not previously visited screen invoked by moving back in the history). """

        if not is_prev_screen:
            self._push_prev_screen_to_history()
            self.sm.transition.direction = 'left'
        else:
            self.sm.transition.direction = 'right'
        if self.sm.current == 'category':
            self.category_screen, self.other_category_screen = self.other_category_screen, self.category_screen
            self.category_screen.name = 'category'
            self.other_category_screen.name = 'other_category'
        self.category_screen.category_id = category_id
        self.category_screen.ids.screen_content_scrollview.scroll_y = 1
        self.sm.current = 'category'
        self._remove_current_screen_from_history()

    def show_articlesmenu_screen(self):
        """ Shows the articles menu screen. """

        self._push_prev_screen_to_history()
        self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'articlesmenu'

    def show_article_screen(self, article_id, search_results=None, is_prev_screen=False):
        """ Shows screen for a particular article defined by its `article_id` parameter.
            Article screen identifier is stored in the application screens history list
            (if it is not previously visited screen invoked by moving back in the history). """

        if not is_prev_screen:
            self._push_prev_screen_to_history()
            self.sm.transition.direction = 'left'
        else:
            self.sm.transition.direction = 'right'
        if self.sm.current == 'article':
            self.article_screen, self.other_article_screen = self.other_article_screen, self.article_screen
            self.article_screen.name = 'article'
            self.other_article_screen.name = 'other_article'
        self.article_screen.ids.screen_content_scrollview.scroll_y = 1
        self.article_screen.article_id = article_id
        if search_results is not None:
            self.article_screen.search_results = search_results
        else:
            self.article_screen.search_results = []
        self.sm.current = 'article'
        self._remove_current_screen_from_history()

    def show_bookmarksmenu_screen(self):
        """ Shows the bookmarks menu screen. """

        self._push_prev_screen_to_history()
        self.bookmarksmenu_screen.ids.bookmarksmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'bookmarksmenu'

    def show_tagsmenu_screen(self):
        """ Shows the tags menu screen. """

        self._push_prev_screen_to_history()
        self.tagsmenu_screen.ids.tagsmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'tagsmenu'

    def show_tag_screen(self, tag_id, is_prev_screen=False):
        """ Shows screen for a particular tag defined by its `tag_id` parameter.
            Tag screen identifier is stored in the application screens history list
            (if it is not previously visited screen invoked by moving back in the history). """

        if not is_prev_screen:
            self._push_prev_screen_to_history()
            self.sm.transition.direction = 'left'
        else:
            self.sm.transition.direction = 'right'
        if self.sm.current == 'tag':
            self.tag_screen, self.other_tag_screen = self.other_tag_screen, self.tag_screen
            self.tag_screen.name = 'tag'
            self.other_tag_screen.name = 'other_tag'
        self.tag_screen.tag_id = tag_id
        self.tag_screen.ids.screen_content_scrollview.scroll_y = 1
        self.sm.current = 'tag'
        self._remove_current_screen_from_history()

    def show_guidesmenu_screen(self):
        """ Show the guides menu screen. """

        self._push_prev_screen_to_history()
        self.guidesmenu_screen.ids.guidesmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'guidesmenu'

    def show_guide_screen(self, guide_name):
        """ Shows screen for a particular guide defined by its `guide_id` parameter. """

        self._push_prev_screen_to_history()
        self.guide_screen.guide_name = guide_name
        self.guide_screen.ids.screen_content_scrollview.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'guide'

    def show_settings_screen(self):
        """ Shows the settings screen. """

        self._push_prev_screen_to_history()
        self.sm.transition.direction = 'left'
        self.sm.current = 'settings'

    def _push_prev_screen_to_history(self):
        if self.sm.current_screen.name == 'article':
            hist.append_screen(self.sm.current_screen.name, self.sm.current_screen.article_id)
        elif self.sm.current_screen.name == 'category':
            hist.append_screen(self.sm.current_screen.name, self.sm.current_screen.category_id)
        elif self.sm.current_screen.name == 'tag':
            hist.append_screen(self.sm.current_screen.name, self.sm.current_screen.tag_id)

    def _remove_current_screen_from_history(self):
        if self.sm.current_screen.name == 'article':
            hist.remove_screen(self.sm.current_screen.name, self.sm.current_screen.article_id)
        elif self.sm.current_screen.name == 'category':
            hist.remove_screen(self.sm.current_screen.name, self.sm.current_screen.category_id)
        elif self.sm.current_screen.name == 'tag':
            hist.remove_screen(self.sm.current_screen.name, self.sm.current_screen.tag_id)


class XenialApp(App):
    """
    Is kivy application class; it sets application root.
    Reads or (if not defined) stores the application's settings.
    """

    def on_start(self):
        if app_settings.exists('active_guide_name') and guides.does_guide_exist(app_settings.get('active_guide_name')):
            guides.set_active_guide(app_settings.get('active_guide_name'))
        elif guides.active_guide is not None:
            self.set_active_guide_name_settings(self, guides.active_guide.guide_name)
        ev.bind(on_active_guide=self.set_active_guide_name_settings)
        if app_settings.exists('ui_lang_code'):
            transl.ui_lang_code = app_settings.get('ui_lang_code')
        ev.bind(on_ui_lang_code=self.set_translator_ui_lang_code_settings)

    @staticmethod
    def set_active_guide_name_settings(*args):
        """ Uses settings management to store the application's active guide. """

        if guides.active_guide is not None:
            app_settings.set('active_guide_name', guides.active_guide.guide_name)
        else:
            app_settings.set('active_guide_name', '')

    @staticmethod
    def set_translator_ui_lang_code_settings(instance, lang_code):
        """ Uses settings management to store the application's UI language. """

        app_settings.set('ui_lang_code', lang_code)

    def build(self):
        """ Returns the application's root widget. """
        self.root = ApplicationRoot()
        return self.root

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
