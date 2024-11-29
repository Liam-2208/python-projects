global letter
letter = ""
def letter_to_number(letter):
    letters = "abcdefghijklmnopqrstuvwxyz"
    # find a number corresponding to a given letter
    number = letters.index(letter)
    return number

def number_to_letter(index):
    letters="abcdefghijklmnopqrstuvwxyz"
    return letters[index]

def shift(letter):
    n = letter_to_number(letter)
    return number_to_letter( (n+13) % 26 )

def rot13(string):
    ciphertext = ""
    for letter in string:
        ciphertext += shift(letter)
    return ciphertext

plaintext = "I love computing"

ciphertext = rot13(plaintext)
print(ciphertext)