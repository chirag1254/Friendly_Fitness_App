from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
import requests
from kivymd.app import MDApp
from functools import partial
class FriendBanner(MDFloatLayout):

    md_bg_color = (1,1,1,1)
    def __init__(self,**kwargs):
        super().__init__()
        self.friend_id = kwargs['friend_id']
        # print(self.friend_id)
        check_reg = requests.get('https://friendly-fitness-419be.firebaseio.com/.json?orderBy="my_friend_id"&equalTo='+self.friend_id)
        # print(check_reg.json())
        data = check_reg.json()
        def getList(dict):
            return [*dict]
        
        unique_identifer = getList(data)[0]
        # print(unique_identifer)
        their_avatar = data[unique_identifer]['avatar']
        # print(their_avatar)
        

        image_button = MDFillRoundFlatIconButton(icon="icons/avatars/" + their_avatar, size_hint=(1, .9),
                                   pos_hint={"top": .9, "right":1},
                                   text=kwargs['friend_id'] ,on_release = partial(MDApp.get_running_app().load_friend_workout_screen,kwargs['friend_id']))

      
        self.add_widget(image_button)
        