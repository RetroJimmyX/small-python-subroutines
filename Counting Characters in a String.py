# My first function
def method1(s):
    letters = {}
    for i in range(len(s)):
        if s[i] in letters:
            letters[s[i]] += 1
        else:
            letters[s[i]] = 1
    return letters

# My improved function
def method2(s):
    return {char:s.count(char) for char in s}

# A pro coder's solution
from collections import Counter as method3

s= "eFwSdVEImDaGeovGahugQeOKauADHIISUcLprrhAWgXqpvUCYlQNmcQDagulYECtqceMdYeZyueuOeWNsZdptWEfvZTe"

print("Method 1:",method1(s))
print("Method 2:",method2(s))
print("Method 3:",method3(s))

# https://www.codewars.com/kata/52efefcbcdf57161d4000091
