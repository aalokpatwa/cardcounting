import pandas as pd

chart = pd.read_csv("BasicStrategy.csv", index_col="Player")

def get_hand_index(player_hand: list, start=False):
    hand = sorted(player_hand)
    
    # If we're on our original two cards, we can split
    if start:
        # Decide whether to split
        if hand[0] == hand[1]:
            return str(hand[0]) + str(hand[1])
        
        # Soft hand
        if hand[1] == "A":
            return "A" + hand[0]
        
        # No ace
        integer_version = [int(card) for card in hand]
        return str(sum(integer_version))
    
    else:
        # If we have AA after doubling/splitting, treat as 12
        if len(hand) == 2 and hand[0] == "A" and hand[1] == "A":
            return "12"
        
        # Otherwise, determine whether to play hard or soft ace
        if hand[-1] == "A":
            previous_ints = [int(card) if card != "A" else 1 for card in hand[:-1]]
            
            # Can't play a soft hand -- previous cards total more than 10
            if sum(previous_ints) > 10:
                return str(sum(previous_ints) + 1)
            
            # Soft hand
            return "A" + str(sum(previous_ints))
        
        # No aces in the hand
        integer_version = [int(card) for card in hand]
        return str(sum(integer_version))
        

def player_strategy(player_hand: list, dealer_card: int, start=False, can_double=True):
    hand_index = get_hand_index(player_hand, start)
        
    strategy = chart.loc[hand_index, dealer_card]
    
    if strategy == "Ds" and not start:
        return "S"
    
    if strategy == "Dh" and not start:
        return "H"
    
    if strategy == "D" and not can_double:
        return "H"
    
    return strategy
                
        
        