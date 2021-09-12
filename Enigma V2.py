# --------------------------------------------------------------
# ROTORS FOR THE ENIGMA MACHINE
# Entry = ABCDEFGHIJKLMNOPQRSTUVWXYZ (rotor right side)
#         ||||||||||||||||||||||||||
# I     = EKMFLGDQVZNTOWYHXUSPAIBRCJ
# II    = AJDKSIRUXBLHWTMCQGZNPYFVOE
# III   = BDFHJLCPRTXVZNYEIWGAKMUSQO
# IV    = ESOVPZJAYQUIRHXLNFTGKDCMWB
# V     = VZBRGITYUPSDNHLXAWMJQOFECK
# link: http://users.telenet.be/d.rijmenants/en/enigmatech.htm
#
# START OF ENCRYPTION PROCESS
# ---------------------------------------------------------------

from string import ascii_lowercase

pluggedLetters = []


def plugging(options):
    plugged = []
    if options:
        x = 0
        print('Put two to be plugged together (ab)')
        while x < 10:
            plugged.append(tuple(input('>>').lower()))  # lets user configure the plugboard
            x += 1
    else:
        plugged = [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h'), ('i', 'j'), ('k', 'l'), ('m', 'n'), ('o', 'p'),
                   ('q', 'r'), ('s', 't')]
    return plugged


def plugboardSwitch(message, list1):
    # This function switches the letter according to the plug
    plugboardMessage = ''
    for i in range(0, len(message)):
        for j in range(len(list1)):
            if message[i] == list1[j][0]:  # Checks if the letter is equal to the first item of the tuple
                plugboardMessage = list1[j][1]  # Returns second item of the tuple
                break
            elif message[i] == list1[j][1]:  # Same but inverted
                plugboardMessage = list1[j][0]
                break
            else:
                plugboardMessage = message[i]  # If the message is not present in pluggedLetters, letter equals letter
    return plugboardMessage


def rotorStep(rotor):
    # This function is responsible for stepping the motor once
    rotor = list(rotor)
    hold = rotor[0]  # Holds the first item for appending later
    rotor.pop(0)  # Removes the first
    rotor.append(hold)  # Appends the first to last position
    rotor = ''.join(rotor)  # Transforms rotor into a string
    return rotor


def mirror(input_):
    # Function basically transforms input into a character with -4 less value
    if ascii_lowercase.find(input_) == -1:  # If not in alphabet, returns input_
        return input_
    number = ord(input_)
    output = number - 4  # Does the mirroring
    if output < 97:
        output = output + 26
    return chr(output)


def startConfig(choice):
    if choice:
        num1 = input('Start position of rotor 1: ')  # lets user configure the rotors starting position
        startPos(rotor1, int(num1))
        num2 = input('Start position of rotor 2: ')
        startPos(rotor2, int(num2))
        num3 = input('Start position of rotor 3: ')
        startPos(rotor3, int(num3))
        print('\n''\n')
    if not choice:
        startPos(rotor1, 0)
        startPos(rotor2, 0)
        startPos(rotor3, 0)


def startPos(rotor, startPos):
    # Start the rotors in a determined position
    global rotor1, rotor2, rotor3
    if startPos > 0:
        if rotor == rotor1:
            c = 1
        elif rotor == rotor2:
            c = 2
        elif rotor == rotor3:
            c = 3
        else:
            c = 0
        for i in range(startPos):
            new = rotorStep(rotor)
            rotor = new
        if c == 1:
            rotor1 = rotor
        elif c == 2:
            rotor2 = rotor
        elif c == 3:
            rotor3 = rotor
        return rotor
    else:
        yeet = 0
        return yeet


alphabet = ascii_lowercase
rotor1 = 'ekmflgdqvzntowyhxuspaibrcj'
rotor2 = 'ajdksiruxblhwtmcqgznpyfvoe'
rotor3 = 'bdfhjlcprtxvznyeiwgakmusqo'


# Put inside the tuples the letter, so, if A was plugged with B, it would be [(a,b)]

# cipherChar = rotor1[alphabet.find(c)]


def encrypt(rotor1, rotor2, rotor3):
    # Main encrypt function
    rotor1 = list(rotor1)
    rotor2 = list(rotor2)
    rotor3 = list(rotor3)
    message = input('Welcome to the Enigma Machine, please enter your code to be encrypted: ').lower()
    stepCount = 0
    stepCountR2 = 0
    encrypted = []
    for c in message:  # Begining of the encryption process
        if ascii_lowercase.find(c) == -1:
            encrypted.append(c)
        else:
            enigma = plugboardSwitch(c, pluggedLetters)
            enigma = rotor1[alphabet.find(enigma)]
            enigma = rotor2[alphabet.find(enigma)]
            enigma = rotor3[alphabet.find(enigma)]
            enigma = mirror(enigma)
            enigma = rotor3[alphabet.find(enigma)]
            enigma = rotor2[alphabet.find(enigma)]
            enigma = rotor1[alphabet.find(enigma)]
            enigma = plugboardSwitch(enigma, pluggedLetters)
            encrypted.append(enigma)
        stepCount += 1
        rotor1 = rotorStep(rotor1)
        if stepCount == 26:
            stepCount = 0
            rotor2 = rotorStep(rotor2)
            stepCountR2 += 1
            if stepCountR2 == 26:
                stepCountR2 = 0
                rotor3 = rotorStep(rotor3)

    finalMessage = ''.join(encrypted)
    print(finalMessage)
    output(finalMessage, 'e')


# ------------------------------
# Decryption functions
# ------------------------------


def rotorStepD(rotor):
    # Same as rotorStep, but inverse
    rotor = list(rotor)
    hold = rotor[-1]
    rotor.pop()
    rotor.insert(0, hold)
    rotor = ''.join(rotor)
    return rotor


def mirrorD(input):
    # Same as mirror, but reverse
    if ascii_lowercase.find(input) == -1:
        return input
    number = ord(input)
    if number < 97 or number > 122:
        print('Error in mirror')
    output = number + 4
    if output > 122:
        output = output - 26
    return chr(output)


def decrypt(rotor1, rotor2, rotor3):
    # Main decrypt function
    cipher = input("Type the encoded message (make sure Enigma's settings are correct): ")
    cipher = cipher[::-1]
    steps = len(cipher) - 1
    if steps >= 676:  # Sets the starting position of the rotors
        steps1 = steps % 26
        steps3 = steps // 676
        steps2 = steps3 // 26
        for y in range(steps2):
            rotor2 = rotorStep(rotor2)
        for z in range(steps1):
            rotor1 = rotorStep(rotor1)
        for m in range(steps3):
            rotor3 = rotorStep(rotor3)
    elif steps >= 26 and steps < 676:
        steps1 = steps % 26
        steps2 = steps // 26
        for y in range(steps2):
            rotor2 = rotorStep(rotor2)
        for z in range(steps1):
            rotor1 = rotorStep(rotor1)
    else:
        for z in range(steps):
            rotor1 = rotorStep(rotor1)
    decrypted = []
    i = 0
    for c in cipher:  # Start of decryption process
        if ascii_lowercase.find(c) == -1:
            decrypted.append(c)
        else:
            enigma = plugboardSwitch(c, pluggedLetters)
            enigma = alphabet[rotor1.find(enigma)]
            enigma = alphabet[rotor2.find(enigma)]
            enigma = alphabet[rotor3.find(enigma)]
            enigma = mirrorD(enigma)
            enigma = alphabet[rotor3.find(enigma)]
            enigma = alphabet[rotor2.find(enigma)]
            enigma = alphabet[rotor1.find(enigma)]
            enigma = plugboardSwitch(enigma, pluggedLetters)
            decrypted.append(enigma)
        rotor1 = rotorStepD(rotor1)
        if i != 0 and len(cipher) % 26 == i % 26:  # 26 - (len(message) % 26) ----------------------------- error
            rotor2 = rotorStepD(rotor2)
        if i % 676 == 0 and i != 0 and len(cipher) % 676 == i and len(cipher) >= 676:
            rotor3 = rotorStepD(rotor3)
        i += 1

    finalMessage = ''.join(decrypted)
    finalMessage = finalMessage[::-1]
    print(finalMessage)
    output(finalMessage, 'd')


def start():
    # Startup interface to select which process will be engaged
    global pluggedLetters

    print("Welcome to Theo's Enigma Machine"'\n')
    pChoice = input('Do you wish to configure the letter plugging? (Y/N)''\n''>>').lower()
    if pChoice == 'y':
        pluggedLetters = plugging(True)
    else:
        pluggedLetters = plugging(False)

    sChoice = input('Do you wish to configure the start position of the rotors? (Y/N)''\n''>>').lower()
    if sChoice == 'y':
        startConfig(True)
    else:
        startConfig(False)

    choice = input('\n''Type E for encryption''\n''Type D for decryption''\n''>>').lower()
    if choice == 'e':
        encrypt(rotor1, rotor2, rotor3)
    elif choice == 'd':
        decrypt(rotor1, rotor2, rotor3)
    else:
        print('Invalid option''\n''\n''\n')
        start()


def output(string, mode):
    myFile = open('output.txt', 'w') # prints out and writes in .txt
    if mode == 'e':
        myFile.write('Encrypted message: ' + string)
    elif mode == 'd':
        myFile.write('Decrypted message: ' + string)


start()
