import hands as h
import corefunctions as cf
from collections import deque

#Original Hand scoring

def checkfortwoofakind(hand):
    seen = hand.get_dupes(hand.ranks)
    for x in seen:
        if seen[x] == 2:
            return 22 + h.get_cardrank_value(x)
    return 0
def gethgihsum(hand):
    sum = 0
    for x in hand.cards:
        sum += x.get_card_value()
    return sum

def original_hand_score(hand):
    finalcheck = 0
    finalcheck += checkfortwoofakind(hand)
    finalcheck += gethgihsum(hand)
    return finalcheck

def get_hand_bet(hand, bettingunit):
    finalcheck = original_hand_score(hand)
    bet = finalcheck * bettingunit
    return bet


#Other scoring

def get_handmiddle_bet(hand, middle, bettingunit):
    hands = h.Hands(hand.hand, middle.cards)
    value = h.checkforhand(hands)
    if value:
        finalvalue = value.hand_score
    else:
        finalvalue = 0
    finalvalue += 30
    if finalvalue <= 0:
        finalvalue = 0
    return finalvalue * bettingunit
