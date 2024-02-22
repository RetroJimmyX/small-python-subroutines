def matched_count(arr1,arr2):
  '''Returns a score consisting of +1 for each match'''
  return sum(x == y for x, y in zip(arr1,arr2))
  # x==y evaluates to 1 for True which can be used as an integer in sum()
  # could use sum(2 for x==y ... to score 2 for each match

matched_count(["a","b","c","d"],["a","b","e","a"])

# https://www.codewars.com/kata/5a3dd29055519e23ec000074
