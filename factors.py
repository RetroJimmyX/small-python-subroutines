def factors(n):
    arr_fac = []
    for i in range(1,int(n**0.5)+1):
        if n%i == 0:
            arr_fac.append(i)
            arr_fac.append(n//i)
    return set(sorted(arr_fac))

while True:
    print(str(factors(int(input("Enter num: ")))))
