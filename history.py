from events import ev
from models import guides


class ScreensHistory:
    def __init__(self):
        self.guides_history_list = [{'guide_name': item['guide_name'], 'visited_screens': []}
                                    for item in guides.guides_list]
        self._promote_active_guide_history()
        ev.bind(on_active_guide=self._promote_active_guide_history)
        ev.bind(on_import_guide=self._add_guides_history_list_item)
        ev.bind(on_remove_guide=self._delete_guides_history_list_item)

    def _promote_active_guide_history(self, *args):
        if self.guides_history_list:
            active_guide_history_idx = next(idx for idx, item in enumerate(self.guides_history_list)
                                            if item['guide_name'] == guides.active_guide.guide_name)
            self.guides_history_list.append(self.guides_history_list.pop(active_guide_history_idx))

    def _add_guides_history_list_item(self, instance, guide_name):
        self.guides_history_list.insert(0, {'guide_name': guide_name, 'visited_screens': []})

    def _delete_guides_history_list_item(self, instance, guide_name):
        if self.guides_history_list[-1]['guide_name'] == guide_name:
            if len(self.guides_history_list) > 1:
                guides.set_active_guide(self.guides_history_list[-2]['guide_name'])
            else:
                guides.set_active_guide('')
            del self.guides_history_list[-1]
            ev.dispatch('on_active_guide')
        else:
            item_idx = next(idx for idx, item in enumerate(self.guides_history_list)
                            if item['guide_name'] == guide_name)
            del self.guides_history_list[item_idx]

    def pop_screen(self):
        if not self.guides_history_list:
            return None
        if self.guides_history_list[-1]['visited_screens']:
            active_guide_last_visited_screen = self.guides_history_list[-1]['visited_screens'].pop()
            return active_guide_last_visited_screen
        else:
            prev_guides_history_list_item = self._get_guides_history_list_item_with_last_visited_screen()
            if prev_guides_history_list_item is None:
                return None
            last_visited_screen = prev_guides_history_list_item['visited_screens'].pop()
            guides.set_active_guide(prev_guides_history_list_item['guide_name'])
            ev.dispatch('on_active_guide')
            return last_visited_screen

    def _get_guides_history_list_item_with_last_visited_screen(self):
        try:
            history_list_item = next(item for item in self.guides_history_list[::-1] if item['visited_screens'])
        except StopIteration:
            return None
        return history_list_item

    def append_screen(self, screen_name, model_id=None):
        last_visited_screen = (screen_name, model_id)
        visited_screens = [screen for screen in self.guides_history_list[-1]['visited_screens']
                           if screen != last_visited_screen] + [last_visited_screen]
        self.guides_history_list[-1]['visited_screens'] = visited_screens


    # def pop_active_guide_history_prev_screen(self):
    #     if not(self.screens_history and self.screens_history[-1][1]):
    #         return None
    #     return self.screens_history[-1][1].pop()
    #
    # def push_active_guide_history_screen(self, screen_name, screen_content_name):
    #     if (screen_name, screen_content_name) in self.screens_history:
    #         self.screens_history.remove((screen_name, screen_content_name))
    #     self.screens_history[-1][1].append((screen_name, screen_content_name))
    #
    # def switch_to_active_guide_history(self):
    #     active_guide_history_idx = next(idx for idx, guide_history in enumerate(self.screens_history)
    #                                     if guide_history[0] == guides.active_guide_name)
    #     active_guide_history = self.screens_history.pop(active_guide_history_idx)
    #     self.screens_history.append(active_guide_history)
    #
    # def is_current_screen_active_guide_history_prev_screen(self, screen_name, screen_content_name):
    #     if not(self.screens_history and self.screens_history[-1][1]):
    #         return False
    #     return self.screens_history[-1][1][-1] == (screen_name, screen_content_name)
    #
    # def active_guide_history_has_prev_screen(self):
    #     return self.screens_history[-1][1]
    #
    # def other_guide_history_has_prev_screen(self):
    #     if not self.screens_history:
    #         return False
    #     try:
    #         next(guide_history for guide_history in reversed(self.screens_history) if guide_history[1])
    #     except StopIteration:
    #         return False
    #     return True
    #
    # def name_of_other_guide_with_prev_screen_in_history(self):
    #     if not self.screens_history:
    #         return ''
    #     try:
    #         other_guide_history = next(guide_history for guide_history in reversed(self.screens_history)
    #                                    if guide_history[1])
    #     except StopIteration:
    #         return ''
    #     return other_guide_history[0]
    #
    # def remove_guide_history(self, guide_name):
    #     self.screens_history = [guide_history for guide_history in self.screens_history
    #                             if guide_name != guide_history[0]]
    #
    # def add_guide_history(self, guide_name):
    #     self.screens_history.insert(0, (guide_name, []))


hist = ScreensHistory()
