from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import io, os
from kivy.core.image import Image as CoreImage
import numpy as np

KV = '''

MDFloatLayout:

    Image:
        source: "background.jpg"
        allow_stretch: True
        keep_ratio: False
        opacity: 0.25

    MDCard:
        id: glass_card
        size_hint: 0.92, 0.9
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        radius: [35]
        md_bg_color: 1,1,1,0.12
        elevation: 20
        padding: 20
        orientation: "vertical"

        FitImage:
            id: cover
            source: app.cover_path
            size_hint_y: 0.4
            radius: [25,]

        MDLabel:
            text: app.current_title
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0,1,1,1

        MDProgressBar:
            id: progress
            value: app.progress_value

        BoxLayout:
            size_hint_y: 0.2
            id: visualizer
            spacing: 3
            padding: 5

        ScrollView:
            size_hint_y: 0.3
            MDList:
                id: song_list

        BoxLayout:
            size_hint_y: None
            height: "70dp"
            spacing: 30
            padding: 10

            MDIconButton:
                id: play_btn
                icon: "play-circle"
                icon_size: "60sp"
                theme_text_color: "Custom"
                text_color: 0,1,1,1
                on_release: app.play_song()

            MDIconButton:
                icon: "pause-circle"
                icon_size: "60sp"
                theme_text_color: "Custom"
                text_color: 1,1,0,1
                on_release: app.pause_song()

            MDIconButton:
                icon: "stop-circle"
                icon_size: "60sp"
                theme_text_color: "Custom"
                text_color: 1,0.3,0.6,1
                on_release: app.stop_song()
'''

class UltraGlassPlayer(MDApp):

    current_title = StringProperty("Sélectionne une musique")
    progress_value = NumericProperty(0)
    cover_path = StringProperty("background.jpg")
    is_playing = BooleanProperty(False)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.sound = None
        self.song_length = 1
        self.song_folder = "musiques"  # dossier spécifique
        self.song_paths = []
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.load_songs(), 1)
        self.create_visualizer()
        return root

    # 📂 Charge les musiques depuis le dossier choisi
    def load_songs(self):
        if not os.path.exists(self.song_folder):
            os.makedirs(self.song_folder)

        from kivymd.uix.list import OneLineListItem
        for file in os.listdir(self.song_folder):
            if file.endswith(".mp3"):
                full_path = os.path.join(self.song_folder, file)
                self.song_paths.append(full_path)
                item = OneLineListItem(
                    text=file,
                    on_release=lambda x, p=full_path: self.select_song(p)
                )
                self.root.ids.song_list.add_widget(item)

    # 🎵 Sélectionne une chanson + cover Spotify-style
    def select_song(self, path):
        if self.sound:
            self.sound.stop()

        self.sound = SoundLoader.load(path)
        if self.sound:
            self.current_title = os.path.basename(path)
            self.song_length = self.sound.length if self.sound.length else 1
            self.progress_value = 0
            self.extract_cover(path)
            self.animate_cover()

    # 🎵 Extraction cover ID3
    def extract_cover(self, path):
        try:
            audio = ID3(path)
            for tag in audio.values():
                if tag.FrameID == "APIC":
                    data = io.BytesIO(tag.data)
                    img = CoreImage(data, ext="jpg")
                    self.cover_path = data
                    return
        except:
            self.cover_path = "background.jpg"

    # ▶ Lecture
    def play_song(self):
        if self.sound:
            self.sound.play()
            self.is_playing = True
            Clock.schedule_interval(self.update_progress, 0.5)
            Clock.schedule_interval(self.update_visualizer, 0.1)
            self.neon_effect()

    def pause_song(self):
        if self.sound:
            self.sound.stop()
            self.is_playing = False

    def stop_song(self):
        if self.sound:
            self.sound.stop()
            self.progress_value = 0
            self.is_playing = False

    # 🎚 Progression animée
    def update_progress(self, dt):
        if self.sound and self.sound.get_pos():
            position = self.sound.get_pos()
            self.progress_value = (position / self.song_length) * 100

    # 📀 Effet disque vinyle
    def animate_cover(self):
        anim = Animation(rotation=360, duration=10)
        anim.repeat = True
        anim.start(self.root.ids.cover)

    # 🌈 Effet néon sur bouton
    def neon_effect(self):
        anim = Animation(text_color=(1,0,1,1), duration=0.5) + Animation(text_color=(0,1,1,1), duration=0.5)
        anim.repeat = True
        anim.start(self.root.ids.play_btn)

    # 🎼 Visualiseur audio simple
    def create_visualizer(self):
        for i in range(20):
            bar = Widget(size_hint_x=None, width=5)
            with bar.canvas:
                Color(0,1,1,1)
                bar.rect = Rectangle(size=(5,50))
            self.root.ids.visualizer.add_widget(bar)

    def update_visualizer(self, dt):
        import random
        for bar in self.root.ids.visualizer.children:
            height = random.randint(20,120)
            bar.rect.size = (5,height)

UltraGlassPlayer().run()