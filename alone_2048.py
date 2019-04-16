# CLI version of the 2048 game in python.
#
# - wasd for controls
# - Does not support windows
from random import randint
from flask import render_template
from app import app
from flask import request, redirect, url_for, json


@app.route("/")
def main():
    if count_zeroes() == 16:
        add_number()
    return render_template('index.html', table=json.dumps(x))


def print_inline(s):
    print(s, end='')


def count_zeroes():
    return sum([sum([1 for c in r if c == 0]) for r in x])


def max_value():
    return max([max(r) for r in x])


def add_number():
    if count_zeroes() > 0:
        pos = randint(0, count_zeroes() - 1)
        for i in range(0, 4):
            for j in range(0, 4):
                if x[i][j] == 0:
                    if pos == 0: x[i][j] = 2
                    pos -= 1


def gravity():
    changed = False
    for i in range(0, 4):
        for j in range(0, 4):
            k = i
            while k < 4 and x[k][j] == 0: k += 1
            if k != i and k < 4:
                x[i][j], x[k][j] = x[k][j], 0
                changed = True
    return changed


def sum_up():
    changed = False
    for i in range(0, 3):
        for j in range(0, 4):
            if x[i][j] != 0 and x[i][j] == x[i + 1][j]:
                x[i][j] = 2 * x[i][j]
                x[i + 1][j] = 0
                changed = True
    return changed


def process_move(c):
    moves = "wasd"  # up, left, down, right
    for i in range(len(moves)):
        if moves[i] == c:
            rotate(i)
            changed = any([gravity(), sum_up(), gravity()])
            rotate(4 - i)
            return changed
    return False


def rotate(n):  # rotate 90 degrees n times
    for i in range(0, n):
        y = [row[:] for row in x]  # clone x
        for i in range(0, 4):
            for j in range(0, 4):
                x[i][3 - j] = y[j][i]


def new_board():
    global x
    x = [[0 for c in range(4)] for r in range(4)]


# Initialize board.
x = [[0 for c in range(4)] for r in range(4)]


@app.route('/play_the_game', methods=['GET', 'POST'])
def play_the_game():
    direction_forward = request.form.get('w')
    direction_backward = request.form.get('s')
    direction_left = request.form.get('a')
    direction_right = request.form.get('d')
    if direction_forward is not None:
        process_move(direction_forward)
        add_number()
        return redirect(url_for('main'))
    if direction_backward is not None:
        process_move(direction_backward)
        add_number()
        return redirect(url_for('main'))
    if direction_left is not None:
        process_move(direction_left)
        add_number()
        return redirect(url_for('main'))
    if direction_right is not None:
        process_move(direction_right)
        add_number()
        return redirect(url_for('main'))


@app.route('/play_the_game/api/moves/<string:move>')
def make_move(move):
    if move == "up":
        moved = process_move("w")
        if moved: add_number()
        return redirect(url_for('main'))
    if move == "down":
        moved = process_move("s")
        if moved: add_number()
        return redirect(url_for('main'))
    if move == "left":
        moved = process_move("a")
        if moved: add_number()
        return redirect(url_for('main'))
    if move == "right":
        moved = process_move("d")
        if moved: add_number()
        return redirect(url_for('main'))
    else:
        return "Invalid move!"


@app.route('/play_the_game/api/new_game')
def new_game():
    new_board()
    add_number()
    return redirect(url_for('main'))
