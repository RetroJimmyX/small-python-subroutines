def queue_time(customers, n):
  '''For a given queue of customers where each customer takes the integer units
  of time to process, returns how long to process all customers using n tills.'''
    tills = [0]*n
    while len(customers) > 0:
        tills.sort()
        tills[0] += customers.pop(0)
    return max(tills)
