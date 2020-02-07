from models.models_constants import *


class Tag:
    def __init__(self, conn, tag_id):
        self.conn = conn
        self.tag_id, self.tag_name = self._fetchone_from_tags_by_id(tag_id)

    def tagged_categories_list(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM categories 
                        WHERE id IN (
                            SELECT category_id from tags_categories
                            WHERE tag_id=? 
                        ); """, (self.tag_id,))
        categories_rows = cur.fetchall()
        return [dict(zip(CATEGORIES_KEYS, row)) for row in categories_rows]

    def num_tagged_categories(self):
        cur = self.conn.cursor()
        cur.execute("""" SELECT COUNT(id) FROM categories
                         WHERE id IN (
                             SELECT category_id FROM tags_categories
                             WHERE tag_id=?
                         ); """, (self.tag_id,))
        return cur.fetchone()[0]

    def tagged_articles_list(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM articles
                        WHERE id IN (
                            SELECT article_id FROM tags_articles
                            WHERE tag_id=?
                        ); """, (self.tag_id,))
        articles_rows = cur.fetchall()
        return [dict(zip(ARTICLES_KEYS, row)) for row in articles_rows]

    def num_tagged_articles(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT COUNT(id) FROM articles
                        WHERE id IN (
                            SELECT article_id FROM tags_articles
                            WHERE tag_id=?
                        ); """, (self.tag_id,))
        return cur.fetchone()[0]

    def _fetchone_from_tags_by_id(self, tag_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM tags WHERE id=?; """, (tag_id,))
        return cur.fetchone()
