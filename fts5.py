import sqlite3
import re


def match(expr, item):
    return re.match(expr, item) is not None


def test():
    conn = sqlite3.connect('guides/dummy/guide.db')
    # conn.create_function("MATCHES", 2, match)
    cur = conn.cursor()
    # cur.execute(""" DROP TABLE IF EXISTS ArticlesSearch; """)
    # cur.execute(""" CREATE VIRTUAL TABLE ArticlesSearch USING fts5(block_type, block_id, block_text)""")
    # cur.execute(""" INSERT INTO ArticlesSearch
    #                 select 'subtitle' as block_type, id as block_id, subtitle_text as block_text from subtitle_blocks
    #                 union select 'paragraph' as block_type, id as block_id, paragraph_text as block_text from paragraph_blocks
    #                 union select 'image' as block_type, id as block_id, caption_text as block_text from image_blocks
    #                 union select 'audio' as block_type, id as block_id, caption_text as block_text from audio_blocks
    #                 union select 'video' as block_type, id as block_id, caption_text as block_text from video_blocks
    #                 order by block_type, block_id""")
    # cur.execute(""" INSERT INTO ArticlesSearch VALUES (1, NULL , 'title', 'This [ref=title]is some title!'); """)
    # cur.execute(""" INSERT INTO ArticlesSearch VALUES (2, NULL , 'synopsis', 'This synopsis does not have any sensible content...'); """)
    # cur.execute(""" INSERT INTO ArticlesSearch VALUES (1, NULL , 'title', 'This is some *****!'); """)
    # conn.commit()
    cur.execute(""" SELECT * FROM article_block_search; """)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.execute(""" SELECT article_id, block_order, block_type, block_id, highlight(article_block_search, 4, '[color=#00FF00]', '[/color]')
                    FROM article_block_search
                    WHERE article_block_search MATCH 'block_text:(avoid unit)' ORDER BY rank
                    ;""")
    # cur.execute(""" select * from article_block_search where article_block_search match 'rest lose + up'; """)
    result = cur.fetchall()
    print('Result:')
    print(result)
