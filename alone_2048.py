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
    if moved:
        b.add_number()
        return json.dumps(board)
    return json.dumps(board)


@app.route('/api/games')
def games():
    return str(global_dict)


@app.route('/api/new_game')
def new_game():
    b = Game()
    uId = str(time.time())
    global_dict[uId] = b
    b.add_number()
    return uId, json.dumps(b.x)
