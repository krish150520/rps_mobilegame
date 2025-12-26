from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivy.resources import resource_add_path
import os
# # from screens.menu import MenuScreen
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# resource_add_path(BASE_DIR)
from screens.menu import MenuScreen
from screens.game import Gamescreen





class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=0.4))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(Gamescreen(name="game"))
        return sm

if __name__ == "__main__":
    MyApp().run()
