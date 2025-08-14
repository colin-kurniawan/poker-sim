from Player import Player
from PotManager import PotManager
import random 

class PlayerManager: 
    def __init__(self, players, pot_manager): 
        self.players = players
        self.dealer_index = None
        self.small_blind_index = None
        self.big_blind_index = None
        self.under_the_gun_index = None
        self.pot_manager = pot_manager
    
    def post_blind(self, player, blind_amount): 
        chips = player.get_chips()

        if chips <= blind_amount:
            actual_blind = chips
            player.set_all_in()
        else:
            actual_blind = blind_amount

        player.increment_chips(-actual_blind)
        player.amount_contributed(actual_blind)
        self.pot_manager.add_bet(actual_blind)

    def add_players(self, num_players): 
        for i in range(num_players): 
            newPlayer = Player(f"Player {i + 1}", 1000)
            self.players.append(newPlayer)
        
    def establish_positions(self, num_players, hand_number): 
        if hand_number == 1:
            self.dealer_index = random.randint(0, num_players - 1)
        else: 
            self.dealer_index = (self.dealer_index + 1) % num_players
        self.players[self.dealer_index].set_position("Dealer")
        
        self.small_blind_index = (self.dealer_index + 1) % num_players
        self.players[self.small_blind_index].set_position("Small Blind")

        self.big_blind_index = (self.small_blind_index + 1) % num_players
        self.players[self.big_blind_index].set_position("Big Blind")

        self.under_the_gun_index = (self.big_blind_index + 1) % num_players
        self.players[self.under_the_gun_index].set_position("Under the Gun")

        self.post_blind(self.players[self.small_blind_index], 5)
        self.post_blind(self.players[self.big_blind_index], 10)

    def deal_hands(self, deck): 
        for player in self.players: 
            player.set_hand(deck.deal())

    def get_under_the_gun_index(self): 
        return self.under_the_gun_index
    
    def get_small_blind_index(self): 
        return self.small_blind_index
    
    def get_big_blind_index(self): 
        return self.big_blind_index
    
    def get_dealer_index(self): 
        return self.dealer_index

    def reset(self): 
        for player in self.players: 
            player.reset()
        self.pot_manager.reset()

    def print_blinds(self): 
        print(f"Little Blind: {self.players[self.small_blind_index].get_name()}")
        print(f"Big Blind: {self.players[self.big_blind_index].get_name()}")
    
