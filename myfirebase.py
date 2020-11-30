import requests
import json
from kivymd.app import MDApp


class My_Firebase():
    wak = "AIzaSyAmTyZGeAtdIaJsWqIluuUHWk4xHMXEJi8"  # Web Api Key

    def sign_up(self, email, password):
        app = MDApp.get_running_app()
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_data = {"email": email,
                       "password": password, "returnSecureToken": True}
        signup_request = requests.post(signup_url, data=signup_data)

        sign_up_data = json.loads(signup_request.content.decode())
        # print("sign_up_data",sign_up_data)
        
        
        if signup_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # save refreshToken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)
            # Save local id to a variable in main app class
            # save id token to a variable main app class
            app.local_id = localId

            app.id_token = idToken
            # creat new key in database from localId
            #get Frined id
            #default avatar
            # friends list
            # Emprt workouts area
            friend_get_reg = requests.get("https://friendly-fitness-419be.firebaseio.com/next_friend_id.json")
            
            my_friend_id = friend_get_reg.json()
            
            
            friend_patch_data = '{"next_friend_id": %s}' % str(my_friend_id+1)
            friend_patch_req = requests.patch("https://friendly-fitness-419be.firebaseio.com/.json",data = friend_patch_data)

            my_data = '{"avatar": "man.png","streak":"0","workouts":"0","friends":"0","my_friend_id": %s}'% my_friend_id
            re_patch = requests.patch("https://friendly-fitness-419be.firebaseio.com/"+localId+".json",data = my_data)
            
            app.change_screen("home_screen")
        else:
            error_data = json.loads(signup_request.content.decode())
            error_message = error_data['error']['message']
            app.root.ids['login_screen'].ids['login_message'].text = error_message

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        # print(refresh_req.ok)
        # print(refresh_req.json())
        return id_token, local_id
 
