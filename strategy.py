from count import Count
import pandas as pd

chart = pd.read_csv("BasicStrategy.csv", index_col="Player")

def get_hand_index(player_hand: list):
    player_hand.sort()
    
    if len(player_hand) == 2:
        if player_hand[0] == player_hand[1]:
            return str(player_hand[0]) + str(player_hand[1])
        
        if player_hand[1] == "A":
            return "A" + player_hand[0]
        
        integer_version = [int(card) for card in player_hand]
        return str(sum(integer_version))
    
    else:
        if player_hand[-1] == "A":
            previous_ints = [int(card) if card != "A" else 1 for card in player_hand[:-1]]
            return "A" + str(sum(previous_ints))
        
        integer_version = [int(card) for card in player_hand]
        return str(sum(integer_version))
        

def player_strategy(player_hand: list, dealer_card: int, count: Count):
    hand_index = get_hand_index(player_hand)
    
    return chart.loc[hand_index, dealer_card]
                
        
        