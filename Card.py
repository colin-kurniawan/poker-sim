import random

class Card: 
    def __init__(self, suit, rank): 
        self.suit = suit
        self.rank = rank

    def get_suit(self): 
        return self.suit

    def get_rank(self): 
        return self.rank
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()

class Deck: 
    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self): 
        self.deck = []
        for suit in Deck.SUITS:
            for rank in Deck.RANKS: 
                self.deck.append(Card(suit, rank)) 
        self.board = None

    def deal(self): 
        index = random.randint(0, len(self.deck) - 1)
        card1 = self.deck[index]
        self.deck.pop(index)
        index = random.randint(0, len(self.deck) - 1)
        card2 = self.deck[index]
        self.deck.pop(index)
        return [card1, card2]
    
    def get_board(self, cards): 
        board = [] 

        for i in range(cards): 
            index = random.randint(0, len(self.deck) - 1)
            card = self.deck[index]
            self.deck.pop(index)
            board.append(card)     
        
        self.board = board

        return board
    
    def print_deck(self, num_cards): 
        print(self.board[0:num_cards])

    def __str__(self): 
        return f"Board: {self.board}"
