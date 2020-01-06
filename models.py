import os
import shutil
import tarfile
import json
from datetime import datetime
from functools import reduce

import sqlite3
from zipfile import ZipFile

GUIDES_DIR = 'guides'


class TagModel:
    def __init__(self, conn, tag_id):
        self.conn = conn
        (self.tag_id, self.tag_name) = self._fetchone_from_tags_by_id(tag_id)[1]

    def tagged_categories_list(self):
        sql_select_all_from_categories_where_tagged_category = """ SELECT * FROM categories 
                                                                   WHERE id IN (
                                                                       SELECT * from tags_categories
                                                                       WHERE tag_id=? 
                                                                   ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories_where_tagged_category, (self.tag_id,))
        categories_rows = cur.fetchall()
        categories_keys = ['category_id', 'category_name', 'category_icon', 'category_description']
        return [dict(zip(categories_keys, row)) for row in categories_rows]

    def num_tagged_categories(self):
        sql_select_count_tagged_tagged_categories = """ SELECT COUNT(id) FROM categories
                                                        WHERE id IN (
                                                            SELECT * FROM tags_categories
                                                            WHERE tag_id=?
                                                        ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_count_tagged_tagged_categories, (self.tag_id,))
        return cur.fetchone()[0]

    def tagged_articles_list(self):
        sql_select_all_from_articles_where_tagged_article = """ SELECT * FROM articles
                                                                WHERE id IN (
                                                                    SELECT * FROM tags_articles
                                                                    WHERE tag_id=?
                                                                ); """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles_where_tagged_article, (self.tag_id,))
        articles_rows = cur.fetchall()
        articles_keys = ['article_id', 'article_name', 'article_icon',
                         'article_title', 'article_synopsis']
        return [dict(zip(articles_keys, row)) for row in articles_rows]

    def num_tagged_articles(self):
        sql_select_count_tagged_tagged_article = """ SELECT COUNT(id) FROM articles
                                                     WHERE id IN (
                                                         SELECT * FROM tags_articles
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
        tags_keys = ['tag_id', 'tag_name']
        return [dict(zip(tags_keys, row)) for row in tags_rows]

    def related_categories_list(self):
        category_tags_ids = self._get_category_tags_ids(self.category_id)
        sql_select_all_from_categories = """ SELECT * FROM categories"""
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories)
        categories_rows = cur.fetchall()
        categories_ids = [row[0] for row in categories_rows]
        related_categories_num_shared_tags = {}
        for inspected_category_id in categories_ids:
            inspected_category_tags_ids = self._get_category_tags_ids(inspected_category_id)
            shared_tags_ids_list = list(set(category_tags_ids) & set(inspected_category_tags_ids))
            if len(shared_tags_ids_list) > 0:
                related_categories_num_shared_tags[inspected_category_id] = len(shared_tags_ids_list)
        sql_select_all_related_categories = """ SELECT * FROM categories
                                                WHERE id in ({placeholders}); """.format(
            placeholders=','.join('?' * len(related_categories_num_shared_tags)))
        cur.execute(sql_select_all_related_categories, list(related_categories_num_shared_tags.keys()))
        related_categories_rows = [row.append(related_categories_num_shared_tags[row[0]]) for row in cur.fetchall()]
        categories_keys = ['category_id', 'category_name', 'category_icon', 'category_description',
                           'category_num_shared_tags']
        return sorted([dict(zip(categories_keys, row)) for row in related_categories_rows],
                      key=lambda c: c['category_num_shared_tags'])

    def articles_list(self):
        category_tags_ids = self._get_category_tags_ids(self.category_id)
        sql_select_all_from_articles = """ SELECT * FROM articles """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles)
        articles_rows = cur.fetchall()
        articles_ids = [row[0] for row in articles_rows]
        category_articles_ids = []
        for article_id in articles_ids:
            article_tags_ids = self._get_article_tags_ids(article_id)
            if set(category_tags_ids) <= set(article_tags_ids):
                category_articles_ids.append(article_id)
        category_articles_rows = [article_row for article_row in articles_rows
                                  if article_row[0] in category_articles_ids]
        articles_keys = ['article_id', 'article_name', 'article_icon',
                         'article_title', 'article_synopsis']
        return [dict(zip(articles_keys, row)) for row in category_articles_rows]

    def _fetchone_from_categories_by_id(self, category_id):
        sql_select_all_from_categories_where_id = """ SELECT * FROM categories
                                                      WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_categories_where_id, (category_id,))
        return cur.fetchone()

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
        return [row[0] for row in cur.fetchall]


class ArticleModel:
    def __init__(self, conn, article_id):
        self.conn = conn
        (self.article_id, self.article_name,
         self.article_icon, self.article_title, self.article_synopsis) = self._fetchone_from_articles_by_id(article_id)

    def tags_list(self):
        sql_select_all_article_tags = """ SELECT t.id, t.name FROM tags AS t
                                          INNER JOIN tags_articles AS ta
                                          ON t.id=ta.tag_id
                                          WHERE ta.article_id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_article_tags, (self.article_id,))
        tags_rows = cur.fetchall()
        tags_keys = ['tag_id', 'tag_name']
        return [dict(zip(tags_keys, row)) for row in tags_rows]

    def related_categories_list(self):
        pass

    def related_articles_list(self):
        pass

    def _fetchone_from_articles_by_id(self, article_id):
        sql_select_all_from_articles_where_id = """ SELECT * FROM articles
                                                    WHERE id=?; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_articles_where_id, (article_id,))
        return cur.fetchone()

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
        return [row[0] for row in cur.fetchall]


class GuideModel:
    conn = None

    def __init__(self, guide_name):
        self.conn = sqlite3.connect(os.path.join(GUIDES_DIR, guide_name, 'guide.db'))
        with open(os.path.join(GUIDES_DIR, guide_name, 'guide.json')) as f:
            guide = json.load(f)

        self.guide_name = guide_name
        self.guide_version = guide['version']
        self.guide_icon = os.path.join(GUIDES_DIR, guide_name, guide['icon'])
        self.guide_title = guide['title']
        self.guide_description = guide['description']
        self.guide_lang = guide['lang']
        self.guide_from_place = guide['from_place']
        self.guide_to_place = guide['to_place']
        self.guide_content = guide['content']

    def tags_list(self):
        sql_select_all_from_tags = """ SELECT * FROM tags; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_tags)
        tags_rows = cur.fetchall()
        tag_keys = ('tag_id', 'tag_name')
        return [dict(zip(tag_keys, row)) for row in tags_rows]

    def tag_by_id(self, tag_id):
        return TagModel(self.conn, tag_id)

    def categories_list(self):
        sql_select_all_from_categories = """ SELECT * FROM categories; """
        cur = self.conn.cursor()
        return cur.execute(sql_select_all_from_categories)

    def category_by_id(self, category_id):
        return CategoryModel(self.conn, category_id)

    def articles_list(self):
        sql_select_all_from_articles = """ SELECT * FROM articles; """
        cur = self.conn.cursor()
        return cur.execute(sql_select_all_from_articles)

    def article_by_id(self, article_id):
        pass

    def bookmarks_list(self):
        sql_select_all_from_bookmarked_articles = """ SELECT b.id, b.created_at,
                                                             b.article_id, a.name, a.icon, a.title, a.synopsis
                                                      FROM bookmarks AS b
                                                      INNER JOIN articles AS a
                                                      ON b.article_id=a.id; """
        cur = self.conn.cursor()
        cur.execute(sql_select_all_from_bookmarked_articles)
        bookmarked_articles_rows = cur.fetchall()
        bookmarked_articles_keys = ['bookmark_id', 'bookmark_created_at',
                                    'bookmark_article_id', 'bookmark_article_name', 'bookmark_article_icon',
                                    'bookmark_article_title', 'bookmark_article_synopsis']
        return [dict(zip(bookmarked_articles_keys, row)) for row in bookmarked_articles_rows]


class GuidesModel:
    def __init__(self, guide_name):
        self.guide_name = guide_name
    
    @staticmethod
    def _validate_guide_json(guide_name, guide_json):
        with open(guide_json, 'r') as f:
            guide = json.load(f)

        required_keys = ['name', 'icon', 'title', 'description', 'version', 'lang', 'from_place', 'to_place']
        for required_key in required_keys:
            value = guide[required_key]
            if required_key == 'name' and value != guide_name:
                raise Exception('JSON guide name is not the same as the archive name')
            if required_key == 'lang' and type(value) != tuple and len(value) != 2:
                raise Exception('Guide language has to be described by a tuple with two string elements (name, code)')

    @staticmethod
    def _create_categories_table(conn):
        sql_create_categories_table = """ CREATE TABLE categories (
                                              id integer PRIMARY KEY,
                                              name text NOT NULL,
                                              icon text,
                                              description text
                                          ); """
        cur = conn.cursor()
        cur.execute(sql_create_categories_table)

    @staticmethod
    def _create_tags_table(conn):
        sql_create_tags_table = """ CREATE TABLE tags (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
        cur = conn.cursor()
        cur.execute(sql_create_tags_table)

    @staticmethod
    def _create_tags_categories_table(conn):
        sql_create_tags_categories_table = """ CREATE TABLE tags_categories (
                                                   id integer PRIMARY KEY,
                                                   tag_id integer NOT NULL
                                                   category_id integer NOT NULL,
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

    @staticmethod
    def _create_articles_table(conn):
        sql_create_articles_table = """ CREATE TABLE articles (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            icon text,
                                            title text,
                                            synopsis text
                                        ); """
        cur = conn.cursor()
        cur.execute(sql_create_articles_table)

    @staticmethod
    def _insert_into_articles(conn, values):
        sql_insert_into_articles = """ INSERT INTO categories (name, icon, title, synopsis)
                                       VALUES (?, ?, ?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_articles, values)
        return cur.lastrowid

    @staticmethod
    def _fetchone_from_articles_where_name(conn, article_name):
        sql_select_all_from_articles_where_name = """ SELECT * FROM articles WHERE name=?; """
        cur = conn.cursor()
        cur.execute(sql_select_all_from_articles_where_name, (article_name,))
        return cur.fetchone()

    @staticmethod
    def _create_tags_articles_table(conn):
        sql_create_tags_articles_table = """ CREATE TABLE tags_articles (
                                                  id integer PRIMARY KEY,
                                                  tag_id integer NOT NULL
                                                  article_id integer NOT NULL,
                                              ); """
        cur = conn.cursor()
        cur.execute(sql_create_tags_articles_table)

    @staticmethod
    def _insert_into_tags_articles(conn, values):
        sql_insert_into_tags_articles = """ INSERT INTO tags_categories (tag_id, category_id)
                                            VALUES (?, ?); """
        cur = conn.cursor()
        cur.execute(sql_insert_into_tags_articles, values)
        return cur.lastrowid

    @staticmethod
    def _create_articles_blocks_table(conn):
        sql_create_articles_blocks_table = """ CREATE TABLE articles_blocks (
                                                   id integer PRIMARY KEY,
                                                   article_id integer NOT NULL,
                                                   block_id integer NOT NULL,
                                                   block_type text NOT NULL
                                               ); """
        cur = conn.cursor()
        cur.execute(sql_create_articles_blocks_table)

    @staticmethod
    def _insert_into_articles_blocks(conn, values):
        sql_insert_into_articles_blocks = """ INSERT INTO articles_blocks (article_id, block_id, block_type)
                                              VALUES (?, ?, ?); """
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
                                                image_source text NOT NULL,
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
    def _create_audio_blocks_table(conn):
        sql_create_audio_blocks_table = """ CREATE TABLE audio_blocks (
                                                id integer PRIMARY KEY,
                                                block_type text NOT NULL DEFAULT 'audio'
                                                audio_source text NOT NULL,
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
    def _create_video_blocks_table(conn):
        sql_create_video_blocks_table = """ CREATE TABLE video_blocks (
                                                id integer PRIMARY KEY,
                                                block_type text NOT NULL DEFAULT 'video'
                                                video_source text NOT NULL,
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
    def _create_bookmarks_table(conn):
        sql_create_bookmarks_table = """ CREATE TABLE bookmarks (
                                             id integer PRIMARY KEY,
                                             article_id integer NOT NULL,
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

    @classmethod
    def import_from_archive(cls, archive):
        """ Import guide from zip archive to sqlite database """

        conn = None
        try:
            guide_name = os.path.basename(archive).split('.')[0]
            with ZipFile(archive, 'r') as zf:
                zf.extractall(os.path.join(GUIDES_DIR, guide_name))

            conn = sqlite3.connect(os.path.join(GUIDES_DIR, guide_name, 'guide.db'))

            cls._validate_guide_json(guide_name, os.path.join(GUIDES_DIR, guide_name, 'guide.json'))

            with open(os.path.join(GUIDES_DIR, guide_name, 'categories.json'), 'r') as f:
                categories = json.load(f)
            cls._create_categories_table(conn)
            cls._create_tags_table(conn)
            cls._create_tags_categories_table(conn)
            for category in categories:
                category_id = cls._insert_into_categories(
                    conn, (category['name'], category['icon'], category['description']))
                for tag_name in set(category['tags']):
                    tag_id = cls._fetchone_from_tags_where_name(conn, tag_name)[0]
                    if not tag_id:
                        tag_id = cls._insert_into_tags(conn, tag_name)
                    cls._insert_into_tags_categories(conn, (tag_id, category_id))
            os.remove(os.path.join(GUIDES_DIR, guide_name, 'categories.json'))

            cls._create_articles_table(conn)
            cls._create_tags_articles_table(conn)
            cls._create_articles_blocks_table(conn)
            cls._create_subtitle_blocks_table(conn)
            cls._create_paragraph_blocks_table(conn)
            cls._create_image_blocks_table(conn)
            cls._create_audio_blocks_table(conn)
            cls._create_video_blocks_table(conn)

            articles_jsons = [filename for filename in os.listdir(os.path.join(GUIDES_DIR, guide_name, 'articles'))]
            for article_json in articles_jsons:
                with open(os.path.join(GUIDES_DIR, guide_name, article_json), 'r') as f:
                    article = json.load(f)
                article_id = cls._insert_into_articles(
                    (conn, article['name'], article['icon'], article['title'], article['synopsis']))
                for block in article['content']:
                    if block['type'] == 'subtitle':
                        block_id = cls._insert_into_subtitle_blocks(conn, block['text'])
                    elif block['type'] == 'paragraph':
                        block_id = cls._insert_into_paragraph_blocks(conn, block['text'])
                    elif block['type'] == 'image':
                        block_id = cls._insert_into_image_blocks(conn, (block['source'], block['caption']))
                    elif block['type'] == 'audio':
                        block_id = cls._insert_into_audio_blocks(conn, (block['source'], block['caption']))
                    elif block['type'] == 'video':
                        block_id = cls._insert_into_video_blocks(conn, (block['source'], block['caption']))
                    else:
                        continue
                    cls._insert_into_articles_blocks((article_id, block_id, block['type']))

                for tag_name in set(article['tags']):
                    tag_id = cls._fetchone_from_tags_where_name(conn, tag_name)[0]
                    if not tag_id:
                        tag_id = cls._insert_into_tags(conn, tag_name)
                    cls._insert_into_tags_articles(conn, (tag_id, article_id))
            shutil.rmtree(os.path.join(GUIDES_DIR, 'articles'))

            with open(os.path.join(GUIDES_DIR, guide_name, 'bookmarks.json'), 'r') as f:
                bookmarks = json.load(f)
            cls._create_bookmarks_table(conn)
            for bookmark in bookmarks:
                article_id = cls._fetchone_from_articles_where_name(conn, bookmark['name'])[0]
                cls._insert_into_bookmarks(conn, (article_id, bookmark['create_at']))
            os.remove(os.path.join(GUIDES_DIR, guide_name, 'bookmarks.json'))

        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

        return GuideModel(guide_name)




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
