"""
Guide model
===========
Contains Guide model class.
"""

import datetime
import json
import os
import sqlite3

from models.models_constants import *
from models.article_model import Article
from models.tag_model import Tag
from models.category_model import Category


class Guide:
    """
    Provides all available guide data from `guide.db` database and `guide.json` file
    :attr: `conn` is a sqlite3 database connection to the guide database.
    """

    conn = None

    def __init__(self, guide_name):
        self.conn = sqlite3.connect(os.path.join(GUIDES_DIR, guide_name, 'guide.db'))
        with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json')) as f:
            guide = json.load(f)

        self.guide_name = guide_name
        self.guide_version = guide['guide_format_version']
        self.guide_icon = guide['guide_icon']
        self.guide_title = guide['guide_title']
        self.guide_description = guide['guide_description']
        self.guide_lang = guide['guide_lang']
        self.guide_from_place = guide['guide_from_place']
        self.guide_to_place = guide['guide_to_place']
        self.guide_content = guide['guide_content']

    def articles_list(self):
        """ Returns list of the guide articles information. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM articles; """)
        articles_rows = cur.fetchall()
        return [dict(zip(ARTICLES_KEYS, row)) for row in articles_rows]

    def article_by_id(self, article_id):
        """ Returns instance of Article model corresponding to the article of given `article_id`. """

        return Article(self.conn, article_id)

    def search_articles(self, query):
        """ Search articles textual data for presence of given `query` text. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT article_id, block_order, block_type, block_id, 
                            highlight(article_block_search, 4, '[color=#24AF24]', '[/color]')
                        FROM article_block_search
                        WHERE article_block_search MATCH ? ORDER BY rank;""", query)
        return cur.fetchall()

    def bookmarks_list(self):
        """ Returns list of bookmarks assigned to the guide articles. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT b.id, b.created_at, b.article_id, a.name, a.icon, a.title, a.synopsis
                        FROM bookmarks AS b
                        INNER JOIN articles AS a
                        ON b.article_id=a.id 
                        ORDER BY b.created_at; """)
        bookmarked_articles_rows = cur.fetchall()
        return [dict(zip(BOOKMARKS_KEYS, row)) for row in bookmarked_articles_rows]

    def add_bookmark(self, article_id):
        """ Adds a bookmark corresponding to the article of given `article_id` to the bookmarks list.
            Should raise exception when a bookmark of the articles already exists in the database. """

        cur = self.conn.cursor()
        cur.execute(""" INSERT INTO bookmarks (article_id, created_at) VALUES (?, ?); """,
                    (article_id, str(datetime.datetime.now())))
        self.conn.commit()

    def delete_bookmark(self, bookmark_id):
        """ Deletes a bookmark of given `bookmark_id`.
            Raises exception if the bookmark does not exist. """

        cur = self.conn.cursor()
        cur.execute(""" DELETE FROM bookmarks WHERE id=?; """, (bookmark_id,))
        self.conn.commit()

    def tags_list(self):
        """ Returns list of tags assigned to the guide articles and articles categories. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT t.id, t.name, IFNULL(tc.count_categories, 0), IFNULL(ta.count_articles, 0) 
                        FROM tags AS t
                        LEFT JOIN (
                            SELECT tag_id, COUNT(article_id) AS count_articles FROM tags_articles
                            GROUP BY tag_id) AS ta
                        ON t.id=ta.tag_id
                        LEFT JOIN (
                            SELECT tag_id, COUNT(category_id) AS count_categories FROM tags_categories
                            GROUP BY tag_id) AS tc
                        ON t.id=tc.tag_id
                        ORDER BY ta.count_articles DESC, tc.count_categories DESC; """)
        tags_rows = cur.fetchall()
        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def tag_by_id(self, tag_id):
        """ Returns instance of Tag model corresponding to the tag of given `tag_id`. """

        return Tag(self.conn, tag_id)

    def categories_list(self):
        """ Returns list of items describing all categories of the guide articles
            (based on tags they are labeled with). """

        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM categories; """)
        categories_rows = cur.fetchall()
        return [dict(zip(CATEGORIES_KEYS, row)) for row in categories_rows]

    def category_by_id(self, category_id):
        """ Returns instance of Category model corresponding to the category of given `category_id`. """

        return Category(self.conn, category_id)
