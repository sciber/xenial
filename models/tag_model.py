from .models import guides, articles, categories


class TagModel:
    @staticmethod
    def all():
        """Return all tags for the active guide"""
        if guides.active_guide is None:
            return []
        guide_tags = guides.active_guide.tags
        return guide_tags

    @staticmethod
    def related_categories(tag_name):
        """Return all active guide categories to which the tag is assigned"""
        related_categories = []
        for tested_category in categories.all():
            if tag_name in tested_category['tags']:
                related_categories.append(tested_category)
        return sorted(related_categories, key=lambda c: c['name'])

    @staticmethod
    def related_articles(tag_name):
        """Return all active guides articles to which the tag is assigned """
        related_articles = []
        for tested_article in articles.all():
            if tag_name in tested_article['tags']:
                related_articles.append(tested_article)
        return sorted(related_articles, key=lambda a: a['title'])
