import os
import json
from datetime import datetime

from .models import guides


class BookmarkModel:
    def __init__(self):
        pass

    @staticmethod
    def all():
        """Return a list of the active guide bookmarks"""
        if guides.active_guide is None:
            return []
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'r') as bookmark_file:
            bookmarks_list = json.load(bookmark_file)
        return bookmarks_list

    @classmethod
    def add(cls, article_id):
        """Add the active guide article to the active guide bookmarks"""
        bookmarks_list = cls.all()
        new_bookmark = {'article_id': article_id, 'created_at': str(datetime.now())}
        bookmarks_list.append(new_bookmark)
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'w') as bookmark_file:
            json.dump(bookmarks_list, bookmark_file)

    @classmethod
    def remove(cls, article_id):
        """Remove the active guide article from the active guide bookmarks"""
        bookmarks_list = cls.all()
        for bookmark in bookmarks_list:
            if bookmark['article_id'] == article_id:
                del bookmark
        bookmark_filename = os.path.join(guides.active_guide_path, 'bookmarks.json')
        with open(bookmark_filename, 'w') as bookmark_file:
            json.dump(bookmarks_list, bookmark_file)
