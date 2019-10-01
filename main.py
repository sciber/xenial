import kivy

from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.11.1')


class XenialApp(App):
    def build(self):
        return Label(text='Xenial')


if __name__ == '__main__':
    app = XenialApp()
    app.run()
