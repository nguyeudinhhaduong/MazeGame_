import json
import pprint
import pickle

class UserDatabase:
    """
        def register_user(username, password) :: 
            Register a new user with username and password
            Return True if success, False if fail

        def login_user(username, password) ::
            Login user with username and password
            Return tuple of (username, password) if success, False if fail

        def load_user(username) ::
            Load data from a user (all game, password, username)
            Return False if fail, return user data if success

        def load_game(username, game_name) ::
            Load a game from a user
            Return False if fail, return game data if success

        def save_game(username, game_name, data) ::
            Save a game to a user
            Return False if fail, return True if success

        def leaderboard() ::
            return False if no user, return a tuple of 3 list:
                - Easy list, Medium list, Hard list in order of increasing time
    """    
    def __init__(self, filename = 'user_data.json'):
        self.filename = filename
        self.users = {}
        self.load_data()

    # Load data from json database
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            self.users = {}

    # Save data to json database
    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=3)

    # Register a new user with username and password -> save to json database
    def register_user(self, username, password):
        if username in self.users or username == '':
            return False                    # Dang ki that bai
        self.users[username] = {'password': password}   ## Khoi tao cac thong so khac cua user
        self.save_data()
        return True                         # Dang ki thanh cong
    
    # Login user with username and password 
    # -> return tuple of (username, password) if success, False if fail
    def login_user(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == password:
                return (username, password)
            else:
                return False # wrong password
        else:
            return False # wrong username

    # Use this function to load data from a user (all game, password, username)    
    def load_users(self, username):
        if username in self.users:
            return self.users[username]
        return False
        
    # Use this function to load a game from a user    
    def load_game(self, username, game_name):
        if username in self.users:
            if game_name in self.users[username]:
                return self.users[username][game_name]
        return False
    
    # Use this function to save a game to a user 
    def save_game(self, username, game_name, data):
        # pprint.pprint(data)
        if username in self.users:
            self.users[username][game_name] = data
            self.save_data()
            return True
        return False

    def leaderboard(self):
        if len(self.users) == 0:
            return False
        easy_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'Easy' and self.users[user][game_name]['isdone'] == True and self.users[user][game_name]['mode_play'] == 'Player':
                        easy_list.append(self.users[user][game_name])
        easy_list.sort(key=lambda x: x['time'][0]* 60 + x['time'][1])

        medium_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'Medium' and self.users[user][game_name]['isdone'] == True and self.users[user][game_name]['mode_play'] == 'Player':
                        medium_list.append(self.users[user][game_name])
        medium_list.sort(key=lambda x: x['time'][0]* 60 + x['time'][1])

        hard_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'Hard' and self.users[user][game_name]['isdone'] == True and self.users[user][game_name]['mode_play'] == 'Player':
                        hard_list.append(self.users[user][game_name])
        hard_list.sort(key=lambda x: x['time'][0]* 60 + x['time'][1])

        return (easy_list, medium_list, hard_list)
