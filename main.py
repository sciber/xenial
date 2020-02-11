import time

import kivy

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.base import EventLoop
from kivy.uix.popup import Popup

from kivy.garden.navigationdrawer import NavigationDrawer

from settings import app_settings
from events.global_events import ev
from translations.translator import transl
from models.guides_model import guides
from history import hist

from presenters.log_presenter import LogScreen
from presenters.category_presenter import CategoriesMenuScreen, CategoryScreen
from presenters.tag_presenter import TagsMenuScreen, TagScreen
from presenters.article_presenter import ArticlesMenuScreen, ArticleScreen
from presenters.settings_presenter import SettingsScreen
from presenters.components.navigationpanel_presenter import NavigationPanel
from presenters.guide_presenter import GuidesMenuScreen, GuideScreen
from presenters.bookmark_presenter import BookmarksMenuScreen
from presenters.search_presenter import SearchScreen

kivy.require('1.11.1')

# # Views components
Builder.load_file('views/components/navigationpanel.kv')
Builder.load_file('views/components/screentitlebar.kv')
Builder.load_file('views/components/categoriesmenu.kv')
Builder.load_file('views/components/articlesmenu.kv')
Builder.load_file('views/components/articlecontent.kv')
Builder.load_file('views/components/tagslist.kv')
Builder.load_file('views/components/leaveappprompt.kv')

# Screens views
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


class LeaveAppPrompt(Popup):
    def __init__(self, **kwargs):
        super(LeaveAppPrompt, self).__init__(**kwargs)
        ev.bind(on_ui_lang_code=self._translate_ui)
        self._translate_ui()

    def _translate_ui(self, *args):
        self.title = transl.translate('Warning')
        self.prompt_text = transl.translate('Do you want to leave the app?')
        self.cancel_button_text = transl.translate('Cancel')
        self.quit_button_text = transl.translate('Quit')

    def _handle_keyboard(self, window, key, *largs):
        super(LeaveAppPrompt, self)._handle_keyboard(window, key, *largs)
        if key == 27:
            self.dismiss()
            return True


class ApplicationRoot(NavigationDrawer):
    def __init__(self, **kwargs):
        super(ApplicationRoot, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.key_handler)

        self.sm = self.ids.manager

        self.log_screen = LogScreen()
        self.sm.add_widget(self.log_screen)
        self.sm.current = 'log'

        start_time = time.time()
        self.search_screen = SearchScreen()
        self.sm.add_widget(self.search_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Search[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.categoriesmenu_screen = CategoriesMenuScreen()
        self.sm.add_widget(self.categoriesmenu_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Categories menu[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.category_screen = CategoryScreen(name='category')
        self.sm.add_widget(self.category_screen)
        self.other_category_screen = CategoryScreen(name='other_category')
        self.sm.add_widget(self.other_category_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Category[/b] screens stubs were built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.tagsmenu_screen = TagsMenuScreen()
        self.sm.add_widget(self.tagsmenu_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Tags menu[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.tag_screen = TagScreen(name='tag')
        self.sm.add_widget(self.tag_screen)
        self.other_tag_screen = TagScreen(name='other_tag')
        self.sm.add_widget(self.other_tag_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Tag[/b] screens stubs were built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.articlesmenu_screen = ArticlesMenuScreen()
        self.sm.add_widget(self.articlesmenu_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Articles menu[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.article_screen = ArticleScreen(name='article')
        self.sm.add_widget(self.article_screen)
        self.other_article_screen = ArticleScreen(name='other_article')
        self.sm.add_widget(self.other_article_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Article[/b] screens stubs were built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.bookmarksmenu_screen = BookmarksMenuScreen()
        self.sm.add_widget(self.bookmarksmenu_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Bookmarks menu[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.guidesmenu_screen = GuidesMenuScreen()
        self.sm.add_widget(self.guidesmenu_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Guides menu[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.guide_screen = GuideScreen()
        self.sm.add_widget(self.guide_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Guide[/b] screen stub was built in: {dt:.2f} ms'.format(dt=dt))

        start_time = time.time()
        self.navigation_panel_container = self.ids.navigation_panel_container
        self.navigation_panel = NavigationPanel()
        self.navigation_panel_container.add_widget(self.navigation_panel)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Navigation panel[/b] was built in: {dt:.2f} ms'.format(dt=dt))

        # Settings screen should be initialized last so all the UI of the previous screens is translated automatically
        start_time = time.time()
        self.settings_screen = SettingsScreen()
        self.sm.add_widget(self.settings_screen)
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.log_screen.add_log_item('[b]Settings[/b] screen was built in: {dt:.2f} ms'.format(dt=dt))

        if guides.active_guide is not None:
            self.show_categoriesmenu_screen()
        else:
            self.show_guidesmenu_screen()

    def key_handler(self, window, key, *largs):
        if key == 27:
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

    def show_log_screen(self):
        self._push_prev_screen_to_history()
        self.log_screen.ids.logslist_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'log'

    def show_search_screen(self):
        self._push_prev_screen_to_history()
        self.sm.transition.direction = 'left'
        self.sm.current = 'search'

    def show_categoriesmenu_screen(self):
        self._push_prev_screen_to_history()
        self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'categoriesmenu'

    def show_category_screen(self, category_id, is_prev_screen=False):
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
        self._push_prev_screen_to_history()
        self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'articlesmenu'

    def show_article_screen(self, article_id, search_results=None, is_prev_screen=False):
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
        self._push_prev_screen_to_history()
        self.bookmarksmenu_screen.ids.bookmarksmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'bookmarksmenu'

    def show_tagsmenu_screen(self):
        self._push_prev_screen_to_history()
        self.tagsmenu_screen.ids.tagsmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'tagsmenu'

    def show_tag_screen(self, tag_id, is_prev_screen=False):
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
        self._push_prev_screen_to_history()
        self.guidesmenu_screen.ids.guidesmenu_widget.parent.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'guidesmenu'

    def show_guide_screen(self, guide_name):
        self._push_prev_screen_to_history()
        self.guide_screen.guide_name = guide_name
        self.guide_screen.ids.screen_content_scrollview.scroll_y = 1
        self.sm.transition.direction = 'left'
        self.sm.current = 'guide'

    def show_settings_screen(self):
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
    def __init__(self, **kwargs):
        super(XenialApp, self).__init__(**kwargs)
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
        if guides.active_guide is not None:
            app_settings.set('active_guide_name', guides.active_guide.guide_name)
        else:
            app_settings.set('active_guide_name', '')

    @staticmethod
    def set_translator_ui_lang_code_settings(instance, lang_code):
        app_settings.set('ui_lang_code', lang_code)

    def build(self):
        start_time = time.time()
        self.root = ApplicationRoot()
        stop_time = time.time()
        dt = (stop_time - start_time) * 1000
        self.root.log_screen.add_log_item('[b]Total initialization[/b] time: {dt:.2f} ms'.format(dt=dt))
        return self.root

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
