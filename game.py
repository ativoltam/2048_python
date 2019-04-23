from random import randint
import random


class Game:
    x = [[0 for c in range(4)] for r in range(4)]

    def __init__(self):
        self.x = self.new_board()

    def print_inline(self, s):
        print(s, end='')

    def count_zeroes(self):
        return sum([sum([1 for c in r if c == 0]) for r in self.x])

    def max_value(self):
        return max([max(r) for r in self.x])

    def add_number(self):
        list_of_num = [2, 4]
        num = random.choice(list_of_num)
        if self.count_zeroes() > 0:
            pos = randint(0, self.count_zeroes() - 1)
            for i in range(0, 4):
                for j in range(0, 4):
                    if self.x[i][j] == 0:
                        if pos == 0: self.x[i][j] = num
                        pos -= 1

    def gravity(self):
        changed = False
        for i in range(0, 4):
            for j in range(0, 4):
                k = i
                while k < 4 and self.x[k][j] == 0: k += 1
                if k != i and k < 4:
                    self.x[i][j], self.x[k][j] = self.x[k][j], 0
                    changed = True
        return changed

    def sum_up(self):
        changed = False
        for i in range(0, 3):
            for j in range(0, 4):
                if self.x[i][j] != 0 and self.x[i][j] == self.x[i + 1][j]:
                    self.x[i][j] = 2 * self.x[i][j]
                    self.x[i + 1][j] = 0
                    changed = True
        return changed

    def process_move(self, c):
        print(self.x, '++')
        moves = "wasd"  # up, left, down, right
        for i in range(len(moves)):
            if moves[i] == c:
                self.rotate(i)
                changed = any([self.gravity(), self.sum_up(), self.gravity()])
                self.rotate(4 - i)
                print(self.x, '**')
                print(changed)
                return changed
        print(self.x, '--')
        return False

    def rotate(self, n):  # rotate 90 degrees n times
        for i in range(0, n):
            y = [row[:] for row in self.x]  # clone x
            for i in range(0, 4):
                for j in range(0, 4):
                    self.x[i][3 - j] = y[j][i]

    def new_board(self):
        global x
        self.x = [[0 for c in range(4)] for r in range(4)]
        self.add_number()
        return self.x
