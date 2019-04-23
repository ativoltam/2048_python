import time
from app import app
from game import *
from flask import request, json, render_template


global_dict = {}
@app.route("/")
def main(board=None):
    if board is None:
        b = Game()
        uId = str(time.time())
        global_dict[uId] = b
        b.add_number()
        return render_template('index.html', table=json.dumps(b.x), uId=uId)
    else:
        return render_template('index.html', table=json.dumps(board))


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
    game_dict = json.dumps(game_data)
    if moved:
        b.add_number()
        game_data = {"board": board, "h_score": h_score, "uId": uId}
        game_dict = json.dumps(game_data)
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
    game_dict = json.dumps(game_data)
    return game_dict
