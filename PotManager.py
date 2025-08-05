class PotManager: 
    def __init__(self):
        self.main_pot = 0
        self.side_pot = []
        self.main_pot_closed = False

    def add_bet(self, bet_amount): 
        self.main_pot += bet_amount

    def update_main_pot(self): 
        return self.main_pot

    def reset(self): 
        self.main_pot = 0