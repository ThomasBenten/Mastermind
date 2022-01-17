import random, time

algorithmList = ["1: Human", "2: Smart", "3: Bruno"]

def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput

def generateSC(length):
    secretCode = []
    for i in range(0, length):
        secretCode.append(str(random.randint(1, 8)))
    #print("DEBUG: secretCode =", secretCode)
    return secretCode

def userGuess():
    while True:
        guess = inputNumber("Guess: ")

        if "0" not in str(guess) and "9" not in str(guess):  # Check if the user's guess are only numbers 1-8
            if len(str(guess)) == SClen:  # Check if the user's guess is the same length as the SC
                return guess
            else:
                print("You have to enter", SClen, "numbers.")
                continue  # Let user enter new guess
        else:
            print("Only numbers 1-8 are allowed.")
            continue  # Let user enter new guess

def checkGuess(guess, SC):
    SCtemp = SC[:]
    guessArray = list(str(guess))
    contains = 0
    correct = 0

    # Find how many numbers are in the correct place
    for i in range(0, SClen):
        if guessArray[i] == SCtemp[i]:
            correct += 1
            guessArray[i] = "0"
            SCtemp[i] = "0"

    # Find how many numbers are in the SC
    for i in range(0, SClen):
        if guessArray[i] != "0" and guessArray[i] in SCtemp:
            contains += 1
            SCtemp[SCtemp.index(guessArray[i])] = "0"
            guessArray[i] = "0"

    print("Correct:", correct, "Contains:", contains)
    return [correct, contains]

# Main loop
while True:
    guessCount = 0
    results = [0, 0]

    print("_______________________")
    print("Welcome to MasterMind!")

    # Make secret code (SC)
    SClen = inputNumber("Length of secret code: ")
    SC = generateSC(SClen)

    print()
    print(*algorithmList, sep=" | ")

    while True:
        algorithm = inputNumber("What algorithm (number)? ")  #Ask what algorithm

        match algorithm:
            case 1:  #Human
                while results[0] != SClen:  #While user hasn't won, guess again
                    guess = userGuess()
                    results = checkGuess(guess, SC)
                    guessCount += 1
                print("That's correct! You took", guessCount, "guesses.")
                break

            case 2:  #Smart
                useTimer = inputNumber("Amount of repetitions: ")
                totguesses = 0
                tottime = 0
                for i in range(0, useTimer):
                    t1 = time.perf_counter()
                    # Generate all possible guesses
                    guessCount = 0
                    results = (0, 0)
                    possibleGuesses = list(range(10**(SClen-1), 10**SClen))
                    for i in range(0, len(possibleGuesses)):
                        possibleGuesses[i] = str(possibleGuesses[i])
                    possibleGuesses = [x for x in possibleGuesses if "9" not in x and "0" not in x]

                    while results[0] != SClen:  #Check if guessed correctly
                        # Submit a random guess from possible guesses
                        print("\nPossible guesses:", len(possibleGuesses))
                        guess = random.choice(possibleGuesses)
                        guessCount += 1
                        print("Guessed:", guess)
                        results = checkGuess(guess, SC)

                        possibleGuesses.remove(guess)  #Remove what is guessed from possible guesses

                        goodGuesses = []

                        for possibleGuess in possibleGuesses:  #Loop through all possible guesses
                            possibleGuessArray = list(str(possibleGuess))
                            guessArray = list(str(guess))
                            correct = 0
                            contains = 0

                            # Check how many numbers with same index are equal (guess and possible guess)
                            for i in range(0, SClen):
                                if possibleGuessArray[i] == guessArray[i]:
                                    correct += 1
                                    guessArray[i] = "0"
                                    possibleGuessArray[i] = "0"

                            for i in range(0, SClen):
                                if possibleGuessArray[i] != "0" and possibleGuessArray[i] in guessArray:
                                    contains += 1
                                    guessArray[guessArray.index(possibleGuessArray[i])] = "0"
                                    possibleGuessArray[i] = "0"

                            if correct == results[0] and contains == results[1]:
                                goodGuesses.append(possibleGuess)

                        possibleGuesses = goodGuesses[:]

                    t2 = time.perf_counter()
                    print(t2 - t1)
                    tottime += t2 - t1
                    totguesses += guessCount
                    print("That's correct! It took", guessCount, "guesses.")
                    SC = generateSC(SClen)
                print("That took an average of ", totguesses/useTimer, " guesses. A total of ", tottime, " seconds, with an average of ", tottime/useTimer, " seconds per run")
                break

            case 3:  #Bruno
                break

            case _:
                print("That algorithm (number) doesn't exist! Try again.")
                continue  #Ask what algorithm again
