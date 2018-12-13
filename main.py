import classes as c
import corefunctions as cf
import time
from collections import deque
import os
startingcash = 5000
"""
This is a program still in development. Please keep that in mind.
If you experience problems:
1) make sure you are running python3
2) make sure that you have all the correct modules installed, though that shouldn't matter
3) Run this file, not a different one
4) make sure you haven't edited the files
5) try redownloading this program
6) contact me if none of this works...
"""


hands = 0

def new(players1, mainplayer1, numberplayers):
    game_deck1 = cf.get_deck()
    middle1 = c.Middle(game_deck)

    game = c.Game(players1, middle1, game_deck1, numberplayers, mainplayer1)
    game.test_deck()

    check = game.game()
    game.middle.get_string()
    game.print_hands()
    try:
        print (check.name)
        print (check.temphandvalue.get_win())
        print ("{} won and now has ${}".format(check.name, check.cash))
        if check.ai:
            print("You lost and ended with ${} cash".format(game.main_player.cash))
    except:
        pass
    if input("Do you want to play again? ").lower() in ['yes', 'y', 'sure', 'yeet', 'yeah']:
        new(game.removedplayers, game.removedmainplayer, numberplayers)

go = True

os.system('clear')
players = []
numberplayers = 5
game_deck = cf.get_deck()

for x in range(numberplayers):
    hand1 = cf.make_hand(game_deck)
    player = c.Player(hand1, startingcash, ("Player" + str(x + 1)), True)
    players.append(player)

hand = cf.make_hand(game_deck)
main_player = c.Player(hand, startingcash, input("What is your name? \n>"), False)

middle = c.Middle(game_deck)

game = c.Game(players, middle, game_deck, numberplayers, main_player)
game.test_deck()

check = game.game()

# game.middle.get_string()
game.middle.get_string()
game.print_hands()
try:
    print (check.name)
    print (check.temphandvalue.get_win())
    print ("{} won and now has ${}".format(check.name, check.cash))
    if check.ai:
        print("You lost and ended with {} cash".format(game.main_player.cash))
except:
    pass

if input("Do you want to play again? ").lower() in ['yes', 'y', 'sure', 'yeet', 'yeah']:
    new(game.removedplayers, game.removedmainplayer, numberplayers)
