#!/usr/bin/env python
import argparse
import random
import sys

import requests

import game


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', default='http://localhost:5000', help='2048 API URL')
    args = parser.parse_args(sys.argv[1:])

    session = Session(args.baseurl)
    resp = session.get('/api/new_game').json()
    uid = resp['uId']
    game_ = Game(resp['board'], resp['c_score'])

    while not resp.get('game_over'):
        payload = {'uId': uid, 'direction': get_next_move(game_)}
        resp = session.post('/api/play_the_game', json=payload).json()
        game_ = Game(resp['board'], resp['c_score'])

    print('Game over. Score: {}'.format(resp['c_score']))


def get_next_move(game):
    return random.choice("wasd")


class Game(game.Game):
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
