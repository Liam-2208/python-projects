import random
print("Welcome to the number guessing game")
print("The objective is to guess the number im thinking about")
print("I will give you clues after your guess")
def guess():
    num = int(input("Please Enter your guess "))
    return num
run = True

secretNumber = random.randint(1,100)
print("I have thought of a number from 1-100")
numGuessed=guess()
while run == True:
    if numGuessed < secretNumber:
        print("Guess is too low, guess higher!")
        numGuessed=guess()
    elif numGuessed == secretNumber:
        print("Thats exactly right!")
        run = False
    else:
        print("Guess is too high! Guess lower")
        numGuessed=guess()