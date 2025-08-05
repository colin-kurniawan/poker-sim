from PotManager import PotManager

class BettingAction:
    def __init__(self, board, players, under_the_gun_index, small_blind_index, big_blind_index, pot_manager): 
        self.board = board
        self.players = players
        self.under_the_gun_index = under_the_gun_index
        self.small_blind_index = small_blind_index
        self.big_blind_index = big_blind_index
        self.current_bet = 0
        self.num_players = len(self.players)
        self.pot_manager = pot_manager

    def betting_round(self, starting_index): 
        current_player_index = starting_index
        active_players = sum(1 for player in self.players if player.folded == False)
        player_to_reach_index = sum(1 for player in self.players if player.folded == False)
        action_count = 0

        while True:
            player = self.players[current_player_index]
            
            if action_count == player_to_reach_index:
                break
            
            if player.folded:
                current_player_index = (current_player_index + 1) % self.num_players
                continue

            if player.all_in: 
                action_count += 1
                continue
            
            action = self.get_available_options(player)

            if action == "fold": 
                self.fold(current_player_index)
                active_players -= 1
                if active_players == 1: 
                    return False
                action_count += 1

            elif action == "bet":
                self.bet(current_player_index) 
                player_to_reach_index = sum(1 for player in self.players if player.folded == False)
                action_count = 1

            elif action == "call":
                self.call(current_player_index)
                action_count += 1

            elif action == "all-in":
                self.all_in(current_player_index)
                player_to_reach_index = sum(1 for player in self.players if player.folded == False)
                action_count = 1

            elif action == "check":
                action_count += 1

            else:
                print("Invalid option")
                continue

            current_player_index = (current_player_index + 1) % self.num_players

        return True


    def bet(self, current_player_index):
        player = self.players[current_player_index]
        player_range_chips = player.get_chips()

        while True: 
            try: 
                bet_size = int(input(f"\n{player.get_name()} (Chips: {player.get_chips()}): How much are you betting? "))
                
                if bet_size < player_range_chips and bet_size > 0: 
                    player.increment_chips(bet_size * -1)
                    player.amount_contributed(bet_size)
                    self.pot_manager.add_bet(bet_size)
                    self.current_bet = bet_size
                    break
                else: 
                    raise ValueError
            except ValueError:
                print("Invalid Bet Size")
                continue 

    def call(self, current_player_index): 
        player = self.players[current_player_index]

        player.increment_chips(self.current_bet * -1)
        player.amount_contributed(self.current_bet)

        self.pot_manager.add_bet(self.current_bet)

    def fold(self, current_player_index): 
        self.players[current_player_index].folded = True


    def all_in(self, current_player_index): 
        player = self.players[current_player_index]

        all_in_size = player.get_chips()

        player.increment_chips(all_in_size * -1)
        player.set_all_in()
        player.amount_contributed(all_in_size)

        self.pot_manager.add_bet(all_in_size)
        self.current_bet = all_in_size
        
    
    def active_player_count(self): 
        return self.active_players

    def update_pot(self): 
        return self.main_pot
    
    def get_available_options(self, player): 
        player_chips = player.get_chips()

        if self.current_bet == 0: 
            while True: 
                try:
                    action = input(f"\n{player.name} (Chips: {player.get_chips()}): Bet, All-in, Check or Fold? ").strip().lower()
                    if action != "bet" and action != "all-in" and action != "fold" and action != "check":
                        raise ValueError
                    return action 
                except ValueError: 
                    print("Invalid Option")
                    continue
        else: 
            if player_chips < self.current_bet: 
                while True: 
                    try:
                        action = input(f"\n{player.name} (Chips: {player.get_chips()}): All-in, or Fold? ").strip().lower()
                        if action != "all-in" and action != "fold":
                            raise ValueError
                        return action 
                    except ValueError: 
                        print("Invalid Option")
                        continue
            else: 
                while True: 
                    try:
                        action = input(f"\n{player.name} (Chips: {player.get_chips()}): Bet, Call, All-in, or Fold? ").strip().lower()
                        if action != "bet" and action != "call" and action != "all-in" and action != "fold":
                            raise ValueError
                        return action 
                    except ValueError: 
                        print("Invalid Option")
                        continue
            