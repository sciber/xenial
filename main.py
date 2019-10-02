import kivy

from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer


kivy.require('1.11.1')


class ApplicationRoot(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavigationDrawer, self).__init__(**kwargs)


class XenialApp(App):
    def build(self):
        return ApplicationRoot()

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = XenialApp()
    app.run()
