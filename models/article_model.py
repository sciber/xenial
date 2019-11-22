import os
import json

from .models import guides, categories


class ArticleModel:
    @staticmethod
    def all():
        """Return a list of all articles in the active guide"""
        if guides.active_guide is None:
            return []
        articles_list_filename = os.path.join(guides.active_guide_path, 'articles.json')
        with open(articles_list_filename, 'r') as articles_list_file:
            articles_list = json.load(articles_list_file)
        return articles_list

    @classmethod
    def by_id(cls, article_id):
        """Return the active guide article data retrieved by its id"""
        articles_list = cls.all()
        if len(articles_list) == 0:
            return None
        article = next(list_item for list_item in articles_list if list_item['id'] == article_id)
        article_content_filename = os.path.join(guides.active_guide_path, 'content', f'{article_id}.json')
        with open(article_content_filename, 'r') as article_content_file:
            article_content = json.load(article_content_file)
        article['content'] = article_content
        return article

    @classmethod
    def related_categories(cls, article_id):
        """Return a list of the active guide categories related to the active guide article"""
        article = cls.by_id(article_id)
        related_categories = []
        for tested_category in categories.all():
            if set(tested_category['tags']) < set(article['tags']):
                related_categories.append(tested_category)
        related_categories.sort(key=lambda c: c['category'])
        return related_categories

    @classmethod
    def related_articles(cls, article_id):
        """Return a list of the active guide articles related to the active guide article"""
        article = cls.by_id(article_id)
        shared_tags_articles = []
        for tested_article in cls.all():
            if tested_article['id'] == article_id:
                continue
            num_shared_tags = len(set(article['tags']) & set(tested_article['tags']))
            if num_shared_tags > 0:
                shared_tags_articles.append((num_shared_tags, tested_article['title'], tested_article))
        related_articles = [tags_article[2] for tags_article in sorted(shared_tags_articles)]
        return related_articles
