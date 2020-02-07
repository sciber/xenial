"""
Models constants
================

All constants used by models modules
"""

GUIDES_DIR = 'guides'

GUIDES_KEYS = ('guide_name', 'guide_icon', 'guide_title', 'guide_description', 'guide_version',
               'guide_lang', 'guide_from_place', 'guide_to_place', 'guide_content')

ARTICLES_KEYS = ('article_id', 'article_name', 'article_icon', 'article_title', 'article_synopsis')
RELATED_ARTICLES_KEYS = ARTICLES_KEYS + ('article_num_shared_tags',)
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

BOOKMARKS_KEYS = ('bookmark_id', 'bookmark_created_at',
                  'bookmark_article_id', 'bookmark_article_name', 'bookmark_article_icon',
                  'bookmark_article_title', 'bookmark_article_synopsis')

TAGS_KEYS = ('tag_id', 'tag_name', 'tag_count_categories', 'tag_count_articles')

CATEGORIES_KEYS = ('category_id', 'category_name', 'category_icon', 'category_description')
RELATED_CATEGORIES_KEYS = CATEGORIES_KEYS + ('category_num_shared_tags',)
