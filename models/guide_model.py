import os
import shutil
import tarfile
import json


class GuideModel:
    GUIDES_DIR = 'guides'
    guides_list = []
    active_guide = None
    active_guide_path = None

    def __init__(self):
        guides_list_filename = os.path.join(self.GUIDES_DIR, 'guides.json')
        with open(guides_list_filename, 'r') as guides_list_file:
            self.guides_list = json.load(guides_list_file)
        if len(self.guides_list) > 0:
            self.active_guide = next(list_item for list_item in self.guides_list if list_item['is_active'])
            self.active_guide_path = os.path.join(self.GUIDES_DIR, self.active_guide['name'])

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
                self.active_guide = list_item
                self.active_guide_path = os.path.join(self.GUIDES_DIR, self.active_guide['name'])
        with open(os.path.join(self.GUIDES_DIR, 'guides.json'), 'w') as guides_list_file:
            json.dump(self.guides_list, guides_list_file)

    def load(self, guide_archive):
        """Load a guide from a corresponding archive"""
        guide_name = os.path.basename(guide_archive)[:-4]  # Expects tgz file extension
        guide_path = os.path.join(self.GUIDES_DIR, guide_name)
        if os.path.exists(guide_path):
            shutil.rmtree(guide_path)
            for list_item in self.guides_list:
                if list_item['name'] == guide_name:
                    del list_item
        os.mkdir(guide_path)
        with tarfile.open(guide_archive, 'r:gz') as tar:
            tar.extractall(guide_path)
        with open(os.path.join(guide_path, 'guide.json'), 'r') as guide_file:
            guide = json.load(guide_file)
        guide['is_active'] = len(self.guides_list) == 0
        self.guides_list.append(guide)
        with open(os.path.join(self.GUIDES_DIR, 'guides.json'), 'w') as guides_list_file:
            json.dump(self.guides_list, guides_list_file)

    def unload(self, guide_name):
        """Remove the guide and all its content"""
        guide_dir = os.path.join(self.GUIDES_DIR, guide_name)
        shutil.rmtree(guide_dir)
        for list_item in self.guides_list:
            if list_item['name'] == guide_name:
                del list_item
        if len(self.guides_list) > 0:
            self.activate(self.guides_list[0]['name'])
        else:
            self.active_guide = None
            with open(os.path.join(self.GUIDES_DIR, 'guides.json'), 'w') as guides_list_file:
                json.dump(self.guides_list, guides_list_file)
