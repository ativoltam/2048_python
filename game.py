from random import randint


class Game:
    x = [[0 for c in range(4)] for r in range(4)]

    def __init__(self):
        self.x = self.new_board()

    def print_inline(self, s):
        print(s, end='')

    def count_zeroes(self):
        return sum([sum([1 for c in r if c == 0]) for r in x])

    def max_value(self):
        return max([max(r) for r in x])

    def add_number(self):
        import random
        list_of_num = [2, 4]
        num = random.choice(list_of_num)
        if Game.count_zeroes(self) > 0:
            pos = randint(0, Game.count_zeroes(self) - 1)
            for i in range(0, 4):
                for j in range(0, 4):
                    if x[i][j] == 0:
                        if pos == 0: x[i][j] = num
                        pos -= 1

    def gravity(self):
        changed = False
        for i in range(0, 4):
            for j in range(0, 4):
                k = i
                while k < 4 and x[k][j] == 0: k += 1
                if k != i and k < 4:
                    x[i][j], x[k][j] = x[k][j], 0
                    changed = True
        return changed

    def sum_up(self):
        changed = False
        for i in range(0, 3):
            for j in range(0, 4):
                if x[i][j] != 0 and x[i][j] == x[i + 1][j]:
                    x[i][j] = 2 * x[i][j]
                    x[i + 1][j] = 0
                    changed = True
        return changed

    def process_move(self, c):
        moves = "wasd"  # up, left, down, right
        for i in range(len(moves)):
            if moves[i] == c:
                Game.rotate(self, i)
                changed = any([Game.gravity(self), Game.sum_up(self), Game.gravity(self)])
                Game.rotate(self, 4 - i)
                return changed
        return False

    def rotate(self, n):  # rotate 90 degrees n times
        for i in range(0, n):
            y = [row[:] for row in x]  # clone x
            for i in range(0, 4):
                for j in range(0, 4):
                    x[i][3 - j] = y[j][i]

    def new_board(self):
        global x
        x = [[0 for c in range(4)] for r in range(4)]
        return x
