"""Simulates a set of rounds of blackjack"""

from shoe import Shoe
from config import GameConfig, CountingConfig
from count import Count
from strategy import player_strategy
from hand import *
from tqdm import tqdm

NUM_ROUNDS = int(1e6)

def play_round(shoe, count, stack):
    """Play a single round of blackjack"""
    
    # If the shoe is past the cut card, start a new shoe and reset the count
    if shoe.should_reshuffle():
        shoe.new_shoe()
        count.reset()
    
    # Based on the count, decide our bet level
    betLevel = count.get_bet()
    n_hands = betLevel.n_hands
    bet = betLevel.bet
    
    # If we can't afford the bet indicated by spread, play one hand all-in
    if n_hands * bet > stack:
        n_hands = 1
        bet = stack
    
    # Represent the set of hands the player is playing
    hands: list[PlayerHand] = []
    
    # Draw the first card for each player hand
    for hand in range(n_hands):
        player_first = shoe.draw()
        count.update(player_first)
        
        this_hand = PlayerHand([player_first], bet)
        hands.append(this_hand)
    
    # Dealer gets their first card, face-up
    dealer_first = shoe.draw()
    count.update(dealer_first)
    
    # Player hands get their second card
    for hand in range(n_hands):
        player_second = shoe.draw()
        count.update(player_second)
        existing_hand = hands[hand]
        existing_hand.add_card(player_second)
    
    # Dealer gets their second card, face-down
    dealer_second = shoe.draw()
    dealer_hand = [dealer_first, dealer_second]
    dealer_hand = convert_face(dealer_hand)

    # Variable to track whether we have counted the dealer's second card yet
    counted_dealer_second = False
    
    stood_hands: list[PlayerHand] = []
        
    # Play each of the hands, in order
    while len(hands) > 0:
        # Pop the first hand from our queue
        this_hand = hands.pop(0)
        
        # Get the cards in this hand
        player_cards = this_hand.get_cards()
        player_cards = convert_face(player_cards)
        
        # Check for player blackjack
        if sorted(player_cards) == ["10", "A"]:
            if not counted_dealer_second:
                count.update(dealer_second)
                counted_dealer_second = True
            if sorted(dealer_hand) != ["10", "A"]:                
                # If this was not a previously splitted hand, we get the BJ payout
                if not this_hand.can_split():
                    stack += this_hand.get_bet() * GameConfig.bj_payout
                # Otherwise, we just get 1x payout
                else:
                    stack += this_hand.get_bet()
            continue # This hand is over and we have registered the win
        
        # Check for dealer blackjack which is an auto-loss
        if sorted(dealer_hand) == ["10", "A"]:
            if not counted_dealer_second:
                count.update(dealer_second)
                counted_dealer_second = True
            stack -= this_hand.get_bet()
            continue # This hand is over and we have registered the loss
        
        # Might be some hands that we are not allowed to hit (e.g. split aces)
        if not this_hand.can_hit():
            decision = "S" # This hand is forced to stand
        else:
            # Otherwise, we can do whatever we want
            decision = player_strategy(player_cards, dealer_first, this_hand.can_split(), this_hand.can_split())
                
        # Playing each hand
        while decision != "S":
            # Decision was to double: double the money on this hand, draw one card and stand
            if decision == "D":
                this_hand.set_bet(this_hand.get_bet() * 2)
                new_card = shoe.draw()
                count.update(new_card)   
                player_cards.append(new_card)
                player_cards = convert_face(player_cards)
                break
            
            # Decision was to split: draw one card for each hand and add back to the queue
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
            
            # Otherwise, hit the hand and keep going unless we bust
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
        
        # Otherwise, double-check for a bust
        if hand_busted(player_cards):
            stack -= this_hand.get_bet()
            continue
        
        # If no bust, store the total
        total = get_highest_total(player_cards)
        this_hand.set_total(total)
        stood_hands.append(this_hand)
    
    # Now, look at the dealer's second card
    if not counted_dealer_second:
        count.update(dealer_second)
        counted_dealer_second = True
    
    # Dealer play -- stand after 17
    while get_highest_total(dealer_hand) < 17:
        
        # Dealer can only hit a soft 17. Stands on hard 17
        if "A" not in dealer_hand and get_highest_total(dealer_hand) == 17:
            break
        
        new_card = shoe.draw()
        count.update(new_card)
        
        dealer_hand.append(new_card)
        dealer_hand = convert_face(dealer_hand)
    
    # Check whether dealer currently has soft 17 -- hit if H17
    if GameConfig.h17 and (get_highest_total(dealer_hand) == 17) and ("A" in dealer_hand):
        new_card = shoe.draw()
        count.update(new_card)
        
        dealer_hand.append(new_card)
        dealer_hand = convert_face(dealer_hand)
            
    # Check player hands' win/losses
    for hand in stood_hands:
        if get_highest_total(dealer_hand) > 21 or get_highest_total(dealer_hand) < hand.get_total():
            stack += this_hand.get_bet()
        elif get_highest_total(dealer_hand) > hand.get_total():
            stack -= this_hand.get_bet()

    return stack

def run_simulation():
    """Run a simulation of NUM_ROUNDS rounds of blackjack"""
    shoe = Shoe(GameConfig.decks_per_shoe, GameConfig.penetration)
    count = Count(GameConfig.decks_per_shoe)
    stack = CountingConfig.starting_stack
    shoes = 0
    ruins = 0

    shoes = 0
    stack = CountingConfig.starting_stack
    
    for round_no in tqdm(range(NUM_ROUNDS)):
        if stack < GameConfig.min_bet:
            ruins += 1
            stack = CountingConfig.starting_stack
            
        if shoe.should_reshuffle():
            shoes += 1
            shoe.new_shoe()
            count.reset()
        
        stack = play_round(shoe, count, stack)
    
    # Measure the number of hours this would have taken
    hours_taken = (NUM_ROUNDS * GameConfig.seconds_per_round / 3600) + (shoes * GameConfig.seconds_per_shuffle / 3600)
    
    # Calculate the average winnings per hour
    evs = (stack - CountingConfig.starting_stack) / hours_taken

    return evs, shoes, ruins

if __name__ == "__main__":
    ev, shoes, ruins = run_simulation()
    print (f"EV: {ev}")
    print (f"Shoes: {shoes}")
    print (f"Ruins: {ruins}")

