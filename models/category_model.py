"""
Category model
==============
Contains Category model class.
"""

from models.models_constants import *


class Category:
    """
    Provides all data stored in a guide database corresponding to a category of given `category_id`
    """

    def __init__(self, conn, category_id):
        self.conn = conn
        (self.category_id, self.category_name,
         self.category_icon, self.category_description) = self._fetchone_from_categories_by_id(category_id)

    def tags_list(self):
        """ Returns list of tags assigned to the category. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT t.id, t.name FROM tags AS t
                        INNER JOIN tags_categories AS tc
                        ON t.id=tc.tag_id
                        WHERE tc.category_id=?
                        ORDER BY t.name; """, (self.category_id,))
        tags_rows = cur.fetchall()
        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def articles_list(self):
        """ Returns list of items containing basic information about articles the category contains.
            All of listed article have assigned all tags which are assigned to the category. """

        category_tags_ids = self._get_category_tags_ids(self.category_id)
        articles_rows = self._get_articles_rows()
        category_articles_rows = []
        for article_row in articles_rows:
            article_id = article_row[0]
            article_tags_ids = self._get_article_tags_ids(article_id)
            if set(category_tags_ids) <= set(article_tags_ids):
                category_articles_rows.append(article_row)
        return [dict(zip(ARTICLES_KEYS, row)) for row in category_articles_rows]

    def related_categories_list(self):
        """ Returns list of items containing basic information about categories related to the category corresponding to
            the class instance. For a category, to be considered related to the category, both categories has to share
            at least one tag assigned to them.
            Categories are sorted from the most similar (shares most tags with the category) to the least similar. """

        category_tags_ids = self._get_category_tags_ids(self.category_id)
        categories_ids = self._get_categories_ids()
        related_categories_num_shared_tags = {}
        for inspected_category_id in categories_ids:
            if inspected_category_id == self.category_id:
                continue
            inspected_category_tags_ids = self._get_category_tags_ids(inspected_category_id)
            num_shared_tags = len(set(category_tags_ids) & set(inspected_category_tags_ids))
            if num_shared_tags > 0:
                related_categories_num_shared_tags[inspected_category_id] = num_shared_tags
        related_categories_ids = list(related_categories_num_shared_tags.keys())
        related_categories_rows = [row + (related_categories_num_shared_tags[row[0]],)
                                   for row in self._fetchall_related_categories(related_categories_ids)]
        return sorted([dict(zip(RELATED_CATEGORIES_KEYS, row)) for row in related_categories_rows],
                      key=lambda c: c['category_num_shared_tags'], reverse=True)

    def _fetchone_from_categories_by_id(self, category_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM categories WHERE id=?; """, (category_id,))
        return cur.fetchone()

    def _get_category_tags_ids(self, category_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT tag_id FROM tags_categories
                        WHERE category_id=?; """, (category_id,))
        return [row[0] for row in cur.fetchall()]

    def _get_articles_rows(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM articles; """)
        return cur.fetchall()

    def _get_article_tags_ids(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT tag_id FROM tags_articles
                        WHERE article_id=?; """, (article_id,))
        return [row[0] for row in cur.fetchall()]

    def _get_categories_ids(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT id FROM categories; """)
        return [row[0] for row in cur.fetchall()]

    def _fetchall_related_categories(self, related_categories_ids):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM categories
                        WHERE id in ({}); """.format(','.join('?' * len(related_categories_ids))),
                    related_categories_ids)
        return cur.fetchall()
