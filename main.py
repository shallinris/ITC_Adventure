from bottle import route, run, template, static_file, request
import random
import json
import pymysql
import json, pymysql


#add database connection here



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
            user_id = add_user(username)
            current_story_id = 1
            create_game(user_id, current_adv_id)
        else:
            # upload uncompleted game
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


    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "current": current_story_id,
                       "text": new_story_object[0]["content"] ,
                       "image": "troll.png",
                       "options": next_steps_results
                       })


@route("/story", method="POST")
def story():
    user_id = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!


    # get current story for user
    previous_story = (get_active_game_by_id(user_id))[0]['current_story_id']

    print("test")

    # amount of stories in current adventure
    number_of_stories = (max_story(current_adv_id))[0]["max"]

    next_story = 0

    if((previous_story + 1) > number_of_stories):
        print("Game complete")

    else:
        next_story = previous_story + 1

    # get new story from database
    new_story_object = (new_story(current_adv_id,next_story))

    next_steps_results = [
        {"id": 1, "option_text": new_story_object[1]["content"]},
        {"id": 2, "option_text": new_story_object[2]["content"]},
        {"id": 3, "option_text": new_story_object[3]["content"]},
        {"id": 4, "option_text": new_story_object[4]["content"]}
        ]
    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "text": new_story_object[0]["content"],
                       "image": "choice.jpg",
                       "options": next_steps_results
                       })

@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()



