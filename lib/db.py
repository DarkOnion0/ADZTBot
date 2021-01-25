import sqlite3
import os
from datetime import datetime


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class user:
    """A class which handle all fonctions for manage user in the sqlite database"""

    def __init__(self, ConnectionPath):
        """Defined the path of the DB"""

        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS UserData (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT , creation_date TEXT, birthday TEXT, lvl INTEGER, lvl_xp INTEGER, os TEXT, description TEXT, game TEXT, coins FLOAT, awards_left, timestamp TEXT)"
        )
        self.connection.commit()

    def add(self, username, username_id):
        """Add user in fonctions of the username passed"""
        user = self.cursor.execute("SELECT user_id FROM UserData").fetchall()
        check = False

        for userTmp in user:  # check if the user already exist in the database
            userTmp = list(userTmp)
            print(userTmp)
            if username_id == userTmp[0]:
                check = True

        if check == False:  # if the user doesn't exist, create his profile
            self.cursor.execute(
                "INSERT INTO UserData(id, user_id, username, creation_date, timestamp) VALUES((SELECT max(id) FROM UserData)+1, ?, ?, ?, ?)",
                (
                    username_id,
                    username,
                    _timestamp(),
                    _timestamp(),
                ),
            )
            print(username, username_id)
            self.connection.commit()
            return 1
        else:
            return 0
    
    def update(self, username, username_id, arg=None):
        user = self.cursor.execute("SELECT id, user_id, username FROM UserData").fetchall()

        print(username, username_id, arg, user)
        print("\nstep 1")

        if arg[0] == "update_name":
            print("step 1.1")            
            if arg[1] == "id": # udpate id
                user = self.cursor.execute("SELECT id, username FROM UserData").fetchall()
                print("\nstep 2 --> id")

                for i, user_tmp in user: 
                    print(i, user_tmp)
                    
                    if username == user_tmp:
                        print("step 2.1")
                        self.cursor.execute("UPDATE UserData SET user_id = ? WHERE id = ?", (username_id, i,),)

                        self.connection.commit()
            
            if arg[1] == "username": # udpate name
                print("\nstep 2 --> name")
                
                for i, username_id_tmp, userTmp in user:  
                    username_id = int(username_id_tmp)
                    
                    print(i, username_id_tmp, userTmp)
                    if username_id == username_id_tmp:
                        print("step 2.1")
                        self.cursor.execute("UPDATE UserData SET username = ? WHERE id = ?", (username, i,),)

                        self.connection.commit()
            

class vote:

    """A class whixh handle all fonctions for all the vote command in the sqlite database"""
    def __init__(self, ConnectionPath):
        """Defined the path of the DB"""

        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS VoteTable (id INTEGER PRIMARY KEY, type TEXT, postId INTEGER, user INTEGER, link TEXT, score INTEGER, voteUser TEXT, FOREIGN KEY(user) REFERENCES UserData(id))"
        )
        self.connection.commit()

    def post(self, username, t, link):
        """Add a musique or video in the database"""
        user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()
        linkTmp2 = self.cursor.execute("SELECT type, link FROM VoteTable").fetchall()
        check = True

        mCount = 0
        vCount = 0

        for user in user:  # check if the user exist in the database
            user = list(user)
            print(user)
            if int(user[1]) == username:
                check = False
                usernameId = int(user[0])

        if check == True:
            return (None, 0.1)
        else:
            check2 = True

            for typeTmp, linkTmp in linkTmp2:
                linkTmp = list(linkTmp)
                if "".join(linkTmp) == link:
                    check2 = False
                if typeTmp == "m":
                    mCount += 1
                if typeTmp == "v":
                    vCount += 1
                print("\n")
                print("".join(linkTmp), link, t, typeTmp)

            if check2 == True:
                if t == "m":
                    idTmp = mCount + 1
                elif t == "v":
                    idTmp = vCount + 1
                voteUser = "0, " + str(usernameId)
                self.cursor.execute(
                    "INSERT INTO VoteTable(id, postId, user, type, link, score, voteUser) VALUES((SELECT max(id) FROM VoteTable)+1, ?, ?, ?, ?, ?, ?)",
                    (
                        idTmp,
                        usernameId,
                        t,
                        link,
                        1,
                        voteUser,
                    ),
                )
                self.connection.commit()
                print(idTmp)
                return (idTmp, 1)
            else:
                return (None, 0.2)

    def vote(self, username, t, i, vote):
        """add vote on post"""
        user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()
        values = self.cursor.execute("SELECT id, type, postId FROM VoteTable").fetchall()
        userVote = self.cursor.execute("SELECT id, voteUser FROM VoteTable").fetchall()
        score = self.cursor.execute("SELECT id, score FROM VoteTable").fetchall()
        check = True

        for user in user:  # check if the user exist in the database
            user = list(user)
            print(user)
            if int(user[1]) == username:
                check = False
                usernameId = int(user[0])

        print("\nstep 1", type(vote), vote)

        if check == False:
            check = True
            for (
                idTmp,
                typeTmp,
                postIdTmp,
            ) in values:  # check if the post id exist in the database
                print(idTmp, typeTmp, postIdTmp, i, t)
                if str(typeTmp) == str(t):
                    print("step 1.1")
                    if int(postIdTmp) == int(i):
                        check = False
                        iTmp = idTmp

            print("step 2")

            if check == False:

                print("step 2.1")
                check = False
                for idTmp, userTmp in userVote:  # check if the user already vote
                    userTmp = userTmp.split(",")
                    userAll = userTmp
                    print(userTmp)
                    if idTmp == iTmp:
                        uTmp = userTmp
                        for userTmp2 in userTmp:
                            print(
                                userTmp2, usernameId, type(userTmp2), type(usernameId)
                            )
                            if int(userTmp2) == usernameId:
                                print("step 2.2")
                                check = True
                print("step 3")
                
                if check == False:  # add vote and username id into the database for the choosen post id
                    
                    uTmp = list(uTmp)
                    uTmp.append(" " + str(usernameId))
                    uTmp = ",".join(uTmp)

                    for idTmp, scoreTmp in score:
                        if idTmp == iTmp:
                            scoreEnd = scoreTmp + (int(vote))
                            print(scoreEnd, type(scoreEnd))

                    userAll.append(iTmp)
                    print(userAll)

                    self.cursor.execute(
                        "UPDATE VoteTable SET score = ?, voteUser = ? WHERE id = ?",
                        (scoreEnd, uTmp, iTmp),
                    )
                    self.connection.commit()

                    print("step 4")

                    return 1  # succses
                else:
                    return 0.3  # the user already vote
            else:
                return 0.2  # the post doesn't exist
        else:
            return 0.1  # user doesn't exist

    def stats(self, t, i):
        """give stats on an existing post in the database"""
        values = self.cursor.execute(
            "SELECT id, type, postId FROM VoteTable"
        ).fetchall()
        
        post_info = self.cursor.execute(
            "SELECT type, postId, user, link, score, voteUser FROM VoteTable"
        ).fetchall()
        
        user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()

        check = True

#        for idTmp, typeTmp, postIdTmp, in values:  # check if the post id exist in the database            
#            print(idTmp, typeTmp, postIdTmp, i, t)
#
#            if str(typeTmp) == str(t):
#                print("\nstep 1")
#
#                if int(postIdTmp) == int(i):
#                    db_id_tmp = idTmp
#                    i_post_tmp = idTmp
#                    check = False
#                    print(db_id_tmp, i_post_tmp)
#
        for type_tmp, postid_tmp, user_tmp, link_tmp, score_tmp, vote_user_tmp in post_info:

            if str(type_tmp) == str(t):
                print("\nstep 1")

                if int(postid_tmp) == int(i):
                    print(("step 1.1"))
                    type_f = type_tmp
                    postid_f = postid_tmp
                    user_f = user_tmp
                    link_f = link_tmp
                    score_f = score_tmp
                    vote_user_f = vote_user_tmp
                    print(type_f, postid_f, user_f, link_f, score_f, vote_user_f)
                    check = False

#        if check == False:
#            check = True
#            print("\nstep 2")
#            for (
#                id_tmp,
#                type_tmp,
#                postid_tmp,
#                user_tmp,
#                link_tmp,
#                score_tmp,
#                vote_user_tmp,
#            ) in post_info:
#
#                if id_tmp == db_id_tmp:
#                    type_f = type_tmp
#                    postid_f = postid_tmp
#                    user_f = user_tmp
#                    link_f = link_tmp
#                    score_f = score_tmp
#                    vote_user_f = vote_user_tmp
#                    print(type_f, postid_f, user_f, link_f, score_f, vote_user_f)
#
#            print("\n   step 2.2")
#
        if check == False:
            for user_id_tmp, user_id_tmp in user:
                if user_id_tmp == user_f:
                    user_f = user_id_tmp
                    check = False
                    print(user_f)

            if check == False:
                print(
                    "\nstep 3", type_f, postid_f, user_f, link_f, score_f, vote_user_f
                )
                return (1, type_f, postid_f, user_f, link_f, score_f, vote_user_f)
            else:
                return (
                    0.2,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )  # if the script failed to get the username of the author of the post
        else:
            return (
                0.1,
                None,
                None,
                None,
                None,
                None,
                None,
            )  # if the post doesn't exist in the database
