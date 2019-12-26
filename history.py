from models import guides


class VisitedScreensHistory:
    def __init__(self):
        self.screens_history = [(guide['name'], []) for guide in guides.all()
                                if guide['name'] != guides.active_guide_name]
        if guides.active_guide_name:
            self.screens_history.append((guides.active_guide_name, []))

    def pop_active_guide_history_prev_screen(self):
        if not(self.screens_history and self.screens_history[-1][1]):
            return None
        return self.screens_history[-1][1].pop()

    def push_active_guide_history_screen(self, screen_name, screen_content_name):
        if (screen_name, screen_content_name) in self.screens_history:
            self.screens_history.remove((screen_name, screen_content_name))
        self.screens_history[-1][1].append((screen_name, screen_content_name))

    def switch_to_active_guide_history(self):
        active_guide_history_idx = next(idx for idx, guide_history in enumerate(self.screens_history)
                                        if guide_history[0] == guides.active_guide_name)
        active_guide_history = self.screens_history.pop(active_guide_history_idx)
        self.screens_history.append(active_guide_history)

    def is_current_screen_active_guide_history_prev_screen(self, screen_name, screen_content_name):
        if not(self.screens_history and self.screens_history[-1][1]):
            return False
        return self.screens_history[-1][1][-1] == (screen_name, screen_content_name)

    def active_guide_history_has_prev_screen(self):
        return self.screens_history[-1][1]

    def other_guide_history_has_prev_screen(self):
        if not self.screens_history:
            return False
        try:
            next(guide_history for guide_history in reversed(self.screens_history) if guide_history[1])
        except StopIteration:
            return False
        return True

    def name_of_other_guide_with_prev_screen_in_history(self):
        if not self.screens_history:
            return ''
        try:
            other_guide_history = next(guide_history for guide_history in reversed(self.screens_history)
                                       if guide_history[1])
        except StopIteration:
            return ''
        return other_guide_history[0]

    def remove_guide_history(self, guide_name):
        self.screens_history = [guide_history for guide_history in self.screens_history
                                if guide_name != guide_history[0]]

    def add_guide_history(self, guide_name):
        self.screens_history.insert(0, (guide_name, []))


history = VisitedScreensHistory()
