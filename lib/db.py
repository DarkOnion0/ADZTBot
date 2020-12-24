import sqlite3, os
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class user:
    """A class which handle all fonctions for adding user in the sqlite database"""
    def __init__(self, ConnectionPath):
        """Defined the path of the DB""" 
        
        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Log (date INTEGER, logfile BLOB)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS UserData (id INTEGER PRIMARY KEY, username TEXT , creation_date TEXT, birthday TEXT, lvl INTEGER, lvl_xp INTEGER, os TEXT, description TEXT, game TEXT, coins FLOAT, awards_left, timestamp TEXT)")
        self.connection.commit()


    
    def add(self, username):
        """Add user in fonctions of the username passed"""
        user = self.cursor.execute("SELECT username FROM UserData").fetchall()
        check = True

        for index, UserTmp in enumerate(user): # check if the user already exist in the database
            UserTmp = str(UserTmp[0])
            
            if username == UserTmp:
                check = False
        
        if check == True: # if the user doesn't exist, create his profile
            self.cursor.execute("INSERT INTO UserData(id, username, creation_date, timestamp) VALUES((SELECT max(id) FROM UserData)+1, ?, ?, ?)", (username, timestamp(), timestamp(),))
            print(username)
            self.connection.commit()
