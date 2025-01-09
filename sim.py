"""Simulates a set of rounds of blackjack"""

from shoe import Shoe
from config import GameConfig, CountingConfig
from count import Count
from strategy import player_strategy

NUM_ROUNDS = 10000

def convert_face(player_hand: list):
    return ["10" if card in ["J", "Q", "K"] else card for card in player_hand]

def get_highest_total(player_hand: list):
    transformed_hand = [int(card) if card != "A" else 1 for card in player_hand]
    total = sum(transformed_hand)
    
    if "A" in player_hand and total <= 11:
        return total + 10
    
    return total

def hand_busted(player_hand: list):
    transformed_hand = [int(card) if card != "A" else 1 for card in player_hand]
    total = sum(transformed_hand)
    return total > 21

shoe = Shoe(GameConfig.decks_per_shoe, GameConfig.penetration)

count = Count(GameConfig.decks_per_shoe)

stack = CountingConfig.starting_stack

shoes = 0

for round in range(NUM_ROUNDS):
    if shoe.should_reshuffle():
        shoes += 1
        shoe.new_shoe()
        count.reset()
        
    bet = count.get_bet()
    
    if bet > GameConfig.min_bet:
        print (bet)
    
    # Player gets their first card
    player_first = shoe.draw()
    count.update(player_first)
    
    # Dealer gets their first card, face-up
    dealer_first = shoe.draw()
    count.update(dealer_first)
    
    # Player gets their first card
    player_second = shoe.draw()
    count.update(player_second)
    
    # Dealer gets their second card, face-down
    dealer_second = shoe.draw()
    
    # Choose our first decision
    player_hand = [player_first, player_second]
    dealer_hand = [dealer_first, dealer_second]
    
    player_hand = convert_face(player_hand)
    dealer_hand = convert_face(dealer_hand)
    
    # Check for blackjack
    if sorted(player_hand) == ["10", "A"]:
        count.update(dealer_second)
        if sorted(dealer_hand) != ["10", "A"]:
            stack += bet * GameConfig.bj_payout
        
        continue
        
    decision = player_strategy(player_hand, dealer_first, True)
    
    # Player section
    while decision != "S":
        new_card = shoe.draw()
        count.update(new_card)            
        
        if decision == "D":
            bet *= 2
            
        elif decision == "P":
            # For now, only use one of the hands
            player_hand.pop()
            
        player_hand.append(new_card)
        
        player_hand = convert_face(player_hand)
        
        if hand_busted(player_hand):
            break
        
        decision = player_strategy(player_hand, dealer_first, False)
        
    if hand_busted(player_hand):
        stack -= bet
        continue   
    
    # Dealer section
    count.update(dealer_second)
    while get_highest_total(dealer_hand) < 18:
        new_card = shoe.draw()
        count.update(new_card)
        
        dealer_hand.append(new_card)
        dealer_hand = convert_face(dealer_hand)
        
    if get_highest_total(dealer_hand) > 21 or get_highest_total(dealer_hand) < get_highest_total(player_hand):
        stack += bet
    else:
        stack -= bet
        
print (f"Final stack: {stack}")
print (f"EV: {(stack - CountingConfig.starting_stack) / NUM_ROUNDS}")
print (f"Shoes: {shoes}")