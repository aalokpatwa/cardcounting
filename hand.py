class PlayerHand:
    def __init__(self, hand: list, bet: int, splitted=False, can_hit=True, total=None):
        self.hand = hand
        self.bet = bet
        self.splitted = splitted
        self.hittable = can_hit
        self.total = total
    
    def can_split(self):
        return len(self.hand) == 2 and not self.splitted
    
    def can_hit(self):
        return self.hittable
    
    def get_cards(self):
        return self.hand
    
    def add_card(self, card):
        self.hand.append(card)
        
    def get_bet(self):
        return self.bet
    
    def set_bet(self, new_bet):
        self.bet = new_bet
        
    def get_total(self):
        return self.total
    
    def set_total(self, new_total):
        self.total = new_total
        
def convert_face(player_hand: list):
    """ Utility to represent all face cards as 10 """
    return ["10" if card in ["J", "Q", "K"] else card for card in player_hand]

def get_highest_total(player_hand: list):
    """ Utility to get the highest possible total of a hand """
    
    # First, get the hard total
    transformed_hand = [int(card) if card != "A" else 1 for card in player_hand]
    total = sum(transformed_hand)
    
    # If we can, get the better soft total
    if "A" in player_hand and total <= 11:
        return total + 10
    
    return total

def hand_busted(player_hand: list):
    """ Check whether a hand has officially busted """
    transformed_hand = [int(card) if card != "A" else 1 for card in player_hand]
    total = sum(transformed_hand)
    return total > 21