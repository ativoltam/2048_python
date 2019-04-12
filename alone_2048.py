# CLI version of the 2048 game in python.
#
# - wasd for controls
# - Does not support windows
from random import randint
from flask import render_template
from app import app
from flask import jsonify, request


@app.route("/")
def main():
    return render_template('index.html', table=x)


def print_inline(s):
    print(s, end='')


def print_new_line():
    print('')


def count_zeroes():
    return sum([sum([1 for c in r if c == 0]) for r in x])


def max_value():
    return max([max(r) for r in x])


def print_board():
    with app.app_context():
        for i in range(0, 4):
            for j in range(0, 4):
                print_inline('{:5d}'.format(x[i][j])),
            print_new_line()
        print_new_line()
        return jsonify(x)


def add_number():
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
    print("invalid move")
    return False


def rotate(n):  # rotate 90 degrees n times
    for i in range(0, n):
        y = [row[:] for row in x]  # clone x
        for i in range(0, 4):
            for j in range(0, 4):
                x[i][3 - j] = y[j][i]


# Initialize board.
x = [[0 for c in range(4)] for r in range(4)]


@app.route('/play_the_game', methods=['GET', 'POST'])
def play_the_game():
    direction_forward = request.form.get('w')
    direction_backward = request.form.get('s')
    direction_left = request.form.get('a')
    direction_right = request.form.get('d')
    add_number()
    print_board()
    if direction_forward is not None:
        moved = process_move(direction_forward)
    if direction_backward is not None:
        moved = process_move(direction_backward)
    if direction_left is not None:
        moved = process_move(direction_left)
    if direction_right is not None:
        moved = process_move(direction_right)
    if moved: add_number()
    return jsonify(x)
