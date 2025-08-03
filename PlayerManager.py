from Player import Player
import random 

class PlayerManager: 
    def __init__(self, players): 
        self.players = players
        dealer_index = None
        small_blind_index = None
        big_blind_index = None
        under_the_gun_index = None
    
    def post_blind(player, blind_amount): 
        chips = player.get_chips()

        if chips <= blind_amount:
            actual_blind = chips
            player.set_all_in(True)
        else:
            actual_blind = blind_amount

        player.increment_chips(-actual_blind)

        return actual_blind

    def add_players(self, num_players): 
        for i in range(num_players): 
            newPlayer = Player(f"Player {i + 1}", 1000)
            self.players.append(newPlayer)
        
    def establish_positions(self, num_players): 
        self.dealer_index = random.randint(0, num_players - 1)
        self.players[self.dealer_index].set_position("Dealer")
        
        self.small_blind_index = (self.dealer_index + 1) % num_players
        self.players[self.small_blind_index].set_position("Small Blind")
        self.players[self.small_blind_index].increment_chips(-5)

        self.big_blind_index = (self.small_blind_index + 1) % num_players
        self.players[self.big_blind_index].set_position("Big Blind")
        self.players[self.big_blind_index].increment_chips(-10)

        self.under_the_gun_index = (self.big_blind_index + 1) % num_players
        self.players[self.under_the_gun_index].set_position("Under the Gun")

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
    
