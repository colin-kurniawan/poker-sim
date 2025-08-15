from Card import Deck
from Player import Player
from Evaluator import Evaluator
from BettingAction import BettingAction
from PlayerManager import PlayerManager
from PotManager import PotManager
import random

class Game: 
    def __init__(self):
       self.players = []
       self.main_pot = 0
       self.side_pot = []
       self.under_the_gun_index = 0
       self.small_blind_index = 0
       self.big_blind_index = 0
       self.current_bet = 0
       self.board = None
       self.pot_manager = PotManager()
       self.hand_number = 1 

    def play_game(self, num_players): 
        player_manager = PlayerManager(self.players, self.pot_manager)
        player_manager.add_players(num_players)

        print("\nYou will be Player 1\n")

        while True: 
            user_input = input("\nPlay hand: Y/N: ")
            if user_input.strip().lower() == "y": 
                self.play_round(player_manager)
            else: 
                break
            
    def play_round(self, player_manager): 
        deck = Deck()
        self.board = deck.get_board(5)
        card_evaluator = Evaluator(self.board)
        player_manager.set_card_evaluator(card_evaluator)
        player_manager.establish_positions(len(self.players), self.hand_number)
        self.main_pot = self.pot_manager.update_main_pot()
        player_manager.deal_hands(deck)
        self.get_hand_number()

        stages = {
            "Pre-Flop": 0,
            "Flop": 3,
            "Turn": 4, 
            "River": 5
        }

        for stage_name, cards in stages.items():
            if self.active_players_count() <= 1: 
                self.end_round()
                return

            self.round(stage_name, cards, player_manager)
            
            betting_action = BettingAction(self.board, self.players, player_manager.get_under_the_gun_index(), player_manager.get_small_blind_index(), player_manager.get_big_blind_index(), self.pot_manager)
            
            if stage_name == "Pre-Flop": 
                round_continues = betting_action.betting_round(player_manager.get_under_the_gun_index())
            else: 
                active_index = (player_manager.get_dealer_index() + 1) % len(self.players)

                while self.players[active_index].folded:
                    active_index = (active_index + 1) % len(self.players)

                round_continues = betting_action.betting_round(active_index)

            if not round_continues:
                self.end_round()
                return
            
            self.main_pot = self.pot_manager.update_main_pot()
        
        self.hand_number += 1
        self.winner(card_evaluator)
        player_manager.reset()
        self.check_for_zero_chips()
    
    def round(self, round_name, cards_shown, player_manager): 
        print(f"\n----------{round_name}-----------")
        self.print_deck(cards_shown)
        print(f"Pot: ${self.main_pot}")
        if round_name == "Pre-Flop": 
            self.current_bet = 10
            player_manager.print_blinds()
        else: 
            self.current_bet = 0
        print("-----------------------------")

    def end_round(self):
        player_index = self.end_round_aux()
        print(f"{self.players[player_index].getName()} wins {self.pot} chips")
        self.players[player_index].increment_chips(self.pot)
        self.pot = 0
        self.current_bet = 0 

    #Finds index of last remaining player 
    def end_round_aux(self): 
        for i in range(len(self.players)): 
            if not self.players[i].folded:
                return i

    def winner(self, card_evaluator): 
        pots = self.winner_aux()
        all_winners = set()

        for pot,players_eligible in pots.items(): 
            winners = []
            best_hand_strength = 0

            for player in players_eligible: 
                card_evaluator.hand_strength(player)
                player_hand_strength = player.get_hand_strength()

                if player_hand_strength > best_hand_strength: 
                    best_hand_strength = player_hand_strength
                    winners = [player]
                elif player_hand_strength == best_hand_strength: 
                    winners.append(player)
            
            if len(winners) == 1: 
                player = winners[0]
                player.increment_chips(pot)
                player.add_chips_won(pot)
            else: 
                split_pot = pot / len(winners)
                for player in winners: 
                    player.increment_chips(split_pot)
                    player.add_chips_won(split_pot)
            
            for player in winners: 
                if player not in all_winners: 
                    all_winners.add(player)

        for player in all_winners: 
            print(f"\n{player.get_name()} won {player.get_chips_won()} chips")
            print(f"\n{player.get_name()}'s Hand: {player.get_hand()}")

    def winner_aux(self):
        contributions = {}

        for player in self.players:
            if player.get_amount_contributed() > 0:
                contributions[player] = player.get_amount_contributed()

        unique_levels = sorted(set(contributions.values()))
        pot_levels = {}

        prev_level = 0
        remaining_players = set(contributions.keys())

        for level in unique_levels:
            level_players = {p for p in remaining_players if contributions[p] >= level}
            pot_amount = (level - prev_level) * len(level_players)

            if pot_amount > 0 and level_players:
                pot_levels[pot_amount] = {p for p in level_players if not p.folded}  # Only allow active players to win

            prev_level = level
            remaining_players = level_players

        return pot_levels

    def print_deck(self, num_cards):
        print(self.board[:num_cards])

    def active_players_count(self): 
        active_count = 0
        for player in self.players: 
            if not player.folded: 
                active_count += 1
        return active_count
    
    def check_for_zero_chips(self): 
        self.players = [p for p in self.players if p.get_chips() > 0]

    def get_hand_number(self): 
        print(f"\n----------Hand #{self.hand_number}-----------\n")
    
if __name__ == "__main__":
    game = Game()
    num_players = int(input("\nEnter number of players: "))
    game.play_game(num_players)