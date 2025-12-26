from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Rectangle,Color
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.clock import Clock
from logic.rps_engine import computer_choice,decide_result
import os
from kivy.resources import resource_find
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader
from kivy.graphics import PushMatrix, PopMatrix, Scale



CHOICE_ANIMATIONS = {
    "rock": resource_find("assets\\images\\rock.png"),
    "paper": resource_find("assets\\images\\paper.png"),
    "scissor": resource_find("assets\\images\\scissor.png"),  
}

RESULT_ANIMATIONS = {
    "win": resource_find("assets\\images\\winwin.png"),
    "lose": resource_find("assets\\images\\cry.jpg"),
    "tie": resource_find("assets\\images\\Fern.jpg"),
}
GAME_FONT = resource_find("assets\\fonts\\LuckiestGuy-Regular.ttf")
def outlined_label(text, font_size, main_color, outline_color, offset=(2, -2)):
    container = AnchorLayout(size_hint_y=None)

    outline = Label(
        text=text,
        font_name=GAME_FONT,
        font_size=font_size,
        color=outline_color
    )

    main = Label(
        text=text,
        font_name=GAME_FONT,
        font_size=font_size,
        color=main_color
    )


    container.outline_label = outline
    container.main_label = main

    container.add_widget(outline)
    container.add_widget(main)

    return container




class Imagebutton(ButtonBehavior, Image):
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
        Animation(x=0.9, y=0.9, duration=0.08).start(self._scale)

    def on_release(self):
        Animation.cancel_all(self._scale)
        Animation(x=1, y=1, duration=0.08).start(self._scale)


class Gamescreen(Screen):
 
 
 
 def update_bg(self, instance, value):
       instance.bg.pos = instance.pos
       instance.bg.size = instance.size
 
 def __init__(self, **kwargs):
  super().__init__(**kwargs)
  self.wins = 0
  self.losses = 0
  self.ties = 0

 





  layout=BoxLayout(orientation="vertical",spacing=20,padding=[40, 30, 40, 30])
  button_row = BoxLayout(
    orientation="horizontal",
    spacing=100,
    size_hint=(None, None),
    size=(800, 220)
  )
  # row_container=AnchorLayout(anchor_x="center",anchor_y="center")
  # row_container.size_hint_y = None
  # row_container.height = 260

 
  BG_PATH = resource_find("assets/images/finalbackground.png")
  ROCK_PATH = resource_find("assets/images/orignalr.png")
  PAPER_PATH = resource_find("assets/images/orignalp.png")
  SCISSOR_PATH = resource_find("assets/images/reals.png")
  self.bg_music = SoundLoader.load(
    resource_find("assets/sound/background.wav")
)

  if self.bg_music:
    self.bg_music.loop = True
    self.bg_music.volume = 0.4
    self.bg_music.play()


  self.sounds = {
    "tap": SoundLoader.load(resource_find("assets/sound/tap.wav")),
    "win": SoundLoader.load(resource_find("assets/sound/win.wav")),
    "lose": SoundLoader.load(resource_find("assets/sound/lose.wav")),
    "tie": SoundLoader.load(resource_find("assets/sound/tie.wav")),
}

# Optional: adjust volume
  for s in self.sounds.values():
    if s:
        s.volume = 0.6

 
  with layout.canvas.before:
   layout.bg=Rectangle(source=BG_PATH,pos=layout.pos,size=layout.size)
   layout.bind(pos=self.update_bg,size=self.update_bg)
  
  # with row_container.canvas.before:
  #   Color(1, 0, 0, 0.2)
  #   Rectangle(pos=row_container.pos, size=row_container.size)

  self.img_button1=Imagebutton(source=SCISSOR_PATH,size_hint=(None,None),fit_mode="contain",size=(200,200))
  self.img_button1.bind(on_release=self.clicked)  

  self.img_button2=Imagebutton(source= ROCK_PATH,size_hint=(None,None),fit_mode="contain",size=(200,200))
  self.img_button2.bind(on_release=self.clicked2)  
  self.img_button3=Imagebutton(source=PAPER_PATH,size_hint=(None,None),fit_mode="contain",size=(200,200))
  self.img_button3.bind(on_release=self.clicked3) 
#   self.img_button1.bind(on_release=self.clicked)
#   self.img_button2.bind(on_release=self.clicked2)
#   self.img_button3.bind(on_release=self.clicked3)


  self.title = outlined_label(
    text="SELECT YOUR MOVE",
    font_size=40,
    main_color=(1, 1, 1, 1),
    outline_color=(0, 0, 0, 1)
 )
  self.title.size_hint_y = None
  self.title.height = 70


  self.score_label = outlined_label(
    text="Wins: 0  Losses: 0  Ties: 0",
    font_size=18,
    main_color=(1, 1, 1, 1),
    outline_color=(0, 0, 0, 1),
    # font_name=GAME_FONT,
    # size_hint=(1, None),
    # height=40
  )
  self.score_label.size_hint_y = None
  self.score_label.height = 30


  self.button2=Button()
  self.button3=Button()
  
  
  button_row.add_widget(self.img_button1)
  button_row.add_widget(self.img_button3)  
  button_row.add_widget(self.img_button2)
  center_container = AnchorLayout(
    anchor_x="center",
    anchor_y="center"
 )
  center_container.add_widget(button_row)

#   layout.add_widget(center_container)
  layout.add_widget(self.title)
  layout.add_widget(self.score_label)
  layout.add_widget(Widget(size_hint_y=1.2))
  layout.add_widget(center_container)
  layout.add_widget(Widget(size_hint_y=1))
#   layout.add_widget(Widget(size_hint_y=0.35))

#   layout.add_widget(row_container)
#   layout.add_widget(Widget(size_hint_y=0.25))
  self.add_widget(layout)


  # return layout

 def show_popup(self, text=None, image_path=None, duration=1.0, next_step=None):
   layout = BoxLayout(orientation="vertical", spacing=15, padding=20)
   layout.opacity = 0
  #  layout.scale = 0.8


   if image_path:
        layout.add_widget(
         Image(
         source=image_path,
         fit_mode="contain",
         size_hint=(1, 0.75)
         )
        )


   if text:
        layout.add_widget(
        outlined_label(
        text=text,
        font_size=26,
        main_color=(1, 1, 1, 1),
        outline_color=(0, 0, 0, 1)
    )
)


   popup = Popup(
        content=layout,
        size_hint=(0.7, 0.5),
        auto_dismiss=False
    )

   popup.open()
   # Animate IN
   anim_in = Animation(opacity=1, duration=0.25)
   anim_in.start(layout)
   def close_popup(dt):
    anim_out = Animation(opacity=0, duration=0.2)

    def _close(*args):
        popup.dismiss()
        if next_step:
            next_step()

    anim_out.bind(on_complete=lambda *x: _close())
    anim_out.start(layout)
   Clock.schedule_once(close_popup, duration)

 def clicked(self,instance):
   self.play_sound("tap")
   print("scissor button clicked")
   self.real_mastermind("scissor")

 def clicked2(self,instance):
   self.play_sound("tap")
   print("rock button clicked")
   self.real_mastermind("rock")

 
 def clicked3(self,instance):
   self.play_sound("tap")
   print("paper button clicked")
   self.real_mastermind("paper")


 def real_mastermind(self, choice):
    Clock.schedule_once(lambda dt: self.disable_buttons(), 0.12)
    self.user_choice = choice
    self.computer_choice = computer_choice()
    self.result = decide_result(self.user_choice, self.computer_choice)

    self.show_user_popup()
    # print("CHOICE_ANIMATIONS:", CHOICE_ANIMATIONS)
    # print("RESULT_ANIMATIONS:", RESULT_ANIMATIONS)


 def show_user_popup(self):
    anim = CHOICE_ANIMATIONS.get(self.user_choice)

    self.show_popup(
        text=f"You chose {self.user_choice}",
        image_path=anim,
        duration=1.0,
        next_step=self.show_computer_popup
    )
 def show_computer_popup(self):
    anim = CHOICE_ANIMATIONS.get(self.computer_choice)

    self.show_popup(
        text=f"Computer chose {self.computer_choice}",
        image_path=anim,
        duration=1.0,
        next_step=self.show_result_popup
    )
 
 def show_result_popup(self):
    anim = RESULT_ANIMATIONS.get(self.result)

    self.show_popup(
        text=self.result.upper(),
        image_path=anim,
        duration=1.5,
        next_step=self.end_round
    )


 def disable_buttons(self):
    self.img_button1.disabled = True
    self.img_button2.disabled = True
    self.img_button3.disabled = True

 def enable_buttons(self):
    self.img_button1.disabled = False
    self.img_button2.disabled = False
    self.img_button3.disabled = False
   
 def end_round(self):
    if self.result == "win":
        self.wins += 1
        self.play_sound("win")
    elif self.result == "lose":
         self.losses += 1
         self.play_sound("lose")
    else:
         self.ties += 1
         self.play_sound("tie")
        #  self.update_score_text()
        #  self.enable_buttons()

    self.update_score_text()
    self.enable_buttons()
    print("END ROUND CALLED")
    print(self.wins, self.losses, self.ties)
 
 def update_score_text(self):
    text = f"Wins: {self.wins}  Losses: {self.losses}  Ties: {self.ties}"
    self.score_label.main_label.text = text
    self.score_label.outline_label.text = text



 def play_sound(self, name):
    sound = self.sounds.get(name)
    if sound:
        sound.stop()   # allow rapid replay
        sound.play()

    # self.enable_buttons()
   
# myapp().run()  