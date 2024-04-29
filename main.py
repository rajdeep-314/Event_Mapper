# Importing Standard Library modules

import hashlib
import string
from functools import partial
from datetime import datetime

# Importing Kivy objects

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.metrics import dp

# Font management

LabelBase.register(name="AlexBrush", fn_regular="fonts/AlexBrush-Regular.ttf")
LabelBase.register(name="Quicksand-Bold", fn_regular="fonts/Quicksand-Bold.otf")
LabelBase.register(name="OstrichSans-Bold", fn_regular="fonts/OstrichSans-Bold.otf",
                   fn_bold="fonts/OstrichSans-Black.otf")
LabelBase.register(name="OpenSans", fn_regular="fonts/OpenSans-Regular.ttf", fn_bold="fonts/OpenSans-Semibold.ttf")
LabelBase.register(name="CamingoCode", fn_regular="fonts/CamingoCode-Regular.ttf", fn_bold="fonts/CamingoCode-Bold.ttf")
LabelBase.register(name="CooperHewitt", fn_regular="fonts/CooperHewitt-Medium.otf",
                   fn_bold="fonts/CooperHewitt-Semibold.otf")
LabelBase.register(name="FiraSans", fn_regular="fonts/FiraSans-Book.otf")

# Color Management

iitpkd_orange = (1, 0.678, 0, 1)
orange_brown = (0.659, 0.416, 0.13, 1)

black = (0, 0, 0, 1)
white = (1, 1, 1, 1)
gray = (0.3, 0.3, 0.3, 1)
mid_gray = (0.5, 0.5, 0.5, 1)
dark_gray = (0.2, 0.2, 0.2, 1)

green = (0.572, 1, 0.576, 1)
light_green = (0.672, 1, 0.676, 1)
red = (1, 0.1, 0.1, 1)
pastel_red = (1, 0.296, 0.249, 1)

transparent = (0, 0, 0, 0)

# pos_hint of different landmarks (buttons) with respect to the Nila Map
relative_coordinates_dict = {
    "Agora": (0.8787, 0.1617),
    "Samgatha": (0.7487, 0.2804),
    "Manogatha": (0.6, 0.37),
    "Kaapi": (0.5432, 0.455),
    "Bageshri": (0.395, 0.685),
    "Shikharam": (0.2866, 0.894),
    "Brindavani": (0.1172, 0.8568),
    "Tilang B": (0.1913, 0.705),
    "Tilang A": (0.2773, 0.555),
    "Tilang Mess": (0.2425, 0.63),
    "Tilang Parking": (0.385, 0.5925),
    "Main Parking": (0.89, 0.355)
}

# size_hint of different landmarks (buttons) with respect to the Nila Map
# defined for 800/600 pixels screen
size_hints_dict = {
    'Agora': (0.1, 0.11),
    'Samgatha': (0.105, 0.13),
    'Manogatha': (0.15, 0.12),
    'Kaapi': (0.07, 0.05),
    'Bageshri': (0.08, 0.1),
    'Shikharam': (0.09, 0.115),
    'Brindavani': (0.15, 0.2),
    'Tilang B': (0.09, 0.1),
    'Tilang A': (0.08, 0.1),
    'Tilang Mess': (0.12, 0.055),
    'Tilang Parking': (0.08, 0.065),
    'Main Parking': (0.125, 0.07)
}

buttons_names = list(relative_coordinates_dict.keys())

# Global variable to keep track of the currently logged in user (or visitor)
current_username = ""

username_acceptable = string.ascii_letters + string.digits + "@_"  # String of characters acceptable in a username
password_acceptable = username_acceptable + "$#*-"  # String of characters acceptable in a password


# Some useful functions

# Returns if `year` is a leap year or not
def is_leap(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


# Used as a key for sorting events by their timing
def comparison_function(input_list):
    return input_list[-1]


# Reads the events database and returns a dictionary for events being organized at venue
def obtain_events(venue):
    with open("events.txt", "r") as events_file:
        data = [entry for entry in events_file.read().split("\n")[:-1]]

    output_dict = {}

    for entry in data:
        event_name, other = entry.split("||")
        extracted_data = other.split("|")

        if extracted_data[0] == venue:
            output_dict[event_name] = extracted_data

    return output_dict


# Filters events to allow only those whose timing is after the current timing
def filter_events(events_dict):
    filtered_events_dict = {}

    for event_name in events_dict:
        event_datetime = events_dict[event_name][2]
        event_date = tuple(int(i) for i in reversed(event_datetime.split()[0].split("/")))
        event_time = tuple(int(i) for i in event_datetime.split()[1].split(":"))
        event_datetime = datetime(*(event_date + event_time))

        if event_datetime >= datetime.now().replace(second=0, microsecond=0):
            filtered_events_dict[event_name] = events_dict[event_name]

    return filtered_events_dict


# An extension of the ScreenManager Kivy class to manage the three screens
class WindowsManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowsManager, self).__init__(**kwargs)

        global login_page  # Being global enables log out and home buttons to function
        login_page = LoginPage(name="login")

        # Adding the three screens to the manager
        self.add_widget(StartingPage(name="starting"))
        self.add_widget(login_page)
        self.add_widget(MapPage(name="map"))


# Starting page screen
class StartingPage(Screen):
    def __init__(self, **kwargs):
        super(StartingPage, self).__init__(**kwargs)

        self.layout = FloatLayout()
        self.background_layout = FloatLayout()

        self.background_layout.add_widget(
            Image(source="images/logo.png", allow_stretch=False, keep_ratio=True))  # Logo in the background

        self.layout.add_widget(self.background_layout)

        self.layout.add_widget(
            Label(text="Event Mapper",
                  font_name="AlexBrush",
                  font_size=135,
                  pos_hint={"x": 0, "y": 0.57},
                  size_hint=(1, 0.5)))

        self.button_visitor = Button(text="Visitor",
                                     font_name="Quicksand-Bold",
                                     background_color=gray,
                                     font_size=35,
                                     pos_hint={"x": 0.35, "y": 0.26},
                                     size_hint=(0.3, 0.125))

        self.button_organiser = Button(text="Organiser",
                                       font_name="Quicksand-Bold",
                                       background_color=gray,
                                       font_size=35,
                                       pos_hint={"x": 0.35, "y": 0.1},
                                       size_hint=(0.3, 0.125))

        self.button_visitor.bind(on_press=self.pressed_visitor, on_release=self.released_visitor)
        self.button_organiser.bind(on_press=self.pressed_organiser, on_release=self.released_organiser)

        self.layout.add_widget(self.button_visitor)
        self.layout.add_widget(self.button_organiser)

        self.add_widget(self.layout)

    def pressed_visitor(self, instance):
        self.button_visitor.background_color = white
        self.button_visitor.color = black

    def released_visitor(self, instance):
        self.button_visitor.background_color = gray
        self.button_visitor.color = white

        self.manager.transition.direction = "left"
        self.manager.current = "map"  # Go to the map screen

    def pressed_organiser(self, instance):
        self.button_organiser.background_color = white
        self.button_organiser.color = black

    def released_organiser(self, instance):
        self.button_organiser.background_color = gray
        self.button_organiser.color = white

        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "up"
        self.manager.current = "login"  # Go to the login screen


# Login page screen
class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)

        self.layout = FloatLayout()
        self.password_mode = True  # password_mode:True --> Password is hidden

        self.layout.add_widget(
            Label(text="Log In",
                  font_name="OstrichSans-Bold",
                  bold=True,
                  font_size=85,
                  color=iitpkd_orange,
                  pos_hint={"x": 0, "y": 0.78},
                  size_hint=(1, 0.2)))

        self.layout.add_widget(
            Label(text="Username",
                  font_name="OpenSans",
                  bold=True,
                  font_size=38,
                  color=iitpkd_orange,
                  pos_hint={"right": 0.4, "center_y": 0.6},
                  size_hint=(None, None)))

        self.layout.add_widget(
            Label(text="Password",
                  font_name="OpenSans",
                  bold=True,
                  font_size=38,
                  color=iitpkd_orange,
                  pos_hint={"right": 0.4, "center_y": 0.45},
                  size_hint=(None, None)))

        self.username_input = TextInput(multiline=False,
                                        font_size=23,
                                        font_name="CamingoCode",
                                        background_color=white,
                                        pos_hint={"x": 0.5, "center_y": 0.6},
                                        size=(dp(300), dp(45)),
                                        size_hint=(None, None))

        self.password_input = TextInput(multiline=False,
                                        font_size=23,
                                        font_name="CamingoCode",
                                        background_color=white,
                                        password=True,
                                        pos_hint={"x": 0.5, "center_y": 0.45},
                                        size=(dp(300), dp(45)),
                                        size_hint=(None, None))

        # The input fields are bound with their text property to enable real-time input validation
        self.username_input.bind(text=self.validate_username)
        self.password_input.bind(text=self.validate_password)

        self.button_sign_in = Button(text="Sign in",
                                     font_name="CooperHewitt",
                                     bold=True,
                                     font_size=38,
                                     background_color=orange_brown,
                                     background_normal="",
                                     background_down="",
                                     color=white,
                                     pos_hint={"right": 0.48, "y": 0.13},
                                     size=(dp(250), dp(65)),
                                     size_hint=(None, None))

        self.button_sign_up = Button(text="Sign up",
                                     font_name="CooperHewitt",
                                     bold=True,
                                     font_size=38,
                                     background_color=orange_brown,
                                     background_normal="",
                                     background_down="",
                                     color=white,
                                     pos_hint={"x": 0.52, "y": 0.13},
                                     size=(dp(250), dp(65)),
                                     size_hint=(None, None))

        self.button_sign_in.bind(on_press=self.pressed_sign_in, on_release=self.released_sign_in)
        self.button_sign_up.bind(on_press=self.pressed_sign_up, on_release=self.released_sign_up)

        self.button_instructions = Button(text="i",
                                          font_name="CamingoCode",
                                          font_size=25,
                                          color=white,
                                          background_color=transparent,
                                          background_normal="",
                                          background_down="",
                                          pos_hint={"right": 0.97, "top": 0.97},
                                          size=(dp(40), dp(40)),
                                          size_hint=(None, None))

        self.button_instructions.bind(on_press=self.pressed_instructions, on_release=self.released_instructions)

        self.button_back = Button(text="<<",
                                  font_name="CamingoCode",
                                  bold=True,
                                  font_size=32,
                                  pos_hint={"x": 0.02, "top": 0.98},
                                  size=(dp(80), dp(50)),
                                  background_color=transparent,
                                  background_normal="",
                                  background_down="",
                                  color=white,
                                  size_hint=(None, None))

        self.button_back.bind(on_press=self.pressed_back, on_release=self.released_back)

        self.button_eye = Button(background_normal="images/eye_" + ['show', 'hide'][self.password_mode] + ".png",
                                 background_down="images/eye_" + ['show', 'hide'][not self.password_mode] + ".png",
                                 pos=(self.width / 2, self.height / 2), size=(dp(70), dp(70)), size_hint=(None, None))

        self.button_eye.bind(on_press=self.pressed_eye, on_release=self.released_eye)

        self.layout.add_widget(self.button_eye)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.button_sign_in)
        self.layout.add_widget(self.button_sign_up)
        self.layout.add_widget(self.button_instructions)
        self.layout.add_widget(self.button_back)

        self.add_widget(self.layout)

    # Manages the position of the `eye` icon whenever the screen is resized`
    def on_size(self, *args):
        self.button_eye.pos = (self.width / 2 + dp(300), self.height * 0.45 - dp(35))

    def pressed_eye(self, *args, forced=False):
        self.password_mode = not self.password_mode

        # forced is an optional parameter to turn on password hide when pressed_eye is called
        # Adding this parameter enables the login page's initialization with a hidden password field
        if forced:
            self.password_mode = True

        self.password_input.password = self.password_mode

    def released_eye(self, *args):
        # Managing the png file for the `eye` icon`
        self.button_eye.background_normal = "images/eye_" + ['show', 'hide'][self.password_mode] + ".png"
        self.button_eye.background_down = "images/eye_" + ['show', 'hide'][not self.password_mode] + ".png"

    def pressed_back(self, instance):
        self.button_back.background_color = dark_gray
        self.button_back.color = iitpkd_orange

    def released_back(self, instance):
        self.button_back.background_color = transparent
        self.button_back.color = white

        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "down"
        self.manager.current = "starting"  # Go back to the starting page

    def pressed_instructions(self, instance):
        self.button_instructions.background_color = dark_gray
        self.button_instructions.color = iitpkd_orange

    def released_instructions(self, instance):
        self.button_instructions.background_color = transparent
        self.button_instructions.color = white

        # Instructions for defining a new username and password
        multiline_instructions = Label(text='''
        Instructions for username :

        -  Minimum allowed length is 4 characters
        -  Allowed characters : Alphanumeric (A-Z, a-z, 0-9) and symbols (@_)
        -  Maximum allowed length is 20 characters


        Instructions for password :

        -  Minimum allowed length is 4
        -  Allowed characters : Alphanumeric (A-Z, a-z, 0-9) and symbols (@_$#*-)
        -  Maximum allowed length is 20 characters
        ''',
                                       font_name="FiraSans",
                                       font_size=20)
        instructions_popup = Popup(title="Instructions",
                                   content=multiline_instructions,
                                   size=(dp(750), dp(500)),
                                   size_hint=(None, None))
        instructions_popup.open()

    def validate_username(self, instance, value):
        # Real-time username validation
        # Doesn't allow a username over 20 characters
        # Doesn't allow non acceptable characters to be entered
        if len(self.username_input.text) > 20:
            self.username_input.text = self.username_input.text[:20]

        if self.username_input.text[-1:] not in username_acceptable:
            self.username_input.text = self.username_input.text[:-1]

    def validate_password(self, instance, value):
        # Real-time password validation
        # Doesn't allow a password over 20 characters
        # Doesn't allow non acceptable characters to be entered
        if len(self.password_input.text) > 20:
            self.password_input.text = self.password_input.text[:20]

        if self.password_input.text[-1:] not in password_acceptable:
            self.password_input.text = self.password_input.text[:-1]

    def pressed_sign_in(self, instance):
        self.button_sign_in.background_color = mid_gray
        self.button_sign_in.color = black

    def released_sign_in(self, instance):
        self.button_sign_in.background_color = orange_brown
        self.button_sign_in.color = white

        # Extracting text from the input boxes
        username = self.username_input.text
        password = self.password_input.text

        # Handling username and password validation rules
        if len(username) < 4:
            self.show_error_message("Username must be at least 4 characters in length")
        elif len(password) < 4:
            self.show_error_message("Password must be at least 4 characters in length")
        else:
            # Obtaining all usernames and their hashed passwords in a dictionary
            with open("credentials.txt", 'r') as credentials_file:
                credentials_dict = self.get_credentials_dict(credentials_file)

            if username not in credentials_dict.keys():  # When the username doesn't exist
                self.show_error_message("This username does not exist, please sign up")

            elif credentials_dict[username] == hashlib.sha512(password.encode()).hexdigest():  # Successfully logged in
                global current_username
                current_username = username  # Updating the global variable

                self.manager.transition.direction = "left"
                self.manager.current = "map"  # Go to map screen as an organiser
                self.reset_entries()  # Reset input fields
            else:
                self.show_error_message(
                    "Incorrect password, please try again")  # Username exists, but the passwords don't match
                self.password_input.text = ""  # Emptying the password field

    def reset_entries(self):
        self.username_input.text = ""
        self.password_input.text = ""

    def pressed_sign_up(self, instance):
        self.button_sign_up.background_color = mid_gray
        self.button_sign_up.color = black

    def released_sign_up(self, instance):
        self.button_sign_up.background_color = orange_brown
        self.button_sign_up.color = white

        # Extracting text from the input boxes
        username = self.username_input.text
        password = self.password_input.text

        # Obtaining all current credentials
        with open("credentials.txt", "r") as credentials_file:
            credentials_dict = self.get_credentials_dict(credentials_file)
        if len(username) < 4:
            self.show_error_message("Username must be at least 4 characters in length")
        elif len(username) > 20:
            self.show_error_message("Username must be no longer than 20 characters")
        elif len(password) > 20:
            self.show_error_message("Password must be no longer than 20 characters")
        elif len(password) < 4:
            self.show_error_message("Password must be at least 4 characters in length")
        elif username in credentials_dict.keys():  # Username is already signed up
            self.show_error_message("This username is taken, please try again")
            self.reset_entries()
        else:
            with open("credentials.txt", "a") as credentials_file:  # Append new credentials in the database
                credentials_file.write(username + ":" + hashlib.sha512(password.encode()).hexdigest() + "\n")

            global current_username
            current_username = username  # Update the global variable

            self.manager.transition.direction = "left"
            self.manager.current = "map"  # Go to map screen
            self.reset_entries()

    def get_credentials_dict(self, file_object):
        # Returns a dictionary after reading all credentials stored in file_object
        sample_dict = {}

        for entry in file_object.readlines():
            entry_split = entry.split(":")
            sample_dict[entry_split[0]] = entry_split[1].strip()

        return sample_dict

    # A generalized function to open a popup for various login-related error messages
    def show_error_message(self, error_message):
        Popup(title="Error",
              content=Label(text=error_message, font_name="FiraSans", font_size=23),
              size_hint=(None, None),
              size=(dp(700), dp(200))).open()


# Map screen
class MapPage(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.add_widget(MapParent())

    def button_pressed(self, instance):
        self.manager.current = "login"


# The layout for MapPage
class MapParent(FloatLayout):
    def __init__(self, **kwargs):
        super(MapParent, self).__init__(**kwargs)

        # adding widget(s)
        self.map_screen = MapScreen()
        self.back_button = Button(
            pos_hint={"right": 0.98, "top": 0.98},
            size=(dp(60), dp(60)),
            size_hint=(None, None),
            on_press=self.back_button_pressed
        )
        self.add_widget(self.back_button)
        self.add_widget(self.map_screen)

        # defining constants
        self.default_scale = self.map_screen.default_scale
        self.spring_effect = 0.1

        self.__initial_map_time = 0

        # update function run every 0.01 seconds
        Clock.schedule_interval(self.update, 0.01)

    # For home/logout button
    def back_button_pressed(self, instance):
        self.parent.manager.transition.direction = "right"
        self.parent.manager.current = "starting"  # Go to starting page

        global current_username
        current_username = ""  # Update the global variable to indicate a logout

    def update(self, instance):
        # Keeping the map in the screen's bounds
        if self.map_screen.y > 0:
            self.map_screen.y -= self.map_screen.y * self.spring_effect

        if self.map_screen.top < Window.height:
            self.map_screen.top += (Window.height - self.map_screen.top) * self.spring_effect

        if self.map_screen.x > 0:
            self.map_screen.x -= self.map_screen.x * self.spring_effect

        if self.map_screen.right < Window.width:
            self.map_screen.right += (Window.width - self.map_screen.right) * self.spring_effect

        # Handling the back button's size based on the mode (visitor/organiser)
        self.back_button.size = (([dp(60), dp(70)][bool(current_username)],) * 2)

        # Handling the png for the home/logout button, based on whether the user is logged in or not
        self.back_button.background_normal = "images/" + ["home", "logout"][bool(current_username)] + ".png"
        self.back_button.background_down = "images/" + ["home", "logout"][bool(current_username)] + ".png"

        # Stores the last time when the map page was active
        if self.parent.manager.current == "map":
            self.__initial_map_time = datetime.now()

        # Resets the map size 0.5 seconds after switching from the map page to make the transition seamless and smooth
        if self.parent.manager.current != "map" and type(self.__initial_map_time) is not int:
            if (datetime.now() - self.__initial_map_time).total_seconds() >= 0.5:
                self.reset_params()

        if self.parent.manager.current == "starting":
            login_page.pressed_eye(forced=True)  # Initializing login page with a hidden password field
            login_page.released_eye()  # Simulating a press of the `eye` button`
            login_page.reset_entries()  # Initializing the login page with empty fields

    # Resetting the map to the default size
    def reset_params(self):
        self.map_screen.transform = Matrix().scale(self.default_scale, self.default_scale, self.default_scale)


# Map Screen
class MapScreen(ScatterLayout):
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs, auto_bring_to_front=False, do_rotation=False)

        # constants declaration
        self.min_scale = 1.05
        self.max_scale = 6
        self.default_scale = 1.05

        # map_image_width / map_image_height
        # map image resolution is 10000 x 8800 pixels
        self.image_aspect_ratio = 10 / 8.8

        # default window aspect ratio in Kivy
        self.old_default_aspect_ratio = 800 / 600

        self.scale_min = self.min_scale
        self.scale_max = self.max_scale

        # add the widgets
        self.nila_map = Image(source="./images/nila_map.png",
                              allow_stretch=False,
                              keep_ratio=True
                              )
        self.add_widget(self.nila_map)

        # all the buttons for different landmarks
        self.buttons_landmarks = {
            location: Button(text=location,
                             font_name="OpenSans",
                             bold=True,
                             font_size=18,
                             color=white,
                             outline_color=black,
                             outline_width=4,
                             size_hint=size_hints_dict[location],
                             on_release=partial(self.location_button_pressed, location),
                             background_color=transparent)
            for location in relative_coordinates_dict}

        self.buttons_landmarks["Tilang Parking"].text = "Tilang\nParking"

        for landmark_button in self.buttons_landmarks.values():
            self.add_widget(landmark_button)

        self.transform = Matrix().scale(self.default_scale, self.default_scale, self.default_scale)

    def dominance(self):
        if self.width >= self.image_aspect_ratio * self.height:
            # Fits along height, i.e., the heights of Nila Map image and scatter layout are the same
            return "height"

        else:
            # Fits along width, i.e., the widths of Nila Map image and scatter layout are the same
            return "width"

    def convert_pos_hint(self, image_hint_x, image_hint_y):
        if self.dominance() == "height":
            return 0.5 + ((image_hint_x - 0.5) * self.image_aspect_ratio * self.height / self.width), image_hint_y
        else:
            return image_hint_x, 0.5 + ((image_hint_y - 0.5) * self.width / (self.image_aspect_ratio * self.height))

    def convert_size_hint(self, size_hint_x, size_hint_y):
        if self.dominance() == "height":
            return size_hint_x * self.old_default_aspect_ratio * (Window.height / Window.width), size_hint_y
        else:
            return size_hint_x, size_hint_y * (1 / self.old_default_aspect_ratio) * (Window.width / Window.height)

    # Manages the position and size of the buttons as the screen is resized
    def on_size(self, *args):
        for landmark in self.buttons_landmarks:
            current_button = self.buttons_landmarks[landmark]

            button_pos_hint = self.convert_pos_hint(relative_coordinates_dict[landmark][0],
                                                    relative_coordinates_dict[landmark][1])
            current_button.pos_hint = {"center_x": button_pos_hint[0], "center_y": button_pos_hint[1]}

            button_size_hint = self.convert_size_hint(size_hints_dict[landmark][0], size_hints_dict[landmark][1])
            current_button.size_hint = (button_size_hint[0], button_size_hint[1])

    # Zooming in and out using the scrollwheel
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == "scrolldown":
                if self.scale < self.max_scale:
                    self.scale *= 1.1

            if touch.button == "scrollup":
                if self.scale > self.min_scale:
                    self.scale *= 0.9
        else:
            super(MapScreen, self).on_touch_down(touch)

    # Called when the remove button is pressed on an event
    def remove_button_pressed(self, *args):
        # Opens a confirmation popup about the event deletion
        self.confirmation_popup = Popup(title="Confirmation", size=(dp(400), dp(200)), size_hint=(None, None))

        confirmation_layout = FloatLayout(size=self.confirmation_popup.size, size_hint=(None, None))

        confirmation_layout.add_widget(Label(text="Are you sure?",
                                             font_size=26,
                                             font_name="OpenSans",
                                             pos_hint={"center_x": 0.47, "center_y": 0.5},
                                             size_hint=(1, 0.4)
                                             ))

        confirmation_layout.add_widget(Button(text="Yes",
                                              font_size=24,
                                              font_name="CooperHewitt",
                                              background_color=green,
                                              pos_hint={"center_x": 0.23, "center_y": 0.15},
                                              size_hint=(0.42, 0.27),
                                              on_release=partial(self.remove_event, *args)
                                              ))

        confirmation_layout.add_widget(Button(text="No",
                                              font_size=24,
                                              font_name="CooperHewitt",
                                              background_color=red,
                                              pos_hint={"center_x": 0.71, "center_y": 0.15},
                                              size_hint=(0.42, 0.27),
                                              on_release=self.confirmation_popup.dismiss
                                              ))

        self.confirmation_popup.content = confirmation_layout
        self.confirmation_popup.open()

    # Called when the organiser confirms the deletion of an event
    def remove_event(self, *args):
        self.confirmation_popup.dismiss()
        event_name = args[0]
        current_location = args[1]

        # Handling the events file
        with open("events.txt", "r") as events_file:
            data = events_file.read().split("\n")[:-1]
        updated_events = "\n".join(entry for entry in data if entry.split("||")[0] != event_name)

        with open("events.txt", "w") as events_file:
            events_file.write(updated_events + "\n")

        self.event_list_popup.dismiss()
        self.location_button_pressed(current_location)

    # Called when the organiser initiates the addition of a new event
    def add_new_event(self, *args):
        # Opens a popup with the form to define a new event
        self.new_event_popup = Popup(title="New Event in " + args[0], size=(dp(620), dp(550)), size_hint=(None, None))

        self.popup_layout = FloatLayout(size=(dp(620), dp(550)), size_hint=(None, None))

        self.popup_layout.add_widget(Label(text="Event name",
                                           font_name="OpenSans",
                                           bold=True,
                                           font_size=26,
                                           color=iitpkd_orange,
                                           pos_hint={"center_x": 0.25, "center_y": 0.82}
                                           ))

        self.name_input = TextInput(multiline=False,
                                    font_size=24,
                                    font_name="CamingoCode",
                                    pos_hint={"x": 0.41, "center_y": 0.82},
                                    size_hint=(0.54, 0.09)
                                    )

        self.popup_layout.add_widget(self.name_input)

        self.popup_layout.add_widget(Label(text="Date (DD/MM/YYYY)",
                                           font_name="OpenSans",
                                           bold=True,
                                           font_size=24,
                                           pos_hint={"center_x": 0.19, "center_y": 0.7}
                                           ))

        self.date_input = TextInput(multiline=False,
                                    font_size=24,
                                    font_name="CamingoCode",
                                    pos_hint={"x": 0.41, "center_y": 0.7},
                                    size_hint=(0.54, 0.09)
                                    )

        self.popup_layout.add_widget(self.date_input)

        self.popup_layout.add_widget(Label(text="Time (HH : MM)",
                                           font_name="OpenSans",
                                           bold=True,
                                           font_size=24,
                                           pos_hint={"center_x": 0.23, "center_y": 0.58}
                                           ))

        self.time_input = TextInput(multiline=False,
                                    font_size=24,
                                    font_name="CamingoCode",
                                    pos_hint={"x": 0.41, "center_y": 0.58},
                                    size_hint=(0.54, 0.09)
                                    )

        self.popup_layout.add_widget(self.time_input)

        self.popup_layout.add_widget(Label(text="Description",
                                           font_name="OpenSans",
                                           bold=True,
                                           font_size=24,
                                           pos_hint={"center_x": 0.24, "center_y": 0.36}
                                           ))

        self.description_input = TextInput(multiline=True,
                                           font_size=24,
                                           font_name="CamingoCode",
                                           pos_hint={"x": 0.41, "center_y": 0.35},
                                           size_hint=(0.54, 0.31)
                                           )

        self.popup_layout.add_widget(self.description_input)

        self.popup_layout.add_widget(Button(text="Add",
                                            font_name="CooperHewitt",
                                            font_size=30,
                                            pos_hint={"center_x": 0.26, "center_y": 0.08},
                                            size_hint=(0.38, 0.11),
                                            background_color=green,
                                            color=white,
                                            on_release=partial(self.new_event_submission, *args)
                                            ))

        self.popup_layout.add_widget(Button(text="Cancel",
                                            font_name="CooperHewitt",
                                            font_size=30,
                                            pos_hint={"center_x": 0.7, "center_y": 0.08},
                                            size_hint=(0.38, 0.11),
                                            background_color=red,
                                            color=white,
                                            on_release=self.new_event_popup.dismiss
                                            ))

        # Binding each of the text inputs to their validation functions
        self.name_input.bind(text=self.validate_name_input)
        self.date_input.bind(text=self.validate_date_input)
        self.time_input.bind(text=self.validate_time_input)
        self.description_input.bind(text=self.validate_description_input)

        self.new_event_popup.content = self.popup_layout
        self.new_event_popup.open()

    # A generalised function to open a popup for new event related errors
    def error_popup(self, error_message):
        Popup(title="Error",
              content=Label(text=error_message,
                            font_name="OpenSans",
                            font_size=26,
                            pos_hint={"x": 0, "y": 0.05}),
              size=(dp(450), dp(250)),
              size_hint=(None, None)).open()

    # Called when the organiser initiates the request to add a new event
    def new_event_submission(self, *args):
        venue = args[0]
        name = self.name_input.text
        date = self.date_input.text
        time = self.time_input.text
        description = self.description_input.text

        # Obtains the current events from the database
        with open("events.txt", "r") as events_file:
            events_data = events_file.read().split("\n")[:-1]

        # Obtaining a dictionary for the events
        events_dict = {entry.split("||")[0]: entry.split("||")[1].split("|") for entry in events_data}

        # Input Validation
        if not (name and date and time and description):  # IF one of the fields is empty
            self.error_popup("Please fill all entries")

        elif len(date) != 10:  # Invalid date length
            self.error_popup("Invalid date")
        else:
            get_date, get_month, get_year = int(date[:2]), int(date[3:5]), int(date[6:])

            days_in_month = [31, 28 + is_leap(get_year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            if get_month > 12 or get_date > days_in_month[get_month - 1]:  # Invalid date parameters
                self.error_popup("Invalid date")
            elif len(time) != 5:  # Invalid time length
                self.error_popup("Invalid time")
            else:
                get_hours, get_minutes = int(time[:2]), int(time[3:])

                if get_hours >= 24 or get_minutes >= 60:  # Invalid time parameters
                    self.error_popup("Invalid time")
                else:
                    event_date = tuple(int(i) for i in reversed(date.split("/")))
                    event_time = tuple(int(i) for i in time.split(":"))
                    event_datetime = datetime(
                        *(event_date + event_time))  # Converting the new event's timing to a datetime object

                    if event_datetime < datetime.now().replace(second=0,
                                                               microsecond=0):
                        # If the new event's timing is before the current time
                        self.error_popup("Event timing must be after\ncurrent timing")
                    else:
                        events_names = list(events_dict.keys())
                        events_name_timing = {event_name: events_dict[event_name][2] for event_name in
                                              events_dict}
                        new_event_timing = date + " " + time

                        # If the event name is already taken
                        if name.strip() in events_names:
                            self.error_popup("Event name is already taken")

                        elif new_event_timing in events_name_timing.values():
                            # Handling a timing clash
                            # Opens a popup warning the organiser of a time clash,
                            # prompting him to ignore it or change the timings
                            self.time_clash_popup = Popup(title="Time clash",
                                                          size=(dp(450), dp(250)),
                                                          size_hint=(None, None))

                            time_clash_layout = FloatLayout(size=(dp(400), dp(200)), size_hint=(None, None))
                            time_clash_layout.add_widget(Label(
                                text="Your event timing clashes with\nanother event.\nContinue?",
                                font_name="OpenSans",
                                font_size=24,
                                pos_hint={"center_x": 0.5, "center_y": 0.67},
                                size_hint=(1, 0.5)
                            ))

                            time_clash_layout.add_widget(Button(
                                text="Yes",
                                font_name="CooperHewitt",
                                font_size=32,
                                background_color=light_green,
                                color=white,
                                pos_hint={"center_x": 0.28, "center_y": 0.18},
                                size_hint=(0.43, 0.3),
                                on_press=partial(self.add_event_manually, name + "||" + "|".join(
                                    [venue, current_username, date + " " + time,
                                     "\\n".join(description.split("\n"))]) + "\n", venue)
                            ))
                            time_clash_layout.add_widget(Button(
                                text="No",
                                font_name="CooperHewitt",
                                font_size=32,
                                background_color=pastel_red,
                                color=white,
                                pos_hint={"center_x": 0.77, "center_y": 0.18},
                                size_hint=(0.43, 0.3),
                                on_press=self.time_clash_popup.dismiss
                            ))
                            self.time_clash_popup.content = time_clash_layout
                            self.time_clash_popup.open()

                        # No exceptions encountered
                        else:
                            with open("events.txt", "a") as events_file:
                                events_file.write(name + "||" + "|".join(
                                    [venue, current_username, date + " " + time,
                                     "\\n".join(description.split("\n"))]) + "\n")

                            self.new_event_popup.dismiss()
                            self.event_list_popup.dismiss()
                            self.location_button_pressed(venue)

    # Called when the organiser decides to ignore the time clash
    def add_event_manually(self, *args):
        self.time_clash_popup.dismiss()
        event_data = args[0]
        venue = args[1]

        # Writes the new event's data to the text file
        with open("events.txt", "a") as events_file:
            events_file.write(event_data)

        self.new_event_popup.dismiss()
        self.event_list_popup.dismiss()
        self.location_button_pressed(venue)

    def validate_name_input(self, instance, value):
        # Real-time validation of the name input
        # Doesn't allow a pipe operator to be used
        # Limits the event name's length to 30 characters
        if self.name_input.text[-1:] == "|":
            self.name_input.text = self.name_input.text[:-1]

        if len(self.name_input.text) > 30:
            self.name_input.text = self.name_input.text[:30]

    def validate_date_input(self, instance, value):
        # Real-time validation of the date input
        # Doesn't allow any format other than DD/MM/YYYY
        current_length = len(self.date_input.text)
        digits = "0123456789"

        if current_length <= 2:
            if self.date_input.text[-1:] not in digits:
                self.date_input.text = self.date_input.text[:-1]

        elif current_length == 3:
            if self.date_input.text[-1] != "/":
                self.date_input.text = self.date_input.text[:-1]

        elif current_length <= 5:
            if self.date_input.text[-1] not in digits:
                self.date_input.text = self.date_input.text[:-1]

        elif current_length == 6:
            if self.date_input.text[-1] != "/":
                self.date_input.text = self.date_input.text[:-1]

        elif current_length <= 10:
            if self.date_input.text[-1] not in digits:
                self.date_input.text = self.date_input.text[:-1]

        else:
            self.date_input.text = self.date_input.text[:10]

    def validate_time_input(self, instance, value):
        # Real-time validation of the time input
        # Doesn't allow any format other than HH : MM
        current_length = len(self.time_input.text)
        digits = "0123456879"

        if current_length <= 2:
            if self.time_input.text[-1:] not in digits:
                self.time_input.text = self.time_input.text[:-1]

        elif current_length == 3:
            if self.time_input.text[-1] != ":":
                self.time_input.text = self.time_input.text[:-1]

        elif current_length <= 5:
            if self.time_input.text[-1] not in digits:
                self.time_input.text = self.time_input.text[:-1]

        else:
            self.time_input.text = self.time_input.text[:-1]

    def validate_description_input(self, instance, value):
        # Real-time validation of the description input
        # Doesn't allow the pipe operator
        # Doesn't allow a length greater than 100 words
        if self.description_input.text[-1:] == "|":
            self.description_input.text = self.description_input.text[:-1]

        while len(self.description_input.text.split()) > 100:
            self.description_input.text = self.description_input.text[:-1]

    # Called whenever a landmark button is pressed
    def location_button_pressed(self, *args):
        location_name = args[0]

        # Handling the popup
        # Format of events_dict : {<event name>:[<location name>,<organiser username>,<DD.MM.YY hh:mm>,<Description>]}

        events_dict = obtain_events(location_name)

        layout = GridLayout(cols=1, size_hint_y=None)  # The main layout inside the popup
        layout.bind(minimum_height=layout.setter("height"))

        # User defined events (automatically handles the visitor/organiser modes)
        events_by_user = {event: events_dict[event]
                          for event in events_dict if events_dict[event][1] == current_username}

        # Events not defined by the user
        events_not_by_user = {event: events_dict[event] for event in events_dict if event not in events_by_user}

        # Sorting each of the events dictionaries by the timing of the events
        events_by_user = self.sort_events(events_by_user)
        events_not_by_user = self.sort_events(events_not_by_user)

        # combined_events is the concatenation of events_by_user and events_not_by_user
        combined_events = dict(events_by_user)
        combined_events.update(events_not_by_user)
        combined_events = filter_events(combined_events)

        add_events_button_layout = FloatLayout(size=(dp(550), dp(80)), size_hint=(None, None))

        add_events_button_layout.add_widget(Button(text="Add New Event",
                                                   font_name="CooperHewitt",
                                                   font_size=26,
                                                   pos_hint={"center_x": 0.5, "center_y": 0.4},
                                                   size_hint=(0.55, 0.8),
                                                   on_release=partial(self.add_new_event, location_name),
                                                   background_color=green,
                                                   color=white
                                                   ))

        # Add events option for organisers
        if current_username:
            layout.add_widget(add_events_button_layout)

        # Displays each event and gives options for their management
        for event_name in combined_events:
            event_data = combined_events[event_name]
            event_date, event_time = event_data[2].split()
            event_description = event_data[3]

            event_info_layout = FloatLayout(size=(dp(550), dp(160)), size_hint=(None, None))
            event_info_layout.add_widget(Label(text=event_name,
                                               font_name="OpenSans",
                                               bold=True,
                                               font_size=32,
                                               pos_hint={"center_x": 0.5, "center_y": 0.8},
                                               color=iitpkd_orange
                                               ))

            event_info_layout.add_widget(Label(text=event_date,
                                               font_name="OpenSans",
                                               bold=True,
                                               font_size=24,
                                               pos_hint={"center_x": 0.5, "center_y": 0.5},
                                               color=white
                                               ))

            event_info_layout.add_widget(Label(text=event_time,
                                               font_name="OpenSans",
                                               bold=True,
                                               font_size=24,
                                               pos_hint={"center_x": 0.5, "center_y": 0.26},
                                               color=white
                                               ))

            event_info_layout.add_widget(Button(text="",
                                                pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                size=event_info_layout.size,
                                                size_hint=(None, None),
                                                background_color=transparent,
                                                on_press=partial(self.open_event_description, event_name,
                                                                 event_description)
                                                ))

            layout.add_widget(event_info_layout)

            if event_name in events_by_user:
                remove_button_layout = FloatLayout(size=(dp(550), dp(80)), size_hint=(None, None))
                remove_event_button = Button(text="Remove above event",
                                             on_release=partial(self.remove_button_pressed, event_name, location_name),
                                             font_size=24,
                                             font_name="CooperHewitt",
                                             pos_hint={"center_x": 0.5, "center_y": 0.5},
                                             background_color=red,
                                             color=white,
                                             size_hint=(0.5, 0.75)
                                             )
                remove_button_layout.add_widget(remove_event_button)
                layout.add_widget(remove_button_layout)

        scroll = ScrollView()
        scroll.add_widget(layout)

        self.event_list_popup = Popup(title=location_name,
                                      content=scroll,
                                      size_hint=(None, None),
                                      size=(dp(550), dp(600)))
        self.event_list_popup.open()

    # Called when an event's name is clicked on. Opens the event's description
    def open_event_description(self, *args):
        event_name = args[0]
        event_description = "\n".join(args[1].split("\\n"))
        content_layout = FloatLayout(size=(dp(600), dp(390)), pos_hint={"x": 0, "y": 0}, size_hint=(None, None))

        self.description_label = Label(text=event_description,
                                       font_name="CamingoCode",
                                       pos_hint={"x": 0, "top": 0.975},
                                       size_hint=(1, 1),
                                       text_size=(dp(550), None),
                                       font_size=22)

        content_layout.add_widget(self.description_label)

        Popup(title=event_name + " - Description",
              size=(dp(600), dp(420)),
              size_hint=(None, None),
              content=content_layout
              ).open()

    # Sorts events based on their timing
    def sort_events(self, events_dict):
        if len(events_dict) == 0:
            return events_dict

        # Handling non-empty inputs
        # Format of entries of events_list : [event_name, number of minutes since 1 January 1970]
        initial_datetime = datetime(1970, 1, 1)
        events_list = []

        # Format of events_list = [event_name, number of seconds elapsed from 1 January, 1970 to the event's time]
        for event_name in events_dict:
            event_timing = events_dict[event_name][2]
            event_date, event_time = event_timing.split()

            event_datetime = datetime(*(tuple(int(i) for i in reversed(event_date.split("/"))) + tuple(
                int(i) for i in event_time.split(":"))))

            events_list.append([event_name, (event_datetime - initial_datetime).total_seconds()])

        events_list.sort(key=comparison_function)
        output_dict = {event[0]: events_dict[event[0]] for event in events_list}

        return output_dict


# Removes those events from the events file that have already ended
def update_events_file():
    with open("events.txt", "r") as event_file:
        events_data = event_file.read().split("\n")[:-1]

    events_dict = {entry.split("||")[0]: entry.split("||")[1].split("|") for entry in events_data}

    new_events_dict = {}

    for event_name in events_dict:
        event_timing = events_dict[event_name][2]
        event_date = tuple(int(i) for i in reversed(event_timing.split(" ")[0].split("/")))
        event_time = tuple(int(i) for i in event_timing.split(" ")[1].split(":"))
        event_datetime = datetime(*(event_date + event_time))

        if event_datetime >= datetime.now().replace(second=0, microsecond=0):
            new_events_dict[event_name] = events_dict[event_name]

    to_write = [event_name + "||" + "|".join(new_events_dict[event_name]) + "\n" for event_name in new_events_dict]

    with open("events.txt", "w") as new_events_file:
        for entry in to_write:
            new_events_file.write(entry)


# The class that manages the entire application
class EventMapperApp(App):
    def build(self):
        return WindowsManager()


if __name__ == "__main__":
    update_events_file()  # Filter out the events that have already ended
    EventMapperApp().run()
