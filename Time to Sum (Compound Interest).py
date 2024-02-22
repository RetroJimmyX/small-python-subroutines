def calculate_years(principal, interest, tax, desired):
  '''Returns the unit time required to reach a desired sum for principal investment for given interest and tax rates)'''
    years = 0
    while principal < desired:
        principal += principal * interest * (1 - tax)
        years += 1
    return years

##    The mathematical approach: 
##    if principal >= desired: return 0
##    return ceil(log(float(desired) / principal, 1 + interest * (1 - tax)))

# https://www.codewars.com/kata/563f037412e5ada593000114/solutions/python
