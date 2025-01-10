from dataclasses import dataclass

class GameConfig:
    decks_per_shoe = 6
    penetration = 0.8
    bj_payout = 1.5
    insurance_payout = 2.0
    min_bet = 25
    max_bet = 1000
    h17 = True
    
    seconds_per_round = 45
    seconds_per_shuffle = 60

@dataclass
class BetLevel:
    n_hands: int
    bet: int

class CountingConfig:
    starting_stack = 20000
    
    spread = {
        0: BetLevel(n_hands=1, bet=25),
        1: BetLevel(n_hands=1, bet=50),
        2: BetLevel(n_hands=2, bet=75),
        3: BetLevel(n_hands=2, bet=125),
        4: BetLevel(n_hands=2, bet=200),
    }
    
    deck_estimation = "half" # or "half" or "quarter"
    
