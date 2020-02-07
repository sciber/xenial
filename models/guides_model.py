"""
Guides model
============

Creates instance of Guides model class.
"""

import json
import os
import shutil
from zipfile import ZipFile, is_zipfile

from models.models_constants import *
from models.guide_model import Guide


class Guides:
    """
    Manages list of guides items containing basic information about guides loaded into the application.
    :attr: `guides_list` is a list of dictionaries containing basic info about particular guide
    :attr: `active_guide` is instance of Guide class which contains all guide model data needed for the application.
    """

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

    def does_guide_exist(self, guide_name):
        """ Test whether there is a guide of given name loaded in the application"""

        try:
            next(item for item in self.guides_list if item['guide_name'] == guide_name)
        except StopIteration:
            return False
        else:
            return True

    def set_active_guide(self, guide_name):
        """ Set the active guide to be the one of the given name"""

        try:
            next(item for item in self.guides_list if item['guide_name'] == guide_name)
        except StopIteration:
            self.active_guide = None
        else:
            self.active_guide = self.guide_by_name(guide_name)

    @staticmethod
    def guide_by_name(guide_name):
        """ Returns a guide of a name `guide_name`. Raise exception if such guide is not loaded into the application."""

        return Guide(guide_name)

    def load_guide(self, guide_name):
        """ Load guide into the application and inserts the guide's data into the `guides_list` list.
            Returns the item inserted into `guides_list`. """

        loaded_guides_names = [item['guide_name'] for item in self.guides_list]
        guide_archive_path = os.path.join(GUIDES_DIR, guide_name + '.zip')
        if (guide_name in loaded_guides_names
                or not os.path.exists(guide_archive_path)
                or not is_zipfile(guide_archive_path)):
            return None

        guide_extract_path = os.path.join(GUIDES_DIR, guide_name)
        with ZipFile(guide_archive_path, 'r') as zipf:
            zipf.extractall(guide_extract_path)

        with open(os.path.join(guide_extract_path, 'guide.json'), 'r') as f:
            guides_list_item = json.load(f)
        guides_list_item['guide_icon'] = os.path.join(GUIDES_DIR, guide_name, guides_list_item['guide_icon'])
        with open(os.path.join(guide_extract_path, 'guide.json'), 'w') as f:
            json.dump(guides_list_item, f)
        self.guides_list.append(guides_list_item)
        self.guides_list.sort(key=lambda item: item['guide_title'])
        return guides_list_item

    def unload_guide(self, guide_name):
        """ Unloads the guide from application. Raises exception if the guide does not exists. """

        self.guides_list = [item for item in self.guides_list if item['guide_name'] != guide_name]
        shutil.rmtree(os.path.join(GUIDES_DIR, guide_name))


# Guides instance shared all over the application
guides = Guides()
