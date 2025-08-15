class Player: 
    def __init__(self, name, chip_stack): 
        self.name = name
        self.chip_stack = chip_stack
        self.hand = None
        self.hand_strength = None
        self.hand_name = None
        self.position = None
        self.folded = False
        self.all_in = False
        self.chips_in_pot = 0
        self.chips_won = 0
        self.is_bot = False
    
    def get_name(self): 
        return self.name
    
    def get_hand(self): 
        return self.hand
    
    def set_hand_strength(self, strength): 
        self.hand_strength = strength

    def get_hand_strength(self): 
        return self.hand_strength
    
    def set_hand_name(self, hand_name): 
        self.hand_name = hand_name
    
    def get_hand_name(self): 
        return self.hand_name
    
    def get_position(self): 
        return self.position
    
    def set_position(self, position): 
        self.position = position 

    def increment_chips(self, chips): 
        self.chip_stack += chips
      
    def get_chips(self): 
        return self.chip_stack
    
    def set_hand(self, hand): 
        self.hand = hand

    def set_position(self, position): 
        self.position = position 

    def set_all_in(self): 
        self.all_in = True

    def reset(self): 
        self.hand = None
        self.hand_strength = None
        self.hand_name = None
        self.position = None
        self.folded = False
        self.all_in = False
        self.chips_in_pot = 0
        self.chips_won = 0

    def amount_contributed(self, bet_amount): 
        self.chips_in_pot += bet_amount

    def get_amount_contributed(self): 
        return self.chips_in_pot
    
    def add_chips_won(self, amount): 
        self.chips_won += amount

    def get_chips_won(self): 
        return self.chips_won
    
    def to_String(self, action, bet_size, call_size):
        if action == "Bet": 
            player_action = f"Bet {bet_size}"
        elif action == "Call": 
            player_action = f"Call {call_size}"
        else: 
            player_action = "Fold"
        return f"----------{self.name}-----------\nChips: {self.chip_stack}\nPosition: {self.position}\nAction: {player_action}\n-----------------------------\n"

class Bot(Player): 
    def __init__(self, name, chip_stack): 
        super().__init__(name, chip_stack)
        self.is_bot = True
    
    #if call-no 3bet go all in
    def bot_action(self, available_options, current_bet, chip_stack):
        if self.hand_strength > 232: 
            return "all-in"
        elif self.hand_strength > 80:
            if current_bet * 3 >= chip_stack: 
                return "all-in"
            else: 
                return "bet"
        elif self.hand_strength > 50: 
            if current_bet > (chip_stack / 3):
                return "fold"
            elif "check" in available_options:
                return "check"
            else:
                return "call"
        else: 
            if "check" in available_options: 
                return "check"
            else: 
                return "fold"
    
