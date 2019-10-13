from functools import reduce

import kivy

from kivy.config import Config
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
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


class CategoriesMenuItem(Button):
    def __init__(self, category, **kwargs):
        super(CategoriesMenuItem, self).__init__(**kwargs)
        self.icon = 'guides/dummy/icons/categories/' + category['icon']
        self.name = category['name']


class CategoriesMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for category in app.guide['categories']:
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
    def __init__(self, icon, name, **kwargs):
        super(CategoryRelatedCategoriesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.name = name


class CategoryRelatedCategoriesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, categories, **kwargs):
        super(CategoryRelatedCategoriesMenu, self).__init__(**kwargs)

        for category in categories:
            icon = 'guides/dummy/icons/categories/' + category['icon']
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
            icon = 'guides/dummy/icons/articles/' + article['icon']
            menu_item = CategoryArticlesMenuItem(icon=icon,
                                                 title=article['title'],
                                                 synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class CategoryScreen(Screen):
    def _get_related_categories(self):
        tagged_categories = []
        for category in app.guide['categories']:
            if category['name'] == self.category_name:
                continue

            categories_shared_tags = list(set(category['tags']) & set(self.category_assigned_tags))
            if len(categories_shared_tags) > 0:
                tagged_categories.append((category, len(categories_shared_tags)))

            tagged_categories.sort(key=lambda c: c[1], reverse=True)
            related_categories = [item[0] for item in tagged_categories]
        return related_categories

    def _get_articles(self):
        tagged_articles = [a for a in app.guide['articles']  if all(t in a['tags'] for t in self.category_assigned_tags)]
        return tagged_articles

    def __init__(self, category_name, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        category = next(c for c in app.guide['categories'] if c['name'] == category_name)
        self.category_icon = 'guides/dummy/icons/categories/' + category['icon']
        self.category_name = category_name
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
        return reduce(lambda x, y: x + 1 if self.name in y['tags'] else x, app.guide['articles'], 0)

    def _get_num_tagged_categories(self):
        return reduce(lambda x, y: x + 1 if self.name in y['tags'] else x, app.guide['categories'], 0)

    def __init__(self, tag, **kwargs):
        super(TagsMenuItem, self).__init__(**kwargs)
        self.name = tag
        self.num_articles = self._get_num_tagged_articles()
        self.num_categories = self._get_num_tagged_categories()


class TagsMenuScreen(Screen):
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for tag in app.guide['tags']:
            tag_button = TagsMenuItem(tag=tag)
            self.items_container.add_widget(tag_button)

    def __init__(self, **kwargs):
        super(TagsMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


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
            icon = 'guides/dummy/icons/categories/' + category['icon']
            menu_item = TaggedCategoriesMenuItem(icon=icon,
                                                 name=category['name'])
            self.items_container.add_widget(menu_item)


class TaggedArticlesMenuItem(Button):
    def __init__(self, icon, title, synopsis, **kwargs):
        super(TaggedArticlesMenuItem, self).__init__(**kwargs)
        self.icon = icon
        self.title = title
        self.synopsis = synopsis


class TaggedArticlesMenu(BoxLayout):
    items_container = ObjectProperty()

    def __init__(self, articles, **kwargs):
        super(TaggedArticlesMenu, self).__init__(**kwargs)
        for article in articles:
            icon = 'guides/dummy/icons/articles/' + article['icon']
            menu_item = TaggedArticlesMenuItem(icon=icon,
                                               title=article['title'],
                                               synopsis=article['synopsis'])
            self.items_container.add_widget(menu_item)


class TagScreen(Screen):
    def _get_tagged_categories(self):
        tagged_categories = [c for c in app.guide['categories'] if self.tag_name in c['tags']]
        return tagged_categories

    def _get_tagged_articles(self):
        tagged_articles = [a for a in app.guide['articles'] if self.tag_name in a['tags']]
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
    items_container = ObjectProperty()

    def _post_init(self, dt):
        for bookmark in app.guide['bookmarks']:
            bookmarks_menu_item = BookmarksMenuItem(bookmark=bookmark)
            self.items_container.add_widget(bookmarks_menu_item)

    def __init__(self, **kwargs):
        super(BookmarksMenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._post_init)


class ApplicationRoot(NavigationDrawer):
    def show_category_screen(self, category_name):
        screen_manager = self.ids.manager
        screens_names = [screen.name for screen in screen_manager.screens]
        screen_name = 'Category: ' + category_name
        if screen_name not in screens_names:
            category_screen = CategoryScreen(name=screen_name,
                                             category_name=category_name)
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


class XenialApp(App):
    from guides.dummy.guide import guide

    def build(self):
        return ApplicationRoot()

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
