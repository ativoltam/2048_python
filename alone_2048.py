import time
from app import app
from game import *
from flask import request, render_template, jsonify


global_dict = {}
@app.route("/")
def main():
    new_game()
    return render_template('index.html')


@app.route('/api/play_the_game')
def play_the_game():
    resp = request.get_json()
    uId = str(resp['uId'])
    direction = resp['direction']
    b = global_dict[uId]
    board = b.x
    moved = b.process_move(direction)
    h_score = b.h_score
    game_data = {"board": board, "h_score": h_score, "uId": uId}
    game_dict = jsonify(game_data)
    if moved:
        b.add_number()
        game_data = {"board": board, "h_score": h_score, "uId": uId}
        game_dict = jsonify(game_data)
        return game_dict
    return game_dict


@app.route('/api/games')
def games():
    return str(global_dict)


@app.route('/api/new_game')
def new_game():
    b = Game()
    uId = str(time.time())
    global_dict[uId] = b
    b.add_number()
    board = b.x
    h_score = b.h_score
    game_data = {"board": board, "h_score": h_score, "uId": uId}
    game_dict = jsonify(game_data)
    return game_dict


@app.route('/save_user_highscore', methods=['POST']) #curl -X POST -F 'u_name=Try_1' -F 'h_score=1500' 127.0.0.1:5000/save_user_highscore
def save_user_highscore():
    name = request.form.get('u_name')
    best_score = request.form.get('h_score')
    print(best_score)
    print(name)
    #save to db // SQLITE3
