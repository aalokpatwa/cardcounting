from dataclasses import dataclass

class GameConfig:
    decks_per_shoe = 2
    penetration = 0.8
    bj_payout = 1.5
    insurance_payout = 2.0
    min_bet = 25
    h17 = True
    
    seconds_per_round = 45
    seconds_per_shuffle = 45

@dataclass
class BetLevel:
    n_hands: int
    bet: int

class CountingConfig:
    starting_stack = 20000
    
    spread = {
        0: BetLevel(n_hands=1, bet=25),
        1: BetLevel(n_hands=1, bet=100),
        2: BetLevel(n_hands=1, bet=200),
        3: BetLevel(n_hands=1, bet=400),
        4: BetLevel(n_hands=1, bet=600),
        5: BetLevel(n_hands=1, bet=1200),
        6: BetLevel(n_hands=1, bet=1500),
        7: BetLevel(n_hands=1, bet=2000),
    }
    
    deck_estimation = "half" # "full" or "half" or "quarter"
    
