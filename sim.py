"""Simulates a set of rounds of blackjack"""

from shoe import Shoe
from config import GameConfig, CountingConfig
from count import Count
from strategy import player_strategy
from hand import *
from tqdm import tqdm

NUM_EXPERIMENTS = 1
NUM_ROUNDS = 1000000

def play_round(shoe, count, stack):
    """Play a single round of blackjack"""
    if shoe.should_reshuffle():
        shoe.new_shoe()
        count.reset()
    
    betLevel = count.get_bet()
    n_hands = betLevel.n_hands
    bet = betLevel.bet
    
    if n_hands * bet > stack:
        # If we can't afford the bet indicated by spread, play one hand all-in
        n_hands = 1
        bet = stack
    
    hands = []
    
    for hand in range(n_hands):
        # Player gets their first card
        player_first = shoe.draw()
        count.update(player_first)
        
        this_hand = PlayerHand([player_first])
        
        hands.append(this_hand)
    
    # Dealer gets their first card, face-up
    dealer_first = shoe.draw()
    count.update(dealer_first)
    
    # Player gets their second card
    for hand in range(n_hands):
        player_second = shoe.draw()
        count.update(player_second)
        existing_hand = hands[hand]
        existing_hand.add_card(player_second)
    
    # Dealer gets their second card, face-down
    dealer_second = shoe.draw()
    dealer_hand = [dealer_first, dealer_second]
    dealer_hand = convert_face(dealer_hand)

    counted_dealer_second = False
    
    totals = []
    
    # Play each of the hands, in order
    while len(hands) > 0:
        # Pop the first hand from our queue
        this_hand = hands.pop(0)
        player_cards = this_hand.get_cards()
        player_cards = convert_face(player_cards)
        
        # Check for player blackjack
        if sorted(player_cards) == ["10", "A"]:
            if not counted_dealer_second:
                count.update(dealer_second)
                counted_dealer_second = True
            if sorted(dealer_hand) != ["10", "A"]:                
                # Don't count blackjack payout if we had split to get blackjack
                if not this_hand.can_split():
                    stack += bet * GameConfig.bj_payout
                else:
                    stack += bet
            continue
        
        # Check for dealer blackjack
        if sorted(dealer_hand) == ["10", "A"]:
            if not counted_dealer_second:
                count.update(dealer_second)
                counted_dealer_second = True
            stack -= bet
            continue
        
        # Might be some hands that we are not allowed to hit (e.g. split aces)
        if not this_hand.can_hit():
            decision = "S"
        else:
            # Otherwise, we can do whatever we want
            decision = player_strategy(player_cards, dealer_first, this_hand.can_split(), this_hand.can_split())
                
        # Playing each hand
        while decision != "S":
            # Decision was to double: draw one card and stand
            if decision == "D":
                bet *= 2
                new_card = shoe.draw()
                count.update(new_card)   
                player_cards.append(new_card)
                player_cards = convert_face(player_cards)
                break
            
            # Decision was to split: draw one card for each hand and add back
            elif decision == "P":
                first_cards = [player_cards[0]]
                new_card = shoe.draw()
                count.update(new_card)
                first_cards.append(new_card)
                
                second_cards = [player_cards[1]]
                new_card = shoe.draw()
                count.update(new_card)
                second_cards.append(new_card)
                                
                # If splitting aces, cannot hit again after split
                hit_next = True
                if player_cards[0] == "A":
                    hit_next = False
                
                first_hand = PlayerHand(first_cards, hit_next)
                second_hand = PlayerHand(second_cards, hit_next)
                                
                hands.insert(0, first_hand)
                hands.insert(0, second_hand) 
                
                break      
            
            # Otherwise, player wants to hit this hand
            else:
                new_card = shoe.draw()
                count.update(new_card)
                player_cards.append(new_card)
                player_cards = convert_face(player_cards)
                        
                if hand_busted(player_cards):
                    break
            
                decision = player_strategy(player_cards, dealer_first, False, False)
        
        # If we split, we'll re-enter the loop to play the split hands in succession
        if decision == "P":
            continue
        
        # Otherwise, check for a bust
        if hand_busted(player_cards):
            stack -= bet
            continue
        
        # If no bust, store the total
        total = get_highest_total(player_cards)
        totals.append(total)
    
    # Dealer play section
    if not counted_dealer_second:
        count.update(dealer_second)
        counted_dealer_second = True
    
    # Dealer hits until they get above a 17
    while get_highest_total(dealer_hand) < 17:
        
        # Dealer can only hit a soft 17. Stands on hard 17
        if "A" not in dealer_hand and get_highest_total(dealer_hand) == 17:
            break
        
        new_card = shoe.draw()
        count.update(new_card)
        
        dealer_hand.append(new_card)
        dealer_hand = convert_face(dealer_hand)
        
    if GameConfig.h17 and (get_highest_total(dealer_hand) == 17) and ("A" in dealer_hand):
        new_card = shoe.draw()
        count.update(new_card)
        
        dealer_hand.append(new_card)
        dealer_hand = convert_face(dealer_hand)
            
    # Player wins if dealer
    for total in totals:
        if get_highest_total(dealer_hand) > 21 or get_highest_total(dealer_hand) < total:
            stack += bet
        elif get_highest_total(dealer_hand) > total:
            stack -= bet

    return stack

def run_simulation():
    """Run a simulation of NUM_ROUNDS rounds of blackjack"""
    shoe = Shoe(GameConfig.decks_per_shoe, GameConfig.penetration)
    count = Count(GameConfig.decks_per_shoe)
    stack = CountingConfig.starting_stack
    shoes = 0
    ruins = 0
    
    avs = []

    for experiment in tqdm(range(NUM_EXPERIMENTS)):
        shoes = 0
        stack = CountingConfig.starting_stack
        for round_no in range(NUM_ROUNDS):
            if stack < GameConfig.min_bet:
                ruins += 1
                stack = CountingConfig.starting_stack
            
            stack = play_round(shoe, count, stack)
            
            if shoe.should_reshuffle():
                shoes += 1
                shoe.new_shoe()
                count.reset()
        
        hours_taken = (NUM_ROUNDS * GameConfig.seconds_per_round / 3600) + (shoes * GameConfig.seconds_per_shuffle / 3600)
        winnings = (stack - CountingConfig.starting_stack) / hours_taken
        avs.append(winnings)

    return sum(avs) / len(avs)

if __name__ == "__main__":
    ev = run_simulation()
    print (f"EV: {ev}")

