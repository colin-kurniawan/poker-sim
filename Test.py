import unittest
from Evaluator import Evaluator
from Card import Card
from Player import Player
from Card import Deck

class TestEvaluator(unittest.TestCase): 
    
    def test_isRoyal(self):
        hand = {
            "♠": [], 
            "♥": [], 
            "♦": [],
            "♣": ["J", "K"]
        }
        board = {
            "♠": ["4", "5"], 
            "♥": [], 
            "♦": [],
            "♣": ["10", "Q", "A"]
        }
        result = Evaluator.is_royal(hand, board)
        print(f'Royal: {result}')
    
    def test_isStraightFlush(self):
        hand = {
            "♠": ["2", "3"], 
            "♥": [], 
            "♦": [],
            "♣": []
        }
        board = {
            "♠": ["4", "5", "6"], 
            "♥": [], 
            "♦": [],
            "♣": ["2", "3"]
        }
        result = Evaluator.is_straight_flush(hand, board)
        print(f'Straight Flush: {result}')
    
    def test_isQuads(self):
        hand = {
            "2": [],
            "3": [],
            "4": [], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q", "Q"], 
            "K": [], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": [], 
            "5": ["5"], 
            "6": ["6"],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q", "Q"], 
            "K": ["K"], 
            "A": []
        }
        result = Evaluator.is_quads(hand, board)
        print(f'Quads: {result}')

    def test_isFullHouse(self):
        hand = {
            "2": [],
            "3": [],
            "4": [], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": ["8"], 
            "9": [], 
            "10": ["10"], 
            "J": [], 
            "Q": [], 
            "K": [], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": ["4", "4"], 
            "5": ["5"], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": ["10", "10"], 
            "J": [], 
            "Q": [], 
            "K": [], 
            "A": []
        }
        result = Evaluator.is_full_house(hand, board)
        print(f'Full House: {result}')

    def test_isFlush(self):
        hand = {
            "♠": ["2", "3"], 
            "♥": [], 
            "♦": [],
            "♣": []
        }
        board = {
            "♠": ["K", "Q", "9"], 
            "♥": [], 
            "♦": [],
            "♣": ["2", "3"]
        }
        result = Evaluator.is_flush(hand, board)
        print(f'Flush: {result}')

    def test_isStraight(self):
        hand = {
            "2": [],
            "3": [],
            "4": [], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q"], 
            "K": ["K"], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": [], 
            "5": ["5"], 
            "6": ["6"],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": ["10"], 
            "J": ["J"], 
            "Q": [], 
            "K": [], 
            "A": ["A"]
        }
        result = Evaluator.is_straight(hand, board)
        print(f'Straight: {result}')

    def test_isTrip(self):
        hand = {
            "2": [],
            "3": [],
            "4": [], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q", "Q"], 
            "K": [], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": [], 
            "5": ["5"], 
            "6": ["6"],  
            "7": ["7"], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q"], 
            "K": ["K"], 
            "A": []
        }
        result = Evaluator.is_trips(hand, board)
        print(f'Trips: {result}')

    def test_TwoPair(self):
        hand = {
            "2": [],
            "3": [],
            "4": [], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q", "Q"], 
            "K": [], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": [], 
            "5": ["5"], 
            "6": ["6"],  
            "7": ["7"], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": [], 
            "K": ["K", "K"], 
            "A": []
        }
        result = Evaluator.is_two_pair(hand, board)
        print(f'Two Pair: {result}')
    
    def test_is_pair(self):
        hand = {
            "2": [],
            "3": [],
            "4": ["4"], 
            "5": [], 
            "6": [],  
            "7": [], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q"], 
            "K": [], 
            "A": []
        }
        board = {
            "2": [],
            "3": [],
            "4": [], 
            "5": ["5"], 
            "6": ["6"],  
            "7": ["7"], 
            "8": [], 
            "9": [], 
            "10": [], 
            "J": [], 
            "Q": ["Q"], 
            "K": ["K"], 
            "A": []
        }
        result = Evaluator.is_pair(hand, board)
        print(f'Pair: {result}')


if __name__ == "__main__":
    unittest.main()