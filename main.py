from kivy.uix.gridlayout import GridLayout
import uuid
import hashlib
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
import webbrowser
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import requests
import random
from datetime import datetime, timedelta

primary_color = "#2196F3"
secondary_color = "#BBDEFB"
background_color = (0.1, 0.1, 0.1, 0.1)  # Darker background for better contrast
text_color = "#FFFFFF"
font_path = "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"
font_size = dp(30)
def generate_uid(name, likes):
    unique_string = f"{name}{likes}{uuid.uuid4().hex}"
    hash_object = hashlib.md5(unique_string.encode())
    return f"UID-{hash_object.hexdigest()[:8]}"
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(*background_color)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        image = Image(source='C:/Users/Aadit/Downloads/DigiFriend logo.png', size_hint=(0.5, 0.5),
                      pos_hint={'center_x': 0.5, 'center_y': 0.72})
        layout.add_widget(image)

        welcome_label = Label(text="Welcome to DigiFriend (Parents)", font_size=50, color=primary_color,
                              pos_hint={'center_x': 0.5, 'center_y': 0.41}, font_name=font_path)
        layout.add_widget(welcome_label)

        start_button = Button(text="Signup", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.30},
                              background_color=primary_color, font_name=font_path, font_size=30)
        start_button.bind(on_press=self.switch_to_input)
        layout.add_widget(start_button)

        mainline_button = Button(text="Show analysis", size_hint=(0.4, 0.09),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.2000000002},
                                 background_color=primary_color, font_name=font_path, font_size=30)
        mainline_button.bind(on_press=self.open_hourly_reports)
        layout.add_widget(mainline_button)

        # Add Cancel button
        cancel_button = Button(text="Exit", size_hint=(0.09, 0.02), pos_hint={'center_x': 0.5, 'center_y': 0.03},
                               background_color=primary_color, font_name=font_path, font_size=22)
        cancel_button.bind(on_press=self.cancel_app)
        layout.add_widget(cancel_button)

        initiate_button = Button(text="Initiate Child's App", size_hint=(0.4, 0.09),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                 background_color=primary_color, font_name=font_path, font_size=30)
        initiate_button.bind(on_press=self.open_lookup_popup)
        layout.add_widget(initiate_button)

        self.add_widget(layout)

    def open_lookup_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.uid_input = TextInput(multiline=False, hint_text='Enter UID', font_name=font_path)
        lookup_button = Button(text='Lookup', font_name=font_path)
        close_button = Button(text='Close', font_name=font_path)

        self.result_label = Label(text="", font_name=font_path)
        self.likes_label = Label(text="", font_name=font_path)
        self.dislikes_label = Label(text="", font_name=font_path)
        self.subject_label = Label(text="", font_name=font_path)
        self.language_label = Label(text="", font_name=font_path)

        content.add_widget(self.uid_input)
        content.add_widget(lookup_button)
        content.add_widget(self.result_label)
        content.add_widget(self.likes_label)
        content.add_widget(self.dislikes_label)
        content.add_widget(self.subject_label)
        content.add_widget(self.language_label)
        content.add_widget(close_button)

        self.popup = Popup(title='UID Lookup', content=content, size_hint=(0.9, 0.9))

        lookup_button.bind(on_press=self.lookup_uid)
        close_button.bind(on_press=self.popup.dismiss)

        self.popup.open()


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_to_input(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'input'

    def switch_to_mainline(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'mainline'

    def open_hourly_reports(self, instance):
        self.manager.current = 'hourly_reports'

    def cancel_app(self, instance):
        App.get_running_app().stop()

    def lookup_uid(self, instance):
        uid = self.uid_input.text
        response = requests.post('http://127.0.0.1:5000/get_data', json={'uid': uid})

        if response.status_code == 200:
            data = response.json()
            name = data['name']
            likes = data['likes']
            dislikes = data['dislikes']
            favorite_subject = data['favorite_subject']
            language = data['language']

            self.result_label.text = f"Hello {name}!"
            self.likes_label.text = f"Likes: {likes}"
            self.dislikes_label.text = f"Dislikes: {dislikes}"
            self.subject_label.text = f"Favorite Subject: {favorite_subject}"
            self.language_label.text = f"Language: {language}"

            # Open the appropriate website based on the language
            language_urls = {
                'Bengali': 'https://digifriend.site/bengali',
                'English': 'https://digifriend.site',
                'Hindi': 'https://digifriend.site/hindi',
                'Chinese': 'https://digifriend.site/chinese',
                'French': 'https://digifriend.site/french',
                'German': 'https://digifriend.site/german',
                'Gujarati': 'https://digifriend.site/gujarati',
                'Italian': 'https://digifriend.site/italian',
                'Japanese': 'https://digifriend.site/japanese',
                'Kannada': 'https://digifriend.site/kannada',
                'Malayalam': 'https://digifriend.site/malayalam',
                'Marathi': 'https://digifriend.site/marathi',
                'Punjabi': 'https://digifriend.site/punjabi',
                'Tamil': 'https://digifriend.site/tamil',
                'Telugu': 'https://digifriend.site/telugu',
                'Urdu': 'https://digifriend.site/urdu'
            }

            if language in language_urls:
                webbrowser.open(language_urls[language])
            else:
                print(f"No specific URL for language: {language}")

        else:
            self.result_label.text = """
            Invalid UID. 
            Please generate another, or try again.
            """
            self.likes_label.text = ""
            self.dislikes_label.text = ""
            self.subject_label.text = ""
            self.language_label.text = ""


class InputScreen(Screen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*background_color)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text="Enter Your Details", font_size=50, font_name=font_path, color=primary_color)
        layout.add_widget(title_label)

        self.name_input = TextInput(hint_text="Your child's name", multiline=False, font_name=font_path, font_size=35,
                                    hint_text_color=(1,1,1,1),background_color=(0.6, 0.9, 1, 1))
        layout.add_widget(self.name_input)

        self.likes_input = TextInput(hint_text="What your child likes (Please enter multiple hobbies)", multiline=False, font_name=font_path, font_size=35,
                                     hint_text_color=(1,1,1,1), background_color=(0.6, 0.8, 1, 1))
        layout.add_widget(self.likes_input)

        self.dislikes_input = TextInput(hint_text="What your child dislikes/fears (DigiFriend will avoid it)", multiline=False, font_name=font_path, font_size=35,
                                        hint_text_color=(1,1,1,1), background_color=(0.4, 0.6, 1, 1))
        layout.add_widget(self.dislikes_input)

        # Dark blue
        self.favorite_subject_input = TextInput(hint_text="Your child's favorite subject", multiline=False, font_name=font_path, font_size=35,
                                                hint_text_color=(1,1,1,1), background_color=(0.2, 0.4, 0.8, 1))
        layout.add_widget(self.favorite_subject_input)

        languages = ['Bengali', 'English', 'Hindi', 'Chinese', 'French', 'German', 'Gujarati',
                     'Italian', 'Japanese', 'Kannada', 'Malayalam', 'Marathi', 'Punjabi',
                     'Tamil', 'Telugu', 'Urdu']
        self.language_spinner = Spinner(text='Select Language', values=languages, font_name=font_path, font_size=35,
                                        background_color=(0.2, 0.6, 1, 1))
        layout.add_widget(self.language_spinner)

        generate_button = Button(text="Generate UID", size_hint_y=None, height=50,
                                 background_color=primary_color, font_name=font_path, font_size=30,)
        generate_button.bind(on_press=self.generate_uid)
        layout.add_widget(generate_button)

        # Add Back button
        back_button = Button(text="Back", size_hint_y=None, height=50,
                             background_color=primary_color, font_name=font_path, font_size=30)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generate_uid(self, instance):
        name = self.name_input.text
        likes = self.likes_input.text
        dislikes = self.dislikes_input.text
        favorite_subject = self.favorite_subject_input.text
        language = self.language_spinner.text
        uid = generate_uid(name, likes)
        self.manager.get_screen('result').set_uid(uid)
        self.manager.transition = FadeTransition()
        self.manager.current = 'result'

        # Send UID to server
        data = {'uid': uid, 'name': name, 'likes': likes, 'dislikes': dislikes,
                'favorite_subject': favorite_subject, 'language': language}
        response = requests.post('http://127.0.0.1:5000/store_data', json=data)
        if response.status_code == 200:
            print("Data stored successfully")
        else:
            print("Error storing data")

    def go_back(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'welcome'


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.particles = []
        Clock.schedule_once(self.setup_background, 0)
        self.layout = FloatLayout()
        self.setup_background(None)

        with self.layout.canvas.before:
            Color(0.05, 0.05, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        self.title = Label(text="Your Generated UID", font_size=dp(65), pos_hint={'center_x': 0.5, 'center_y': 0.9},
                           color=(0.2, 0.6, 1, 1), font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",)
        self.layout.add_widget(self.title)

        self.uid_label = Label(text="", font_size=dp(50), halign='center',
                               pos_hint={'center_x': 0.5, 'center_y': 0.6},
                               color=(0.2, 0.8, 1, 1))
        self.layout.add_widget(self.uid_label)

        self.copy_button = Button(text="Tap to copy", size_hint=(0.3, 0.08), font_size = 30,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                  background_color=(0.2, 0.6, 1, 1), font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",)
        self.copy_button.bind(on_press=self.copy_uid)
        self.layout.add_widget(self.copy_button)

        self.generate_another_button = Button(text="Generate Another", size_hint=(0.5, 0.08),
                                              pos_hint={'center_x': 0.5, 'center_y': 0.3}, font_size=35,
                                              background_color=(0.2, 0.6, 1, 1), font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",)
        self.generate_another_button.bind(on_press=self.generate_another)
        self.layout.add_widget(self.generate_another_button)

        self.mainline_button = Button(text="View Analysis", size_hint=(0.5, 0.08),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.2}, font_size=35,
                                      background_color=(0.2, 0.6, 1, 1), font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",)
        self.mainline_button.bind(on_press=self.open_hourly_reports)
        self.layout.add_widget(self.mainline_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_uid(self, uid):
        self.uid_label.text = uid
        anim = Animation(color=(1, 1, 0, 1), duration=0.5) + Animation(color=(0.2, 0.8, 1, 1), duration=0.5)
        anim.repeat = True
        anim.start(self.uid_label)

    def copy_uid(self, instance):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.uid_label.text)
        instance.text = "Copied!"
        Clock.schedule_once(lambda dt: setattr(instance, 'text', "Tap to copy"), 1)

    def generate_another(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'input'

    def switch_to_mainline(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'mainline'

    def setup_background(self, dt):
        with self.canvas.before:
            Color(0.05, 0.05, 0.1)  # Dark background
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Clear existing particles
        self.canvas.after.clear()
        self.particles.clear()

        # Create particles
        for i in range(100):
            self.create_particle()

        Clock.schedule_interval(self.update_particles, 0.1)

    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
        # Reposition particles when the widget size changes
        for particle in self.particles:
            particle.pos = (random.uniform(0, self.width), random.uniform(0, self.height))

    def restart_particle_animation(self, animation, particle):
        new_anim = Animation(
            pos=(random.uniform(0, self.width), random.uniform(0, self.height)),
            duration=random.uniform(2, 2)
        )
        new_anim.bind(on_complete=self.restart_particle_animation)
        new_anim.start(particle)

    def create_particle(self):
        with self.canvas.after:
            Color(random.uniform(0.2, 0.8), random.uniform(0.4, 1), 1, 0.5)
            size = random.randint(3, 8)
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            particle = Ellipse(pos=(x, y), size=(size, size))
            self.particles.append(particle)

        anim = Animation(
            pos=(random.uniform(0, self.width), random.uniform(0, self.height)),
            duration=random.uniform(3, 3)
        )
        anim.bind(on_complete=self.restart_particle_animation)
        anim.start(particle)

    def update_particles(self, dt):
        if self.width == 0 or self.height == 0:
            return  # Skip if the widget has no size yet

        for particle in self.particles:
            # Ensure particles stay within bounds
            x, y = particle.pos
            if x < 0 or x > self.width or y < 0 or y > self.height:
                particle.pos = (random.uniform(0, self.width), random.uniform(0, self.height))

    def open_hourly_reports(self, instance):
        self.manager.current = 'hourly_reports'


class MainlineScreen(Screen):
    def __init__(self, **kwargs):
        super(MainlineScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create Top Bar
        self.create_top_bar()

        # Create Graph Section
        self.create_graph_section()

        # Add Lookup Button
        self.create_lookup_button()

        # Add View Hourly Reports Button
        self.create_hourly_reports_button()

        self.add_widget(self.layout)

    def create_hourly_reports_button(self):
        hourly_reports_button = Button(
            text='View Hourly Reports',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1),
            font_name=font_path
        )
        hourly_reports_button.bind(on_press=self.open_hourly_reports)
        self.layout.add_widget(hourly_reports_button)

    def open_hourly_reports(self, instance):
        self.manager.current = 'hourly_reports'

    def create_top_bar(self):
        top_bar = BoxLayout(size_hint=(1, None), height=dp(60), spacing=10)
        menu_button = Button(text='≡', size_hint=(None, 1), width=dp(60),
                             background_color=(0.2, 0.6, 1, 1))
        menu_button.bind(on_press=self.show_menu)
        top_bar.add_widget(menu_button)

        logo = Image(source='C:/Users/Aadit/Downloads/DigiFriend logo.png', size_hint=(None, None),
                     size=(dp(50), dp(50)))
        top_bar.add_widget(logo)

        digifriend_label = Label(text='', color=(0.2, 0.6, 1, 1),
                                 font_name=font_path,
                                 font_size=dp(24),
                                 size_hint=(1, 1),
                                 halign='center')
        top_bar.add_widget(digifriend_label)
        self.layout.add_widget(top_bar)

    def create_lookup_button(self):
        lookup_button = Button(
            text='Initiate child\'s app',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1),
            font_name=font_path
        )
        lookup_button.bind(on_press=self.open_lookup_popup)
        self.layout.add_widget(lookup_button)

    def open_lookup_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.uid_input = TextInput(multiline=False, hint_text='Enter UID', font_name=font_path)
        lookup_button = Button(text='Lookup', font_name=font_path)
        close_button = Button(text='Close', font_name=font_path)

        self.result_label = Label(text="", font_name=font_path)
        self.likes_label = Label(text="", font_name=font_path)
        self.dislikes_label = Label(text="", font_name=font_path)
        self.subject_label = Label(text="", font_name=font_path)
        self.language_label = Label(text="", font_name=font_path)

        content.add_widget(self.uid_input)
        content.add_widget(lookup_button)
        content.add_widget(self.result_label)
        content.add_widget(self.likes_label)
        content.add_widget(self.dislikes_label)
        content.add_widget(self.subject_label)
        content.add_widget(self.language_label)
        content.add_widget(close_button)

        self.popup = Popup(title='UID Lookup', content=content, size_hint=(0.9, 0.9))

        lookup_button.bind(on_press=self.lookup_uid)
        close_button.bind(on_press=self.popup.dismiss)

        self.popup.open()

    def lookup_uid(self, instance):
        uid = self.uid_input.text
        response = requests.post('http://127.0.0.1:5000/get_data', json={'uid': uid})

        if response.status_code == 200:
            data = response.json()
            name = data['name']
            likes = data['likes']
            dislikes = data['dislikes']
            favorite_subject = data['favorite_subject']
            language = data['language']

            self.result_label.text = f"Hello {name}!"
            self.likes_label.text = f"Likes: {likes}"
            self.dislikes_label.text = f"Dislikes: {dislikes}"
            self.subject_label.text = f"Favorite Subject: {favorite_subject}"
            self.language_label.text = f"Language: {language}"

            # Open the appropriate website based on the language
            language_urls = {
                'Bengali': 'https://digifriend.site/bengali',
                'English': 'https://digifriend.site',
                'Hindi': 'https://digifriend.site/hindi',
                'Chinese': 'https://digifriend.site/chinese',
                'French': 'https://digifriend.site/french',
                'German': 'https://digifriend.site/german',
                'Gujarati': 'https://digifriend.site/gujarati',
                'Italian': 'https://digifriend.site/italian',
                'Japanese': 'https://digifriend.site/japanese',
                'Kannada': 'https://digifriend.site/kannada',
                'Malayalam': 'https://digifriend.site/malayalam',
                'Marathi': 'https://digifriend.site/marathi',
                'Punjabi': 'https://digifriend.site/punjabi',
                'Tamil': 'https://digifriend.site/tamil',
                'Telugu': 'https://digifriend.site/telugu',
                'Urdu': 'https://digifriend.site/urdu'
            }

            if language in language_urls:
                webbrowser.open(language_urls[language])
            else:
                print(f"No specific URL for language: {language}")

        else:
            self.result_label.text = """
            Invalid UID. 
            Please generate another, or try again.
            """
            self.likes_label.text = ""
            self.dislikes_label.text = ""
            self.subject_label.text = ""
            self.language_label.text = ""

    def create_reports_section(self, reports_scrollview):
        reports_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        reports_layout.bind(minimum_height=reports_layout.setter('height'))

        with reports_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 0.1)
            self.rect = Rectangle(size=reports_layout.size, pos=reports_layout.pos)
        reports_layout.bind(size=self._update_rect, pos=self._update_rect)

        reports_label = Label(text='Hourly Reports for 12th November 2024:', color=(0.2, 0.6, 1, 1), font_size=dp(20), size_hint_y=None,
                              height=dp(30), font_name=font_path)
        reports_layout.add_widget(reports_label)

        hours = [f'{i:02d}-{i+1:02d}' for i in range(17)]
        self.report_spinner = Spinner(text='Select Hour', values=hours,
                                      font_name=font_path,
                                      size_hint_y=None, font_size=35, height=dp(40))
        self.report_spinner.bind(text=self.update_report)
        reports_layout.add_widget(self.report_spinner)

        self.report_display = Label(text="", color=(0.2, 0.6, 1, 1), size_hint_y=0.1, height=dp(80), font_name=font_path)
        reports_layout.add_widget(self.report_display)

        reports_scrollview.add_widget(reports_layout)

    def create_graph_section(self):
        self.graph_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=10, spacing=20)
        graph_title = Label(text='Emotion Duration:', color=(0.2, 0.6, 1, 1), font_size=dp(24), size_hint_y=None, height=dp(30), font_name=font_path)
        self.graph_layout.add_widget(graph_title)

        with self.graph_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 0.1)
            self.graph_rect = Rectangle(size=self.graph_layout.size, pos=self.graph_layout.pos)
        self.graph_layout.bind(size=self._update_graph_rect, pos=self._update_graph_rect)

        self.create_graph()

        # Add spacing
        self.graph_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))

        self.emotion_durations = Label(text=self.format_emotion_durations(), markup=True, color=(0.2, 0.6, 1, 1),
                                       size_hint_y=None, height=dp(100), font_name=font_path)
        self.graph_layout.add_widget(self.emotion_durations)

        # Add this layout to the bottom of the main layout
        self.layout.add_widget(self.graph_layout)

    def format_emotion_durations(self):
        emotions = ['Angry', 'Happy', 'Neutral', 'Fear', 'Disgust', 'Surprise']
        durations = [0.5, 6, 10, 0.17, 0, 0]
        formatted_text = ""
        for emotion, duration in zip(emotions, durations):
            duration_text = f'{duration:.0f} hours' if duration >= 1 else f'{duration * 60:.0f} minutes'
            formatted_text += f"[b]{emotion}:[/b] {duration_text}\n"
        return formatted_text

    def create_graph(self):
        emotions = ['Angry', 'Happy', 'Neutral', 'Fear', 'Disgust', 'Surprise']
        durations = [0.5, 6, 10, 0.17, 0, 0]

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#0c0c14')
        ax.set_facecolor('#0c0c14')

        bar_colors = ['#FF6666', '#6699FF', '#99FF66', '#FFCC66', '#FF66CC', '#66CCFF']
        bars = ax.bar(emotions, durations, color=bar_colors)
        ax.set_ylabel('Hours', color='white', fontname=font_path)
        ax.set_title('Emotion Duration on 12th November', color='white', fontname=font_path)
        ax.tick_params(axis='x', colors='white', labelrotation=45)
        ax.tick_params(axis='y', colors='white')

        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.2f}h' if height > 0 else '0m',
                    ha='center', va='bottom', color='white', fontname=font_path)

        plt.tight_layout()
        graph_widget = FigureCanvasKivyAgg(figure=fig)
        self.graph_layout.add_widget(graph_widget)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_graph_rect(self, instance, value):
        self.graph_rect.pos = instance.pos
        self.graph_rect.size = instance.size

    def update_report(self, spinner, text):
        selected_hour = text
        if selected_hour == '16-17':
            self.report_display.text = "Concepts learned: Inertia\nTime talked: 50 minutes"
        else:
            # Generate random data for other hours
            concepts = ["Force", "Motion", "Energy", "Gravity", "Momentum", "Friction", "Acceleration"]
            concept = random.choice(concepts)
            time_talked = random.randint(30, 60)
            self.report_display.text = f"Concepts learned: {concept}\nTime talked: {time_talked} minutes"

    def show_menu(self, instance):
        self.manager.current = 'menu'
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Button(text='Updating preferences', on_press=self.updating_preferences, font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",))
        layout.add_widget(Button(text='Feedback and Complaints', on_press=self.feedback, font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",))
        layout.add_widget(Button(text='Factory reset', on_press=self.factory_reset, font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",))
        layout.add_widget(Button(text='Generate Another', on_press=self.generate_another, font_name= "C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf",))
        self.add_widget(layout)

    def updating_preferences(self, instance):
        self.manager.current = 'preferences'

    def feedback(self, instance):
        self.manager.current = 'feedback'

    def factory_reset(self, instance):
        App.get_running_app().stop()

    def generate_another(self, instance):
        self.manager.current = 'input'

    def back_to_mainline(self, instance):
        self.manager.current = 'mainline'


class PreferencesScreen(Screen):
    def __init__(self, **kwargs):
        super(PreferencesScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text="Update Preferences", font_size=24, color=(1, 1, 1, 1),
                                font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        layout.add_widget(TextInput(hint_text="Name", hint_text_color=(1, 1, 1, 1),
                                    font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf", background_color=(0.8, 0.9, 1, 1)))
        layout.add_widget(TextInput(hint_text="Likes", hint_text_color=(1, 1, 1, 1),
                                    font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf", background_color=(0.6, 0.8, 1, 1)))
        layout.add_widget(TextInput(hint_text="Dislikes", hint_text_color=(1, 1, 1, 1),
                                    font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf", background_color=(0.4, 0.6, 1, 1)))
        layout.add_widget(TextInput(hint_text="Favorite Subject", hint_text_color=(1, 1, 1, 1),
                                    font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf", background_color=(0.2, 0.4, 0.8, 1)))
        layout.add_widget(Button(text="Save", on_press=self.save_preferences,
                                 font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"), )
        layout.add_widget(Button(text="Back", on_press=self.go_back,
                                 font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        self.add_widget(layout)

    def save_preferences(self, instance):
        self.go_back(instance)

    def go_back(self, instance):
        self.manager.current = 'menu'


class FeedbackScreen(Screen):
    def __init__(self, **kwargs):
        super(FeedbackScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text="Feedback and Complaints", font_size=24, color=(1, 1, 1, 1),
                                font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        layout.add_widget(TextInput(hint_text="Enter your feedback here", multiline=True,
                                    font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        layout.add_widget(Button(text="Submit", on_press=self.submit_feedback,
                                 font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        layout.add_widget(Button(text="Back", on_press=self.go_back,
                                 font_name="C:/Users/Aadit/Downloads/lexend-main/lexend-main/fonts/lexend/ttf/Lexend-Regular.ttf"))
        self.add_widget(layout)

    def submit_feedback(self, instance):
        self.go_back(instance)

    def go_back(self, instance):
        self.manager.current = 'menu'


class HourlyReportsScreen(Screen):
    def __init__(self, **kwargs):
        super(HourlyReportsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        self.title_label = Label(text='Hourly Reports',
                                 color=(0.2, 0.6, 1, 1),
                                 font_size=dp(50),
                                 size_hint_y=0.2,
                                 height=dp(40),
                                 font_name=font_path)
        self.layout.add_widget(self.title_label)

        reports_scrollview = ScrollView(size_hint=(1, None), height=dp(450))
        self.create_reports_section(reports_scrollview)
        self.layout.add_widget(reports_scrollview)

        # Back Button with increased size and font
        back_button = Button(
            text='Generate another',
            size_hint=(1, None),
            height=dp(60),  # Increased button height
            background_color=(0.2, 0.6, 1, 1),
            font_name=font_path,
            font_size=dp(20)  # Increased font size
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def create_reports_section(self, reports_scrollview):
        self.reports_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(10), padding=dp(10))
        self.reports_layout.bind(minimum_height=self.reports_layout.setter('height'))

        # Get the current date and time
        current_time = datetime.now()
        self.title_label.text = f'Hourly Reports for {current_time.strftime("%d %B %Y")}:'

        # Generate hours list for the past 24 hours
        hours = [(current_time - timedelta(hours=i)).strftime('%H-%H') for i in range(24, 0, -1)]

        self.report_spinner = Spinner(text='Select Hour', values=hours,
                                      font_name=font_path,
                                      size_hint_y=None, font_size=30, height=dp(40))
        self.report_spinner.bind(text=self.update_report)
        self.reports_layout.add_widget(self.report_spinner)

        self.report_display = Label(text="", color=text_color, size_hint_y=None, height=dp(120),
                                    font_name=font_path, font_size=font_size, halign='left', valign='top')
        self.reports_layout.add_widget(self.report_display)

        reports_scrollview.add_widget(self.reports_layout)

    def update_report(self, spinner, text):
        selected_hour = text
        # Parse the selected hour
        start_hour, _ = map(int, selected_hour.split('-'))

        # Subtract 5.5 hours
        adjusted_hour = (start_hour - 6) % 24
        adjusted_end_hour = (adjusted_hour + 1) % 24

        # Format the adjusted time range
        adjusted_time_range = f"{adjusted_hour:02d}-{adjusted_end_hour:02d}"

        # Fetch conversation data
        response = requests.get(f'http://127.0.0.1:5000/get_conversation_data?hour={adjusted_time_range}')
        if response.status_code == 200:
            data = response.json()
            concepts = data.get('concepts', 'N/A')
            time_talked = data.get('time_talked', 'N/A')
            conversation_length = data.get('conversation_length', 'N/A')
            languages = data.get('languages', 'N/A')
            positivity_index = data.get('positivity_index', '9')

            # Initialize the mood_shifts_text variable
            mood_shifts_text = "No mood shifts recorded for this hour"

            # Fetch mood shifts data
            mood_shifts_response = requests.get(f'http://127.0.0.1:5000/get_mood_shifts?hour={adjusted_time_range}')
            if mood_shifts_response.status_code == 200:
                mood_shifts_data = mood_shifts_response.json()
                if mood_shifts_data and 'mood_shifts' in mood_shifts_data:
                    mood_shifts = mood_shifts_data['mood_shifts']
                    if mood_shifts:
                        mood_shifts_text = ""
                        for shift in mood_shifts:
                            timestamp = datetime.fromisoformat(shift['timestamp'])
                            mood_shifts_text += (
                                f"{shift['from_mood']}-{shift['to_mood']}: "
                                f"at {timestamp.strftime('%H:%M:%S')}\n"
                            )

            self.report_display.text = (
                f"Data for {adjusted_time_range}:\n"
                f"Concepts learned: {concepts}\n"
                f"Time talked: {time_talked}\n"
                f"Conversation length: {conversation_length}\n"
                f"Languages used: {languages}\n"
                f"Positivity Index: {positivity_index}/10\n"
                f"Mood shifts:\n{mood_shifts_text}"
            )

            # Resize the report_display widget to fit the new text
            self.report_display.texture_update()
            self.report_display.size = self.report_display.texture_size
            self.reports_layout.minimum_height = self.reports_layout.height
        else:
            self.report_display.text = f"Error fetching data for {adjusted_time_range}"
    def go_back(self, instance):
        self.manager.current = 'input'
class DigiFriendApp(App):
    def build(self):
        Window.clearcolor = background_color
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(MainlineScreen(name='mainline'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PreferencesScreen(name='preferences'))
        sm.add_widget(FeedbackScreen(name='feedback'))
        sm.add_widget(HourlyReportsScreen(name='hourly_reports'))
        return sm

if __name__ == "__main__":
    DigiFriendApp().run()
