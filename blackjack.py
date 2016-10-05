import random
import time
import sys

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def get_float():
    # If the user tries to enter letters and shit...
    while True:
        try:
            return float(input("-> "))
        except ValueError:
            print("When I ask for a number, give me a number. "
                  "Come on! You had ONE JOB!")
        else:
            break  # how would we get here?


def validate_bet(user_input, user_cash):
    # If the user tries to bet negative money or more than they have, try again

    while user_input < 0 or user_input > user_cash:
        if user_input < 0:
            print("You can't bet negative money, asshole. Try again")
            user_input = get_float()
        elif user_input > user_cash:
            print("You can't bet more than you have, asshole. Try again")
            user_input = get_float()
        elif user_input < 10:
            print("The minimum bet is $10, asshole. Try again")
            user_input = get_float()
    return user_input


def validate_tip(user_input, user_cash):
    while user_input < 0 or user_input > user_cash:
        if user_input < 0:
            print("You can't tip negative money, asshole. Try again")
            user_input = get_float()
        elif user_input > user_cash:
            print("You don't even have that much to give, asshole. Try again")
            user_input = get_float()
    if user_input == 0:
        print("*Weeps quietly*")
    return user_input


def get_user_action():
    print("Hit or Stay? (type hit or stay and hit enter)")
    return input("-> ")


def validate_user_action(user_input):
    valid_actions = ["hit", "stay", "tip"]
    while str(user_input).lower() not in valid_actions:
        print("Please type either hit or stay")
        user_input = input("-> ")


def assemble_deck():
    deck = []  # an array of card dictionaries
    suits = ["S", "C", "D", "H"]
    face_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                   "J", "Q", "K", "A"]
    for suit in suits:
        for face_value in face_values:
            if face_value in ["J", "Q", "K"]:
                card_value = 10
            elif face_value == "A":
                card_value = [1, 11]
            else:
                card_value = int(face_value)
            deck.append({
                "Suit": suit,
                "Face Value": face_value,
                "Card Value": card_value,
                "Visible": True
                })
    return deck


def calculate_hand_score(hand):
    hand_score = {"Low": 0, "High": 0}  # maybe two options if there are aces
    ace_flag = False
    for card in hand:
        if card['Face Value'] == "A":
            ace_flag = True
            hand_score["Low"] += 1
            hand_score["High"] += 1
        else:
            # If no aces, both possible scores are the same
            # How can I do this better?
            hand_score["Low"] += card['Card Value']
            hand_score["High"] += card['Card Value']
    if ace_flag:
        if hand_score["High"] + 10 <= 21:  # Can we make an ace an 11?
            hand_score["High"] += 10
    return hand_score


def check_for_blackjack(hand):
    return len(hand) == 2 and calculate_hand_score(hand)["High"] == 21


def check_for_bust(hand):
    return calculate_hand_score(hand)["Low"] > 21


def display_dealer_hand():
    for card in dealer.hand:
        if card['Visible']:
            print("{} of {}".format(card['Face Value'], card['Suit']))
        else:
            print("(One card facedown)")


def display_player_hand(hand):
    for card in hand:
        print("{} of {}".format(card['Face Value'], card['Suit']))


def display_table():
    print("Currently, the dealer has:")
    for card in dealer.hand:
        if card['Visible']:
            print("{} of {}".format(card['Face Value'], card['Suit']))
        else:
            print("(One card facedown)")
    print("")
    for index, player in enumerate(players):
        print("Player {} has:".format(index))
        for card in player.hand:
            print("{} of {}".format(card['Face Value'], card['Suit']))


def cashout():
    print("Thanks for playing! You finished with ${}".format(bobby.cash))


class Player(object):
    def __init__(self):
        self.cash = 100.0
        self.bet = None
        self.hand = []
        self.hand_score = {"High": 0, "Low": 0}  # Can be two values with aces

    def place_bet(self):
        print("How much would you like to bet? Enter 0 to cash out")
        print("Minimum bet is $10")
        user_input = get_float()
        self.bet = validate_bet(user_input, self.cash)
        print("You bet {}".format(self.bet))

    def tip_dealer(self):
        print("How much would you like to tip me? Enter 0 to make me cry")
        user_input = get_float()
        self.cash -= validate_tip(user_input, self.cash)

    def perform_action(self):
        action = get_user_action()
        # Easter Egg!
        if action == "tip":
            self.tip_dealer()
        elif action == "hit":
            self.hand.append(dealer.deal_card())
            display_player_hand(self.hand)
        elif action == "stay":
            print("Playing it safe. Do you pee sitting down or something?")
        return action


class Dealer(object):
    def __init__(self):
        self.hand = []
        self.hand_score = {"High": 0, "Low": 0}  # Can be two values with aces
        self.tips = 0.0
        self.deck = []

    def shuffle_deck(self):
        print("Shuffling the deck...")
        time.sleep(2)
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        else:
            print("We ran out of cards... Go home, you're drunk")
            sys.exit()

    def deal_to_players(self):
        for player in players:
            player.hand.append(self.deal_card())

    def initial_deal(self):
        # Deal one to self face down
        self.hand.append(self.deal_card())
        self.hand[0]['Visible'] = False

        # Deal first card to players
        self.deal_to_players()

        # Deal second card to self face up
        self.hand.append(self.deal_card())

        # Deal card card to players
        self.deal_to_players()


def play_blackjack():
    while bobby.cash > 0:
        bobby.hand = []  # reset hands
        dealer.hand = []
        print("You have ${}".format(bobby.cash))
        dealer.deck = assemble_deck()
        # logger.debug("dealer's deck: {}".format(dealer.deck))
        dealer.shuffle_deck()
        bobby.place_bet()
        if bobby.bet == 0:
            cashout()
            sys.exit()
        dealer.initial_deal()
        display_table()
        if check_for_blackjack(bobby.hand):
            print("Blackjack!")
            bobby.cash += bobby.bet * 1.5
            continue
        else:
            while not (check_for_bust(bobby.hand)):
                action = bobby.perform_action()  # player hits/stays
                if action == "stay":
                    break
            if check_for_bust(bobby.hand):
                print("You busted!")
                bobby.cash -= bobby.bet
                continue
            else:
                # If the player didn't bust and stayed, it's the dealer's turn
                # Turn over the face down card
                dealer.hand[0]["Visible"] = True
                display_table()
                if check_for_blackjack(dealer.hand):
                    print("Dealer got Blackjack!")
                    bobby.cash -= bobby.bet
                else:
                    while True:
                        dealer.hand_score = calculate_hand_score(dealer.hand)
                        if check_for_bust(dealer.hand):
                            print("Dealer busted!")
                            bobby.cash += bobby.bet
                            break
                        if dealer.hand_score["Low"] >= 17 or \
                                dealer.hand_score["High"] >= 17:
                            print("Dealer stays")
                            break
                        else:
                            print("Dealer hits")
                            dealer.hand.append(dealer.deal_card())
                            display_dealer_hand()
        if not check_for_bust(dealer.hand):
            # Now both players have stayed or busted or black jacked
            # Here we will choose whether to use high or low score (aces)

            bobby.hand_score = calculate_hand_score(bobby.hand)
            if bobby.hand_score["High"] > 21:
                bobby.hand_score = bobby.hand_score["Low"]
            else:
                bobby.hand_score = bobby.hand_score["High"]
            if dealer.hand_score["High"] > 21:
                dealer.hand_score = dealer.hand_score["Low"]
            else:
                dealer.hand_score = dealer.hand_score["High"]
            display_table()
            if bobby.hand_score > dealer.hand_score:
                print("You won this round!")
                bobby.cash += bobby.bet
            elif bobby.hand_score == dealer.hand_score:
                print("It was a tie!")
            else:
                print("The dealer won this round!")
                bobby.cash -= bobby.bet
    if bobby.cash == 0:
        print("You ran out of cash, loser! lolololol")

print("Welcome to blackjack. I hope you're ready to lose money lololol")
players = []  # Future feature: Multiple players
bobby = Player()
players.append(bobby)
dealer = Dealer()

play_blackjack()
