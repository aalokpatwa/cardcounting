class GameConfig:
    decks_per_shoe = 6
    penetration = 0.75
    bj_payout = 1.5
    insurance_payout = 2.0
    min_bet = 25
    max_bet = 1000

class CountingConfig:
    starting_stack = 20000
    
    spread = {
        0: 25,
        1: 50,
        2: 100,
        3: 200,
        4: 400
    }
    
    deck_estimation = "full" # or "half" or "quarter"
    
