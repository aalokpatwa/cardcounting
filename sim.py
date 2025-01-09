"""Simulates a set of rounds of blackjack"""

from shoe import Shoe
from config import GameConfig, CountingConfig
from count import Count
from strategy import player_strategy

NUM_ROUNDS = 1000

def hand_busted(player_hand: list):
    transformed_hand = [int(card) if card != "A" else 1 for card in player_hand]
    total = sum(transformed_hand)
    return total > 21

shoe = Shoe(GameConfig.decks_per_shoe, GameConfig.penetration)

count = Count(GameConfig.decks_per_shoe)

stack = CountingConfig.starting_stack

for round in range(NUM_ROUNDS):
    if shoe.should_reshuffle():
        shoe.new_shoe()
        count.reset()
        
    bet = count.get_bet()
    
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
    
    # Check for blackjack
    if sorted(player_hand) == ["10", "A"]:
        count.update(dealer_second)
        if sorted(dealer_hand) != ["10", "A"]:
            stack += bet * GameConfig.bj_payout
        
        continue
        
    decision = player_strategy(player_hand, dealer_first, count)
    
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
        
        if hand_busted(player_hand):
            break
        
        decision = player_strategy(player_hand, dealer_first, count)        
            