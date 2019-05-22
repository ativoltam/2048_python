#!/usr/bin/env python
import argparse
import copy
import random
import sys

import requests

import game


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', default='http://localhost:5000', help='2048 API URL')
    parser.add_argument('--team', help='Team name to use')
    parser.add_argument('--debug', action='store_true', help='Show game state before move')
    args = parser.parse_args(sys.argv[1:])

    session = Session(args.baseurl)
    resp = session.post('/api/new_game', json={'team_name': args.team}).json()
    uid = resp['uId']
    game_ = Game(resp['board'], resp['c_score'])

    move_count = 0
    while not resp.get('game_over'):
        if args.debug:
            print(game_)
        move_count += 1
        direction = get_next_move(game_)
        print('Move {}: {}'.format(move_count, direction))
        payload = {'uId': uid, 'direction': direction}
        resp = session.post('/api/play_the_game', json=payload).json()
        game_ = Game(resp['board'], resp['c_score'])

    print('Game over. Score: {}'.format(resp['c_score']))


def get_next_move(game):
    return random.choice("wasd")


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
