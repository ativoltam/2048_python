# CLI version of the 2048 game in python.
#
# - wasd for controls
# - Does not support windows
import time
from app import app
from game import *
from flask import request, redirect, url_for, json, render_template

global_list = []
@app.route("/")
def main(board=None):
    if board is None:
        b = Game()
        uid = time.time()
        local_dict = {uid: b.x}
        global_list.append(local_dict)
        b.add_number()
        return render_template('index.html', table=json.dumps(b.x))
    return render_template('index.html', table=json.dumps(board))


@app.route('/play_the_game', methods=['GET', 'POST'])
def play_the_game():
    resp = request.get_json()
    sessionId = resp['sessionId']
    direction = resp['direction']
    game = global_list['sessionId']
    table = game.move(direction)
    return table
    direction_forward = request.form.get('w')
    direction_backward = request.form.get('s')
    direction_left = request.form.get('a')
    direction_right = request.form.get('d')
    if direction_forward is not None:
        moved = board.process_move(direction_forward)
        if moved: board.add_number()
        return redirect(url_for('main'))
    if direction_backward is not None:
        moved = board.process_move(direction_backward)
        if moved: board.add_number()
        return redirect(url_for('main'))
    if direction_left is not None:
        moved = board.process_move(direction_left)
        if moved: board.add_number()
        return redirect(url_for('main'))
    if direction_right is not None:
        moved = board.process_move(direction_right)
        if moved: board.add_number()
        return redirect(url_for('main'))


@app.route('/play_the_game/api/moves/<string:move>')
def make_move(board, move):
    if move == "up":
        moved = board.process_move("w")
        if moved: board.add_number()
        return redirect(url_for('main'))
    if move == "down":
        moved = board.process_move("s")
        if moved: board.add_number()
        return redirect(url_for('main'))
    if move == "left":
        moved = board.process_move("a")
        if moved: board.add_number()
        return redirect(url_for('main'))
    if move == "right":
        moved = board.process_move("d")
        if moved: board.add_number()
        return redirect(url_for('main'))
    else:
        return "Invalid move!"


@app.route('/play_the_game/api/new_game')
def new_game():
    board = Game()
    board.new_board()
    board.add_number()
    return redirect(url_for('main'))
