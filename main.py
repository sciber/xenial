import os

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.base import EventLoop
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from kivy.garden.navigationdrawer import NavigationDrawer

# from models import guides, bookmarks

# from controllers.guide_controller import GuidesMenuScreen, GuideScreen, GuideLoadFailedWarning
# from controllers.tag_controller import TagsMenuScreen, TagScreen
# from controllers.category_controller import CategoriesMenuScreen, CategoryScreen
# from controllers.article_controller import ArticlesMenuScreen, ArticleScreen
# from controllers.bookmark_controller import BookmarksMenuScreen
# from controllers.search_controller import SearchScreen
# from controllers.settings_controller import SettingsScreen
#
# from history import history
#
# from translator import translator

kivy.require('1.11.1')

# Config.set('kivy', 'default_font',
#            '''["Noto Sans",
#                "assets/fonts/NotoSans-Regular.ttf",
#                "assets/fonts/NotoSans-Italic.ttf",
#                "assets/fonts/NotoSans-Bold.ttf",
#                "assets/fonts/NotoSans-BoldItalic.ttf"
#               ]''')

# # Views components
# Builder.load_file('views/components/historyswitchguideprompt.kv')
# Builder.load_file('views/components/leaveappprompt.kv')
# Builder.load_file('views/components/navigationpanel.kv')
# Builder.load_file('views/components/screentitlebar.kv')
# Builder.load_file('views/components/tagslist.kv')
# Builder.load_file('views/components/categoriesmenu.kv')
# Builder.load_file('views/components/articlesmenu.kv')
# Builder.load_file('views/components/articlecontent.kv')
#
# # Screens views
# Builder.load_file('views/screens/guidesmenu_screen.kv')
# Builder.load_file('views/screens/guide_screen.kv')
# Builder.load_file('views/screens/tagsmenu_screen.kv')
# Builder.load_file('views/screens/tag_screen.kv')
# Builder.load_file('views/screens/articlesmenu_screen.kv')
# Builder.load_file('views/screens/categoriesmenu_screen.kv')
# Builder.load_file('views/screens/category_screen.kv')
# Builder.load_file('views/screens/bookmarksmenu_screen.kv')
#
# Builder.load_file('views/screens/article_screen.kv')
# Builder.load_file('views/screens/search_screen.kv')
# Builder.load_file('views/screens/settings_screen.kv')
#
# # Application root view
# Builder.load_string('''
# <ApplicationRoot>:
#     anim_type: 'slide_above_simple'
#     BoxLayout:
#         id: navigation_panel_container
#     ScreenManager:
#         id: manager
# ''')
#
#
# class NavigationPanel(ScrollView):
#     def __init__(self, is_active_guide, **kwargs):
#         super(NavigationPanel, self).__init__(**kwargs)
#         self.is_active_guide = is_active_guide
#
#
# class HistorySwitchGuidePrompt(Popup):
#     def __init__(self, guide_name, **kwargs):
#         super(HistorySwitchGuidePrompt, self).__init__(**kwargs)
#         self.guide_name = guide_name
#         guide_title = guides.by_name(self.guide_name)['title']
#         self.message = translator.translate('Switch to\n"[b]{}[/b]"\n guide to get previous screen?',
#                                             translator.active_lang_code).format(guide_title)
#
#     def switch_active_guide_for_screen(self):
#         guides.activate(self.guide_name)
#         history.switch_to_active_guide_history()
#         prev_screen_history_item = history.pop_active_guide_history_prev_screen()
#         app.root.show_prev_screen(*prev_screen_history_item)
#
#
# class LeaveAppPrompt(Popup):
#     pass
#
#
# class ApplicationRoot(NavigationDrawer):
#     is_active_guide = BooleanProperty()
#
#     def __init__(self, **kwargs):
#         super(ApplicationRoot, self).__init__(**kwargs)
#         self.esc_prompt = None
#         self.navigation_panel_container = self.ids.navigation_panel_container
#         self.sm = self.ids.manager
#         self.add_children_widgets()
#         self.settings_screen = SettingsScreen()
#         self.sm.add_widget(self.settings_screen)
#         self.is_active_guide = bool(guides.active_guide_name)
#         EventLoop.window.bind(on_keyboard=self.key_handler)
#         if guides.active_guide_name:
#             self.show_categoriesmenu_screen()
#         else:
#             self.show_guidesmenu_screen()
#
#     def remove_children_widgets(self):
#         self.navigation_panel_container.remove_widget(self.navigation_panel)
#         self.navigation_panel = None
#         self.sm.remove_widget(self.categoriesmenu_screen)
#         self.categoriesmenu_screen = None
#         self.sm.remove_widget(self.category_screen)
#         self.category_screen = None
#         self.sm.remove_widget(self.guidesmenu_screen)
#         self.guidesmenu_screen = None
#         self.sm.remove_widget(self.guide_screen)
#         self.guide_screen = None
#         self.sm.remove_widget(self.tagsmenu_screen)
#         self.tagsmenu_screen = None
#         self.sm.remove_widget(self.tag_screen)
#         self.tag_screen = None
#         self.sm.remove_widget(self.articlesmenu_screen)
#         self.articlesmenu_screen = None
#         self.sm.remove_widget(self.article_screen)
#         self.article_screen = None
#         self.sm.remove_widget(self.bookmarksmenu_screen)
#         self.bookmarksmenu_screen = None
#         self.sm.remove_widget(self.search_screen)
#         self.search_screen = None
#
#     def add_children_widgets(self):
#         self.navigation_panel = NavigationPanel(self.is_active_guide)
#         self.navigation_panel_container.add_widget(self.navigation_panel)
#         self.categoriesmenu_screen = CategoriesMenuScreen()
#         self.sm.add_widget(self.categoriesmenu_screen)
#         self.category_screen = CategoryScreen()
#         self.sm.add_widget(self.category_screen)
#         self.guidesmenu_screen = GuidesMenuScreen()
#         self.sm.add_widget(self.guidesmenu_screen)
#         self.guide_screen = GuideScreen()
#         self.sm.add_widget(self.guide_screen)
#         self.tagsmenu_screen = TagsMenuScreen()
#         self.sm.add_widget(self.tagsmenu_screen)
#         self.tag_screen = TagScreen()
#         self.sm.add_widget(self.tag_screen)
#         self.articlesmenu_screen = ArticlesMenuScreen()
#         self.sm.add_widget(self.articlesmenu_screen)
#         self.article_screen = ArticleScreen()
#         self.sm.add_widget(self.article_screen)
#         self.bookmarksmenu_screen = BookmarksMenuScreen()
#         self.sm.add_widget(self.bookmarksmenu_screen)
#         self.search_screen = SearchScreen()
#         self.sm.add_widget(self.search_screen)
#
#     def key_handler(self, window, key, *largs):
#         if key == 27:
#             if self.esc_prompt:
#                 self.esc_prompt.dismiss()
#                 self.esc_prompt = None
#                 return True
#             screen_content_names_dict = {
#                 'article': 'article_name',
#                 'category': 'category_name',
#                 'tag': 'tag_name'
#             }
#             if self.sm.current in screen_content_names_dict:
#                 screen_content_name_key = screen_content_names_dict[self.sm.current]
#                 if history.is_current_screen_active_guide_history_prev_screen(
#                         self.sm.current,
#                         getattr(self.sm.current_screen, screen_content_name_key)):
#                     history.pop_active_guide_history_prev_screen()
#             if history.active_guide_history_has_prev_screen():
#                 prev_screen_history_item = history.pop_active_guide_history_prev_screen()
#                 self.show_prev_screen(*prev_screen_history_item)
#             elif history.other_guide_history_has_prev_screen():
#                 other_guide_name = history.name_of_other_guide_with_prev_screen_in_history()
#                 self.esc_prompt = HistorySwitchGuidePrompt(other_guide_name)
#                 self.esc_prompt.open()
#             elif self.sm.current != 'categoriesmenu':
#                 self.sm.current = 'categoriesmenu'
#             else:
#                 self.esc_prompt = LeaveAppPrompt()
#                 self.esc_prompt.open()
#         return True
#
#     def show_guidesmenu_screen(self):
#         self.sm.current = 'guidesmenu'
#
#     def load_guide(self, guide_archive_paths):
#         guide_archive_path = guide_archive_paths[0]
#         guide_name = os.path.basename(guide_archive_path).split('.')[0]
#         if guides.load(guide_archive_path):
#             self.guidesmenu_screen.update_guidesmenu_items()
#         else:
#             guide_archive_name = os.path.basename(guide_archive_path)
#             GuideLoadFailedWarning(
#                 translator.translate('"[b]{}[/b]"\n guide load failed!',
#                                      translator.active_lang_code).format(guide_archive_name)).open()
#             guide_name = None
#         self.is_active_guide = bool(guides.active_guide_name)
#         if guides.active_guide_name == guide_name:
#             self.screens_history.append({guide_name: []})
#         elif guide_name is not None:
#             history.screens_history.insert(0, {guide_name: []})
#
#     def activate_guide(self, guide_name):
#         guides.activate(guide_name)
#         self.is_active_guide = bool(guides.active_guide_name)
#         history.switch_to_active_guide_history()
#
#     def show_guide_screen(self, guide_name):
#         if self.guide_screen.guide_name != guide_name:
#             prev_guide_screen = self.guide_screen
#             prev_guide_screen.name = 'prev_guide'
#             new_guide_screen = GuideScreen(name='guide')
#             new_guide_screen.update_guide_screen_items(guide_name)
#             self.sm.add_widget(new_guide_screen)
#             self.guide_screen = new_guide_screen
#             self.sm.remove_widget(prev_guide_screen)
#         self.sm.current = 'guide'
#
#     def unload_guide(self, guide_name):
#         guides.unload(guide_name)
#         history.remove_guide_history(guide_name)
#         self.guidesmenu_screen.update_guidesmenu_items()
#         self.show_guidesmenu_screen()
#         self.is_active_guide = bool(guides.active_guide_name)
#
#     def show_tagsmenu_screen(self):
#         if self.tagsmenu_screen.from_guide_name != guides.active_guide_name:
#             self.tagsmenu_screen.update_tagsmenu_items()
#             self.tagsmenu_screen.tagsmenu_widget.parent.scroll_y = 1
#         self.sm.current = 'tagsmenu'
#
#     def show_tag_screen(self, tag_name, push_in_history=True):
#         if (self.tag_screen.from_guide_name != guides.active_guide_name
#                 or self.tag_screen.tag_name != tag_name):
#             if not push_in_history:
#                 self.sm.transition.direction = 'left'
#             prev_tag_screen = self.tag_screen
#             prev_tag_screen.name = 'prev_tag'
#             new_tag_screen = TagScreen(name='tag')
#             new_tag_screen.update_tag_screen_items(tag_name)
#             self.sm.add_widget(new_tag_screen)
#             self.tag_screen = new_tag_screen
#             self.sm.remove_widget(prev_tag_screen)
#             if push_in_history:
#                 history.push_active_guide_history_screen('tag', tag_name)
#             else:
#                 self.sm.transition.direction = 'right'
#         self.sm.current = 'tag'
#
#     def show_categoriesmenu_screen(self):
#         if self.categoriesmenu_screen.from_guide_name != guides.active_guide_name:
#             self.categoriesmenu_screen.update_categoriesmenu_items()
#             self.categoriesmenu_screen.ids.categoriesmenu_container.scroll_y = 1
#         self.sm.current = 'categoriesmenu'
#
#     def show_category_screen(self, category_name, push_in_history=True):
#         if (self.category_screen.from_guide_name != guides.active_guide_name
#                 or self.category_screen.category_name != category_name):
#             if not push_in_history:
#                 self.sm.transition.direction = 'left'
#             prev_category_screen = self.category_screen
#             prev_category_screen.name = 'prev_category'
#             new_category_screen = CategoryScreen(name='category')
#             new_category_screen.update_category_screen_items(category_name)
#             self.sm.add_widget(new_category_screen)
#             self.category_screen = new_category_screen
#             self.sm.remove_widget(prev_category_screen)
#             if push_in_history:
#                 history.push_active_guide_history_screen('category', category_name)
#             else:
#                 self.sm.transition.direction = 'right'
#         self.sm.current = 'category'
#
#     def show_articlesmenu_screen(self):
#         if self.articlesmenu_screen.from_guide_name != guides.active_guide_name:
#             self.articlesmenu_screen.update_articlesmenu_items()
#             self.articlesmenu_screen.ids.articlesmenu_container.scroll_y = 1
#         self.sm.current = 'articlesmenu'
#
#     def show_article_screen(self, article_name, push_in_history=True):
#         if (self.article_screen.from_guide_name != guides.active_guide_name
#                 or self.article_screen.article_name != article_name):
#             if not push_in_history:
#                 self.sm.transition.direction = 'left'
#             prev_article_screen = self.article_screen
#             prev_article_screen.name = 'prev_article'
#             new_article_screen = ArticleScreen(name='article')
#             new_article_screen.update_article_screen_items(article_name)
#             self.sm.add_widget(new_article_screen)
#             self.article_screen = new_article_screen
#             self.sm.remove_widget(prev_article_screen)
#             if push_in_history:
#                 history.push_active_guide_history_screen('article', article_name)
#             else:
#                 self.sm.transition.direction = 'right'
#         self.sm.current = 'article'
#
#     def show_prev_screen(self, screen_name, screen_content_name):
#         if screen_name == 'article':
#             self.show_article_screen(screen_content_name, False)
#         elif screen_name == 'category':
#             self.show_category_screen(screen_content_name, False)
#         elif screen_name == 'tag':
#             self.show_tag_screen(screen_content_name, False)
#
#
#     def show_bookmarksmenu_screen(self):
#         self.bookmarksmenu_screen.update_bookmarksmenu_items()
#         self.bookmarksmenu_screen.ids.bookmarksmenu_widget.parent.scroll_y = 1
#         self.sm.current = 'bookmarksmenu'
#
#     def remove_bookmark(self, article_name):
#         bookmarks.remove(article_name)
#         self.bookmarksmenu_screen.update_bookmarksmenu_items()
#
#     def show_search_screen(self):
#         self.sm.current = 'search'
#
#     def show_settings_screen(self):
#         self.sm.current = 'settings'

from kivy.uix.label import Label

from models import GuidesModel
from settings import app_settings

class ApplicationRoot(Label):
    def __init__(self, **kwargs):
        super(ApplicationRoot, self).__init__(**kwargs)
        self.text = 'Application started!'


class XenialApp(App):
    # GUIDES_DIR = guides.GUIDES_DIR
    # lang_code = StringProperty('en')

    # def on_lang_code(self, instance, value):
    #     translator.active_lang_code = self.lang_code
    #     self.root.settings_screen.name = 'old_settings'
    #     new_settings_screen = SettingsScreen()
    #     self.root.sm.add_widget(new_settings_screen)
    #     self.root.sm.current = 'settings'
    #     self.root.sm.remove_widget(self.root.settings_screen)
    #     self.root.settings_screen = new_settings_screen
    #     self.root.remove_children_widgets()
    #     self.root.add_children_widgets()
    #     self.root.show_settings_screen()

    def __init__(self, **kwargs):
        super(XenialApp, self).__init__(**kwargs)
        self.guides = GuidesModel()
        if app_settings.exists('active_guide_name'):
            self.active_guide_name = app_settings.get('active_guide_name')
        elif self.guides.guides_list:
            self.active_guide_name = self.guides.guides_list[0]['name']
            app_settings.set('active_guide_name', self.active_guide_name)
        else:
            self.active_guide_name = ''
        if app_settings.exists('app_lang_code'):
            self.app_lang_code = app_settings.get('app_lang_code')
        else:
            self.app_lang_code = 'en'

        # new_guides_list_item = self.guides.import_from_archive('guides/dummy.zip')
        # print(new_guides_list_item)

        for guides_list_item in self.guides.guides_list:
            print(guides_list_item)
        # print(self.guides.guides_list)
        # for guides_list_item in self.guides.guides_list:
        #     print(guides_list_item)
        guide_name = self.guides.guides_list[0]['name']
        guide = self.guides.guide_by_name(guide_name)
        print(guide.guide_name)
        print(guide.categories_list())

    def build(self):
        self.root = ApplicationRoot()
        return self.root

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
