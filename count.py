from config import CountingConfig, BetLevel
import math

class Count:
    def __init__(self, decks):
        self.running_count = 0
        self.total_decks = decks
        self.decks_remaining = decks
    
    def update(self, card):
        """ Updates the count based on the Hi-Lo approach """
        if card in ["2", "3","4", "5", "6"]:
            self.running_count += 1
        elif card in ["10", "J", "Q", "K", "A"]:
            self.running_count -= 1
        
        self.decks_remaining -= 1 / 52.0
    
    def reset(self):
        """ Used to reset the count at the start of a new shoe """
        self.running_count = 0
        self.decks_remaining = self.total_decks
    
    def get_running_count(self):
        return self.running_count

    def get_true_count(self):
        """ Estimates true count based on running count and decks remaining """
        if CountingConfig.deck_estimation == "full":
            estimated_decks = round(self.decks_remaining)
        elif CountingConfig.deck_estimation == "half":
            estimated_decks = round(self.decks_remaining * 2) / 2.0
        else:
            estimated_decks = round(self.decks_remaining * 4) / 4.0
        
        # Just treat all negative counts as 0-counts
        if self.running_count / estimated_decks < 0:
            return 0
        
        return math.floor(self.running_count / estimated_decks)
    
    def get_bet(self) -> BetLevel:
        """ Uses calculated true count to determine bet level """
        true_count = self.get_true_count()
        
        spread = CountingConfig.spread
        counts = spread.keys()
        
        if true_count > max(counts):
            true_count = max(counts)
        
        if true_count < min(counts):
            true_count = min(counts)
        
        return spread[true_count]
        
        