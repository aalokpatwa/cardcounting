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
            
        # Face cards all treated as a 10 -- doesn't affect the game
        self.cards.extend([str(10)] * 16 * self.num_decks)
        
        # Aces are added as 'A'
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
        
    