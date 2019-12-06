import os
import shutil
import tarfile
import json
from datetime import datetime
from functools import reduce


class GuideModel:
    GUIDES_DIR = 'guides'
    guides_list = []
    active_guide_name = ''
    active_guide_path = ''

    def __init__(self):
        guides_list_filename = os.path.join(self.GUIDES_DIR, 'guides.json')
        with open(guides_list_filename, 'r') as guides_list_file:
            self.guides_list = json.load(guides_list_file)
        if len(self.guides_list) > 0:
            self.active_guide_name = next(list_item for list_item in self.guides_list if list_item['is_active'])['name']
            self.active_guide_path = os.path.join(self.GUIDES_DIR, self.active_guide_name)

    def all(self):
        """Return a list of all guides"""
        return self.guides_list

    def by_name(self, guide_name):
        """Return a guide data by its name"""
        guide = next(list_item for list_item in self.guides_list if list_item['name'] == guide_name)
        return guide

    def activate(self, guide_name):
        """Activate a guide of given name"""
        for list_item in self.guides_list:
            list_item['is_active'] = list_item['name'] == guide_name
            if list_item['is_active']:
                self.active_guide_name = list_item['name']
                self.active_guide_path = os.path.join(self.GUIDES_DIR, self.active_guide_name)
        with open(os.path.join(self.GUIDES_DIR, 'guides.json'), 'w') as guides_list_file:
            json.dump(self.guides_list, guides_list_file, indent=4)

    def load(self, guide_archive_path):
        """Load a guide from a corresponding archive"""
        guides_json = os.path.join(self.GUIDES_DIR, 'guides.json')
        guides_json_backup = os.path.join(self.GUIDES_DIR, 'guides.backup')
        shutil.copyfile(guides_json, guides_json_backup)
        guide_name = os.path.basename(guide_archive_path).split('.')[0]
        guide_dir = os.path.join(self.GUIDES_DIR, guide_name)
        try:
            if os.path.exists(guide_dir):
                self.unload(guide_name)
            os.mkdir(guide_dir)
            with tarfile.open(guide_archive_path, 'r:gz') as tar:
                tar.extractall(guide_dir)
            with open(os.path.join(guide_dir, 'guide.json'), 'r') as guide_file:
                guide = json.load(guide_file)
            guide['is_active'] = len(self.guides_list) == 0
            self.guides_list.append(guide)
            with open(guides_json, 'w') as guides_list_file:
                json.dump(self.guides_list, guides_list_file, indent=4)
            if guide['is_active']:
                self.activate(guide['name'])
        except:
            if os.path.exists(guide_dir):
                shutil.rmtree(guide_dir)
            os.remove(guides_json)
            shutil.copyfile(guides_json_backup, guides_json)
            result = False
        else:
            result = True
        finally:
            os.remove(guides_json_backup)
        return result

    def unload(self, guide_name):
        """Remove the guide and all its content"""
        guide_dir = os.path.join(self.GUIDES_DIR, guide_name)
        shutil.rmtree(guide_dir)
        was_active_guide = self.active_guide_name == guide_name
        for idx, list_item in enumerate(self.guides_list):
            if list_item['name'] == guide_name:
                del self.guides_list[idx]
        if was_active_guide:
            if len(self.guides_list) > 0:
                self.activate(self.guides_list[0]['name'])
            else:
                self.active_guide_name = ''
                self.active_guide_path = ''
        with open(os.path.join(self.GUIDES_DIR, 'guides.json'), 'w') as guides_list_file:
            json.dump(self.guides_list, guides_list_file, indent=4)


class TagModel:
    def __init__(self):
        pass

    @staticmethod
    def all():
        """Return all tags for the active guide"""
        if not guides.active_guide_name:
            return []
        active_guide = guides.by_name(guides.active_guide_name)
        guide_tags = active_guide['tags']
        return guide_tags

    def tagged_categories(self, tag_name):
        """Return all active guide categories to which the tag is assigned"""
        related_categories = []
        for tested_category in categories.all():
            if tag_name in tested_category['tags']:
                related_categories.append(tested_category)
        return sorted(related_categories, key=lambda c: c['name'])

    def tagged_articles(self, tag_name):
        """Return all active guides articles to which the tag is assigned """
        related_articles = []
        for tested_article in articles.all():
            if tag_name in tested_article['tags']:
                related_articles.append(tested_article)
        return sorted(related_articles, key=lambda a: a['title'])


class CategoryModel:
    def __init__(self):
        pass

    @staticmethod
    def all():
        """Return a list of all categories in the active guide"""
        if not guides.active_guide_name:
            return []
        categories_list_filename = os.path.join(guides.active_guide_path, 'categories.json')
        with open(categories_list_filename, 'r') as categories_list_file:
            categories_list = json.load(categories_list_file)
        return categories_list

    def by_name(self, category_name):
        """Return the active guide category data retrieved by its name"""
        categories_list = self.all()
        if len(categories_list) == 0:
            return None
        category = next(list_item for list_item in categories_list if list_item['name'] == category_name)
        return category

    def related_categories(self, category_name):
        """Return a list of the active guide categories related to the active guide category"""
        category = self.by_name(category_name)
        shared_tags_categories = []
        for tested_category in self.all():
            if tested_category['name'] == category_name:
                continue
            num_shared_tags = len(set(category['tags']) & set(tested_category['tags']))
            if num_shared_tags > 0:
                shared_tags_categories.append((num_shared_tags, tested_category['name'], tested_category))
        related_categories = [tags_category[2] for tags_category in sorted(shared_tags_categories)]
        return related_categories

    def related_articles(self, category_name):
        """Return a list of the active guide articles related to the active guide category"""
        category = self.by_name(category_name)
        related_articles = []
        for tested_article in articles.all():
            if set(tested_article['tags']) > set(category['tags']):
                related_articles.append(tested_article)
        related_articles.sort(key=lambda a: a['title'])
        return related_articles


class ArticleModel:
    def __init__(self):
        pass

    @staticmethod
    def all():
        """Return a list of all articles in the active guide"""
        if not guides.active_guide_name:
            return []
        articles_list_filename = os.path.join(guides.active_guide_path, 'articles.json')
        with open(articles_list_filename, 'r') as articles_list_file:
            articles_list = json.load(articles_list_file)
        return articles_list

    def by_name(self, article_name):
        """Return the active guide article data retrieved by its name"""
        articles_list = self.all()
        if len(articles_list) == 0:
            return None
        article = next(list_item for list_item in articles_list if list_item['name'] == article_name)
        return article

    def content(self, article_name):
        """Return the active guide article content"""
        articles_list = self.all()
        if len(articles_list) == 0:
            return None
        article_content_filename = os.path.join(guides.active_guide_path, 'content', f'{article_name}.json')
        with open(article_content_filename, 'r') as article_content_file:
            article_content = json.load(article_content_file)
        return article_content

    def related_categories(self, article_name):
        """Return a list of the active guide categories related to the active guide article"""
        article = self.by_name(article_name)
        related_categories = []
        for tested_category in categories.all():
            if set(tested_category['tags']) < set(article['tags']):
                related_categories.append(tested_category)
        related_categories.sort(key=lambda c: c['name'])
        return related_categories

    def related_articles(self, article_name):
        """Return a list of the active guide articles related to the active guide article"""
        article = self.by_name(article_name)
        shared_tags_articles = []
        for tested_article in self.all():
            if tested_article['name'] == article_name:
                continue
            num_shared_tags = len(set(article['tags']) & set(tested_article['tags']))
            if num_shared_tags > 0:
                shared_tags_articles.append((num_shared_tags, tested_article['title'], tested_article))
        related_articles = [tags_article[2] for tags_article in sorted(shared_tags_articles)]
        return related_articles


class BookmarkModel:
    def __init__(self):
        pass

    @staticmethod
    def all():
        """Return a list of the active guide bookmarks"""
        if not guides.active_guide_name:
            return []
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'r') as bookmark_file:
            bookmarks_list = json.load(bookmark_file)
        return bookmarks_list

    def is_article_bookmarked(self, article_name):
        """Return whether is the active guide article bookmarked"""
        return reduce(lambda x, y: x or (y['article_name'] == article_name), self.all(), False)

    def bookmarked_articles(self):
        """Return a list of all bookmarked articles in the active guided"""
        bookmarked_articles_names = [bookmark['article_name'] for bookmark in self.all()]
        return (article for article in articles.all() if article['name'] in bookmarked_articles_names)

    def add(self, article_name):
        """Add the active guide article to the active guide bookmarks"""
        bookmarks_list = self.all()
        new_bookmark = {'article_name': article_name, 'created_at': str(datetime.now())}
        bookmarks_list.append(new_bookmark)
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'w') as bookmark_file:
            json.dump(bookmarks_list, bookmark_file, indent=4)

    def remove(self, article_name):
        """Remove the active guide article from the active guide bookmarks"""
        bookmarks_list = self.all()
        for bookmark_idx, bookmark in enumerate(bookmarks_list):
            if bookmark['article_name'] == article_name:
                del bookmarks_list[bookmark_idx]
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'w') as bookmark_file:
            json.dump(bookmarks_list, bookmark_file, indent=4)


guides = GuideModel()
tags = TagModel()
categories = CategoryModel()
articles = ArticleModel()
bookmarks = BookmarkModel()
