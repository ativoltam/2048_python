from random import randint
import random


class Game:

    x = [[0 for c in range(4)] for r in range(4)]

    c_score = 0

    copy_board = []

    def __init__(self):
        self.x = self.new_board()
        self.c_score = self.c_score
        self.copy_board = self.copy_board

    def print_inline(self, s):
        print(s, end='')

    def count_zeroes(self):
        return sum([sum([1 for c in r if c == 0]) for r in self.x])

    def max_value(self):
        return max([max(r) for r in self.x])

    def add_number(self):
        list_of_num = [2, 2, 2, 2, 4]
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

    def gravity_copy(self):
        changed = False
        for i in range(0, 4):
            for j in range(0, 4):
                k = i
                while k < 4 and self.copy_board[k][j] == 0: k += 1
                if k != i and k < 4:
                    self.copy_board[i][j], self.copy_board[k][j] = self.copy_board[k][j], 0
                    changed = True
        return changed

    def sum_up_copy(self):
        changed = False
        for i in range(0, 3):
            for j in range(0, 4):
                if self.copy_board[i][j] != 0 and self.copy_board[i][j] == self.copy_board[i + 1][j]:
                    self.copy_board[i][j] = 2 * self.copy_board[i][j]
                    self.copy_board[i + 1][j] = 0
                    changed = True
        return changed

    def sum_up(self):
        changed = False
        for i in range(0, 3):
            for j in range(0, 4):
                if self.x[i][j] != 0 and self.x[i][j] == self.x[i + 1][j]:
                    self.x[i][j] = 2 * self.x[i][j]
                    self.c_score = self.c_score + self.x[i][j]
                    self.x[i + 1][j] = 0
                    changed = True
        return changed

    def process_move(self, c):
        moves = "wasd"  # up, left, down, right
        for i in range(len(moves)):
            if moves[i] == c:
                self.rotate(i)
                changed = any([self.gravity(), self.sum_up(), self.gravity()])
                self.rotate(4 - i)
                self.copy_board = [row[:] for row in self.x]
                return changed
        return False

    def rotate(self, n):  # rotate 90 degrees n times
        for i in range(0, n):
            y = [row[:] for row in self.x]  # clone x
            for i in range(0, 4):
                for j in range(0, 4):
                    self.x[i][3 - j] = y[j][i]

    def rotate_copy(self, n):  # rotate 90 degrees n times
        for i in range(0, n):
            y = [row[:] for row in self.copy_board]  # clone x
            for i in range(0, 4):
                for j in range(0, 4):
                    self.copy_board[i][3 - j] = y[j][i]

    def process_move_copy(self, c):
        moves = "wasd"  # up, left, down, right
        for i in range(len(moves)):
            if moves[i] == c:
                self.rotate_copy(i)
                changed = any([self.gravity_copy(), self.sum_up_copy(), self.gravity_copy()])
                self.rotate_copy(4 - i)
                #self.copy_board = [row[:] for row in self.x]
                return changed
        return False

    def next_step_check(self):
        changed = any([self.process_move_copy("w"), self.process_move_copy("a"), self.process_move_copy("s"),
                       self.process_move_copy("d")])
        return changed

    def new_board(self):
        self.x = [[0 for c in range(4)] for r in range(4)]
        self.copy_board = self.x
        self.add_number()
        return self.x