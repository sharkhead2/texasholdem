import corefunctions as cf
from collections import deque

class HandValue(object):
    def __init__(self, hand_score, tie_score):
        self.hand_score = hand_score
        self.tie_score = tie_score
    def get_win(self):
        if self.hand_score == 23:
            return "Royal Flush"
        elif self.hand_score == 22:
            return "Straight Flush"
        elif self.hand_score == 21:
            return "Four of a Kind"
        elif self.hand_score == 20:
            return "Full House"
        elif self.hand_score == 19:
            return "Flush"
        elif self.hand_score == 18:
            return "Straight"
        elif self.hand_score == 17:
            return "Three of a Kind"
        elif self.hand_score == 16:
            return "Two Pair"
        elif self.hand_score == 15:
            return "Pair"
        else:
            return "High Card"


class Hands(object):
    def check_suits(self, cards):
        final = None
        thing = None
        for x in cards:
            w = x.suit
            if thing == None:
                thing = w
            elif w != thing:
                final = False
        if final != False:
            final = True
        return final
    def split_ranks(self):
        final = []
        for x in self.cards:
            final.append(x.rank)
        self.ranks = final
    def __init__(self, player_cards, other_cards):
        self.cards = player_cards + other_cards
        self.samesuit = None
        self.ranks = []
        self.samesuit = self.check_suits(self.cards)
        self.split_ranks()
    def get_string(self):
        final = []
        for x in self.cards:
            final.append(x.get_string())
        return final
    def get_dupes(self, a):
        seen = {}
        dupes = []
        for x in a:
            if x not in seen:
                seen[x] = 1
            else:
                dupes.append(x)
                seen[x] += 1
        return seen

def get_cardrank_value(cardrank):
    values = {'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8, 'Nine' : 9, 'Ten' : 10, 'Jack' : 11, 'Queen' : 12, 'King' : 13, 'Ace' : 14}
    return values[cardrank]
def suit_to_number(suit):
    if suit == "Spades":
        return 3
    elif suit == 'Hearts':
        return 2
    elif suit == 'Diamonds':
        return 1
    elif suit == 'Clubs':
        return 0

def checkforroyalflush(hands):
    if 'Ace' in hands.ranks and 'King' in hands.ranks and 'Queen' in hands.ranks and 'Jack' in hands.ranks and 'Ten' in hands.ranks:
        check_cards_hearts = []
        check_cards_ranks_hearts = []
        check_cards_spades = []
        check_cards_ranks_spades = []
        check_cards_clubs = []
        check_cards_ranks_clubs = []
        check_cards_diamonds = []
        check_cards_ranks_diamonds = []
        for x in hands.cards:
            if x.rank == 'Ace' or x.rank == 'King' or x.rank == 'Queen' or x.rank == 'Jack' or x.rank == 'Ten':
                if x.suit == 'Clubs':
                    if x.rank in check_cards_ranks_clubs:
                        pass
                    else:
                        check_cards_clubs.append(x)
                        check_cards_ranks_clubs.append(x.rank)
                elif x.suit == 'Hearts':
                    if x.rank in check_cards_ranks_hearts:
                        pass
                    else:
                        check_cards_hearts.append(x)
                        check_cards_ranks_hearts.append(x.rank)
                elif x.suit == 'Spades':
                    if x.rank in check_cards_ranks_spades:
                        pass
                    else:
                        check_cards_ranks_spades.append(x)
                        check_cards_ranks_spades.append(x.rank)
                elif x.suit == 'Diamonds':
                    if x.rank in check_cards_ranks_diamonds:
                        pass
                    else:
                        check_cards_diamonds.append(x)
                        check_cards_ranks_diamonds.append(x.rank)
        if len(check_cards_hearts) == 5 or len(check_cards_diamonds) == 5 or len(check_cards_clubs) == 5 or len(check_cards_spades) == 5:
            if len(check_cards_hearts) == 5:
                if hands.check_suits(check_cards_hearts):
                    return HandValue(23, 3)
                else:
                    return False
            elif len(check_cards_diamonds) == 5:
                if hands.check_suits(check_cards_diamonds):
                    return HandValue(23, 2)
                else:
                    return False
            elif len(check_cards_spades) == 5:
                if hands.check_suits(check_cards_spades):
                    return HandValue(23, 4)
                else:
                    return False
            elif len(check_cards_clubs) == 5:
                if hands.check_suits(check_cards_clubs):
                    return HandValue(23, 1)
                else:
                    return False
        else:
            return False
    else:
        return False

def checkforstraighflush(hands):
    check_cards_hearts = []
    check_cards_ranks_hearts = []
    check_cards_spades = []
    check_cards_ranks_spades = []
    check_cards_clubs = []
    check_cards_ranks_clubs = []
    check_cards_diamonds = []
    check_cards_ranks_diamonds = []
    for x in hands.cards:
        w = x.suit
        if w == 'Hearts':
            check_cards_hearts.append(x)
            check_cards_ranks_hearts.append(x.rank)
        elif w == 'Clubs':
            check_cards_clubs.append(x)
            check_cards_ranks_clubs.append(x.rank)
        elif w == 'Spades':
            check_cards_spades.append(x)
            check_cards_ranks_spades.append(x.rank)
        elif w == 'Diamonds':
            check_cards_diamonds.append(x)
            check_cards_ranks_diamonds.append(x.rank)
    if len(check_cards_hearts) >= 5:
        if 'Two' in check_cards_ranks_hearts and 'Three' in check_cards_ranks_hearts and 'Four' in check_cards_ranks_hearts and 'Five' in check_cards_ranks_hearts and 'Six' in check_cards_ranks_hearts:
            return HandValue(22, 7)
        elif 'Seven' in check_cards_ranks_hearts and 'Three' in check_cards_ranks_hearts and 'Four' in check_cards_ranks_hearts and 'Five' in check_cards_ranks_hearts and 'Six' in check_cards_ranks_hearts:
            return HandValue(22, 11)
        elif 'Seven' in check_cards_ranks_hearts and 'Eight' in check_cards_ranks_hearts and 'Four' in check_cards_ranks_hearts and 'Five' in check_cards_ranks_hearts and 'Six' in check_cards_ranks_hearts:
            return HandValue(22, 15)
        elif 'Seven' in check_cards_ranks_hearts and 'Eight' in check_cards_ranks_hearts and 'Nine' in check_cards_ranks_hearts and 'Five' in check_cards_ranks_hearts and 'Six' in check_cards_ranks_hearts:
            return HandValue(22, 19)
        elif 'Seven' in check_cards_ranks_hearts and 'Eight' in check_cards_ranks_hearts and 'Nine' in check_cards_ranks_hearts and 'Ten' in check_cards_ranks_hearts and 'Six' in check_cards_ranks_hearts:
            return HandValue(22, 23)
        elif 'Seven' in check_cards_ranks_hearts and 'Eight' in check_cards_ranks_hearts and 'Nine' in check_cards_ranks_hearts and 'Ten' in check_cards_ranks_hearts and 'Jack' in check_cards_ranks_hearts:
            return HandValue(22, 27)
        elif 'Queen' in check_cards_ranks_hearts and 'Eight' in check_cards_ranks_hearts and 'Nine' in check_cards_ranks_hearts and 'Ten' in check_cards_ranks_hearts and 'Jack' in check_cards_ranks_hearts:
            return HandValue(22, 31)
        elif 'Queen' in check_cards_ranks_hearts and 'King' in check_cards_ranks_hearts and 'Nine' in check_cards_ranks_hearts and 'Ten' in check_cards_ranks_hearts and 'Jack' in check_cards_ranks_hearts:
            return HandValue(22, 35)
        elif 'Two' in check_cards_ranks_hearts and 'Three' in check_cards_ranks_hearts and 'Four' in check_cards_ranks_hearts and 'Five' in check_cards_ranks_hearts and 'Ace' in check_cards_ranks_hearts:
            return HandValue(22, 3)
        else:
            return False
    elif len(check_cards_clubs) >= 5:
        if 'Two' in check_cards_ranks_clubs and 'Three' in check_cards_ranks_clubs and 'Four' in check_cards_ranks_clubs and 'Five' in check_cards_ranks_clubs and 'Six' in check_cards_ranks_clubs:
            return HandValue(22, 5)
        elif 'Seven' in check_cards_ranks_clubs and 'Three' in check_cards_ranks_clubs and 'Four' in check_cards_ranks_clubs and 'Five' in check_cards_ranks_clubs and 'Six' in check_cards_ranks_clubs:
            return HandValue(22, 9)
        elif 'Seven' in check_cards_ranks_clubs and 'Eight' in check_cards_ranks_clubs and 'Four' in check_cards_ranks_clubs and 'Five' in check_cards_ranks_clubs and 'Six' in check_cards_ranks_clubs:
            return HandValue(22, 13)
        elif 'Seven' in check_cards_ranks_clubs and 'Eight' in check_cards_ranks_clubs and 'Nine' in check_cards_ranks_clubs and 'Five' in check_cards_ranks_clubs and 'Six' in check_cards_ranks_clubs:
            return HandValue(22, 17)
        elif 'Seven' in check_cards_ranks_clubs and 'Eight' in check_cards_ranks_clubs and 'Nine' in check_cards_ranks_clubs and 'Ten' in check_cards_ranks_clubs and 'Six' in check_cards_ranks_clubs:
            return HandValue(22, 21)
        elif 'Seven' in check_cards_ranks_clubs and 'Eight' in check_cards_ranks_clubs and 'Nine' in check_cards_ranks_clubs and 'Ten' in check_cards_ranks_clubs and 'Jack' in check_cards_ranks_clubs:
            return HandValue(22, 25)
        elif 'Queen' in check_cards_ranks_clubs and 'Eight' in check_cards_ranks_clubs and 'Nine' in check_cards_ranks_clubs and 'Ten' in check_cards_ranks_clubs and 'Jack' in check_cards_ranks_clubs:
            return HandValue(22, 29)
        elif 'Queen' in check_cards_ranks_clubs and 'King' in check_cards_ranks_clubs and 'Nine' in check_cards_ranks_clubs and 'Ten' in check_cards_ranks_clubs and 'Jack' in check_cards_ranks_clubs:
            return HandValue(22, 33)
        elif 'Two' in check_cards_ranks_clubs and 'Three' in check_cards_ranks_clubs and 'Four' in check_cards_ranks_clubs and 'Five' in check_cards_ranks_clubs and 'Ace' in check_cards_ranks_clubs:
            return HandValue(22, 1)
        else:
            return False
    elif len(check_cards_spades) >= 5:
        if 'Two' in check_cards_ranks_spades and 'Three' in check_cards_ranks_spades and 'Four' in check_cards_ranks_spades and 'Five' in check_cards_ranks_spades and 'Six' in check_cards_ranks_spades:
            return HandValue(22, 8)
        elif 'Seven' in check_cards_ranks_spades and 'Three' in check_cards_ranks_spades and 'Four' in check_cards_ranks_spades and 'Five' in check_cards_ranks_spades and 'Six' in check_cards_ranks_spades:
            return HandValue(22, 12)
        elif 'Seven' in check_cards_ranks_spades and 'Eight' in check_cards_ranks_spades and 'Four' in check_cards_ranks_spades and 'Five' in check_cards_ranks_spades and 'Six' in check_cards_ranks_spades:
            return HandValue(22, 16)
        elif 'Seven' in check_cards_ranks_spades and 'Eight' in check_cards_ranks_spades and 'Nine' in check_cards_ranks_spades and 'Five' in check_cards_ranks_spades and 'Six' in check_cards_ranks_spades:
            return HandValue(22, 20)
        elif 'Seven' in check_cards_ranks_spades and 'Eight' in check_cards_ranks_spades and 'Nine' in check_cards_ranks_spades and 'Ten' in check_cards_ranks_spades and 'Six' in check_cards_ranks_spades:
            return HandValue(22, 24)
        elif 'Seven' in check_cards_ranks_spades and 'Eight' in check_cards_ranks_spades and 'Nine' in check_cards_ranks_spades and 'Ten' in check_cards_ranks_spades and 'Jack' in check_cards_ranks_spades:
            return HandValue(22, 28)
        elif 'Queen' in check_cards_ranks_spades and 'Eight' in check_cards_ranks_spades and 'Nine' in check_cards_ranks_spades and 'Ten' in check_cards_ranks_spades and 'Jack' in check_cards_ranks_spades:
            return HandValue(22, 32)
        elif 'Queen' in check_cards_ranks_spades and 'King' in check_cards_ranks_spades and 'Nine' in check_cards_ranks_spades and 'Ten' in check_cards_ranks_spades and 'Jack' in check_cards_ranks_spades:
            return HandValue(22, 36)
        elif 'Two' in check_cards_ranks_spades and 'Three' in check_cards_ranks_spades and 'Four' in check_cards_ranks_spades and 'Five' in check_cards_ranks_spades and 'Ace' in check_cards_ranks_spades:
            return HandValue(22, 4)
        else:
            return False
    elif len(check_cards_diamonds) >= 5:
        if 'Two' in check_cards_ranks_diamonds and 'Three' in check_cards_ranks_diamonds and 'Four' in check_cards_ranks_diamonds and 'Five' in check_cards_ranks_diamonds and 'Six' in check_cards_ranks_diamonds:
            return HandValue(22, 6)
        elif 'Seven' in check_cards_ranks_diamonds and 'Three' in check_cards_ranks_diamonds and 'Four' in check_cards_ranks_diamonds and 'Five' in check_cards_ranks_diamonds and 'Six' in check_cards_ranks_diamonds:
            return HandValue(22, 10)
        elif 'Seven' in check_cards_ranks_diamonds and 'Eight' in check_cards_ranks_diamonds and 'Four' in check_cards_ranks_diamonds and 'Five' in check_cards_ranks_diamonds and 'Six' in check_cards_ranks_diamonds:
            return HandValue(22, 14)
        elif 'Seven' in check_cards_ranks_diamonds and 'Eight' in check_cards_ranks_diamonds and 'Nine' in check_cards_ranks_diamonds and 'Five' in check_cards_ranks_diamonds and 'Six' in check_cards_ranks_diamonds:
            return HandValue(22, 18)
        elif 'Seven' in check_cards_ranks_diamonds and 'Eight' in check_cards_ranks_diamonds and 'Nine' in check_cards_ranks_diamonds and 'Ten' in check_cards_ranks_diamonds and 'Six' in check_cards_ranks_diamonds:
            return HandValue(22, 22)
        elif 'Seven' in check_cards_ranks_diamonds and 'Eight' in check_cards_ranks_diamonds and 'Nine' in check_cards_ranks_diamonds and 'Ten' in check_cards_ranks_diamonds and 'Jack' in check_cards_ranks_diamonds:
            return HandValue(22, 26)
        elif 'Queen' in check_cards_ranks_diamonds and 'Eight' in check_cards_ranks_diamonds and 'Nine' in check_cards_ranks_diamonds and 'Ten' in check_cards_ranks_diamonds and 'Jack' in check_cards_ranks_diamonds:
            return HandValue(22, 30)
        elif 'Queen' in check_cards_ranks_diamonds and 'King' in check_cards_ranks_diamonds and 'Nine' in check_cards_ranks_diamonds and 'Ten' in check_cards_ranks_diamonds and 'Jack' in check_cards_ranks_diamonds:
            return HandValue(22, 34)
        elif 'Two' in check_cards_ranks_diamonds and 'Three' in check_cards_ranks_diamonds and 'Four' in check_cards_ranks_diamonds and 'Five' in check_cards_ranks_diamonds and 'Ace' in check_cards_ranks_diamonds:
            return HandValue(22, 2)
        else:
            return False
    else:
        return False

def checkforfourofakind(hands):
    seen = hands.get_dupes(hands.ranks)
    for x in seen:
        if seen[x] == 4:
            return HandValue(21, get_cardrank_value(x))
    return False

def checkforthreeofakind(hands):
    seen = hands.get_dupes(hands.ranks)
    for x in seen:
        if seen[x] == 3:
            return HandValue(17, get_cardrank_value(x))
    return False

def checkfortwoofakind(hands):
    seen = hands.get_dupes(hands.ranks)
    for x in seen:
        if seen[x] == 2:
            return HandValue(15, get_cardrank_value(x))
    return False

def checkforfullhouse(hands):
    if checkfortwoofakind(hands) != False and checkforthreeofakind(hands) != False:
        return HandValue(20, (2 * checkfortwoofakind(hands).tie_score) + (3 * checkforthreeofakind(hands).tie_score))
    else:
        return False

def checkforflush(hands):
    check_cards_hearts = []
    check_cards_spades = []
    check_cards_clubs = []
    check_cards_diamonds = []
    for x in hands.cards:
        w = x.suit
        if w == 'Hearts':
            check_cards_hearts.append(x)
        elif w == 'Clubs':
            check_cards_clubs.append(x)
        elif w == 'Spades':
            check_cards_spades.append(x)
        elif w == 'Diamonds':
            check_cards_diamonds.append(x)
    if len(check_cards_hearts) >= 5:
        return HandValue(19, 1)
    elif len(check_cards_clubs) >= 5:
        return HandValue(19, 1)
    elif len(check_cards_spades) >= 5:
        return HandValue(19, 1)
    elif len(check_cards_diamonds) >= 5:
        return HandValue(19, 1)
    else:
        return False

def checkforstraight(hands):
    check_cards = hands.ranks
    if 'Two' in check_cards and 'Three' in check_cards and 'Four' in check_cards and 'Five' in check_cards and 'Six' in check_cards:
        return HandValue(18, 2)
    elif 'Seven' in check_cards and 'Three' in check_cards and 'Four' in check_cards and 'Five' in check_cards and 'Six' in check_cards:
        return HandValue(18, 3)
    elif 'Seven' in check_cards and 'Eight' in check_cards and 'Four' in check_cards and 'Five' in check_cards and 'Six' in check_cards:
        return HandValue(18, 4)
    elif 'Seven' in check_cards and 'Eight' in check_cards and 'Nine' in check_cards and 'Five' in check_cards and 'Six' in check_cards:
        return HandValue(18, 5)
    elif 'Seven' in check_cards and 'Eight' in check_cards and 'Nine' in check_cards and 'Ten' in check_cards and 'Six' in check_cards:
        return HandValue(18, 6)
    elif 'Seven' in check_cards and 'Eight' in check_cards and 'Nine' in check_cards and 'Ten' in check_cards and 'Jack' in check_cards:
        return HandValue(18, 7)
    elif 'Queen' in check_cards and 'Eight' in check_cards and 'Nine' in check_cards and 'Ten' in check_cards and 'Jack' in check_cards:
        return HandValue(18, 8)
    elif 'Queen' in check_cards and 'King' in check_cards and 'Nine' in check_cards and 'Ten' in check_cards and 'Jack' in check_cards:
        return HandValue(18, 9)
    elif 'Two' in check_cards and 'Three' in check_cards and 'Four' in check_cards and 'Five' in check_cards and 'Ace' in check_cards:
        return HandValue(18, 1)
    else:
        return False

def checkfortwopair(hands):
    check_cards = hands.ranks
    seen = hands.get_dupes(check_cards)
    final = 0
    higher_pair = None
    for x in seen:
        if seen[x] >= 2:
            final += 1
            if higher_pair != None:
                if get_cardrank_value(higher_pair) > get_cardrank_value(x):
                    pass
                else:
                    higher_pair = x
            else:
                higher_pair = x
    if final >= 2:
        return HandValue(16, get_cardrank_value(higher_pair))
    else:
        return False

def checkforhand(hands):
    check = False
    check = checkforroyalflush(hands)
    if not check:
        check = checkforstraighflush(hands)
    if not check:
        check = checkforfourofakind(hands)
    if not check:
        check = checkforfullhouse(hands)
    if not check:
        check = checkforflush(hands)
    if not check:
        check = checkforstraight(hands)
    if not check:
        check = checkforthreeofakind(hands)
    if not check:
        check = checkfortwopair(hands)
    if not check:
        check = checkfortwoofakind(hands)
    if check != False:
        return check
    else:
        return False
