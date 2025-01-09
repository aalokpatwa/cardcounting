import random

class Shoe:
    def __init__(self, num_decks, penetration):
        self.num_decks = num_decks
        self.penetration = penetration
        self.cards = []
        self.new_shoe()
    
    def new_shoe(self):
        self.cards = []
        
        for rank in range(2, 11):
            self.cards.extend([str(rank)] * 4 * self.num_decks)
            
        self.cards.extend([str(10)] * 4 * self.num_decks)
        self.cards.extend([str("J")] * 4 * self.num_decks)
        self.cards.extend([str("Q")] * 4 * self.num_decks)
        self.cards.extend([str("K")] * 4 * self.num_decks)
        self.cards.extend(["A"] * 4 * self.num_decks)
        
        # Shuffle the shoe
        self.shuffle()
    
    def should_reshuffle(self):
        return len(self.cards) < (1 - self.penetration) * self.num_decks * 52
    
    def is_empty(self):
        return len(self.cards) == 0
    
    def draw(self):
        if self.is_empty():
            raise ValueError("Attempted to draw from an empty shoe")
        
        return self.cards.pop()
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    