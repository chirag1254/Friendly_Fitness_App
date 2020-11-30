from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image


class WorkoutBanner(MDGridLayout):
    rows = 1
    md_bg_color = (1,1,1,1)
    def __init__(self,**kwargs):
        super().__init__()

        left = MDFloatLayout()
        left_image = Image(source="icons/workouts/" + kwargs['workout_image'], size_hint=(1, 0.8), pos_hint={"top": 1, "right": 1})
        left_label = MDLabel(text=kwargs['description'], size_hint=(1, .2), pos_hint={"top":0.2 , "right": 1},halign = "center")
        left.add_widget(left_image)
        left.add_widget(left_label)

        # Need middle MDFloatLayot
        middle = MDFloatLayout()
        
        middle_image = Image(source=""+ kwargs['type_image'], size_hint=(1, 0.8), pos_hint={"top": 1, "right": 1})
        middle_label = MDLabel( text =str(kwargs['number'])+" "+kwargs['units'], size_hint=(1, .2), pos_hint={"top": 0.2, "right": 1},halign = "center")
        middle.add_widget(middle_image)
        middle.add_widget(middle_label)

        # Need right MDFloatLayot
        right = MDFloatLayout()
        right_image = Image(source="icons/likes.png", size_hint=(1, 0.8), pos_hint={"top": 1, "right": 1})
        right_Label = MDLabel(text=str(kwargs['likes']) + " fist bumps", size_hint=(1, .2), pos_hint={"top": .2, "right": 1},halign = 'center')
        right.add_widget(right_image)
        right.add_widget(right_Label)

        self.add_widget(left)
        self.add_widget(middle)
        self.add_widget(right)