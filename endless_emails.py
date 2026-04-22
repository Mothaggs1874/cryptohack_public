from Crypto.Util.number import long_to_bytes, getPrime, bytes_to_long, isPrime
from math import gcd
from sympy.ntheory.modular import crt


def cube_root(y):
    left = 0
    right = y

    while left < right:
        mid = (left + right) // 2
        m = mid ** 3
        if m == y:
            return mid

        elif m < y:
            left = mid + 1

        else:
            right = mid

    return 0


n = []
c = []

with open("emails.txt", "r") as f:
    for line in f:
        l = line.rstrip()
        if l != "":
            if l[0] == "n":
                n.append(int(l[4:]))
            if l[0] == "c":
                c.append(int(l[4:]))



for j in range(0, 128):
    try_c = []
    try_n = []
    for i in range(0,7):
        if (2 ** i) & j > 0:
            try_n.append(n[i])
            try_c.append(c[i])

    x, mod = crt(try_n, try_c)
    r = cube_root(x)
    if r != 0:
        print(j)
        print(long_to_bytes(r))










