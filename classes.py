import random
import corefunctions as cf
import time
import hands as h
from collections import deque
import AI_hands as aih

class Card(object):
    cardsymbol = {
     'Ace': 'A',
     'Two': '2',
     'Three': '3',
     'Four': '4',
     'Five': '5',
     'Six': '6',
     'Seven':'7',
     'Eight': '8',
     'Nine': '9',
     'Ten': '10',
     'Jack': 'J',
     'Queen': 'Q',
     'King': 'K'
     }
    def __init__(self, s, r):
        self.suit = s
        self.rank = r
    def get_string(self):
        return(self.rank + " of " + self.suit)
    def get_card_value(self):
        values = {'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8, 'Nine' : 9, 'Ten' : 10, 'Jack' : 11, 'Queen' : 12, 'King' : 13, 'Ace' : 14}
        return values[self.rank]

class Deck(object):
    def __init__(self):
        self.deck = []
        self.cardnumbers = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        self.cardsuits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
    def make_cards(self):
        for x in self.cardsuits:
            for w in self.cardnumbers:
                self.deck.append(Card(x, w))
    def shuffle(self):
        random.shuffle(self.deck)
    def get_deck(self):
        final = []
        for x in self.deck:
            final.append(x)
        return final
    def get_deck_string(self):
        final = []
        for x in self.deck:
            w = x.get_string()
            final.append(w)
        return final
    def draw_card(self):
        final = self.deck.pop(len(self.deck) - 1)
        return final
    def add_card(self, card):
        self.deck.insert(0, card)


class Hand(object):
    def __init__(self, hand):
        self.hand = hand
    def get_string(self):
        final = []
        for x in self.hand:
            final.append(x.get_string())
        return final
    def get_highest_card(self):
        high_card = None
        for x in self.hand:
            w = x.get_card_value()
            if high_card != None:
                if high_card.get_card_value() < w:
                    high_card = x
            else:
                high_card = x
        return high_card
    def print_cards(self):
        card1 = self.hand[0]
        card2 = self.hand[1]
        print(cf.ascii_version_of_card(card1, card2))


class Middle(object):
    def __init__(self, deck):
        card1 = deck.draw_card()
        deck.add_card(card1)
        card2 = deck.draw_card()
        deck.add_card(card2)
        card3 = deck.draw_card()
        deck.add_card(card3)
        self.cards = [card1, card2, card3]
    def turn(self, deck):
        card4 = deck.draw_card()
        deck.add_card(card4)
        self.cards.append(card4)
    def river(self, deck):
        card5 = deck.draw_card()
        deck.add_card(card5)
        self.cards.append(card5)
    def get_string(self):
        if len(self.cards) == 3:
            card1 = self.cards[0]
            card2 = self.cards[1]
            card3 = self.cards[2]
            print (cf.ascii_version_of_card(card1, card2, card3))
        elif len(self.cards) == 4:
            card1 = self.cards[0]
            card2 = self.cards[1]
            card3 = self.cards[2]
            card4 = self.cards[3]
            print (cf.ascii_version_of_card(card1, card2, card3, card4))
        elif len(self.cards) == 5:
            card1 = self.cards[0]
            card2 = self.cards[1]
            card3 = self.cards[2]
            card4 = self.cards[3]
            card5 = self.cards[4]
            print (cf.ascii_version_of_card(card1, card2, card3, card4, card5))
        else:
            cf.game_crash("an error with card printing...")

    def get_string_normal(self):
        final = []
        for x in self.cards:
            final.append(x.get_string())
        return final

class Player(object):
    def __init__(self, hand, cash, name, ai):
        self.hand = hand
        self.cash = cash
        self.temphandvalue = None
        self.tempbetstate = True
        self.tempbetvalue = 0
        self.name = name
        self.ai = ai
        self.lastbetvalue = 0
    #Ai stuff
    def get_bet_hand(self, last_bet):
        bet_unit = 5
        bet = aih.get_hand_bet(h.Hands(self.hand.hand, []), bet_unit)
        if (last_bet - self.lastbetvalue) > 50 * bet_unit:
            if random.randrange(1, 10) < 7:
                return 'call'
        if bet < last_bet - 20:
            return 'fold'
        elif bet < last_bet:
            return 'call'
        elif bet in range((last_bet) - 10, (last_bet) + 10):
            return 'call'
        elif bet > ((last_bet - self.lastbetvalue) + 10):
            if (last_bet) + 20 < bet:
                return (last_bet - self.lastbetvalue) + (bet_unit * 4)
            else:
                return 'call'
    def get_bet_other(self, last_bet, middle):
        bet_unit = 5
        bet = aih.get_handmiddle_bet(self.hand, middle, bet_unit)
        if (last_bet - self.lastbetvalue) > 100 * bet_unit:
            if random.randrange(1, 10) < 7:
                return 'call'
        if bet < (last_bet) - 20:
            return 'fold'
        elif bet < (last_bet):
            return 'call'
        elif bet in range((last_bet) - 10, (last_bet) + 10):
            return 'call'
        elif bet > ((last_bet) + 10):
            if (last_bet) + 20 < bet:
                return (last_bet - self.lastbetvalue) + (bet_unit * 4)
            else:
                return 'call'
        else:
            return 'fold'


class Game(object):
    def __init__(self, players, middle, deck, playernumber, main_player):
        self.players = deque()
        for x in players:
            self.players.append(x)
        self.middle = middle
        self.deck = deck
        self.playernumber = playernumber
        self.main_player = main_player
        self.pot = 0
        if len(players) == playernumber:
            pass
        else:
            cf.game_crash("an error with player creation...")
    def get_tempbetting_value(self, allplayers):
        values = None
        for x in allplayers:
            if x.tempbetstate != 'fold':
                if x.tempbetstate == 'raise' or x.tempbetstate == 'call' or x.tempbetstate == True:
                    if values == None:
                        values = x.tempbetvalue
                    else:
                        if values != x.tempbetvalue:
                            return False
        if values == None:
            return True
        else:
            return values

    def test_deck(self):
        test = 'hi'
        try:
            self.deck.get_deck_string()
        except:
            cf.game_crash("an error in deck creation...")
    def check_for_winner(self):
        final = None
        players = self.players
        players.append(self.main_player)
        for x in players:
            if final == None:
                final = x
            else:
                if x.temphandvalue.hand_score > final.temphandvalue.hand_score:
                    final = x
                elif x.temphandvalue.hand_score == final.temphandvalue.hand_score:
                    if x.temphandvalue.tie_score > final.temphandvalue.tie_score:
                        final = x
        return final
    def print_hands(self):
        players = list(self.players)[:6]
        for x in players:
            print (x.name + ":")
            x.hand.print_cards()
            print ("\n\n")
    def Fold(self, player, last_bet):
        print(player.name + " folds at {}!".format((last_bet + player.lastbetvalue)))
        player.tempbetstate = 'fold'
        player.tempbetvalue = 0
        player.lastbetvalue = 0
        return last_bet
    def Raise(self, last_bet, player, bet):
        if player.lastbetvalue == None:
            print("none")
            handvalue = 0
        else:
            handvalue = player.lastbetvalue
        if bet > 0:
            if bet > (last_bet -handvalue):
                if (player.cash - bet) >= 0:
                    print(player.name + " bets " + str(bet))
                    self.pot += bet
                    player.cash -= bet
                    player.tempbetstate = 'raise'
                    player.tempbetvalue = bet
                    player.lastbetvalue = bet
                    return (bet + handvalue)
                else:
                    if player.cash > (last_bet - handvalue):
                        bet = (last_bet - handvalue) + 1
                        print(player.name + " bets " + str(bet))
                        self.pot += bet
                        player.cash -= bet
                        player.tempbetstate = 'raise'
                        player.tempbetvalue = bet
                        player.lastbetvalue = bet
                        return (bet + handvalue)
                    else:
                        return self.Fold(player, last_bet)
            else:
                if player.cash > (last_bet - handvalue):
                    bet = (last_bet - handvalue) + 1
                    print(player.name + " bets " + str(bet))
                    self.pot += bet
                    player.cash -= bet
                    player.tempbetstate = 'raise'
                    player.tempbetvalue = bet
                    player.lastbetvalue = bet
                    return (bet + handvalue)
                else:
                    return self.Fold(player, last_bet)
        else:
            return self.Fold(player, last_bet)
    def Call(self, last_bet, player):
        if player.lastbetvalue == None:
            print("none")
            handvalue = 0
        else:
            handvalue = player.lastbetvalue
        if (player.cash - (last_bet - handvalue)) > 0:
            print(player.name + " calls!")
            player.cash -= (last_bet - handvalue)
            self.pot += (last_bet - handvalue)
            player.tempbetstate = 'call'
            player.tempbetvalue = last_bet
            player.lastbetvalue = last_bet
            return last_bet
        else:
            return self.Fold(player, last_bet)
    def blind(self, player):
        blind = 5 #blind amount here
        player.cash -= blind
        player.tempbetstate = 'call'
        player.tempbetvalue = blind
        print(player.name + " gets a blind of " + str(blind))
        return blind
    def removeplayers(self):
        final = []
        for x in self.players:
            if x.tempbetstate != 'fold':
                x.tempbetstate = True
                x.tempbetvalue = 0
                final.append(x)
        if self.main_player.tempbetstate == 'fold':
            print("Because you folded you lose and can't finish the game!")
            exit()
        else:
            self.main_player.tempbetstate = True
            self.main_player.tempbetvalue = 0
        del self.players
        self.players = deque()
        for x in final:
            self.players.append(x)
    def betting(self, round, last_bet=None):
        allplayers = deque()
        for x in self.players:
            if x.tempbetstate != 'fold':
                allplayers.append(x)
        if self.main_player.tempbetstate != 'fold':
            allplayers.append(self.main_player)
        if round == 'hand':
            blind = random.randrange(0, len(allplayers))
            last_bet = self.blind(allplayers[blind - 1])
            allplayers.rotate(blind)
        allplayers = list(allplayers)
        if len(allplayers) == 1:
            allplayers[0].cash += self.pot
            print ("{} won and now has ${}".format(allplayers[0].name, allplayers[0].cash))
            exit()
        while not self.get_tempbetting_value(allplayers):
            for x in allplayers:
                if self.get_tempbetting_value(allplayers):
                    return self.get_tempbetting_value(allplayers)
                if x.tempbetstate != 'fold':
                    if x.ai:
                        if round == 'hand':
                            bet = x.get_bet_hand(last_bet)
                            if bet == 'fold':
                                last_bet = self.Fold(x, last_bet)
                            elif bet == 'call':
                                last_bet = self.Call(last_bet, x)
                            elif isinstance(bet, int):
                                last_bet = self.Raise(last_bet, x, bet)
                        else:
                            bet = x.get_bet_other(last_bet, self.middle)
                            if bet == 'fold':
                                last_bet = self.Fold(x, last_bet)
                            elif bet == 'call':
                                last_bet = self.Call(last_bet, x)
                            elif isinstance(bet, int):
                                last_bet = self.Raise(last_bet, x, bet)
                    elif not x.ai:
                        print("You have {} cash left".format(x.cash))
                        bettype = input("Would you like to Fold(1), Call(2), or Raise(3)? ")
                        if bettype in ['1', 1, 'fold', 'Fold', '!', 'one', 'ONE', 'One', 'FOLD']:
                            last_bet = self.Fold(x, last_bet)
                        elif bettype in ['2', 2, 'Two', 'two', 'TWO', 'Call', 'call', 'CALL', '@']:
                            last_bet = self.Call(last_bet, x)
                        elif bettype in ['3', 3, 'Three', 'three', 'THREE', 'Raise', 'raise', 'RAISE', '#']:
                            try:
                                print("You have {} cash left".format(x.cash))
                                bet = int(input("How much would you like to bet? "))
                            except:
                                last_bet = self.Fold(x, last_bet)
                            try:
                                last_bet = self.Raise(last_bet, x, bet)
                            except:
                                raise Exception("Your game has run into an issue with your input! Please contact support! ")
                        else:
                            raise Exception("There are 24 different things you can input! You got none of them! ")
        self.removeplayers()
        return last_bet

    def turn1(self, deck):
        print("Your hand: ")
        self.main_player.hand.print_cards()
        print ("\n\n")
        thing = self.betting('hand')
        print ("\n\n")
        time.sleep(1)
        return thing
    def turn2(self, deck, last_bet):
        print("Your hand: ")
        self.main_player.hand.print_cards()
        print ("\n\n")
        print("Here comes the flop!")
        print ("\n\n")
        self.middle.get_string()
        print ("\n\n")
        self.removeplayers()
        thing = self.betting('flop', last_bet)
        print ("\n\n")
        time.sleep(1)
        return thing
    def turn3(self, deck, last_bet):
        print("Your hand: ")
        self.main_player.hand.print_cards()
        print ("\n\n")
        print("Here comes the turn!")
        print ("\n\n")
        self.middle.turn(deck)
        self.middle.get_string()
        print ("\n\n")
        self.removeplayers()
        thing = self.betting('turn', last_bet)
        print ("\n\n")
        time.sleep(1)
        return thing
    def turn4(self, deck, last_bet):
        print("Your hand: ")
        self.main_player.hand.print_cards()
        print ("\n\n")
        print("Here comes the river!")
        print ("\n\n")
        self.middle.river(deck)
        self.middle.get_string()
        print ("\n\n")
        self.removeplayers()
        thing = self.betting('river', last_bet)
        print ("\n\n")
        time.sleep(1)
        return thing
    def final(self, deck):
        test = h.Hands(self.main_player.hand.hand, self.middle.cards)
        thing = h.checkforhand(test)
        if thing != False:
            self.main_player.temphandvalue = thing
        else:
            self.main_player.temphandvalue = h.HandValue(self.main_player.hand.get_highest_card().get_card_value(), 1)
        for x in self.players:
            hands1 = h.Hands(x.hand.hand, self.middle.cards)
            things1 = h.checkforhand(hands1)
            if things1 != False:
                x.temphandvalue = things1
            else:
                x.temphandvalue = h.HandValue(x.hand.get_highest_card().get_card_value(), 1)
        winner = self.check_for_winner()
        winner.cash += self.pot
        return winner
        time.sleep(1)
    def game(self):
        thing =self.turn1(self.deck)
        thing2 = self.turn2(self.deck, thing)
        thing3 = self.turn3(self.deck, thing2)
        self.turn4(self.deck, thing3)
        return self.final(self.deck)
