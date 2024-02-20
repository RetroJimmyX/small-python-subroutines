def disemvowel(s):
    return "".join(x for x in s if x not in "aeiou")

print(disemvowel("This function uses lifst comprehension".))
