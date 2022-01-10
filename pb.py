import random 
import eval7

def get_all_hands(deck):
    hands = []
    for card in deck:
        for card_2 in deck:
            if card != card_2:
                hands.append([card, card_2])
    return hands


def do_mc():
    odds_dict = {}
    deck = eval7.Deck()
    all_possible = get_all_hands(deck)
    random.shuffle(all_possible)
    for hand in all_possible:
        print(hand)
        for card in hand: #removing our hole cards from the deck
                deck.cards.remove(card)

        iters = 5000
            
        wins = 0
        ties = 0
        score = 0
        changes = 0

        for _ in range(iters): # MC the probability of winning
            hole_cards = hand[:]
            deck.shuffle()

            _OPP = 2 
            _COMM = 5

            draw = deck.peek(_OPP + _COMM)

            opp_hole = draw[:_OPP]
            community = draw[_OPP:]

            change = 0
            for i in range(2):
                if random.random() <= .10:
                    change += 1
                    hole_cards[i] = deck.peek(7+change)[6+change]

            for i in range(2):
                if random.random() <= .050:
                    change += 1
                    hole_cards[i] = deck.peek(7+change)[6+change]

            if hole_cards != hand:
                changes += 1

            our_hand = hole_cards + community
            opp_hand = opp_hole + community

            our_hand_value = eval7.evaluate(our_hand)
            opp_hand_value = eval7.evaluate(opp_hand)


            if our_hand_value > opp_hand_value:
                wins += 1
                score += 2
            elif our_hand_value == opp_hand_value:
                ties += 1   
                score += 1

        hand_strength = score/(2*iters) # win probability 

        odds_dict[tuple(hand)] = (wins/iters, ties/iters, hand_strength)
        break

    print(changes/iters, changes)
    return odds_dict


print(do_mc())