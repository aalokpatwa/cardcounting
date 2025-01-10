from config import CountingConfig, BetLevel
import math

class Count:
    def __init__(self, decks):
        self.running_count = 0
        self.total_decks = decks
        self.decks_remaining = decks
    
    def update(self, card):
        if card in ["2", "3","4", "5", "6"]:
            self.running_count += 1
        elif card in ["10", "J", "Q", "K", "A"]:
            self.running_count -= 1
        
        self.decks_remaining -= 1 / 52.0
    
    def reset(self):
        self.running_count = 0
        self.decks_remaining = self.total_decks
    
    def get_running_count(self):
        return self.running_count

    def get_true_count(self):
        # In real counting situations, we must estimate the number
        if CountingConfig.deck_estimation == "full":
            estimated_decks = round(self.decks_remaining)
        elif CountingConfig.deck_estimation == "half":
            estimated_decks = round(self.decks_remaining * 2) / 2.0
        else:
            estimated_decks = round(self.decks_remaining * 4) / 4.0
        
        if self.running_count / estimated_decks < 0:
            return 0
        
        return math.floor(self.running_count / estimated_decks)
    
    def get_bet(self) -> BetLevel:
        true_count = self.get_true_count()
        
        spread = CountingConfig.spread
        counts = spread.keys()
        
        if true_count > max(counts):
            true_count = max(counts)
        
        if true_count < min(counts):
            true_count = min(counts)
        
        return spread[true_count]
        
        