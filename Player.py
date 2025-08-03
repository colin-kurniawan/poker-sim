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

    def to_String(self, action, bet_size, call_size):
        if action == "Bet": 
            player_action = f"Bet {bet_size}"
        elif action == "Call": 
            player_action = f"Call {call_size}"
        else: 
            player_action = "Fold"
        return f"----------{self.name}-----------\nChips: {self.chip_stack}\nPosition: {self.position}\nAction: {player_action}\n-----------------------------\n"
