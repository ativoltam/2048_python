import time, pickle
from app import app, db
from app.models import Game_obj
from game import *
from flask import request, render_template, jsonify


# global_dict = {}
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/api/play_the_game', methods=['POST', 'GET'])
def play_the_game():
    resp = request.get_json()
    uId = str(resp['uId'])
    direction = resp['direction']
    z = Game_obj.query.filter_by(uId=uId).first()
    b = Game(board=z.board)
    board = b.x
    moved = b.process_move(direction)
    legit = b.next_step_check()
    c_score = b.c_score
    if legit:
        if moved and b.count_zeroes() != 0:
            b.add_number()
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            db.session.commit()
            return game_dict
        elif moved:
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            db.session.commit()
            return game_dict
        else:
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            db.session.commit()
            return game_dict
    game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": True}
    game_dict = jsonify(game_data)
    Game_obj.query.filter_by(uId=uId).update(dict(board=board))
    db.session.commit()
    return game_dict


# @app.route('/api/games')
# def games():
#     return str(global_dict)


@app.route('/api/new_game')
def new_game():
    b = Game(board=None)
    uId = str(time.time())
    b.add_number()
    board = b.x
    c_score = b.c_score
    game_obj = Game_obj(uId=uId, c_score=c_score, board=board)
    game_data = {"board": board, "c_score": c_score, "uId": uId}
    game_dict = jsonify(game_data)
    # global_dict[uId] = b
    # db.save_to_games_db(uId, pickle.dumps(b))
    db.session.add(game_obj)
    db.session.commit()
    return game_dict


@app.route('/save_user_highscore', methods=['POST', 'GET'])
def save_user_highscore():
    resp = request.get_json()
    u_name = resp['u_name']
    c_score = resp['c_score']
    db.save_to_scores_db(u_name, c_score)
    msg = "Saved!"
    return msg
