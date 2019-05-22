#!/usr/bin/env python
import argparse
import copy
import datetime
import logging
import multiprocessing
import random
import sys

import requests

import game


log = logging.getLogger('client')
logging.getLogger('urllib3').setLevel(logging.WARNING)  # silence pesky connection dropped

MOVES = dict(zip('wasd', ('UP', 'LEFT', 'DOWN', 'RIGHT')))
CPU_COUNT = multiprocessing.cpu_count()
SAMPLE_WIDTH = 10
SAMPLE_DEPTH = 10


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--team', help='Team name to use (implies running in prod)')
    parser.add_argument('--debug', action='store_true', help='Show game state before move (slows performance)')
    args = parser.parse_args(argv or sys.argv[1:])
    logging.basicConfig(
        format='[%(asctime)s.%(msecs)03d] %(levelname)4.4s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if args.debug else logging.INFO)

    baseurl = 'https://thegame-2048.herokuapp.com' if args.team else 'http://localhost:5000'
    log.info('Running against %s', baseurl)
    session = Session(baseurl)
    if args.team:
        # prod endpoint (requires team_name) is incompatible with local one
        resp = session.post('/api/new_game', json={'team_name': args.team}).json()
    else:
        resp = session.get('/api/new_game').json()
    uid = resp['uId']
    game_ = Game(resp['board'], resp['c_score'])

    start_time = datetime.datetime.utcnow()
    move_count = 0
    while not resp.get('game_over'):
        log.debug(game_)
        move_count += 1
        direction = get_next_move(game_)
        log.debug('Move %s: %s', move_count, MOVES[direction])
        payload = {'uId': uid, 'direction': direction}
        resp = session.post('/api/play_the_game', json=payload).json()
        game_ = Game(resp['board'], resp['c_score'])
    game_time = (datetime.datetime.utcnow() - start_time).total_seconds()
    log.info('Game over. %s points in %s seconds (%s pts/s)', resp['c_score'], game_time, resp['c_score'] / game_time)
    log.info('Final game state:\n%s', game_)


def get_next_move(game):
    valid_moves = game._valid_moves  # cache
    if not valid_moves:
        return 'w'  # up as in "give up" - no more moves
    pool = multiprocessing.Pool(CPU_COUNT)
    pool_inputs = [(game, move) for move in valid_moves] * SAMPLE_WIDTH
    results = pool.map(generate_start_move_score, pool_inputs)
    move_scores = {}
    for move, score in results:
        move_scores.setdefault(move, 0)
        move_scores[move] += score
    return max(move_scores, key=lambda move: move_scores[move])


def generate_start_move_score(args):
    game, start_move = args
    game = copy.deepcopy(game)
    game.process_move(start_move)
    game.add_number()
    valid_moves = game._valid_moves
    step = 0
    while step < SAMPLE_DEPTH and valid_moves:
        game.process_move(random.choice(valid_moves))
        game.add_number()
        step += 1
        valid_moves = game._valid_moves
    return start_move, game.c_score


class Game(game.Game):
    @property
    def _valid_moves(self):
        return [d for d in 'wasd' if copy.deepcopy(self).process_move(d)]

    @property
    def _empty_cells(self):
        return sum(cell == 0 for row in self.x for cell in row)

    def __repr__(self):
        header = 'Game(c_score={})'.format(self.c_score)
        cells = [str(cell).rjust(4) for row in self.x for cell in row]
        rows = [','.join(str(cell).rjust(4) for cell in row) for row in self.x]
        return '\n'.join([header] + rows)


class Session(requests.Session):
    def __init__(self, baseurl):
        super().__init__()
        self.baseurl = baseurl

    def request(self, method, url, **kwargs):
        return super().request(method, self.baseurl + url, **kwargs)


if __name__ == '__main__':
    main()
