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



check_user('Tomer Marx')
add_user("Barak Marxx")


# check if active game for specific user
def get_active_game(userName):
    with connection.cursor() as cursor:
        sql = "SELECT  FROM games WHERE user_id = '{0}'".format(userName)
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("No active game for user")
            return False
        else:
            return result




# update life and step


# get new story

# if game over or complete change game status to complete





