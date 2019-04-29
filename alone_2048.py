import time, pickle
from app import app, db
from game import *
from flask import request, render_template, jsonify, session


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/api/play_the_game', methods=['POST', 'GET'])
def play_the_game():
    resp = request.get_json()
    uId = str(resp['uId'])
    direction = resp['direction']
    b = pickle.loads(session['uId'])  # Itt a b az maga egy Game object, amit a sessionben tárolt uId alapján hívunk meg
    board = b.x  # Maga a board (16 db szám) -- A b Game object x paramétere. (mátrix)
    moved = b.process_move(direction)  # A játék (b) process_move függvényének a visszatérési értéke (boolean)
    legit = b.next_step_check()  # A játék (b) next_step_check függvényének a visszatérési értéke (boolean)
    c_score = b.c_score  # A játék (b) c_score (mint current score) változója
    if legit:
        if moved and b.count_zeroes() != 0:
            b.add_number()
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict
        elif moved:
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict
        else:
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            session['uId'] = pickle.dumps(b)
            return game_dict
    game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": True}
    game_dict = jsonify(game_data)
    return game_dict


@app.route('/api/new_game')
def new_game():
    b = Game()  # Egy új Game object.
    uId = str(time.time())
    b.add_number()  # A játék (b) add_number metódusa meghívása, amivel elhelyez 2 random tile-t a board-on.
    board = b.x  # Maga a board (16 db szám) -- A b Game object x paramétere. (mátrix)
    c_score = b.c_score  # A játék (b) c_score (mint current score) változója
    game_data = {"board": board, "c_score": c_score, "uId": uId}
    game_dict = jsonify(game_data)
    session['uId'] = pickle.dumps(b)
    return game_dict


@app.route('/save_user_highscore', methods=['POST', 'GET']) #curl -H 'Content-Type: application/json' -X GET 127.0.0.1:5000/save_user_highscore -d '{"u_name": "test_1", "c_score": 1000}'
def save_user_highscore():
    resp = request.get_json()
    u_name = resp['u_name']  # User name rövidítése, front-end-en user adja meg, ezzel mentjük el az adatbázisba
    c_score = resp['c_score']  # Current score, front-end-en user adja meg, ezzel mentjük el az adatbázisba
    db.save_to_db(u_name, c_score)
    msg = "Saved!"
    return msg
