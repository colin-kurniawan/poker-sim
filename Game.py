from Card import Deck
from Player import Player
from Evaluator import Evaluator
from BettingAction import BettingAction
from PlayerManager import PlayerManager
import random

class Game: 
    def __init__(self):
       self.players = []
       self.pot = 0
       self.under_the_gun_index = 0
       self.small_blind_index = 0
       self.big_blind_index = 0
       self.current_bet = 0
       self.board = None

    def play_game(self, num_players): 
        player_manager = PlayerManager(self.players)
        player_manager.add_players(num_players)

        while True: 
            user_input = input("Play hand: Y/N: ")
            if user_input.strip().lower() == "y": 
                self.play_round(player_manager)
            else: 
                break
            
    def play_round(self, player_manager): 
        deck = Deck()
        self.board = deck.get_board(5)
        card_evaluator = Evaluator(self.board)
        player_manager.establish_positions(len(self.players))
        player_manager.deal_hands(deck)

        stages = {
            "preflop": self.preflop,
            "flop": self.flop,
            "turn": self.turn, 
            "river": self.river
        }

        for stage_name, stage_function in stages.items():
            if self.active_players_count() <= 1: 
                self.end_round()
                return 
            
            stage_function()
            
            betting_action = BettingAction(self.board, self.players, player_manager.get_under_the_gun_index(), player_manager.get_small_blind_index(), player_manager.get_big_blind_index(), self.pot)
            
            if stage_name == "preflop": 
                round_continues = betting_action.betting_round(player_manager.get_under_the_gun_index())
            else: 
                active_index = (player_manager.get_dealer_index() + 1) % len(self.players)

                while self.players[active_index].folded:
                    active_index = (active_index + 1) % len(self.players)

                round_continues = betting_action.betting_round(active_index)

            if not round_continues:
                self.end_round()
                return
            
            self.pot = betting_action.update_pot()
        
        self.winner(card_evaluator)
        player_manager.reset()

        self.check_for_zero_chips()
    
    def preflop(self): 
        print("\n----------Pre-Flop-----------")
        print(f"Pot: ${self.pot}")
        self.current_bet = 10
        print("-----------------------------")

    def flop(self): 
        print("\n----------Flop-----------")
        self.print_deck(3)
        print(f"Pot: ${self.pot}")
        self.current_bet = 0
        print("-----------------------------")
    
    def turn(self): 
        print("\n----------Turn-----------")
        self.print_deck(4)
        print(f"Pot: ${self.pot}")
        self.current_bet = 0
        print("-----------------------------")

    def river(self): 
        print("\n----------River-----------")
        self.print_deck(5)
        print(f"Pot: ${self.pot}")
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
        self.winner_aux(card_evaluator)
        
        winners = []
        best_hand_strength = 0

        for player in self.players:
            if player.folded: 
                continue
            else: 
                if player.get_hand_strength() > best_hand_strength:
                    winners = [player]
                    best_hand_strength = player.hand_strength
                elif player.hand_strength == best_hand_strength:
                    winners.append(player)

        if len(winners) == 1:
            print(f"\nWinner: {winners[0].name} ({winners[0].hand_name})\n")
            winners[0].increment_chips(self.pot)
        else:
            print("\nIt's a chopped pot between:")
            split_pot = self.pot/len(winners)
            for player in winners:
                print(f"{player.name} ({player.hand_name})")
                winners[0].increment_chips(split_pot)
    
    #Calculates hand strength for each active player
    def winner_aux(self, card_evaluator): 
        for player in self.players: 
            if player.folded: 
                continue
            else: 
                card_evaluator.hand_strength(player)
                print(f"\n{player.get_name()}'s Hand: {player.get_hand()}")

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
    
if __name__ == "__main__":
    game = Game()
    num_players = int(input("Enter number of players: "))
    game.play_game(num_players)