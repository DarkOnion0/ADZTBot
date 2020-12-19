import sqlite3, os, glob
from datetime import datetime

# Data
#PATH = os.path.abspath(os.path.split(__file__)[0])
#data_dir = os.path.join(PATH, "data")
#
#data_db = os.path.join(data_dir, "data_darkbot.db")

#listdir = os.listdir(PATH)
#index_dir = len(listdir)
#print(type(listdir), listdir, index_dir)

#try:
#    assert glob.glob(os.path.join(PATH, "data"))
#except AssertionError:
#    os.mkdir(os.path.join(PATH, "data"))
#    print("Data Folder create")

#connection = sqlite3.connect("data/data_darkbot.db")
#print(connection.total_changes)
#cursor = connection.cursor()

class user:
    """A class which handle all fonctions for adding user in the sqlite database"""
    def __init__(self, ConnectionPath):
        """Defined the path of the DB""" 
        
        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Log (date INTEGER, logfile BLOB)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS UserData (username TEXT ,lvl INTEGER, lvl_xp INTEGER, os TEXT, description TEXT, game TEXT)")
        self.connection.commit()

    
    def add(self, username):
        """Add user in fonctions of the username passed"""
        user = self.cursor.execute("SELECT username FROM UserData").fetchall()
        
        check = True

        print(user, type(user), check)
        
        for index, UserTmp in enumerate(user):
            UserTmp = str(UserTmp[0])
            print("\n",username, UserTmp, type(username), type(UserTmp))
            
            if username == UserTmp:
                check = False
        print(check)
        
        if check == True:
            self.cursor.execute("INSERT INTO UserData(username) VALUES (?)", (username,))
            print(username)
            self.connection.commit()
#if __name__ == "__main__":
#    u = "init"
#    a = user(u)
#    a.add(u)
#    rows = cursor.execute("SELECT username FROM UserData").fetchall()
#    print(rows)
#    print("Sucess")
