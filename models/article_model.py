"""
Article model
=============
Contains Article model class.
"""

from models.models_constants import *


class Article:
    """
    Provides all data stored in a guide database corresponding to an article of given `article_id`
    """

    def __init__(self, conn, article_id):
        self.conn = conn
        (self.article_id, self.article_name, self.article_icon,
         self.article_title, self.article_synopsis) = self._fetchone_from_articles_by_id(article_id)

    def content_blocks_list(self):
        """ Returns blocks forming the article content ordered by the `block['content_order']`. """

        subtitle_blocks_list = self._get_article_subtitle_blocks(self.article_id)
        paragraph_blocks_list = self._get_article_paragraph_blocks(self.article_id)
        image_blocks_list = self._get_article_image_blocks(self.article_id)
        audio_blocks_list = self._get_article_audio_blocks(self.article_id)
        video_blocks_list = self._get_article_video_blocks(self.article_id)
        sorted_content_blocks_list = sorted(subtitle_blocks_list + paragraph_blocks_list
                                            + image_blocks_list + audio_blocks_list
                                            + video_blocks_list, key=lambda block: block['content_order'])
        return sorted_content_blocks_list

    def bookmark(self):
        """ Returns bookmark data of the article if the article is bookmarked;
            returns None if the article is not bookmarked. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT id, created_at FROM bookmarks
                        WHERE article_id=?; """, (self.article_id,))
        bookmark_row = cur.fetchone()
        if bookmark_row is None:
            return None
        return dict(zip(('bookmark_id', 'bookmark_created_at'), bookmark_row))

    def tags_list(self):
        """ Returns list of tags assigned to the articles. """

        cur = self.conn.cursor()
        cur.execute(""" SELECT t.id, t.name FROM tags AS t
                        INNER JOIN tags_articles AS ta
                        ON t.id=ta.tag_id
                        WHERE ta.article_id=?; """, (self.article_id,))
        tags_rows = cur.fetchall()
        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def related_articles_list(self):
        """ Returns list of items containing basic information about articles related to the article corresponding to
            the class instance. To be an article considered related to the article, both articles hast to share at least
            one tag assigned to them.
            Articles are sorted from the most similar (shares most tags with the article) to the least similar. """

        article_tags_ids = self._get_article_tags_ids(self.article_id)
        articles_ids = self._get_articles_ids()
        related_articles_num_shared_tags = {}
        for inspected_article_id in articles_ids:
            if inspected_article_id == self.article_id:
                continue
            inspected_article_tags_ids = self._get_article_tags_ids(inspected_article_id)
            num_shared_tags = len(set(article_tags_ids) & set(inspected_article_tags_ids))
            if num_shared_tags > 0:
                related_articles_num_shared_tags[inspected_article_id] = num_shared_tags
        related_articles_ids = list(related_articles_num_shared_tags.keys())
        related_articles_rows = [row + (related_articles_num_shared_tags[row[0]],)
                                 for row in self._fetchall_related_articles(related_articles_ids)]
        return sorted([dict(zip(RELATED_ARTICLES_KEYS, row)) for row in related_articles_rows],
                      key=lambda a: a['article_num_shared_tags'], reverse=True)

    def categories_list(self):
        """ Returns list of items containing basic information about categories containing the article.
            All tags in listed category have to be also assigned to the article. """

        article_tags_ids = self._get_article_tags_ids(self.article_id)
        categories_rows = self._get_categories_rows()
        article_categories_rows = []
        for category_row in categories_rows:
            category_id = category_row[0]
            category_tags_ids = self._get_category_tags_ids(category_id)
            if set(category_tags_ids) <= set(article_tags_ids):
                article_categories_rows.append(category_row)
        return [dict(zip(CATEGORIES_KEYS, row)) for row in article_categories_rows]

    def _fetchone_from_articles_by_id(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM articles WHERE id=?; """, (article_id,))
        return cur.fetchone()

    def _get_article_subtitle_blocks(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT ab.block_id, ab.block_type, ab.block_order, subtitles.subtitle_text
                        FROM articles_blocks AS ab
                        LEFT JOIN subtitle_blocks AS subtitles
                        ON ab.block_id=subtitles.id
                        WHERE ab.article_id=? AND ab.block_type='subtitle'; """, (article_id,))
        subtitle_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_SUBTITLE_BLOCKS_KEYS, row)) for row in subtitle_blocks_rows]

    def _get_article_paragraph_blocks(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT ab.block_id, ab.block_type, ab.block_order, paragraphs.paragraph_text
                        FROM articles_blocks AS ab
                        LEFT JOIN paragraph_blocks AS paragraphs
                        ON ab.block_id=paragraphs.id
                        WHERE ab.article_id=? AND ab.block_type='paragraph'; """, (article_id,))
        paragraph_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_PARAGRAPH_BLOCKS_KEYS, row)) for row in paragraph_blocks_rows]

    def _get_article_image_blocks(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT ab.block_id, ab.block_type, ab.block_order, images.image_source, images.caption_text
                        FROM articles_blocks AS ab
                        LEFT JOIN image_blocks AS images
                        ON ab.block_id=images.id
                        WHERE ab.article_id=? and ab.block_type='image'; """, (article_id,))
        image_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_IMAGE_BLOCKS_KEYS, row)) for row in image_blocks_rows]

    def _get_article_audio_blocks(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT ab.block_id, ab.block_type, ab.block_order, 
                            audios.audio_source, IFNULL(audios.audio_length, 0), audios.caption_text
                        FROM articles_blocks AS ab
                        LEFT JOIN audio_blocks AS audios
                        ON ab.block_id=audios.id
                        WHERE ab.article_id=? and ab.block_type='audio'; """, (article_id,))
        audio_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_AUDIO_BLOCKS_KEYS, row)) for row in audio_blocks_rows]

    def _get_article_video_blocks(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT ab.block_id, ab.block_type, ab.block_order,
                            videos.video_source, IFNULL(videos.video_length, 0), 
                            IFNULL(videos.video_cover_source, ''), videos.caption_text
                        FROM articles_blocks AS ab
                        LEFT JOIN video_blocks AS videos
                        ON ab.block_id=videos.id
                        WHERE ab.article_id=? and ab.block_type='video'; """, (article_id,))
        video_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_VIDEO_BLOCKS_KEYS, row)) for row in video_blocks_rows]

    def _get_article_tags_ids(self, article_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT tag_id FROM tags_articles
                        WHERE article_id=?; """, (article_id,))
        return [row[0] for row in cur.fetchall()]

    def _get_articles_ids(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT id FROM articles; """)
        return [row[0] for row in cur.fetchall()]

    def _fetchall_related_articles(self, related_articles_ids):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM articles
                        WHERE id in ({}); """.format(','.join('?' * len(related_articles_ids))), related_articles_ids)
        return cur.fetchall()

    def _get_categories_rows(self):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM categories; """)
        return cur.fetchall()

    def _get_category_tags_ids(self, category_id):
        cur = self.conn.cursor()
        cur.execute(""" SELECT tag_id FROM tags_categories
                        WHERE category_id=?; """, (category_id,))
        return [row[0] for row in cur.fetchall()]
