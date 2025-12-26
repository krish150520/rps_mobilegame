from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.app import App
from kivy.resources import resource_find
from kivy.animation import Animation
import os
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import PushMatrix, PopMatrix, Scale
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import sys



BG_PATH1 = resource_find("assets\\images\\finalmain.png")
START_IMG = resource_find("assets\\images\\startbutton.png")
EXIT_IMG = resource_find("assets\\images\\exitbutton.png")

# from kivy.graphics import PushMatrix, PopMatrix, Scale
# from kivy.animation import Animation

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            self._scale = Scale(1, 1, 1)
            self._scale.origin = self.center

        with self.canvas.after:
            PopMatrix()

        self.bind(center=self._update_origin)

    def _update_origin(self, *args):
        self._scale.origin = self.center

    def on_press(self):
        Animation.cancel_all(self._scale)
        Animation(
            x=0.92,
            y=0.92,
            duration=0.08,
            t="out_quad"
        ).start(self._scale)

    def on_release(self):
        Animation.cancel_all(self._scale)
        Animation(
            x=1,
            y=1,
            duration=0.12,
            t="out_back"
        ).start(self._scale)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg_rect = Rectangle(source=BG_PATH1, pos=self.pos, size=self.size)

        self.bind(size=self._update_bg, pos=self._update_bg)

        root = AnchorLayout(anchor_x="center", anchor_y="center")
        self.click_sound = SoundLoader.load(
          resource_find("assets/sound/tap.wav")
       )

        if self.click_sound:
           self.click_sound.volume = 0.6


        layout = BoxLayout(
            orientation="vertical",
            spacing=35,
            size_hint=(None, None),
            size=(350, 250)
        )

        self.start_btn = ImageButton(
            source=START_IMG,
            size_hint=(None, None),
            size=(300, 190)
        )

        self.exit_btn = ImageButton(
            source=EXIT_IMG,
            size_hint=(None, None),
            size=(300, 190)
        )

        self.start_btn.bind(on_release=self.start_game)
        self.exit_btn.bind(on_release=self.exit_game)

        layout.add_widget(self.start_btn)
        layout.add_widget(self.exit_btn)

        root.add_widget(layout)
        self.add_widget(root)
        print("MENU BG:", BG_PATH1)


    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def start_game(self, *args):
         self.play_click()
         self.manager.current = "game"
    def exit_game(self, *args):
        self.play_click()
        App.get_running_app().stop()
        sys.exit()


    def play_click(self):
     if self.click_sound:
        self.click_sound.stop()  
        self.click_sound.play()