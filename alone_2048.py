import time, pickle
from app import app, db
from game import *
from flask import request, render_template, jsonify, session


global_dict = {}
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/api/play_the_game', methods=['POST', 'GET'])
def play_the_game():
    # get the move from front-end
    resp = request.get_json()
    uId = str(resp['uId'])
    direction = resp['direction']
    # loads the board from session
    b = pickle.loads(session['uId'])

    # moves with the board
    board = b.x
    moved = b.process_move(direction)
    legit = b.next_step_check()
    c_score = b.c_score

    # if game is on
    if legit:
        if moved and b.count_zeroes() != 0:
            b.add_number()
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict

        # why this 2 exists??
        elif moved:
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict

        # cant move
        else:
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict

    # game is over
    game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": True}
    game_dict = jsonify(game_data)
    return game_dict


@app.route('/api/games')
def games():
    return str(global_dict)


@app.route('/api/new_game')
def new_game():
    b = Game()
    uId = str(time.time())
    b.add_number()
    board = b.x
    c_score = b.c_score
    game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over" : False}
    game_dict = jsonify(game_data)
    session['uId'] = pickle.dumps(b)
    return game_dict


# @app.route('/save_user_highscore', methods=['POST']) #curl -X POST -F 'u_name=Try_1' -F 'c_score=1500' 127.0.0.1:5000/save_user_highscore
# def save_user_highscore():
#     u_name = request.form.get('u_name')
#     c_score = request.form.get('c_score')
#     db.save_to_db(u_name, c_score)
#     return print(c_score, u_name)

@app.route('/save_user_highscore', methods=['POST', 'GET']) #curl -H 'Content-Type: application/json' -X GET 127.0.0.1:5000/save_user_highscore -d '{"u_name": "test_1", "c_score": 1000}'
def save_user_highscore():
    resp = request.get_json()
    u_name = resp['u_name']
    c_score = resp['c_score']
    db.save_to_db(u_name, c_score)
    msg = "Saved!"
    return msg
