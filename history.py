from events.global_events import ev
from models.guides_model import guides


class ScreensHistory:
    def __init__(self):
        self.guides_history_list = [{'guide_name': item['guide_name'], 'visited_screens': []}
                                    for item in guides.guides_list]
        self._promote_active_guide_history()
        ev.bind(on_active_guide=self._promote_active_guide_history)
        ev.bind(on_load_guide=self._add_guides_history_list_item)
        ev.bind(on_unload_guide=self._delete_guides_history_list_item)

    def _promote_active_guide_history(self, *args):
        if self.guides_history_list:
            active_guide_history_idx = next(idx for idx, item in enumerate(self.guides_history_list)
                                            if item['guide_name'] == guides.active_guide.guide_name)
            self.guides_history_list.append(self.guides_history_list.pop(active_guide_history_idx))

    def _add_guides_history_list_item(self, instance, guide_name):
        self.guides_history_list.insert(0, {'guide_name': guide_name, 'visited_screens': []})
        if len(guides.guides_list) == 1:
            guides.set_active_guide(guide_name)
            ev.dispatch('on_active_guide')
        ev.dispatch('on_change_guides_list')

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
        ev.dispatch('on_change_guides_list')

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

    def remove_screen(self, screen_name, model_id):
        if self.guides_history_list and (screen_name, model_id) in self.guides_history_list[-1]['visited_screens']:
            self.guides_history_list[-1]['visited_screens'].remove((screen_name, model_id))

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


hist = ScreensHistory()
