import random
import time
import classes as c
from os import system, name
import threading
import sys
import itertools
from collections import deque

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m' + '\033[37m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def get_deck():
    deck = c.Deck()
    deck.make_cards()
    deck.shuffle()
    return deck

def make_hand(deck):
    card1 = deck.draw_card()
    deck.add_card(card1)
    card2 = deck.draw_card()
    deck.add_card(card2)
    hand = c.Hand([card1, card2])
    return hand


def loading(timetotake):
    done = False
    #here is the animation
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(timetotake)
    done = True
    print("\n\n")

def game_crash(error):
    clear()
    loading(3)
    print("Your game crashed due to " + error)
    time.sleep(1)
    print("Please contact support!")
    loading(2)
    exit()
    sys.exit()

def ascii_version_of_card(*cards, return_string=True):

    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', color.RED + '♦' + color.END, color.RED + '♥'+ color.END, '♣']

    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        if card.cardsymbol[card.rank] == '10':
            rank = card.cardsymbol[card.rank]
            space = ''
        else:
            rank = card.cardsymbol[card.rank][0]
            space = ' '

        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]


        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))


    if return_string:
        return '\n'.join(result)
    else:
        return result
