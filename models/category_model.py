import os
import json

from .models import guides, articles


class CategoryModel:
    @staticmethod
    def all():
        """Return a list of all categories in the active guide"""
        if guides.active_guide is None:
            return []
        categories_list_filename = os.path.join(guides.active_guide_path, 'categories.json')
        with open(categories_list_filename, 'r') as categories_list_file:
            categories_list = json.load(categories_list_file)
        return categories_list

    @classmethod
    def by_id(cls, category_id):
        """Return the active guide category data retrieved by its id"""
        categories_list = cls.all()
        if len(categories_list) == 0:
            return None
        category = next(list_item for list_item in categories_list if list_item['id'] == category_id)
        return category

    @classmethod
    def related_categories(cls, category_id):
        """Return a list of the active guide categories related to the active guide category"""
        category = cls.by_id(category_id)
        shared_tags_categories = []
        for tested_category in cls.all():
            if tested_category['id'] == category_id:
                continue
            num_shared_tags = len(set(category['tags']) & set(tested_category['tags']))
            if num_shared_tags > 0:
                shared_tags_categories.append((num_shared_tags, tested_category['name'], tested_category))
        related_categories = [tags_category[2] for tags_category in sorted(shared_tags_categories)]
        return related_categories

    @classmethod
    def related_articles(cls, category_id):
        """Return a list of the active guide articles related to the active guide category"""
        category = cls.by_id(category_id)
        related_articles = []
        for tested_article in articles.all():
            if set(tested_article['tags']) > set(category['tags']):
                related_articles.append(tested_article)
        related_articles.sort(key=lambda a: a['title'])
        return related_articles
