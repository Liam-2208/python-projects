import random
import os
import time

# currently the value of the "score" and "dealer_score" variables aren't calculated

def get_value(card, score):
    try:
        return int(card) # if the card is just a number it will return that to be added to the player's current score
    except:
        if card != "A": # if the card is a J Q or K it will return 10
            return 10
        if score + 11 <= 21: # returns 11 for an ace if it won't make player go bust
            return 11
        else:
            return 1 # returns 1 for an ace if 1 would make dealer go bust

def round(hand, score, dealer_hand, dealer_score, deck):
    while True and len(deck) != 0: # manages player turn
        print(f"Your current hand is {hand} with a score of {score}")
        if score > 21: # breaks loop if you go bust
            break
        player_choice = input("Hit (H) or Stand (S): ").lower() # takes player choice
        
        if player_choice == "h":
            card = deck.pop() # takes the card off the top of the deck
            hand.append(card) # adds the card to the player's hand
            score += get_value(card, score) #adds new card to player's score
            
            print(f"You picked up: {card}")
            time.sleep(1)
            os.system("cls")
        else:
            break
    
    while dealer_score < 17 and len(deck) != 0: # manages dealers turn
        card = deck.pop() # takes the card off the top of the deck
        dealer_hand.append(card) # adds the card to the dealers's hand
        dealer_score += get_value(card, dealer_score) #adds new card to dealer's score
    
    return hand, score, dealer_hand, dealer_score, deck

def win(money, bet):
    money += bet*2
    return money

def tie():
    money += bet
    return money

# MAIN PROGRAM

print("""Automatic Jackblack Player
--------------------------""")
money = int(input("Input starting money: "))
os.system("cls")
games = 0
blackjack = 0
game_end = 0
bust = 0

deck = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]*4 # creates the cards that will be in the deck
random.shuffle(deck) # shuffles the deck

while True:
    print("""Automatic Jackblack Player
--------------------------""")
    hand = []
    score = 0
    dealer_hand = []
    dealer_score = 0

    print(f"Your money: {money}")
    bet = int(input("Input bet: "))
    money -= bet

    while True and len(deck) != 0: # this controls if a round is active or not
        hand, score, dealer_hand, dealer_score, deck = round(hand, score, dealer_hand, dealer_score, deck)
        break
    print(f"""-------------------------------------------------")
Your Score: {score}\nDealer Score: {dealer_score}""")
    
    if score > dealer_score and score < 22 and dealer_score < 22: # win
        if score == 21:
            print("You've won with a blackjack!")
            blackjack += 0
        else:
            print(f"You've won by {score - dealer_score}")
            game_end = 0
        money = win(money, bet)
    elif score < dealer_score and score < 22 and dealer_score < 22: # loss
        if dealer_score == 21:
            print("You lost as the dealer got a blackjack")
            game_end = 0
        else:
            print(f"You've lost by {dealer_score - score}")
            game_end = 0
    elif score == dealer_score and score < 22 and dealer_score < 22: # tie
        print("You have tied with the dealer")
        if score == 21:
            blackjack += 1
        else:
            game_end += 1
        money = tie(money, bet)
    
    if score > 21 and dealer_score > 21:
        print("Both you and the dealer have gone bust") # tie
        bust += 1
        money = tie(money, bet)
    elif score > 21:
        print("You have lost as you have gone bust") # loss
        bust += 1
    elif dealer_score > 21:
        print("You win because the dealer has gone bust") # win
        if score == 21:
            blackjack += 1
        else:
            game_end += 1
        money = win(money, bet)
    
    games += 1

    if len(deck) < 1:
        print("The deck has run out of cards")
        break

    continue_quit = input("Press ENTER to continue or type QUIT to quit: ")
    if continue_quit != "":
        break
    os.system("cls")

print(f"""You played {games} game(s).
You got {blackjack} blackjack(s).
You got {game_end} game(s) that you didn't get blackjack or bust.
You bust {bust} time(s).""")