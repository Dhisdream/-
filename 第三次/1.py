def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

phi = 1008 * 3642
sum = 0
e = 3
while e < phi:
    if gcd(e, phi) == 1 and gcd(e - 1, 1008) == 2 and gcd(e - 1, 3642) == 2:
        sum += e
    e = e + 2

print("result : ", sum)

