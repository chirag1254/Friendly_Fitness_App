from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextFieldRect
from os import walk
from workoutbanner import WorkoutBanner
from friendbanner import FriendBanner
import requests
from functools import partial
import json
from myfirebase import My_Firebase
from kivy.uix.screenmanager import NoTransition, CardTransition

# from kivymd.uix.floatlayout import MDFloatLayout


Window.size = (350, 600)


class FriendsListScreen(MDScreen):
    pass


class ChangeAvatarScreen(MDScreen):
    pass


class AddFriendScreen(MDScreen):
    pass


class AddWorkoutScreen(MDScreen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class HomeScreen(MDScreen):
    pass


class SettingScreen(MDScreen):
    pass


class FriendWorkoutScreen(MDScreen):
    pass


class LoginScreen(MDScreen):
    pass


class MainApp(MDApp):
    my_friend_id = 1
    workout_image = None
    option_choice = None
    

    def build(self):
        self.icon = 'icon.jpg'
        self.my_firebase = My_Firebase()
        self.theme_cls.primary_palette = "Blue"
        GUI = Builder.load_file('main.kv')
        return GUI

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def change_avatar(self, image, widget_id):
        # change avatar in app
        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/avatars/" + image

        # change avatar in databasekivymd.uix.picker.MDDatePicker
        my_data = '{"avatar":"%s"}' % image
        requests.patch("https://friendly-fitness-419be.firebaseio.com/" +
                       str(self.my_friend_id)+".json", data=my_data)

    def add_friend(self, friend_id):
        # query database and make sure friendid exist
        check_reg = requests.get(
            'https://friendly-fitness-419be.firebaseio.com/.json?orderBy="my_friend_id"&equalTo='+friend_id)
        data = check_reg.json()

        if data == {}:
            self.root.ids['add_friend_screen'].ids["add_friend_label"].text = "Invalid friend ID"

        else:
            keys = [*data]
            key = keys[0]
            next_friend_id = data[key]['my_friend_id']
            self.root.ids['add_friend_screen'].ids["add_friend_label"].text = "Friend ID %s added scccessfully !!" % friend_id
            self.friends_list += ", %s" % friend_id
            patch_data = '{"friends":"%s"}' % self.friends_list
            patch_req = requests.patch(
                "https://friendly-fitness-419be.firebaseio.com/"+self.local_id+".json", data=patch_data)

    def add_workout(self):
        workout_ids = self.root.ids['add_workout_screen'].ids
        # self.workoutt_image
        description = workout_ids['breif_description'].text
        # Already have option choice
        quantity_input = workout_ids['quantity'].text
        units_input = workout_ids['units'].text
        day = workout_ids['day'].text
        month = workout_ids['month'].text
        year = workout_ids['year'].text
        # make sure fields are not garbage
        if self.workout_image == None:
            pass
        # allowed to empty description
        if self.option_choice == None:
            workout_ids['time_label'].text_color = (1, 0, 0, 1)
            workout_ids['distance_label'].text_color = (1, 0, 0, 1)
            workout_ids['sets_label'].text_color = (1, 0, 0, 1)
            return
        try:
            int_quantity = float(quantity_input)
        except:
            workout_ids['quantity'].background_color = (1, 0, 0, 1)
            return
        if units_input == "":
            workout_ids['units'].background_color = (1, 0, 0, 1)
            return
        try:
            int_month = int(month)
            if int_month > 12:
                workout_ids['month'].background_color = (1, 0, 0, 1)
                return
        except:
            workout_ids['month'].background_color = (1, 0, 0, 1)
            return
        try:
            int_day = int(day)
            if int_day > 31:
                workout_ids['day'].background_color = (1, 0, 0, 1)
                return
        except:
            workout_ids['day'].background_color = (1, 0, 0, 1)
            return
        try:
            if len(year) == 2:
                year = '20'+year
            int_year = int(year)
        except:
            workout_ids['year'].background_color = (1, 0, 0, 1)
            return

    # send data to Firebase
        workout_payload = {"workout_image": self.workout_image, "description": description, "likes": 0,
                           "number": float(int_quantity), "type_image": self.option_choice, "units": units_input,
                           "date": day + "/" + month + "/ 20"+year}
        workout_request = requests.post(
            "https://friendly-fitness-419be.firebaseio.com/%s/workouts.json" % (self.local_id), data=json.dumps(workout_payload))

        # print(workout_request.json())

    def update_workout_image(self, filename, widget_id):
        self.workout_image = filename

    def load_friend_workout_screen(self, friend_id, widget):
        friend_data_reg = requests.get(
            'https://friendly-fitness-419be.firebaseio.com/.json?orderBy="my_friend_id"&equalTo='+friend_id)
        # print(friend_data_reg.json())
        friend_data = friend_data_reg.json()
        # print(friend_data)
       
        workouts = []
        for key,value in friend_data.items() :
            workouts.append(value)
        
        
        workouts = workouts[0]['workouts']
        # print(workouts)

        friend_banner_grid = self.root.ids['friend_workout_screen'].ids["friend_banner_grid"]
        print(friend_banner_grid)
        for w in friend_banner_grid.walk():
            if w.__class__ == WorkoutBanner:
                friend_banner_grid.remove_widget(w)

        if workouts == {} or workouts == "" or workouts == "0":
            self.change_screen("friend_workout_screen")
            return
        for key in workouts.keys():
            workout = workouts[key]
            # print(workout, key)
            W = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'],
                              type_image=workout['type_image'], number=workout['number'], units=workout['units'],
                              likes=workout['likes'])
            friend_banner_grid.add_widget(W)
        friend_streak_label = self.root.ids['friend_workout_screen'].ids['friend_streak_label']
        
        streak_label =[]
        for key,value in friend_data.items():
            streak_label.append(value)
        streak_label = streak_label[0]['streak']
        friend_streak_label.text = str(streak_label)
        
        

        self.change_screen("friend_workout_screen")

    def logout(self):
        try:
            with open("refresh_token.txt", "r+") as f:
                    f.truncate(0)
            self.change_screen('login_screen')
        except :
            pass

    def on_start(self):
        try:
            # try to read persistant signin crediantials
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()
            # use refresh token to get new id token
            id_token, local_id = self.my_firebase.exchange_refresh_token(
                refresh_token)

            self.local_id = local_id
            self.id_token = id_token

            result = requests.get(
                "https://friendly-fitness-419be.firebaseio.com/"+local_id+".json")

            data = json.loads(result.content.decode())

            avatar_image = self.root.ids['avatar_image']
            avatar_image.source = "icons/avatars/"+data['avatar']
            # get friend list

            self.friends_list = data['friends']
            # print(self.friends_list)
            # Populate freinds_list_grid
            friends_list_array = self.friends_list.split(",")
            friends_list_array = friends_list_array[1:]
            # print(friends_list_array)

            for friend in friends_list_array:
                friend = friend.replace(" ", "")

                # print(friend)
                friend_banner = FriendBanner(friend_id=friend)
                self.root.ids["freinds_list_screen"].ids["friends_list_grid"].add_widget(
                    friend_banner)

            streak_label = self.root.ids['home_screen'].ids['streak_label']
            streak_label.text = str(data['streak'])+" Day Streak!"
            # get friend id on setting screen
            self.my_friend_id = data['my_friend_id']
            friend_label = self.root.ids['setting_screen'].ids['friend_id_label']
            friend_label.text = "Friend id : " + str(self.my_friend_id)

            banner_grid = self.root.ids['home_screen'].ids['banner_grid']

            workouts = data['workouts']
            
            workout_keys = workouts.keys()
            # print(workout_keys)
            for workout_key in workout_keys:

                workout = workouts[workout_key]
                W = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'],
                                  type_image=workout['type_image'], number=workout['number'], units=workout['units'],
                                  likes=workout['likes'])
                banner_grid.add_widget(W)
            self.root.ids['screen_manager'].transition = NoTransition()
            self.change_screen("home_screen")
            self.root.ids['screen_manager'].transition = CardTransition()

        except Exception as e:
            print(e)
            pass
        # populate avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folders, files in walk("icons/avatars"):
            for f in files:
                img = ImageButton(source="icons/avatars/"+f,
                                  on_release=partial(self.change_avatar, f))
                avatar_grid.add_widget(img)
        # populate workout image grid
        workout_image_grid = self.root.ids['add_workout_screen'].ids['workout_image_grid']
        for root_dir, folders, files in walk("icons/workouts"):
            for f in files:
                img = ImageButton(source="icons/workouts/"+f,
                                  on_release=partial(self.update_workout_image, f))
                workout_image_grid.add_widget(img)


if __name__ == "__main__":
    ma = MainApp()
    ma.run()
