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
            "CREATE TABLE IF NOT EXISTS UserData (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT , creation_date TEXT, birthday TEXT, xp_full INTEGER, os TEXT, description TEXT, game TEXT, coins FLOAT, awards_left, timestamp TEXT)"
        )
        self.connection.commit()

    def add(self, username, username_id):
        """Add user in fonctions of the username passed"""
        user = self.cursor.execute("SELECT user_id, username FROM UserData").fetchall()
        check = False

        for (
            user_id,
            user_name,
        ) in user:  # check if the user already exist in the database
            print(user_id, user_name)
            if username_id == user_id or username == user_name:
                check = True

        if check == False:  # if the user doesn't exist, create his profile
            self.cursor.execute(
                "INSERT INTO UserData(id, user_id, username, creation_date, timestamp, xp_full) VALUES((SELECT max(id) FROM UserData)+1, ?, ?, ?, ?, ?)",
                (
                    username_id,
                    username,
                    _timestamp(),
                    _timestamp(),
                    1,
                ),
            )
            print(username, username_id)
            self.connection.commit()
            return 1
        else:
            return 0

    def update(self, username, username_id, arg=None):
        user = self.cursor.execute(
            "SELECT id, user_id, username FROM UserData"
        ).fetchall()

        print(username, username_id, arg, user)
        print("\nstep 1")

        if arg[0] == "update_name":
            print("step 1.1")
            if arg[1] == "id":  # udpate id
                user = self.cursor.execute(
                    "SELECT id, username FROM UserData"
                ).fetchall()
                print("\nstep 2 --> id")

                for i, user_tmp in user:
                    print(i, user_tmp)

                    if username == user_tmp:
                        print("step 2.1")
                        self.cursor.execute(
                            "UPDATE UserData SET user_id = ? WHERE id = ?",
                            (
                                username_id,
                                i,
                            ),
                        )

                        self.connection.commit()

            if arg[1] == "username":  # udpate name
                print("\nstep 2 --> name")

                for i, username_id_tmp, userTmp in user:
                    username_id = int(username_id_tmp)

                    print(i, username_id_tmp, userTmp)
                    if username_id == username_id_tmp:
                        print("step 2.1")
                        self.cursor.execute(
                            "UPDATE UserData SET username = ? WHERE id = ?",
                            (
                                username,
                                i,
                            ),
                        )

                        self.connection.commit()
    
    def stats(self, user_id: int, result="full"):
        """
        A object that return the stats on a user
        """
        print(int(user_id))
        check = True
        # collect the user info from the DB
        try:
            user = self.cursor.execute("SELECT id, user_id, creation_date, birthday, os, description, game, xp_full FROM UserData WHERE user_id = ?", (int(user_id),),).fetchall() # try a direct query
            
            user = list(user[0])
            print(user, len(user))

            id_f = user[0]
            creation_f = user[2]
            birthday_f = user[3]
            
            tmp = self.xp(user_id=user[1], xp=user[7], show=True)
            tmp = list(tmp)
            if tmp[0] == 1:
                lvl_f = tmp[1]
            else:
                lvl_f = f"ERROR {tmp[0]}"
        
            #print(tmp, "TMP")
            
            #lvlxp_f = user[5]
            os_f = user[4]
            description_f = user[5]
            game_f = user[6]
            xp_f = user[7]

            check = False

            print("step 1_1 stats", xp_f)
            
        except:
            user = self.cursor.execute("SELECT id, user_id, creation_date, birthday, os, description, game, xp_full FROM UserData").fetchall() # try a large query if the first try failed
            for id_tmp, user_id_tmp, creation_tmp, birthday_tmp, os_tmp, description_tmp, game_tmp, xp_tmp in user:
                if str(user_id_tmp) == str(user_id):
 
                    id_f = id_tmp
                    creation_f = creation_tmp
                    birthday_f = birthday_tmp
                    
                    tmp = self.xp(user_id=user_id_tmp, xp=xp_tmp, show=True)
                    tmp = list(tmp)
                    if tmp[0] == 1:
                        lvl_f = tmp[1]
                    else:
                        lvl_f = f"ERROR {tmp[0]}"
                    
                    #lvlxp_f = lvlxp_tmp
                    os_f = os_tmp
                    description_f = description_tmp
                    game_f = game_tmp
                    xp_f = xp_tmp

                    check = False
                    print("step 1_2")
                    pass

        if check == False:

            if result == "small":
                print("step 2_1")
                post_tmp = self.cursor.execute("SELECT id FROM VoteTable WHERE user = ?", (str(id_f)),).fetchall()
                post_f = len(post_tmp)
                return 1, creation_f, lvl_f, post_f

            elif result == "full":
                print("step 2_2")
                # get the number of post and score for a giver user
                post_tmp = self.cursor.execute("SELECT id, score FROM VoteTable WHERE user = ?", (str(id_f)),).fetchall()
                
                post_f = len(post_tmp)
                score_f = int()
                
                for id_tmp, score_tmp in post_tmp:
                    score_f += score_tmp
                
                return 1,  creation_f, lvl_f, post_f, score_f, birthday_f, os_f, description_f, game_f, xp_f
        else:
            return 0.1

    def xp(self, user_id: int, xp: int, show = False):
        """
        An object that manage all the things related to add or delete xp to a user\n
        
        Result
        ==========
         1      all was done successfully
         0.1    the user doesn't exist
         0.2    an error occured during the job

        """
        
        check = False
        
        print(user_id)
                
        # Get user indo from the database
        try:
            user_info = self.cursor.execute("SELECT xp_full FROM UserData WHERE user_id = ?", (int(user_id),),).fetchall()
            print(user_info, "user_info")
            assert len(user_info) == 1
            check = True
            is_user_id = True
            print("\n\nSUCCES")
        except:
            try:
                user_info = self.cursor.execute("SELECT lvl, lvl_xp, xp_full FROM UserData WHERE id = ?", (str(user_id),),).fetchall()
                check = True
                is_user_id = False
            except:
                check = False
            print("\n\nERROR")

        if check == True:
            
            print("user_info", xp, show, user_info)
            user_info = list(user_info[0])
            user_xp = user_info[0]
            print(user_xp, xp, show, "start")
            
            if show == True:
                try:
                    lvl = user_xp / 5
                    lvl = int(lvl)

                    print(lvl, user_xp, "end")

                    r = (1, lvl)
                    return r
                except:
                    r = (0.2, None)
                    return r 
            else:
                try:
                    user_xp = user_xp + (xp)
                    print(user_xp)

                    self.connection.execute("UPDATE UserData SET xp_full = ? WHERE user_id = ?", (user_xp,int(user_id),),)

                    self.connection.commit()
                    r = (1, None) # SUCCSES
                    return r
                except:
                    r = (0.2, None)
                    return r
        
        else:
            r = (0.1, None) # ERROR 0: the user doesn't exists
            return r
                
class vote:

    """A class which handle all fonctions for all the vote command in the sqlite database"""

    def __init__(self, ConnectionPath: str):
        """Defined the path of the DB"""

        self.connection = sqlite3.connect(ConnectionPath)
        print(self.connection.total_changes)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS VoteTable (id INTEGER PRIMARY KEY, type TEXT, postId INTEGER, user INTEGER, link TEXT, score INTEGER, voteUser TEXT, FOREIGN KEY(user) REFERENCES UserData(id))"
        )
        self.connection.commit()

        self.user_xp = user(ConnectionPath)


    def post(self, username, t, link):
        """Add a musique or video in the database"""
        user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()
        linkTmp2 = self.cursor.execute("SELECT type, link FROM VoteTable").fetchall()
        check = True

        link = link.split("?si=")
        
        mCount = 0
        vCount = 0

        for db_id, user_id in user:  # check if the user exist in the database
            print(user)
            if user_id == username:
                check = False
                usernameId = db_id

        if check == True:
            return (None, 0.1)
        else:
            check2 = True

            for typeTmp, linkTmp in linkTmp2:
                #linkTmp = str(linkTmp)
                linkTmp = linkTmp.split("?si=")
                print("linkTmp = {}".format(linkTmp))
                if linkTmp[0] == link[0]:
                    check2 = False
                if typeTmp == "m":
                    mCount += 1
                if typeTmp == "v":
                    vCount += 1
                #print("\n")
                #print("".join(linkTmp), link[0], t, typeTmp)

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
                        link[0],
                        0,
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
        #user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall() # DEPRECATED
        user_v2 = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()
        values = self.cursor.execute("SELECT user, id, type, postId FROM VoteTable").fetchall()
        userVote = self.cursor.execute("SELECT id, voteUser FROM VoteTable").fetchall()
        score = self.cursor.execute("SELECT id, score FROM VoteTable").fetchall()
        check = True

        for user in user_v2:  # check if the user exist in the database
            user = list(user)
            print(user)
            if int(user[1]) == username:
                check = False
                usernameId = int(user[0])
                user_id = int(user[1])

        print("\nstep 1", type(vote), vote)

        if check == False:
            check = True
            
            for user_tmp, idTmp, typeTmp, postIdTmp in values:  # check if the post id exist in the database and retrive the user id in the DB
                print(idTmp, typeTmp, postIdTmp, i, t)
            
                if str(typeTmp) == str(t):
                    print("step 1.1")
            
                    if int(postIdTmp) == int(i):
                        check = False
                        iTmp = idTmp
                        user_id_f = user_tmp

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
                        print("step 2.1.1\n", uTmp)
                    
                        for userTmp2 in userTmp:
                            print(userTmp2, usernameId, type(userTmp2), type(usernameId))

                            if int(userTmp2) == usernameId:
                                print("step 2.2")
                                check = True

                print("step 3")

                if check == False:  # add vote and username id into the database for the chosen post id
                    print("step 3.1")
                    uTmp = list(uTmp)
                    uTmp.append(" " + str(usernameId))
                    uTmp = ",".join(uTmp)

                    if vote == "+":
                        vote = +1
                    elif vote == "-":
                        vote = -1

                    for idTmp, scoreTmp in score:
                        print("step 3.2")
                        if idTmp == iTmp:
                            scoreEnd = scoreTmp + (int(vote))
                            print(scoreEnd, type(scoreEnd))

                    userAll.append(iTmp)
                    print(userAll, "userAll")
                    print(user_id_f, user_id, vote)
                    
                    print(user_v2)
                    for user in user_v2:  # check if the user exist in the database
                        print(user)
                        user = list(user)
                        print(user)
                        if int(user[0]) == user_id_f:
                            check = False
                            user_id_poster = int(user[1]) 


                    result = self.user_xp.xp(user_id=user_id_poster, xp=vote, show=False)
                    result = list(result)

                    if int(result[0]) == 1:
                        print("step 3.3")
                    
                        self.cursor.execute(
                            "UPDATE VoteTable SET score = ?, voteUser = ? WHERE id = ?",
                            (scoreEnd, uTmp, iTmp),
                        )

                        self.connection.commit()

                        print("step 4")

                        return 1 # success
                    else:
                        return 0.4  # adding the xp failed
                else:
                    return 0.3  # the user already vote
            else:
                return 0.2  # the post doesn't exist
        else:
            return 0.1  # user doesn't exist

    def stats(self, t : str, i : int):
        """give stats on an existing post in the database"""
        t = str(t)
        i = str(i)
        user = self.cursor.execute("SELECT id, user_id FROM UserData").fetchall()

        try:
            post_info = self.cursor.execute("SELECT type, postId, user, link, score, voteUser FROM VoteTable WHERE type=? AND postId=?", (str(t), int(i)),).fetchall()
            type_f, postid_f, user_tmp, link_f, score_f, vote_user_f = post_info[0]

            print(type_f, postid_f, user_tmp, link_f, score_f, vote_user_f, type(user_tmp))
            status = 1
            #try:
            #    user_f = self.cursor.execute("SELECT id, user_id FROM UserData WHERE id = ?", (user_tmp),).fetchall()
            #    status = 1
            #    print("step 2")
            #except ValueError as e:
            #    status = 0.2
            #    print("error 2 --> ", e)
        except:
            status = 0.1
            print("error 1")

        try:
            for db_id_tmp, user_id_tmp in user:
                if db_id_tmp == user_tmp:
                    user_f = user_id_tmp
                    check = False
                    print(user_f)
            return (status, type_f, postid_f, user_f, link_f, score_f, vote_user_f)
        except:
            return (status, None, None, None, None, None, None)