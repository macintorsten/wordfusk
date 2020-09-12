#!/bin/python3
import bisect
import random
import string

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

WORDLIST = []
ALFABET = string.ascii_uppercase + "ÅÄÖ"
FOUND = []

with open("ss100_utf8.txt") as wl:
    WORDLIST = sorted([word.strip().upper() for word in wl.readlines()])

def random_plan():
    frequent_letters = "AAAAAAAAEEEEEEEETTTTTTTNNNNNNNRRRRRRSSSSS" + \
                       "IIIIDDDDLLLLOOOOMMMMGGGKKKHHHÄÄUUFFCÅPÖB"
    alfabet = ALFABET + frequent_letters
    plan = []

    for _ in range(4):
        rad = [random.choice(alfabet) for _ in range(4)]
        plan.append(rad)

    return plan

def all_moves(x_pos, y_pos):
    y_lo = 0 if y_pos == 0 else y_pos - 1
    x_lo = 0 if x_pos == 0 else x_pos - 1
    y_hi = 3 if y_pos == 3 else y_pos + 1
    x_hi = 3 if x_pos == 3 else x_pos + 1

    all = []
    for y in range(y_lo, y_hi+1):
        for x in range(x_lo, x_hi+1):
            all.append((x, y))
    return all

def possible_next(moves):
    next_moves = []
    cur_x, cur_y = moves[-1]
    for potential_next in all_moves(cur_x, cur_y):
        if potential_next not in moves:
            next_moves.append(potential_next)
    return next_moves

def extend_moves(moves):
    more_moves = []
    for new_move in possible_next(moves):
        longer_move = moves.copy()
        longer_move.append(new_move)
        more_moves.append(longer_move)
    return more_moves

def word(plan, move):
    w = ""
    for x, y in move:
        w += plan[x][y]
    return w

def print_move(move, plan):
    size=len(plan[0])
    print("+-" + size * 2 * "-" + "+")
    for x, row in enumerate(plan):
        print("| ", end='')
        for y, letter in enumerate(row):
            if (x, y) in move:
                if move[0] == (x,y):
                    print(color.RED + color.BOLD + letter + color.END + " ", end='')
                else:
                    print(color.CYAN + letter + color.END + " ", end='')
            else:
                print(letter + " ", end='')
        print("|")
    print("+-" + size * 2 * "-" + "+")

def print_plan(plan):
    print_move([], plan)
    return

def dead_end(potential_word, wordlist):
    index = bisect.bisect_left(wordlist, potential_word)
    return not wordlist[index].startswith(potential_word)

def find_moar(plan, moves, wl, minlength=1):
    for mov in extend_moves(moves):
        potential_word = word(plan, mov)
        if potential_word in wl and potential_word not in FOUND:
            FOUND.append(potential_word)
            if len(mov) >= minlength:
                print(potential_word)
                print_move(mov, plan)
                print()
        elif dead_end(potential_word, wl):
            continue
        find_moar(plan, mov, wl, minlength)

def read_plan():
    letters = []
    while True:
        inp = input()
        new = list(filter(lambda c: c in ALFABET, inp.upper()))
        letters += new
        if len(letters) >= 16:
            break
    plan = []
    for i in range(0, 16, 4):
        plan.append(letters[i:i+4])
    return plan

def main():
    print("Ange spelplan (4 bokstäver per rad):")
    plan = read_plan()
    wl = WORDLIST
    minlength=6
    for x in range(4):
        for y in range(4):
            moves = [(x,y)]
            find_moar(plan, moves, wl, minlength)
    wordcount = len([w for w in FOUND if len(w) >= minlength])
    print("Hittade {} ord. {} ord var kortare än {} bokstäver".format(wordcount, len(FOUND)-wordcount, minlength))


if __name__ == "__main__":
    main()
