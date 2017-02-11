import random
import json

import json, pymysql

# add database connection here



# ================ DATABASE INTERFACE  ======================


# defining database connection

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='talmap',
                             db='adventure',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


# check if user exists
def check_user(userName):
    # check if user exists
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE user_name = '{0}'".format(userName)
        cursor.execute(sql)
        result = cursor.fetchall()

    if(len(result) == 0):
        print("User does not exist")
        return False

    elif(len(result) > 0):
        print("Matching user found")
        return True

# function to add user
def add_user(userName):
    with connection.cursor() as cursor:
        sql = "INSERT INTO users VALUES (default,'{0}');".format(userName)
        cursor.execute(sql)
        connection.commit()

# check if active game for specific user
def get_active_game(userName):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM games JOIN users ON games.user_id = users.user_id WHERE users.user_name = "{0}" AND games.game_completed = 1;'.format(userName)
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("No active game for user")
            return False
        else:
            return result

# create new game (return id of new game)
def create_game(userID, adventureID):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO games VALUES (default,{0},{1},{2},{3},{4},{5});'.format(userID,adventureID,100,10,1,0)
        cursor.execute(sql)
        connection.commit()

        sql= 'SELECT max(game_id) AS current_game FROM games;'
        cursor.execute(sql)

        result = cursor.fetchall()
        game_id = result[0]['current_game']

        return game_id

# update life and step
def update_game(gameID, lifeUnit, wealthUnit, storyId):
    with connection.cursor() as cursor:
        sql = 'UPDATE games SET user_life= {0}, user_money = {1}, current_story_id = {2} WHERE game_id = {3};'.format(lifeUnit,wealthUnit,storyId,gameID)
        cursor.execute(sql)
        connection.commit()

# game completed
def complete_game(gameID, lifeUnit, wealthUnit):
    with connection.cursor() as cursor:
        sql = 'UPDATE games SET user_life= {0}, user_money = {1}, game_completed = {2} WHERE game_id = {3};'.format(lifeUnit, wealthUnit,1, gameID)
        cursor.execute(sql)
        connection.commit()

# get new story
def new_story(adventureID, storyID):
    with connection.cursor() as cursor:
        sql = 'SELECT adventure_id, story_id, question_type, content FROM story WHERE adventure_id = {0} AND story_id = {1} ORDER BY question_type ;'.format(adventureID, storyID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result




print(not True)



