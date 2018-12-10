import classes as c
import corefunctions as cf
import time
from collections import deque

startingcash = 5000

hands = 0


go = True


players = []
numberplayers = 5
game_deck = cf.get_deck()

for x in range(numberplayers):
    hand1 = cf.make_hand(game_deck)
    player = c.Player(hand1, startingcash, ("Player" + str(x + 1)), True)
    players.append(player)

hand = cf.make_hand(game_deck)
main_player = c.Player(hand, startingcash, "Theo", False)

middle = c.Middle(game_deck)

game = c.Game(players, middle, game_deck, numberplayers, main_player)
game.test_deck()

check = game.game()

# game.middle.get_string()
game.middle.get_string()
game.print_hands()

print (check.name)
print (check.temphandvalue.get_win())
print ("{} won and now has ${}".format(check.name, check.cash))
