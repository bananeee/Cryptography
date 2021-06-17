from math import sqrt
from prime import *
# Extended Euclidean algorithm


def extended_gcd(aa, bb):
    """extended euclid algorithm

    Args:
        aa : [description]
        bb : [description]

    """
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(
            lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


def gcd(x, y):
    while(y):
        x, y = y, x % y

    return x


def modinv(a, m):
    """modular inverse a^-1 mod m

    Args:
        a: input number
        m : prime

    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def modexp(x, y, p):
    """modular exponential x^y mod p

    Returns:
        [type]: [description]
    """
    res = 1     # Initialize result
    # Update x if it is more than or equal to p
    x = x % p
    if (x == 0):
        return 0

    while (y > 0):
        if ((y & 1) == 1):
            res = (res * x) % p

        y = y >> 1
        x = (x * x) % p

    return res


def findPrimefactors(s, n):
    # Print the number of 2s that divide n
    while (n % 2 == 0):
        s.add(2)
        n = n // 2

    # n must be odd at this po. So we can
    # skip one element (Note i = i +2)
    for i in range(3, int(sqrt(n)), 2):

        # While i divides n, print i and divide n
        while (n % i == 0):
            s.add(i)
            n = n // i

    # This condition is to handle the case
    # when n is a prime number greater than 2
    if (n > 2):
        s.add(n)


def primeFactors(n):
    arr = []
    if(n % 2 == 0):
        arr.append(2)

    while n % 2 == 0:
        n = n/2

    for i in range(3, int(sqrt(n)+1), 2):
        while n % i == 0:
            if(len(arr) == 0):
                arr.append(i)
            elif(arr[len(arr)-1] != i):
                arr.append(i)
            n = n/i
    if n > 2:
        arr.append(int(n))
    return arr


def primitive(n):
    # s = set()

    # Find value of Euler Totient function of n. Since n is a prime number, the
    # value of Euler Totient function is n-1 as there are n-1 relatively prime numbers.
    phi = n - 1
    # Find prime factors of phi and store in a set
    # findPrimefactors(s, phi)

    s = primeFactors(phi)

    # Check for every number from 2 to phi
    for r in range(2, phi + 1):

        # Iterate through all prime factors of phi and check if we found a power with value 1
        flag = False
        for it in s:

            # Check if r^((phi)/primefactors) mod n is 1 or not
            if (modexp(r, phi // it, n) == 1):

                flag = True
                break

        # If there was no power with value 1.
        if (flag == False):
            return r

    # If no primitive root found
    return -1

# double function


def ecc_double(x1, y1, p, a):
    s = ((3*(x1**2) + a) * modinv(2*y1, p)) % p
    x3 = (s**2 - x1 - x1) % p
    y3 = (s*(x1-x3) - y1) % p
    return (x3, y3)

# add function


def ecc_add(x1, y1, x2, y2, p, a):
    s = 0
    if (x1 == x2):
        s = ((3*(x1**2) + a) * modinv(2*y1, p)) % p
    else:
        s = ((y2-y1) * modinv(x2-x1, p)) % p
    x3 = (s**2 - x1 - x2) % p
    y3 = (s*(x1 - x3) - y1) % p
    return (x3, y3)


def double_and_add(multi, generator, p, a):
    (x3, y3) = (0, 0)
    (x1, y1) = generator
    (x_tmp, y_tmp) = generator
    init = 0
    for i in str(bin(multi)[2:]):
        if (i == '1') and (init == 0):
            init = 1
        elif (i == '1') and (init == 1):
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x3, y3) = ecc_add(x1, y1, x3, y3, p, a)
            (x_tmp, y_tmp) = (x3, y3)
        else:
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x_tmp, y_tmp) = (x3, y3)
    return (x3, y3)

def convertToInt(s):
    sum = 0
    for i in range(0, len(s)):
        sum += ((ord(s[i]) - ord('a')) * 24**i)
    return sum

def convertToString(n):
    s = ""
    while n > 0:
        s = s + chr(n % 24 + ord('a'))
        n = n // 24
    return s

# print(primitive)
