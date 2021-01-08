import sqlite3
import os
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class user:
    """A class which handle all fonctions for manage user in the sqlite database"""

    def __init__(self, ConnectionPath):
        """Defined the path of the DB"""

        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS UserData (id INTEGER PRIMARY KEY, username TEXT , creation_date TEXT, birthday TEXT, lvl INTEGER, lvl_xp INTEGER, os TEXT, description TEXT, game TEXT, coins FLOAT, awards_left, timestamp TEXT)"
        )
        self.connection.commit()

    def add(self, username):
        """Add user in fonctions of the username passed"""
        user = self.cursor.execute("SELECT username FROM UserData").fetchall()
        check = True

        for userTmp in user:  # check if the user already exist in the database
            userTmp = str(userTmp[0])
            if username == userTmp:
                check = False

        if check:  # if the user doesn't exist, create his profile
            self.cursor.execute(
                "INSERT INTO UserData(id, username, creation_date, timestamp) VALUES((SELECT max(id) FROM UserData)+1, ?, ?, ?)",
                (
                    username,
                    timestamp(),
                    timestamp(),
                ),
            )
            print(username)
            self.connection.commit()


class vote:
    """A class whixh handle all fonctions for all the vote command in the sqlite database"""

    def __init__(self, ConnectionPath):
        """Defined the path of the DB"""

        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS VoteTable (id INTEGER PRIMARY KEY, user INTEGER, type TEXT, link TEXT, score INTEGER)"
        )
        self.connection.commit()

    def post(self, username, t, link):
        """Add a musique or video in the database"""
        user = self.cursor.execute("SELECT id, username FROM UserData").fetchall()
        linkTmp2 = self.cursor.execute("SELECT link FROM VoteTable").fetchall()
        check = True

        for user in user:  # check if the user exist in the database
            user = list(user)
            if str(user[1]) == username:
                check = False
                usernameId = int(user[0])

        if check == True:
            return "0.1"
        else:
            check2 = True

            for linkTmp in linkTmp2:
                linkTmp = list(linkTmp)
                if str(linkTmp[0]) == link:
                    check2 = False

            if check2 == True:
                self.cursor.execute(
                    "INSERT INTO VoteTable(user, type, link) VALUES(?, ?, ?)",
                    (
                        usernameId,
                        t,
                        link,
                    ),
                )
                self.connection.commit()
                return "1"
            else:
                return "0.2"
