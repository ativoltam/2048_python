# CLI version of the 2048 game in python.
#
# - wasd for controls
# - Does not support windows
import time
from app import app
from game import *
from flask import request, redirect, url_for, json, render_template

global_dict = {}
@app.route("/")
def main(board=None):
    if board is None:
        b = Game()
        uId = time.time()
        global_dict[uId] = b
        b.add_number()
        return render_template('index.html', table=json.dumps(b.x))
    return render_template('index.html', table=json.dumps(board))


@app.route('/play_the_game')
def play_the_game():
    resp = request.get_json()
    uId = resp['uId']
    direction = resp['direction']
    board = global_dict[uId]
    moved = board.process_move(direction)
    if moved: board.add_number()
    return json.dumps(board.x)


# @app.route('/play_the_game/api/moves/<string:move>')
# def make_move(board, move):
#     if move == "up":
#         moved = board.process_move("w")
#         if moved: board.add_number()
#         return redirect(url_for('main'))
#     if move == "down":
#         moved = board.process_move("s")
#         if moved: board.add_number()
#         return redirect(url_for('main'))
#     if move == "left":
#         moved = board.process_move("a")
#         if moved: board.add_number()
#         return redirect(url_for('main'))
#     if move == "right":
#         moved = board.process_move("d")
#         if moved: board.add_number()
#         return redirect(url_for('main'))
#     else:
#         return "Invalid move!"


@app.route('/play_the_game/api/new_game')
def new_game():
    board = Game()
    board.new_board()
    board.add_number()
    return json.dumps(board.x)
