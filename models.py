import os
import shutil
import json
import re
import sqlite3
from zipfile import ZipFile
from datetime import datetime
from connector import audio_meter, video_meter

GUIDES_DIR = 'guides'

GUIDES_KEYS = ('guide_name', 'guide_icon', 'guide_title', 'guide_description', 'guide_version',
               'guide_lang', 'guide_from_place', 'guide_to_place', 'guide_content')
TAGS_KEYS = ('tag_id', 'tag_name', 'tag_count_categories', 'tag_count_articles')
CATEGORIES_KEYS = ('category_id', 'category_name', 'category_icon', 'category_description')
RELATED_CATEGORIES_KEYS = CATEGORIES_KEYS + ('category_num_shared_tags',)
ARTICLES_KEYS = ('article_id', 'article_name', 'article_icon', 'article_title', 'article_synopsis')
ARTICLE_CONTENT_SUBTITLE_BLOCKS_KEYS = ('block_id', 'block_type', 'content_order',
                                        'subtitle_text')
ARTICLE_CONTENT_PARAGRAPH_BLOCKS_KEYS = ('block_id', 'block_type', 'content_order',
                                         'paragraph_text')
ARTICLE_CONTENT_IMAGE_BLOCKS_KEYS = ('block_id', 'block_type', 'content_order',
                                     'image_source', 'image_caption_text')
ARTICLE_CONTENT_AUDIO_BLOCKS_KEYS = ('block_id', 'block_type', 'content_order',
                                     'audio_source', 'audio_length', 'audio_caption_text')
ARTICLE_CONTENT_VIDEO_BLOCKS_KEYS = ('block_id', 'block_type', 'content_order',
                                     'video_source', 'video_length', 'video_cover_source', 'video_caption_text')
RELATED_ARTICLES_KEYS = ARTICLES_KEYS + ('article_num_shared_tags',)
BOOKMARKS_KEYS = ('bookmark_id', 'bookmark_created_at',
                  'bookmark_article_id', 'bookmark_article_name', 'bookmark_article_icon',
                  'bookmark_article_title', 'bookmark_article_synopsis')


class GuidesModel:
    guides_list = []
    active_guide = None

    def __init__(self):
        guides_names = [filename for filename in os.listdir(GUIDES_DIR)
                        if os.path.isdir(os.path.join(GUIDES_DIR, filename))]
        for guide_name in guides_names:
            with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json'), 'r') as f:
                guide_json = json.load(f)
            self.guides_list.append(guide_json)
        self.guides_list.sort(key=lambda item: item['guide_title'])
        if guides_names:
            self.set_active_guide(guides_names[0])

    def set_active_guide(self, guide_name):
        try:
            next(item for item in self.guides_list if item['guide_name'] == guide_name)
        except StopIteration:
            self.active_guide = None
        else:
            self.active_guide = self.guide_by_name(guide_name)

    def guide_by_name(self, guide_name):
        return GuideModel(guide_name)

    def import_from_archive(self, archive):
        """ Import guide from zip archive to sqlite database """

        guides_names = [filename for filename in os.listdir(GUIDES_DIR)
                        if os.path.isdir(os.path.join(GUIDES_DIR, filename))]
        guide_name = os.path.basename(archive).split('.')[0]

        if guide_name in guides_names:
            self.guides_list = [item for item in self.guides_list if item['guide_name'] != guide_name]
            shutil.rmtree(os.path.join(GUIDES_DIR, guide_name))

        with ZipFile(archive, 'r') as zf:
            zf.extractall(os.path.join(GUIDES_DIR, guide_name))

        conn = sqlite3.connect(os.path.join(GUIDES_DIR, guide_name, 'guide.db'))

        with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json'), 'r') as f:
            guides_list_item = json.load(f)

        guides_list_item = self._validate_guides_list_item(guide_name, guides_list_item)

        self._import_from_archive_guide_categories(conn, guide_name)
        self._import_from_archive_guide_articles(conn, guide_name)
        self._import_from_archive_guide_bookmarks(conn, guide_name)

        conn.commit()
        conn.close()

        self.guides_list.append(guides_list_item)
        self.guides_list.sort(key=lambda item: item['guide_title'])

        return guides_list_item

    def remove_guide(self, guide_name):
        guides_list_item_idx = next(idx for idx, guides_list_item in enumerate(self.guides_list)
                                    if guides_list_item['guide_name'] == guide_name)
        # if self.active_guide.guide_name == guide_name:
        #     if len(self.guides_list) > guides_list_item_idx + 1:
        #         self.set_active_guide(self.guides_list[guides_list_item_idx + 1]['guide_name'])
        #     elif len(self.guides_list) > 1:
        #         self.set_active_guide(self.guides_list[guides_list_item_idx - 1]['guide_name'])
        #     else:
        #         self.set_active_guide('')
        del self.guides_list[guides_list_item_idx]
        shutil.rmtree(os.path.join(GUIDES_DIR, guide_name))

    @staticmethod
    def _validate_guides_list_item(guide_name, guides_list_item):
        validated_guide_list_item = {}
        validated_guide_list_item['guide_name'] = guides_list_item['name']
        if validated_guide_list_item['guide_name'] != guide_name:
            raise Exception('JSON guide name is not the same as the archive name')
        validated_guide_list_item['guide_icon'] = os.path.join(GUIDES_DIR, guide_name, guides_list_item['icon'])
        validated_guide_list_item['guide_title'] = guides_list_item['title']
        validated_guide_list_item['guide_description'] = guides_list_item['description']
        validated_guide_list_item['guide_version'] = guides_list_item['version']
        validated_guide_list_item['guide_lang'] = guides_list_item['lang']
        if (validated_guide_list_item['guide_lang']
                and type(validated_guide_list_item['guide_lang']) != tuple
                and len(validated_guide_list_item['guide_lang']) != 2):
            raise Exception('Guide language has to be described by a tuple with two string elements (name, code)')
        validated_guide_list_item['guide_from_place'] = guides_list_item['from_place']
        validated_guide_list_item['guide_to_place'] = guides_list_item['to_place']
        validated_guide_list_item['guide_content'] = guides_list_item['content']

        with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json'), 'w') as f:
            json.dump(validated_guide_list_item, f)

        return validated_guide_list_item

    def _import_from_archive_guide_categories(self, conn, guide_name):
        with open(os.path.join(GUIDES_DIR, guide_name, 'categories.json'), 'r') as f:
            categories = json.load(f)
        self._create_categories_table(conn)
        self._create_tags_table(conn)
        self._create_tags_categories_table(conn)
        for category in categories:
            category_id = self._insert_into_categories(
                conn, (category['name'],
                       os.path.join(GUIDES_DIR, guide_name, category['icon']),
                       category['description']))
            for tag_name in set(category['tags']):
                tag_row = self._fetchone_from_tags_where_name(conn, tag_name)
                if tag_row is not None:
                    tag_id = tag_row[0]
                else:
                    tag_id = self._insert_into_tags(conn, tag_name)
                self._insert_into_tags_categories(conn, (tag_id, category_id))
        os.remove(os.path.join(GUIDES_DIR, guide_name, 'categories.json'))

    @staticmethod
    def _create_categories_table(conn):
        sql_create_categories_table = """ CREATE TABLE categories (
                                              id integer PRIMARY KEY,
                                              name text UNIQUE NOT NULL,
                                              icon text,
                                              description text
                                          ); """
        cur = conn.cursor()
        cur.execute(sql_create_categories_table)

    @staticmethod
    def _create_tags_table(conn):
        sql_create_tags_table = """ CREATE TABLE tags (
                                        id integer PRIMARY KEY,
                                        name text UNIQUE NOT NULL
                                    ); """
        cur = conn.cursor()
        cur.execute(sql_create_tags_table)

    @staticmethod
    def _create_tags_categories_table(conn):
        sql_create_tags_categories_table = """ CREATE TABLE tags_categories (
                                                   tag_id integer NOT NULL,
                                                   category_id integer NOT NULL,
                                                   UNIQUE(tag_id, category_id)
                                               ); """
        cur = conn.cursor()
        cur.execute(sql_create_tags_categories_table)

    @staticmethod
    def _insert_into_categories(conn, values):
        sql_insert_into_categories = """ INSERT INTO categories (name, icon, description)
                                         VALUES (?, ?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_categories, values)
        return cur.lastrowid

    @staticmethod
    def _fetchone_from_tags_where_name(conn, tag_name):
        sql_select_all_from_tags_where_name = """ SELECT * FROM tags WHERE name=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_tags_where_name, (tag_name,))
        return cur.fetchone()

    @staticmethod
    def _insert_into_tags(conn, value):
        sql_insert_into_tags = """ INSERT INTO tags (name) VALUES (?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_tags, (value,))
        return cur.lastrowid

    @staticmethod
    def _insert_into_tags_categories(conn, values):
        sql_insert_into_tags_categories = """ INSERT INTO tags_categories (tag_id, category_id)
                                              VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_tags_categories, values)
        return cur.lastrowid

    def _import_from_archive_guide_articles(self, conn, guide_name):
        self._create_articles_table(conn)
        self._create_tags_articles_table(conn)
        self._fill_articles_tags_articles_tables(conn, guide_name)
        shutil.rmtree(os.path.join(GUIDES_DIR, guide_name, 'articles'))

        self._create_articles_blocks_table(conn)
        self._create_subtitle_blocks_table(conn)
        self._create_paragraph_blocks_table(conn)
        self._create_image_blocks_table(conn)
        self._create_audio_blocks_table(conn)
        self._create_video_blocks_table(conn)

        self._fill_articles_content_block_tables(conn, guide_name)
        self._create_and_fill_article_block_search_table(conn)

    @staticmethod
    def _create_and_fill_article_block_search_table(conn):
        cur = conn.cursor()
        cur.execute(""" CREATE VIRTUAL TABLE article_block_search  USING fts5(block_type, block_id, block_text); """)
        cur.execute(""" INSERT INTO article_block_search
                        SELECT 'subtitle' AS block_type, id AS block_id, subtitle_text AS block_text 
                        FROM subtitle_blocks
                        UNION 
                        SELECT 'paragraph' AS block_type, id AS block_id, paragraph_text AS block_text 
                        FROM paragraph_blocks
                        UNION SELECT 'image' AS block_type, id AS block_id, caption_text AS block_text 
                        FROM image_blocks
                        UNION SELECT 'audio' AS block_type, id AS block_id, caption_text AS block_text 
                        FROM audio_blocks
                        UNION SELECT 'video' AS block_type, id AS block_id, caption_text AS block_text 
                        FROM video_blocks
                        ORDER BY block_type, block_id; """)
        conn.commit()

    @staticmethod
    def _create_articles_table(conn):
        sql_create_articles_table = """ CREATE TABLE articles (
                                            id integer PRIMARY KEY,
                                            name text UNIQUE NOT NULL,
                                            icon text,
                                            title text,
                                            synopsis text,
                                            content text
                                        ); """
        cur = conn.cursor()
        cur.execute(sql_create_articles_table)

    def _fill_articles_tags_articles_tables(self, conn, guide_name):
        articles_jsons = [filename for filename in os.listdir(os.path.join(GUIDES_DIR, guide_name, 'articles'))]
        for article_json in articles_jsons:
            with open(os.path.join(GUIDES_DIR, guide_name, 'articles', article_json), 'r') as f:
                article = json.load(f)

            article_name = os.path.basename(article_json).split('.')[0]
            if article_name != article['name']:
                continue

            article_id = self._insert_into_articles(
                conn, (article['name'],
                       os.path.join(GUIDES_DIR, guide_name, article['icon']),
                       article['title'],
                       article['synopsis'],
                       json.dumps(article['content'])))

            for tag_name in set(article['tags']):
                tag_row = self._fetchone_from_tags_where_name(conn, tag_name)
                if tag_row is not None:
                    tag_id = tag_row[0]
                else:
                    tag_id = self._insert_into_tags(conn, tag_name)
                self._insert_into_tags_articles(conn, (tag_id, article_id))

    @staticmethod
    def _insert_into_articles(conn, values):
        sql_insert_into_articles = """ INSERT INTO articles (name, icon, title, synopsis, content)
                                       VALUES (?, ?, ?, ?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_articles, values)
        return cur.lastrowid

    @staticmethod
    def _fetchall_id_name_content_from_articles(conn):
        sql_select_id_name_from_articles = """ SELECT id, name, content FROM articles; """
        cur = conn.cursor()
        cur.execute(sql_select_id_name_from_articles)
        return cur.fetchall()

    @staticmethod
    def _fetchone_from_articles_where_name(conn, article_name):
        sql_select_all_from_articles_where_name = """ SELECT * FROM articles WHERE name=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_articles_where_name, (article_name,))
        return cur.fetchone()

    @staticmethod
    def _create_tags_articles_table(conn):
        sql_create_tags_articles_table = """ CREATE TABLE tags_articles (
                                                  tag_id integer NOT NULL,
                                                  article_id integer NOT NULL,
                                                  UNIQUE(tag_id, article_id)
                                              ); """
        cur = conn.cursor()
        cur.execute(sql_create_tags_articles_table)

    @staticmethod
    def _insert_into_tags_articles(conn, values):
        sql_insert_into_tags_articles = """ INSERT INTO tags_articles (tag_id, article_id)
                                            VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_tags_articles, values)
        return cur.lastrowid

    def _fill_articles_content_block_tables(self, conn, guide_name):
        articles_rows = self._fetchall_id_name_content_from_articles(conn)
        articles_dicts = {row[1]: [row[0], row[2]] for row in articles_rows}
        for article_name in articles_dicts:
            article_id = articles_dicts[article_name][0]
            article_content = json.loads(articles_dicts[article_name][1])
            block_order = 0
            for block in article_content:
                if block['type'] == 'subtitle':
                    block_id = self._insert_into_subtitle_blocks(conn, block['text'])
                elif block['type'] == 'paragraph':
                    updated_refs_paragraph = self._update_text_refs(block['text'], articles_dicts)
                    block_id = self._insert_into_paragraph_blocks(conn, updated_refs_paragraph)
                elif block['type'] == 'image':
                    guide_block_source = os.path.join(GUIDES_DIR, guide_name, block['source'])
                    image_block_row = self._fetchone_from_image_blocks_where_image_source(conn, guide_block_source)
                    if image_block_row is not None:
                        block_id = image_block_row[0]
                    else:
                        updated_refs_image_caption_text = self._update_text_refs(block['caption'], articles_dicts)
                        block_id = self._insert_into_image_blocks(
                            conn, (guide_block_source, updated_refs_image_caption_text))
                elif block['type'] == 'audio':
                    guide_block_source = os.path.join(GUIDES_DIR, guide_name, block['source'])
                    audio_block_row = self._fetchone_from_audio_blocks_where_audio_source(conn, guide_block_source)
                    if audio_block_row is not None:
                        block_id = audio_block_row[0]
                    else:
                        updated_refs_audio_caption_text = self._update_text_refs(block['caption'], articles_dicts)
                        block_id = self._insert_into_audio_blocks(
                            conn, (guide_block_source, updated_refs_audio_caption_text))
                elif block['type'] == 'video':
                    guide_block_source = os.path.join(GUIDES_DIR, guide_name, block['source'])
                    video_block_row = self._fetchone_from_video_blocks_where_video_source(conn, guide_block_source)
                    if video_block_row is not None:
                        block_id = video_block_row[0]
                    else:
                        updated_refs_audio_caption_text = self._update_text_refs(block['caption'], articles_dicts)
                        block_id = self._insert_into_video_blocks(
                            conn, (guide_block_source, updated_refs_audio_caption_text))
                else:
                    continue
                self._insert_into_articles_blocks(conn, (article_id, block_id, block_order, block['type']))
                block_order += 1

        self._alter_table_articles_drop_column_content(conn)
        self._update_audio_length_in_audio_blocks_table(conn)
        self._update_video_length_and_cover_in_video_blocks(conn)

    @staticmethod
    def _update_audio_length_in_audio_blocks_table(conn):
        sql_select_audio_source_from_audio_blocks = """ SELECT audio_source FROM audio_blocks; """
        sql_update_audio_blocks_audio_length = """ UPDATE audio_blocks
                                                   SET audio_length=?
                                                   WHERE audio_source=?; """
        cur = conn.cursor()
        cur.execute(sql_select_audio_source_from_audio_blocks)
        audio_blocks_sources_rows = cur.fetchall()
        for row in audio_blocks_sources_rows:
            audio_source = row[0]
            audio_length = audio_meter.get_audio_length(audio_source)
            cur.execute(sql_update_audio_blocks_audio_length, (audio_length, audio_source))

    def _update_video_length_and_cover_in_video_blocks(self, conn):

        sql_select_video_source_from_video_blocks = """ SELECT video_source FROM video_blocks; """
        cur = conn.cursor()
        cur.execute(sql_select_video_source_from_video_blocks)
        video_blocks_sources_rows = cur.fetchall()
        video_block_sources = [row[0] for row in video_blocks_sources_rows]
        cur.execute("PRAGMA database_list;")
        dbname = cur.fetchone()[-1]
        video_meter.get_videos_lengths_and_covers(video_block_sources, self.store_video_metrics, dbname)

    @staticmethod
    def store_video_metrics(video_metrics, dbname):
        sql_update_video_blocks_video_length_and_cover = """ UPDATE video_blocks
                                                             SET video_length=?,
                                                                 video_cover_source=?
                                                             WHERE video_source=?; """
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        for video_source in video_metrics:
            cur.execute(sql_update_video_blocks_video_length_and_cover,
                        (video_metrics[video_source]['video_length'],
                         video_metrics[video_source]['video_cover_source'],
                         video_source))
        conn.commit()
        conn.close()

    @staticmethod
    def _alter_table_articles_drop_column_content(conn):
        sql_create_articles_new_table = """
            CREATE TABLE articles_new (
                id integer PRIMARY KEY,
                name text UNIQUE NOT NULL,
                icon text,
                title text,
                synopsis text
            );
        """
        sql_insert_data_from_articles_to_articles_new = """
            INSERT INTO articles_new (id, name, icon, title, synopsis)
            SELECT id, name, icon, title, synopsis FROM articles;
        """
        sql_drop_articles_table = """ 
            DROP TABLE articles; 
        """
        sql_rename_articles_new_to_articles = """
            ALTER TABLE articles_new RENAME TO articles;
        """
        cur = conn.cursor()
        cur.execute(sql_create_articles_new_table)
        cur.execute(sql_insert_data_from_articles_to_articles_new)
        cur.execute(sql_drop_articles_table)
        cur.execute(sql_rename_articles_new_to_articles)
        conn.commit()

    @staticmethod
    def _update_text_refs(block_text, articles_dicts):
        def replace_name_ref(matchobj):
            article_name = matchobj.group(1).strip()
            if article_name not in articles_dicts:
                replacement = '[ref=]'
            else:
                article_id = articles_dicts[article_name][0]
                replacement = '[ref={ref}]'.format(ref=article_id)
            return replacement

        result = re.sub(r'\[ref=(.*?)\]', replace_name_ref, block_text)
        return result

    @staticmethod
    def _create_articles_blocks_table(conn):
        sql_create_articles_blocks_table = """ CREATE TABLE articles_blocks (
                                                   article_id integer NOT NULL,
                                                   block_id integer NOT NULL,
                                                   block_order integer NOT NULL,
                                                   block_type text NOT NULL,
                                                   UNIQUE(article_id, block_id, block_order, block_type)
                                               ); """
        cur = conn.cursor()
        cur.execute(sql_create_articles_blocks_table)

    @staticmethod
    def _insert_into_articles_blocks(conn, values):
        sql_insert_into_articles_blocks = """ INSERT INTO articles_blocks 
                                                  (article_id, block_id, block_order, block_type)
                                              VALUES (?, ?, ?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_articles_blocks, values)

    @staticmethod
    def _create_subtitle_blocks_table(conn):
        sql_create_subtitle_blocks_table = """ CREATE TABLE subtitle_blocks (
                                                   id integer PRIMARY KEY,
                                                   subtitle_text text NOT NULL
                                               ); """
        cur = conn.cursor()
        cur.execute(sql_create_subtitle_blocks_table)

    @staticmethod
    def _insert_into_subtitle_blocks(conn, value):
        sql_insert_into_subtitle_blocks_table = """ INSERT INTO subtitle_blocks (subtitle_text)
                                                    VALUES (?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_subtitle_blocks_table, (value,))
        return cur.lastrowid

    @staticmethod
    def _create_paragraph_blocks_table(conn):
        sql_create_paragraph_blocks_table = """ CREATE TABLE paragraph_blocks (
                                                    id integer PRIMARY KEY,
                                                    paragraph_text text NOT NULL
                                                 ); """
        cur = conn.cursor()
        cur.execute(sql_create_paragraph_blocks_table)

    @staticmethod
    def _insert_into_paragraph_blocks(conn, value):
        sql_insert_into_paragraph_blocks_table = """ INSERT INTO paragraph_blocks (paragraph_text)
                                                     VALUES (?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_paragraph_blocks_table, (value,))
        return cur.lastrowid

    @staticmethod
    def _create_image_blocks_table(conn):
        sql_create_image_blocks_table = """ CREATE TABLE image_blocks (
                                                id integer PRIMARY KEY,
                                                image_source text UNIQUE NOT NULL,
                                                caption_text text
                                            ); """
        cur = conn.cursor()
        cur.execute(sql_create_image_blocks_table)

    @staticmethod
    def _insert_into_image_blocks(conn, values):
        sql_insert_into_image_blocks_table = """ INSERT INTO image_blocks (image_source, caption_text)
                                                 VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_image_blocks_table, values)
        return cur.lastrowid

    @staticmethod
    def _fetchone_from_image_blocks_where_image_source(conn, image_source):
        sql_select_all_from_image_blocks_where_image_source = """ SELECT * FROM image_blocks
                                                                  WHERE image_source=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_image_blocks_where_image_source, (image_source,))
        return cur.fetchone()

    @staticmethod
    def _create_audio_blocks_table(conn):
        sql_create_audio_blocks_table = """ CREATE TABLE audio_blocks (
                                                id integer PRIMARY KEY,
                                                block_type text NOT NULL DEFAULT 'audio',
                                                audio_source text UNIQUE NOT NULL,
                                                audio_length real,
                                                caption_text text
                                            ); """
        cur = conn.cursor()
        cur.execute(sql_create_audio_blocks_table)

    @staticmethod
    def _insert_into_audio_blocks(conn, values):
        sql_insert_into_audio_blocks_table = """ INSERT INTO audio_blocks (audio_source, caption_text)
                                                 VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_audio_blocks_table, values)
        return cur.lastrowid

    @staticmethod
    def _fetchone_from_audio_blocks_where_audio_source(conn, audio_source):
        sql_select_all_from_audio_blocks_where_audio_source = """ SELECT * FROM audio_blocks
                                                                  WHERE audio_source=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_audio_blocks_where_audio_source, (audio_source,))
        return cur.fetchone()

    @staticmethod
    def _create_video_blocks_table(conn):
        sql_create_video_blocks_table = """ CREATE TABLE video_blocks (
                                                id integer PRIMARY KEY,
                                                video_source text UNIQUE NOT NULL,
                                                video_length real,
                                                video_cover_source text,
                                                caption_text text
                                            ); """
        cur = conn.cursor()
        cur.execute(sql_create_video_blocks_table)

    @staticmethod
    def _insert_into_video_blocks(conn, values):
        sql_insert_into_video_blocks_table = """ INSERT INTO video_blocks (video_source, caption_text)
                                                 VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_video_blocks_table, values)
        return cur.lastrowid

    @staticmethod
    def _fetchone_from_video_blocks_where_video_source(conn, video_source):
        sql_select_all_from_video_blocks_where_video_source = """ SELECT * FROM video_blocks
                                                                  WHERE video_source=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_video_blocks_where_video_source, (video_source,))
        return cur.fetchone()

    def _import_from_archive_guide_bookmarks(self, conn, guide_name):
        with open(os.path.join(GUIDES_DIR, guide_name, 'bookmarks.json'), 'r') as f:
            bookmarks = json.load(f)
        self._create_bookmarks_table(conn)
        for bookmark in bookmarks:
            article_id = self._fetchone_from_articles_where_name(conn, bookmark['article_name'])[0]
            self._insert_into_bookmarks(conn, (article_id, bookmark['created_at']))
        os.remove(os.path.join(GUIDES_DIR, guide_name, 'bookmarks.json'))

    @staticmethod
    def _create_bookmarks_table(conn):
        sql_create_bookmarks_table = """ CREATE TABLE bookmarks (
                                             id integer PRIMARY KEY,
                                             article_id integer UNIQUE NOT NULL,
                                             created_at text
                                         ); """
        cur = conn.cursor()
        cur.execute(sql_create_bookmarks_table)

    @staticmethod
    def _insert_into_bookmarks(conn, values):
        sql_insert_into_bookmarks = """ INSERT INTO bookmarks (article_id, created_at) VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_bookmarks, values)
        return cur.lastrowid


class GuideModel:
    conn = None

    def __init__(self, guide_name):
        self.conn = sqlite3.connect(os.path.join(GUIDES_DIR, guide_name, 'guide.db'))
        with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json')) as f:
            guide = json.load(f)

        self.guide_name = guide_name
        self.guide_version = guide['guide_version']
        self.guide_icon = guide['guide_icon']
        self.guide_title = guide['guide_title']
        self.guide_description = guide['guide_description']
        self.guide_lang = guide['guide_lang']
        self.guide_from_place = guide['guide_from_place']
        self.guide_to_place = guide['guide_to_place']
        self.guide_content = guide['guide_content']

    def tags_list(self):
        sql_select_joined_tags = """ SELECT t.id, t.name, IFNULL(tc.count_categories, 0), IFNULL(ta.count_articles, 0) 
                                     FROM tags AS t
                                     LEFT JOIN (
                                         SELECT tag_id, COUNT(article_id) AS count_articles FROM tags_articles
                                         GROUP BY tag_id) AS ta
                                     ON t.id=ta.tag_id
                                     LEFT JOIN (
                                         SELECT tag_id, COUNT(category_id) AS count_categories FROM tags_categories
                                         GROUP BY tag_id) AS tc
                                     ON t.id=tc.tag_id; """
        cur = self.conn.cursor()
        cur.execute(sql_select_joined_tags)
        tags_rows = cur.fetchall()
        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def tag_by_id(self, tag_id):
        return TagModel(self.conn, tag_id)

    def categories_list(self):
        sql_select_all_from_categories = """ SELECT * FROM categories; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories)
        categories_rows = cur.fetchall()
        return [dict(zip(CATEGORIES_KEYS, row)) for row in categories_rows]

    def category_by_id(self, category_id):
        return CategoryModel(self.conn, category_id)

    def articles_list(self):
        sql_select_all_from_articles = """ SELECT * FROM articles; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles)
        articles_rows = cur.fetchall()
        return [dict(zip(ARTICLES_KEYS, row)) for row in articles_rows]

    def article_by_id(self, article_id):
        return ArticleModel(self.conn, article_id)

    def bookmarks_list(self):
        sql_select_all_from_bookmarked_articles = """ SELECT b.id, b.created_at,
                                                             b.article_id, a.name, a.icon, a.title, a.synopsis
                                                      FROM bookmarks AS b
                                                      INNER JOIN articles AS a
                                                      ON b.article_id=a.id 
                                                      ORDER BY b.created_at; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_bookmarked_articles)
        bookmarked_articles_rows = cur.fetchall()
        return [dict(zip(BOOKMARKS_KEYS, row)) for row in bookmarked_articles_rows]

    def add_bookmark(self, article_id):
        sql_insert_into_bookmarks = """ INSERT INTO bookmarks (article_id, created_at) VALUES (?, ?); """
        cur = self.conn.cursor()
        cur.execute(sql_insert_into_bookmarks, (article_id, str(datetime.now())))
        self.conn.commit()

    def delete_bookmark(self, bookmark_id):
        sql_delete_from_bookmarks = """ DELETE FROM bookmarks WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_delete_from_bookmarks, (bookmark_id,))
        self.conn.commit()


class TagModel:
    def __init__(self, conn, tag_id):
        self.conn = conn
        self.tag_id, self.tag_name = self._fetchone_from_tags_by_id(tag_id)

    def tagged_categories_list(self):
        sql_select_all_from_categories_where_tagged_category = """ SELECT * FROM categories 
                                                                   WHERE id IN (
                                                                       SELECT category_id from tags_categories
                                                                       WHERE tag_id=? 
                                                                   ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories_where_tagged_category, (self.tag_id,))
        categories_rows = cur.fetchall()
        return [dict(zip(CATEGORIES_KEYS, row)) for row in categories_rows]

    def num_tagged_categories(self):
        sql_select_count_tagged_tagged_categories = """ SELECT COUNT(id) FROM categories
                                                        WHERE id IN (
                                                            SELECT category_id FROM tags_categories
                                                            WHERE tag_id=?
                                                        ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_count_tagged_tagged_categories, (self.tag_id,))
        return cur.fetchone()[0]

    def tagged_articles_list(self):
        sql_select_all_from_articles_where_tagged_article = """ SELECT * FROM articles
                                                                WHERE id IN (
                                                                    SELECT article_id FROM tags_articles
                                                                    WHERE tag_id=?
                                                                ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles_where_tagged_article, (self.tag_id,))
        articles_rows = cur.fetchall()
        return [dict(zip(ARTICLES_KEYS, row)) for row in articles_rows]

    def num_tagged_articles(self):
        sql_select_count_tagged_tagged_article = """ SELECT COUNT(id) FROM articles
                                                     WHERE id IN (
                                                         SELECT article_id FROM tags_articles
                                                         WHERE tag_id=?
                                                     ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_count_tagged_tagged_article, (self.tag_id,))
        return cur.fetchone()[0]

    def _fetchone_from_tags_by_id(self, tag_id):
        sql_select_all_from_tags_where_id = """ SELECT * FROM tags WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_tags_where_id, (tag_id,))
        return cur.fetchone()


class CategoryModel:
    def __init__(self, conn, category_id):
        self.conn = conn
        (self.category_id, self.category_name,
         self.category_icon, self.category_description) = self._fetchone_from_categories_by_id(category_id)

    def tags_list(self):
        sql_select_all_category_tags = """ SELECT t.id, t.name FROM tags AS t
                                           INNER JOIN tags_categories AS tc
                                           ON t.id=tc.tag_id
                                           WHERE tc.category_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_category_tags, (self.category_id,))
        tags_rows = cur.fetchall()

        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def related_categories_list(self):
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

    def articles_list(self):
        category_tags_ids = self._get_category_tags_ids(self.category_id)
        articles_rows = self._get_articles_rows()
        category_articles_rows = []
        for article_row in articles_rows:
            article_id = article_row[0]
            article_tags_ids = self._get_article_tags_ids(article_id)
            if set(category_tags_ids) <= set(article_tags_ids):
                category_articles_rows.append(article_row)
        return [dict(zip(ARTICLES_KEYS, row)) for row in category_articles_rows]

    def _fetchone_from_categories_by_id(self, category_id):
        sql_select_all_from_categories_where_id = """ SELECT * FROM categories
                                                      WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories_where_id, (category_id,))
        return cur.fetchone()

    def _get_categories_ids(self):
        sql_select_id_from_categories = """ SELECT id FROM categories; """
        cur = self.conn.cursor()
        cur.execute(sql_select_id_from_categories)
        return [row[0] for row in cur.fetchall()]

    def _get_articles_rows(self):
        sql_select_all_from_articles = """ SELECT * FROM articles; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles)
        return cur.fetchall()

    def _get_category_tags_ids(self, category_id):
        sql_select_tag_id_from_tags_categories = """ SELECT tag_id FROM tags_categories
                                                     WHERE category_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_tag_id_from_tags_categories, (category_id,))
        return [row[0] for row in cur.fetchall()]

    def _fetchall_related_categories(self, related_categories_ids):
        sql_select_all_related_categories = """ SELECT * FROM categories
                                                WHERE id in ({placeholders}); """.format(
            placeholders=','.join('?' * len(related_categories_ids)))
        cur = self.conn.cursor()
        cur.execute(sql_select_all_related_categories, related_categories_ids)
        return cur.fetchall()

    def _get_article_tags_ids(self, article_id):
        sql_select_tag_id_from_tags_articles = """ SELECT tag_id FROM tags_articles
                                                   WHERE article_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_tag_id_from_tags_articles, (article_id,))
        return [row[0] for row in cur.fetchall()]


class ArticleModel:
    def __init__(self, conn, article_id):
        self.conn = conn
        (self.article_id, self.article_name,
         self.article_icon, self.article_title, self.article_synopsis) = self._fetchone_from_articles_by_id(article_id)

    def bookmark(self):
        sql_select_article_bookmark = """ SELECT id, created_at FROM bookmarks
                                          WHERE article_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_bookmark, (self.article_id,))
        bookmark_row = cur.fetchone()
        if bookmark_row is None:
            return None
        return dict(zip(('bookmark_id', 'bookmark_created_at'), bookmark_row))

    def tags_list(self):
        sql_select_all_article_tags = """ SELECT t.id, t.name FROM tags AS t
                                          INNER JOIN tags_articles AS ta
                                          ON t.id=ta.tag_id
                                          WHERE ta.article_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_article_tags, (self.article_id,))
        tags_rows = cur.fetchall()
        return [dict(zip(TAGS_KEYS, row)) for row in tags_rows]

    def categories_list(self):
        article_tags_ids = self._get_article_tags_ids(self.article_id)
        categories_rows = self._get_categories_rows()
        article_categories_rows = []
        for category_row in categories_rows:
            category_id = category_row[0]
            category_tags_ids = self._get_category_tags_ids(category_id)
            if set(category_tags_ids) <= set(article_tags_ids):
                article_categories_rows.append(category_row)
        return [dict(zip(CATEGORIES_KEYS, row)) for row in article_categories_rows]

    def related_articles_list(self):
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

    def content_blocks_list(self):
        subtitle_blocks_list = self._get_article_subtitle_blocks(self.article_id)
        paragraph_blocks_list = self._get_article_paragraph_blocks(self.article_id)
        image_blocks_list = self._get_article_image_blocks(self.article_id)
        audio_blocks_list = self._get_article_audio_blocks(self.article_id)
        video_blocks_list = self._get_article_video_blocks(self.article_id)
        sorted_content_blocks_list = sorted(subtitle_blocks_list + paragraph_blocks_list
                                      + image_blocks_list + audio_blocks_list
                                      + video_blocks_list, key=lambda block: block['content_order'])
        return sorted_content_blocks_list

    def _get_article_subtitle_blocks(self, article_id):
        sql_select_article_subtitle_blocks_rows = """ SELECT ab.block_id, ab.block_type, ab.block_order, 
                                                          subtitles.subtitle_text
                                                      FROM articles_blocks AS ab
                                                      LEFT JOIN subtitle_blocks AS subtitles
                                                      ON ab.block_id=subtitles.id
                                                      WHERE ab.article_id=? AND ab.block_type='subtitle'; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_subtitle_blocks_rows, (article_id,))
        subtitle_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_SUBTITLE_BLOCKS_KEYS, row)) for row in subtitle_blocks_rows]

    def _get_article_paragraph_blocks(self, article_id):
        sql_select_article_paragraph_blocks_rows = """ SELECT ab.block_id, ab.block_type, ab.block_order, 
                                                           paragraphs.paragraph_text
                                                       FROM articles_blocks AS ab
                                                       LEFT JOIN paragraph_blocks AS paragraphs
                                                       ON ab.block_id=paragraphs.id
                                                       WHERE ab.article_id=? AND ab.block_type='paragraph'; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_paragraph_blocks_rows, (article_id,))
        paragraph_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_PARAGRAPH_BLOCKS_KEYS, row)) for row in paragraph_blocks_rows]

    def _get_article_image_blocks(self, article_id):
        sql_select_article_image_blocks_rows = """ SELECT ab.block_id, ab.block_type, ab.block_order,
                                                       images.image_source, images.caption_text
                                                   FROM articles_blocks AS ab
                                                   LEFT JOIN image_blocks AS images
                                                   ON ab.block_id=images.id
                                                   WHERE ab.article_id=? and ab.block_type='image'; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_image_blocks_rows, (article_id,))
        image_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_IMAGE_BLOCKS_KEYS, row)) for row in image_blocks_rows]

    def _get_article_audio_blocks(self, article_id):
        sql_select_article_audio_blocks_rows = """ SELECT ab.block_id, ab.block_type, ab.block_order,
                                                       audios.audio_source, IFNULL(audios.audio_length, 0), 
                                                       audios.caption_text
                                                   FROM articles_blocks AS ab
                                                   LEFT JOIN audio_blocks AS audios
                                                   ON ab.block_id=audios.id
                                                   WHERE ab.article_id=? and ab.block_type='audio'; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_audio_blocks_rows, (article_id,))
        audio_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_AUDIO_BLOCKS_KEYS, row)) for row in audio_blocks_rows]

    def _get_article_video_blocks(self, article_id):
        sql_select_article_video_blocks_rows = """ SELECT ab.block_id, ab.block_type, ab.block_order,
                                                       videos.video_source, IFNULL(videos.video_length, 0), 
                                                       IFNULL(videos.video_cover_source, ''), videos.caption_text
                                                   FROM articles_blocks AS ab
                                                   LEFT JOIN video_blocks AS videos
                                                   ON ab.block_id=videos.id
                                                   WHERE ab.article_id=? and ab.block_type='video'; """
        cur = self.conn.cursor()
        cur.execute(sql_select_article_video_blocks_rows, (article_id,))
        video_blocks_rows = cur.fetchall()
        return [dict(zip(ARTICLE_CONTENT_VIDEO_BLOCKS_KEYS, row)) for row in video_blocks_rows]

    def _fetchone_from_articles_by_id(self, article_id):
        sql_select_all_from_articles_where_id = """ SELECT * FROM articles
                                                    WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles_where_id, (article_id,))
        return cur.fetchone()

    def _get_categories_rows(self):
        sql_select_id_from_categories = """ SELECT * FROM categories; """
        cur = self.conn.cursor()
        cur.execute(sql_select_id_from_categories)
        return cur.fetchall()

    def _get_articles_ids(self):
        sql_select_all_from_articles = """ SELECT id FROM articles; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles)
        return [row[0] for row in cur.fetchall()]

    def _get_category_tags_ids(self, category_id):
        sql_select_tag_id_from_tags_categories = """ SELECT tag_id FROM tags_categories
                                                     WHERE category_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_tag_id_from_tags_categories, (category_id,))
        return [row[0] for row in cur.fetchall()]

    def _get_article_tags_ids(self, article_id):
        sql_select_tag_id_from_tags_articles = """ SELECT tag_id FROM tags_articles
                                                   WHERE article_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_tag_id_from_tags_articles, (article_id,))
        return [row[0] for row in cur.fetchall()]

    def _fetchall_related_articles(self, related_articles_ids):
        sql_select_all_related_articles = """ SELECT * FROM articles
                                              WHERE id in ({placeholders}); """.format(
            placeholders=','.join('?' * len(related_articles_ids)))
        cur = self.conn.cursor()
        cur.execute(sql_select_all_related_articles, related_articles_ids)
        return cur.fetchall()


guides = GuidesModel()
