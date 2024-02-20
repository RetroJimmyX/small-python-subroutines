def rot13(message):
    encoded = ""
    for i in range(len(message)):
        ordchr = 0
        if message[i].islower():
            ordchr = (ord(message[i])+13-97)%26+97
        elif message[i].isupper():
            ordchr = (ord(message[i])+13-65)%26+65
        else:
            ordchr = ord(message[i])
        encoded = encoded + chr(ordchr)
    return encoded
# https://www.codewars.com/kata/530e15517bc88ac656000716
