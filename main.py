from bottle import route, run, template, static_file, request
import random
import json, pymysql
import os
from os import environ as env
from sys import argv

# ================ DATABASE INTERFACE  ======================

# defining database connection
connection = pymysql.connect(host='sql11.freemysqlhosting.net',
                             port=3306,
                             user='sql11158744',
                             password='c1svKiKCGI',
                             db='sql11158744',
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

        # get user id of newly added user
        sql = "SELECT user_id FROM users WHERE user_name = '{0}';".format(userName)
        cursor.execute(sql)
        result = cursor.fetchall()

        return result[0]['user_id']

def get_user_id(userName):
    with connection.cursor() as cursor:
        # get user id of newly added user
        sql = "SELECT user_id FROM users WHERE user_name = '{0}';".format(userName)
        cursor.execute(sql)
        result = cursor.fetchall()

        return result[0]['user_id']

# check if active game for specific user
def get_active_game_by_id(userID):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM games JOIN users ON games.user_id = users.user_id WHERE users.user_id = "{0}" AND games.game_completed = 0;'.format(userID)
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("No active game for user")
            return False
        else:
            return result

# check if active game for specific user
def get_active_game(userName):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM games JOIN users ON games.user_id = users.user_id WHERE users.user_name = "{0}" AND games.game_completed = 0;'.format(userName)
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

# get the amount of stories in an adventure
def max_story(adventureID):
    with connection.cursor() as cursor:
        sql = 'SELECT max(story_id) AS "max" FROM story WHERE adventure_id = {0};'.format(adventureID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

# funtion to get story data
def get_story_data(adventure_id, story_id, question_type):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM story WHERE adventure_id = {0} AND story_id = {1} AND question_type = {2};'.format(adventure_id, story_id, question_type)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#funtion to update current state of game (health, game complete, coins, stage in game)
def update_database(game_id, health, wealth, complete_status):
    with connection.cursor() as cursor:
        sql = 'UPDATE games SET game_completed = {0}, user_life = {1}, user_money = {2} WHERE game_id = {3};'.format(complete_status, health, wealth, game_id)
        cursor.execute(sql)
        connection.commit()

# funtion to update current state of game (story id)
def update_story_id(game_id, story_id):
    with connection.cursor() as cursor:
        sql = 'UPDATE games SET current_story_id = {0} WHERE game_id = {1};'.format(story_id, game_id)
        cursor.execute(sql)
        connection.commit()

# get new image for story
def get_story_image(adventure_id, story_id):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM images WHERE adventure_id = {0} AND story_id = {1};'.format(adventure_id, story_id)
        cursor.execute(sql)
        try:
            result = (cursor.fetchall())[0]
        except:
            result = {"image_name" : " "}

        return result


# ======================= GAME LOGIC ===============================

def check_answer(adventure_id, story_id, answer, user_id):

    # get current game id from database
    game_data = (get_active_game_by_id(user_id))[0]

    # get user health and coins from database
    user_health = game_data["user_life"]
    user_wealth = game_data["user_money"]
    game_status = game_data["game_completed"]
    game_id = game_data["game_id"]


    print("current player status, wealth: {0}, health: {1}, game Status: {2}".format(user_wealth, user_health,game_status))


    # get information regarding specific story (current answer, damage, coins)

    print("Test for sql query, adventure id: {0}, story_id: {1}, user answer: {2}".format(adventure_id,story_id,answer))
    story_data = (get_story_data(adventure_id,story_id,answer))[0]

    story_life_damage = story_data["life_unit"]
    story_wealth_damage = story_data["wealth_unit"]

    print("Specific story info story life {0} and story wealth {1}".format(story_life_damage,story_wealth_damage))


    # update health and wealth
    user_health = user_health - story_life_damage
    user_wealth = user_wealth - story_wealth_damage

    print("Updated player status, wealth: {0}, health: {1}, game Status: {2}".format(user_wealth, user_health, game_status))

    # check if user is dead
    database_game_status = 0

    if(user_health > 0 and user_wealth > 0):
        # user is dead
        game_status = 0
    else:
        game_status = -1
        database_game_status = 1


    # update databse with new health, coins and game status
    update_database(game_id,user_health,user_wealth,database_game_status)


    # if game_status is -1, user died, if 0 game still contunues
    return game_status



# ======================= SERVER ===============================

@route("/", method="GET")
def index():
    return template("adventure.html")

@route("/start", method="POST")
def start():
    username = request.POST.get("user")
    current_adv_id = request.POST.get("adventure_id")

    user_id = 0
    current_story_id = 0
    image=""



    # check if user exists
    if(not check_user(username)):
        # if does not exist create new user and game
        user_id = add_user(username)
        current_story_id = 1
        create_game(user_id,current_adv_id)


    else:
        # if user exists but all games are completed

        user_id = get_user_id(username)

        if(not get_active_game_by_id(user_id)):

            current_story_id = 1
            create_game(user_id, current_adv_id)
        else:
            # upload uncompleted game
            print("active game found")
            game_info = (get_active_game_by_id(user_id))[0]
            current_story_id = game_info["current_story_id"]
            current_adv_id = game_info["adventure_id"]


    # amount of stories in current adventure
    number_of_stories = (max_story(current_adv_id))[0]["max"]


    if ((current_story_id) > number_of_stories):
        print("Game complete")

    # get new story from database
    new_story_object = (new_story(current_adv_id, current_story_id))

    next_steps_results = [
        {"id": 1, "option_text": new_story_object[1]["content"]},
        {"id": 2, "option_text": new_story_object[2]["content"]},
        {"id": 3, "option_text": new_story_object[3]["content"]},
        {"id": 4, "option_text": new_story_object[4]["content"]}
        ]


    image = str((get_story_image(current_adv_id,current_story_id))["image_name"])


    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "current": current_story_id,
                       "text": new_story_object[0]["content"] ,
                       "image": image,
                       "options": next_steps_results
                       })

@route("/story", method="POST")
def story():

    # Get information from the AJAX request
    user_id = int(float(request.POST.get("user")))
    current_adv_id = int(float(request.POST.get("adventure")))
    current_story_id = int(float(request.POST.get("current_story"))) #this is what the user chose - use it!
    current_story_answer = int(float(request.POST.get("current_story_answer")))


    print("user answer from frontend: " + str(current_story_answer))

    # check user answer and update life and coins
    game_complete = check_answer(current_adv_id, current_story_id, current_story_answer, user_id)



    print("Game status after check answer: " + str(game_complete))


    # For testing purposes
    print("User ID: {0},  Adventure: {1},  Story: {2}, Answer: {3}".format(user_id,current_adv_id,current_story_id,current_story_answer))


    # amount of stories in current adventure
    number_of_stories = (max_story(current_adv_id))[0]["max"]

    # declare needed variables
    next_story = current_story_id + 1
    story_question = ""
    next_steps_results = []


    # condition is user is alive or dead
    if(game_complete == 0):

        # if user is alive and no stories left
        if((next_story) > number_of_stories):
            game_complete = 1

            next_steps_results = [
                {"id": 1, "option_text": ""},
                {"id": 2, "option_text": ""},
                {"id": 3, "option_text": ""},
                {"id": 4, "option_text": ""}
            ]
        else:
            # get new story from database
            new_story_object = (new_story(current_adv_id,next_story))

            # update database with story number
            game_id = (get_active_game_by_id(user_id))[0]["game_id"]
            update_story_id(game_id, next_story)



            next_steps_results = [
                {"id": 1, "option_text": new_story_object[1]["content"]},
                {"id": 2, "option_text": new_story_object[2]["content"]},
                {"id": 3, "option_text": new_story_object[3]["content"]},
                {"id": 4, "option_text": new_story_object[4]["content"]}
                ]

            story_question = new_story_object[0]['content']

    # if user is dead
    else:
        game_complete = -1

        next_steps_results = [
            {"id": 1, "option_text": ""},
            {"id": 2, "option_text": ""},
            {"id": 3, "option_text": ""},
            {"id": 4, "option_text": ""}
        ]

    print("Game status: " + str(game_complete))

    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    image = (get_story_image(current_adv_id, next_story))["image_name"]


    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "text": story_question,
                       "image": image,
                       "options": next_steps_results,
                       "story_id": next_story,
                       "complete": game_complete
                       })

@route("/js/<filename:re:.*\.js>")
def javascripts(filename):
    response = static_file(filename, root="js")
    response.set_header("Cache-Control", "public, max-age=2")
    return response

@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')

@route('/images/<filename:re:.*\.(jpg|jpeg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='0.0.0.0', port=argv[1])

# def main():
#     run(host='localhost', port=9000)


if __name__ == '__main__':
    main()



