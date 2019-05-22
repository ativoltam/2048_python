#!/usr/bin/env python
import argparse
import copy
import logging
import random
import sys

import requests

import game


log = logging.getLogger('2048-client')

MOVES = dict(zip('wasd', ('UP', 'LEFT', 'DOWN', 'RIGHT')))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', default='http://localhost:5000', help='2048 API URL')
    parser.add_argument('--team', help='Team name to use')
    parser.add_argument('--debug', action='store_true', help='Show game state before move')
    args = parser.parse_args(sys.argv[1:])
    logging.basicConfig(
        format='[%(asctime)s.%(msecs)03d] %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if args.debug else None)

    session = Session(args.baseurl)
    if args.team:
        # running live - endpoint is incompatible with local tests
        resp = session.post('/api/new_game', json={'team_name': args.team}).json()
    else:
        resp = session.get('/api/new_game').json()
    uid = resp['uId']
    game_ = Game(resp['board'], resp['c_score'])

    move_count = 0
    while not resp.get('game_over'):
        log.debug(game_)
        move_count += 1
        direction = get_next_move(game_)
        log.debug('Move %s: %s', move_count, MOVES[direction])
        payload = {'uId': uid, 'direction': direction}
        resp = session.post('/api/play_the_game', json=payload).json()
        game_ = Game(resp['board'], resp['c_score'])

    log.info('Game over. Score: %s', resp['c_score'])


def get_next_move(game):
    move_scores = {d: [] for d in game._valid_moves}
    if not move_scores:
        return 'w'  # Up as in "give up" - no more moves
    for move, scores in move_scores.items():
        # log.debug('Evaluating %s', move)
        start_game = copy.deepcopy(game)
        start_game.process_move(move)
        sample_size = 10
        for i in range(sample_size):
            scores.append(random_play_score(start_game))
            # log.debug('%s / %s: score %s', i+1, sample_size, scores[-1])
    return max(move_scores, key=lambda move: sum(move_scores[move]))


def random_play_score(game, max_step=10):
    step = 0
    game = copy.deepcopy(game)
    valid_moves = game._valid_moves
    while step < max_step and valid_moves:
        game.process_move(random.choice(valid_moves))
        game.add_number()
        step += 1
        valid_moves = game._valid_moves
    return game.c_score


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
