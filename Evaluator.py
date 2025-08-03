class Evaluator: 
    def __init__(self, board): 
        self.board = board

    def sort_board_suit(self): 
        board_values_suit = {
            "♠": [], 
            "♥": [], 
            "♦": [],
            "♣": []
        }

        for card in self.board: 
            board_values_suit[card.get_suit()].append(card.get_rank())

        return board_values_suit

    def sort_board_num(self): 
        board_values_num = {
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
            "Q": [], 
            "K": [], 
            "A": []
        }
        
        for card in self.board: 
            board_values_num[card.get_rank()].append(card.get_rank())
        
        return board_values_num
    
    @staticmethod
    def sort_hand_suit(player_hand): 
        hand_values_suit = {
            "♠": [], 
            "♥": [], 
            "♦": [],
            "♣": []
        }

        for card in player_hand: 
            hand_values_suit[card.get_suit()].append(card.get_rank())
            
        return hand_values_suit

    @staticmethod
    def sort_hand_num(player_hand): 
        hand_values_num = {
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
            "Q": [], 
            "K": [], 
            "A": []
        }

        for card in player_hand: 
            hand_values_num[card.get_rank()].append(card.get_rank())

        return hand_values_num

    def hand_strength(self, player): 
        hand_values_suit = self.sort_hand_suit(player.get_hand())
        board_values_suit = self.sort_board_suit()

        hand_values_num = self.sort_hand_num(player.get_hand())
        board_values_num = self.sort_board_num()

        royal_value = Evaluator.is_royal(hand_values_suit, board_values_suit)
        if royal_value != 0:
            player.set_hand_strength(royal_value)
            player.set_hand_name("Royal Flush")
            return
        
        straight_flush_value = Evaluator.is_straight_flush(hand_values_suit, board_values_suit)
        if straight_flush_value != 0: 
            player.set_hand_strength(straight_flush_value)
            player.set_hand_name("Straight Flush")
            return

        quads_value = Evaluator.is_quads(hand_values_num, board_values_num)
        if quads_value != 0: 
            player.set_hand_strength(quads_value)
            player.set_hand_name("Quads")
            return 
        
        full_house_value = Evaluator.is_full_house(hand_values_num, board_values_num)
        if full_house_value != 0: 
            player.set_hand_strength(full_house_value)
            player.set_hand_name("Full House")
            return 
        
        flush_value = Evaluator.is_flush(hand_values_suit, board_values_suit)
        if flush_value != 0: 
            player.set_hand_strength(flush_value)
            player.set_hand_name("Flush")
            return 
        
        straight_value = Evaluator.is_straight(hand_values_num, board_values_num)
        if straight_value != 0: 
            player.set_hand_strength(straight_value)
            player.set_hand_name("Straight")
            return 
        
        trips_value = Evaluator.is_trips(hand_values_num, board_values_num)
        if trips_value != 0: 
            player.set_hand_strength(trips_value)
            player.set_hand_name("Trips")
            return 
        
        two_pair_value = Evaluator.is_two_pair(hand_values_num, board_values_num)
        if two_pair_value != 0: 
            player.set_hand_strength(two_pair_value)
            player.set_hand_name("Two Pair")
            return 
        
        pair_value = Evaluator.is_pair(hand_values_num, board_values_num)
        if pair_value != 0: 
            player.set_hand_strength(pair_value)
            player.set_hand_name("Pair")
            return

        player.set_hand_strength(Evaluator.highest(hand_values_num, board_values_num))
        player.set_hand_name("High Card")
        return 

    #Returns 1274
    @staticmethod
    def is_royal(hand, board): 
        royal_set = {"10", "J", "Q", "K", "A"}

        for suit in hand:
            combined = set(hand.get(suit) + board.get(suit, []))
            if royal_set.issubset(combined):
                return 1274
            
        return 0
        
    #Base: 1257 + Highest Card + Next / 10 + Next / 100 + Next / 1000 + Next / 10000
    #Between: 1262-1273
    #Lowest: A, 2, 3, 4, 5
    #Highest: A, K, Q, J, 10
    @staticmethod 
    def is_straight_flush(hand, board): 
        straight_sets = [
            ['A', '2', '3', '4', '5'],
            ['2', '3', '4', '5', '6'],
            ['3', '4', '5', '6', '7'],
            ['4', '5', '6', '7', '8'],
            ['5', '6', '7', '8', '9'],
            ['6', '7', '8', '9', '10'],
            ['7', '8', '9', '10', 'J'],
            ['8', '9', '10', 'J', 'Q'],
            ['9', '10', 'J', 'Q', 'K'],
            ['10', 'J', 'Q', 'K', 'A'],
        ]

        best_straight_flush = []
        ace_first_check = False

        for suit in hand:
            combined = set(hand.get(suit, []) + board.get(suit, []))
            
            if len(combined) >= 5:
                for straight in straight_sets:
                    if set(straight).issubset(combined):
                        best_straight_flush = straight
                        ace_first_check = (straight == ['A', '2', '3', '4', '5'])
    
        if len(best_straight_flush) != 0: 
            total = 0
            best_straight_flush.reverse()

            for i in range(0, 5, 1): 
                total += Evaluator.get_hand_value(best_straight_flush[i], ace_first_check) / (10 ** i)
            
            return 1257 + total 
            
        return 0


    #Base: 683 + (Quad Value * 10) * 4 + Next
    #Between: 766-1256
    #Lowest: 2, 2, 2, 2, 3
    #Highest: A, A, A, A, K
    @staticmethod 
    def is_quads(hand, board):
        all_ranks = []
        quad_value = None

        for rank in hand: 
            combined = hand.get(rank, []) + board.get(rank, [])
            if len(combined) >= 1: 
                all_ranks.append(rank)
            if len(combined) == 4: 
                quad_value = rank
        
        if not quad_value: 
            return 0
            
        kicker_values = []
        quad_numeric = Evaluator.get_hand_value(quad_value, False)

        for card in all_ranks: 
            if card != quad_value: 
                kicker_values.append(Evaluator.get_hand_value(card, False))
    
        kicker = max(kicker_values)

        return 683 + ((quad_numeric * 10) * 4) + kicker
        
    #Base: 236 + (Trips Value * 10) * 3 + Pair Value * 2
    #Between: 302-682
    #Lowest: 2, 2, 2, 3, 3
    #Highest: A, A, A, K, K
    @staticmethod 
    def is_full_house(hand, board): 
        trip_value = None
        pair_value = None

        for rank in hand:
            combined = hand.get(rank, []) + board.get(rank, [])
            if len(combined) >= 3:
                trip_value = rank
                break

        if not trip_value:
            return 0
        
        for rank in hand:
            if rank == trip_value:
                continue
            combined = hand.get(rank, []) + board.get(rank, [])
            if len(combined) >= 2:
                pair_value = rank
                break

        if trip_value and pair_value:
            trip_numeric = Evaluator.get_hand_value(trip_value, False)
            pair_numeric = Evaluator.get_hand_value(pair_value, False)
            return 236 + ((trip_numeric * 10) * 3) + (pair_numeric * 2)

        return 0
    
    #Base: 219 + Highest Card + Next / 10 + Next / 100 + Next / 1000 + Next / 10000
    #Between: 226-235
    #Lowest: 2, 3, 4, 5, 7
    #Highest: A, K, Q, J, 9
    @staticmethod
    def is_flush(hand, board): 
        for suit in hand:
            combined = hand.get(suit, []) + board.get(suit, [])

            if len(combined) >= 5:
                combined_list = []

                for num in combined: 
                    value = Evaluator.get_hand_value(num, False)
                    combined_list.append(value)

                combined_list = sorted(combined_list)
                combined_list.reverse()

                total = 0
                
                for i in range(0, 5, 1):
                    total += combined_list[i] / (10 ** i)
                return 219 + total 
        return 0
     
    #Base: 202 + Highest + Next / 10 + Next / 100 + Next / 1000 + Next / 10000
    #Between: 207-218
    #Lowest: A, 2, 3, 4, 5
    #Highest: 10, J, Q, K, A
    @staticmethod
    def is_straight(hand, board): 
        straight_sets = [
            ['A', '2', '3', '4', '5'],
            ['2', '3', '4', '5', '6'],
            ['3', '4', '5', '6', '7'],
            ['4', '5', '6', '7', '8'],
            ['5', '6', '7', '8', '9'],
            ['6', '7', '8', '9', '10'],
            ['7', '8', '9', '10', 'J'],
            ['8', '9', '10', 'J', 'Q'],
            ['9', '10', 'J', 'Q', 'K'],
            ['10', 'J', 'Q', 'K', 'A'],
        ]

        all_ranks = []

        for rank in hand: 
            combined = set(hand.get(rank, []) + board.get(rank, []))

            if len(combined) >= 1: 
                all_ranks.append(rank)
        
        best_straight = None
    
        for straight in straight_sets: 
            if set(straight).issubset(set(all_ranks)): 
                best_straight = straight
        
        if not best_straight: 
            return 0
        
        first_ace_check = False
        if best_straight == ['A', '2', '3', '4', '5']: 
            first_ace_check = True
        
        total = 0

        for i in range(len(best_straight)): 
            total += Evaluator.get_hand_value(best_straight[i], first_ace_check) / (10 ** i)

        return 202 + total


    #Base: 157 + (Trips Value * 3) + Next / 10 + Next / 100
    #Between: 163-201
    #Lowest: 2, 2, 2, 3, 4
    #Highest: A, A, A, K, Q
    @staticmethod
    def is_trips(hand, board): 
        all_ranks = []
        trip_value = None

        for rank in hand: 
            combined = hand.get(rank, []) + board.get(rank, [])

            if len(combined) >= 1: 
                all_ranks.append(rank)
            if len(combined) == 3: 
                trip_value = rank
        
        if not trip_value: 
            return 0
        
        all_rank_values = []

        for rank in all_ranks: 
            if rank != trip_value: 
                all_rank_values.append(Evaluator.get_hand_value(rank, False))
        
        all_rank_values.sort()
        
        kicker1 = all_rank_values[-1]
        kicker2 = all_rank_values[-2]

        trip_value_numeric = Evaluator.get_hand_value(trip_value, False)
        return 157 + (trip_value_numeric * 3) + (kicker1 / 10) + (kicker2 / 100)


    #Base: 90 + (High Pair Value) * 2 + (Pair Value / 100) * 2 + Next / 10000
    #Between 104-156 
    #Lowest: 2, 2, 3, 3, 4
    #Highest: A, A, K, K, Q
    @staticmethod
    def is_two_pair(hand, board): 
        all_ranks = []
        pair1_value = None
        pair2_value = None
        pair_check = False

        for rank in hand: 
            combined = hand.get(rank, []) + board.get(rank, [])
     
            if len(combined) >= 1: 
                all_ranks.append(rank)
            if len(combined) == 2: 
                pair1_value = rank
                pair_check = True
                hand_nums = list(hand.keys())
                start_index = hand_nums.index(rank)   

                for num in hand_nums[start_index + 1:]: 
                    combined = hand.get(num, []) + board.get(num, [])

                    if len(combined) >= 1:
                        all_ranks.append(num)
                    if len(combined) == 2: 
                        pair2_value = num
            
            if pair_check == True: 
                break
        
        if not pair1_value or not pair2_value: 
            return 0
        
        all_rank_values = []

        
        for rank in all_ranks: 
            if rank != pair1_value and rank != pair2_value: 
                all_rank_values.append(Evaluator.get_hand_value(rank, False))

        all_rank_values.sort()
        kicker = all_rank_values[-1]
        pair1_value = Evaluator.get_hand_value(pair1_value, False)
        pair2_value = Evaluator.get_hand_value(pair2_value, False)

        return 90 + (pair2_value) * 2 + (pair1_value / 100) * 2 + kicker / 1000

    #Base: 60 + (Pair Value * 2) + Next / 10 + Next / 100 + Next / 1000
    #Between 64-89 
    #Lowest: 2, 2, 3, 4, 5
    #Highest: A, A, K, Q, J
    @staticmethod
    def is_pair(hand, board): 
        all_ranks = []
        pair_value = None

        for rank in hand: 
            combined = hand.get(rank, []) + board.get(rank, [])

            if len(combined) >= 1: 
                all_ranks.append(rank)
            if len(combined) == 2: 
                pair_value = rank
        
        if not pair_value: 
            return 0
        
        all_rank_values = []

        for rank in all_ranks: 
            if rank != pair_value: 
                all_rank_values.append(Evaluator.get_hand_value(rank, False))
        
        all_rank_values.sort()
        pair_value = Evaluator.get_hand_value(pair_value, False)
        kicker1 = all_rank_values[-1]
        kicker2 = all_rank_values[-2]
        kicker3 = all_rank_values[-3]

        return 60 + pair_value * 2 + kicker1 / 10 + kicker2 / 100 + kicker3 / 1000 

    #Between 21-59
    #Lowest: 2, 3, 4, 5, 7
    #Highest: A, K, Q, J, 9
    @staticmethod
    def highest(hand, board): 
        all_ranks = []

        for rank in hand: 
            combined = set(hand.get(rank, []) + board.get(rank, []))

            if len(combined) >= 1: 
                all_ranks.append(Evaluator.get_hand_value(rank, False))
        
        all_ranks.sort()

        return all_ranks[-1] + all_ranks[-2] / 10 + all_ranks[-3] / 100 + all_ranks[-4] / 1000 + all_ranks[-5] / 10000


    @staticmethod
    def get_hand_value(card, ace_first_check): 
        if card == "J": 
            return 11
        elif card == "Q": 
            return 12
        elif card == "K": 
            return 13
        elif card == "A": 
            if ace_first_check: 
                return 1
            else: 
                return 14
        else: 
            return int(card)