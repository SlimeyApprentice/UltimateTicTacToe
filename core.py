#!/usr/bin/python3

import os


WINDEX = {"O": ["+---+", "|   |", "|   |", "|   |", "+---+"],
          "X": ["\   /", " \ / ", "  *  ", " / \\ ", "/   \\"],
          "#": ["\---/", "|\ /|", "| * |", "|/ \|", "/---\\"]}


def wild_line(a, b, c):
    if " " in [a, b, c]:
        return False, ''
    if a == b == c:
        return True, a
    if a == '#' and b == c:
        return True, b
    if b == '#' and a == c:
        return True, a
    if c == '#' and a == b:
        return True, a
    if a == b == '#':
        return True, c
    if a == c == '#':
        return True, b
    if b == c == '#':
        return True, a
    return False, ''


def check_board(state):
    winner = " "
    judgement = False
    verdict, line = wild_line(state[0], state[1], state[2])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[3], state[4], state[5])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[6], state[7], state[8])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[0], state[3], state[6])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[1], state[4], state[7])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[2], state[5], state[8])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[0], state[4], state[8])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    verdict, line = wild_line(state[2], state[4], state[6])
    if verdict and winner == " ":
        winner = line
    if verdict and judgement and line != winner:
        return True, "#"
    judgement = judgement or verdict
    if not judgement:
        if " " not in state:
            return True, "#"
        return False, -1
    return judgement, winner


# test0 = [" "]*9
# test1 = ["X", "X", "X"] + [" "]*6
# test2 = [" "]*3 + ["O", "O", "O"] + [" "]*3
# test3 = ["X", "X", "X", "O", "O", "O"] + [" "]*3
# test4 = ["#", "X", "X"] + [" "]*6
# test5 = ["#", " ", " ", " ", "#", " ", " ", " ", "X"]
#
# print([test0, test1, test2, test3, test4, test5])
# print([check_board(k) for k in [test0, test1, test2, test3, test4, test5]])


class MiniBoard:
    def __init__(self):
        self.__state = [" "]*9
        self.__winner = " "

    def play(self, position, player):
        if self.__state[position] != " ":
            return -1, " "
        self.__state[position] = player
        flag, state = check_board(self.__state)
        if flag:
            self.__winner = state
            return 1, state
        return 0, " "

    def render(self, line, is_host):
        cap1 = ""
        cap2 = ""
        if is_host:
            cap1 = "\033[5;7m"
            cap2 = "\033[0m"
        if self.__winner != " ":
            return WINDEX[self.__winner][line]
        if line % 2 == 0:
            true_line = line // 2
            return cap1+"│".join([self.__state[true_line*3 + k] for k in range(3)])+cap2
        return cap1+"─┼─┼─"+cap2

    def winner(self):
        return self.__winner

    def is_open(self):
        return self.__winner == " "


class Board:
    def __init__(self):
        self.__state = [MiniBoard() for _ in range(9)]
        self.__winner = " "

    def play(self, grid, location, player):
        code, state = self.__state[grid].play(location, player)
        if code == -1:
            return -1, " "
        if code == 1:
            flag, winner = check_board([k.winner() for k in self.__state])
            print([k.winner() for k in self.__state], flag, winner)
            if flag:
                return 1, winner
            return 0, " "
        return 0, " "

    def render(self, host):
        cap1 = ""
        cap2 = ""
        if host == -1:
            cap1 = "\033[5;7m"
            cap2 = "\033[0m"
        print(cap1+"       │       │       "+cap2)
        for i in range(5):
            print(cap1+" "+self.__state[0].render(i, host == 0)+" │ "+self.__state[1].render(i, host == 1)+" │ " +
                  self.__state[2].render(i, host == 2)+" "+cap2)
        print(cap1+"       │       │       "+cap2)
        print(cap1+"───────┼───────┼───────"+cap2)
        print(cap1+"       │       │       "+cap2)
        for i in range(5):
            print(cap1+" "+self.__state[3].render(i, host == 3)+" │ "+self.__state[4].render(i, host == 4)+" │ " +
                  self.__state[5].render(i, host == 5)+" "+cap2)
        print(cap1+"       │       │       "+cap2)
        print(cap1+"───────┼───────┼───────"+cap2)
        print(cap1+"       │       │       "+cap2)
        for i in range(5):
            print(cap1+" "+self.__state[6].render(i, host == 6)+" │ "+self.__state[7].render(i, host == 7)+" │ " +
                  self.__state[8].render(i, host == 8)+" "+cap2)
        print(cap1+"       │       │       "+cap2)

    def check_open(self, grid):
        return self.__state[grid].is_open()


def main():
    board = Board()
    host = -1
    running = True
    player = "X"
    flag = 0
    winner = '#'
    report = ""
    while running:
        os.system("clear")
        board.render(host)
        if flag == -1:
            print("that's not a valid move:", report)
        elif flag == 1:
            print(winner, "WINS!")
            running = False
            continue
        print(player, "to play")
        if host >= 0:
            print("host x:", (host % 3) + 1, "y: ", (host // 3) + 1)
        else:
            print("specify host")
        action = input("\n\n>")
        try:
            action = int(action)-1
        except ValueError:
            flag = -1
            report = "input not an integer"
            continue
        if action > 9:
            flag = -1
            report = "input greater than 9"
            continue
        if host == -1:
            if board.check_open(action):
                host = action
            else:
                flag = -1
                report = "space is occupied"
            continue
        flag, winner = board.play(host, action, player)
        if flag == -1:
            report = "space is occupied"
        if flag == 0:
            player = {"X": "O", "O": "X"}[player]
            if board.check_open(action):
                host = action
            else:
                host = -1


if __name__ == "__main__":
    main()
# +---+
# |   |
# |   |
# |   |
# +---+
#
# \   /
#  \ /
#   *
#  / \
# /   \
