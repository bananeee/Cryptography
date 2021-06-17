from prime import generate_prime_number, is_prime, randrange
from support import *
import math


def is_square(i):
    return i == math.isqrt(i) ** 2


def findFirstPoint(a, b, p):
    x = 0
    while True:
        f = x**3 + a*x + b
        if is_square(f):
            y = int(sqrt(f))
            return (x, y)
        else:
            x += 1
    return


def ecc_encrypt(M, a, b, p, P, B):
    # M = double_and_add(x, P, p, a)
    print("M:", M)
    k = randrange(1, 100, 1)

    M1 = double_and_add(k, P, p, a)
    M2 = ecc_add(M[0], M[1], double_and_add(k, B, p, a)[
                 0], double_and_add(k, B, p, a)[0], p, a)
    return M1, M2


def ecc_decrypt(M1, M2, s, p, a):
    return ecc_add(M2[0], M2[1], double_and_add(s, M1, p, a)[0], -double_and_add(s, M1, p, a)[0], p, a)


def ecc_signature(d, a, n, p, M, P):
    r1 = 0
    s1 = 0
    while True:
        k = randrange(1, 10000, 1)
        (x1, y1) = double_and_add(k, P, p, a)
        r1 = x1 % n
        if r1 == 0:
            continue
        h = M[0]
        s1 = s1 = ((h + d*r1)*modinv(k, n)) % n
        if s1 == 0:
            continue
        break
    return (r1, s1)


def ecc_verify(s, r, a, n, M, P, Q):
    w = modinv(s, n)
    h = M[0]
    u1 = (h*w) % n
    u2 = (r*w) % n
    uP = double_and_add(u1, P, n, a)
    uQ = double_and_add(u2, Q, n, a)
    T = ecc_add(uP[0], uP[1], uQ[0], uQ[1], p, a)
    return T[0] == r

if __name__ == "__main__":
    # a = 53
    # b = 7
    # p = 1114597119506223026265579259036275469126397408411
    # P = findFirstPoint(a, b, p)

    # s = int(input("Enter secret key:"))  # secret key

    # M = input("Enter point to encrypt:")
    # M = tuple(int(x.strip()) for x in M.split(','))

    # # print(s, M, p, a)
    # B = double_and_add(s, P, p, a)

    # print("Public key is (a, b, p, P, B): (", a,
    #       ",", b, ",", p, ",", P, ",", B, ")")
    # print("Private key is (s):", s)

    # M1, M2 = ecc_encrypt(M, a, b, p, P, B)

    # print("EEC encryption is(", M1, ",", M2, ")")
    # print("EEC decryption is", ecc_decrypt(M1, M2, s, p, a))
    
    
    a = 53
    b = 7
    p = 1114597119506223026265579259036275469126397408411
    n = 1114597119506223026265580072500994466839748057413
    P = findFirstPoint(a, b, p)

     # NOTE: Alice
    s = int(input("Enter Alice secret key:")) 
    B = double_and_add(s, P, p, a)

    print("Public key of Alice is (a, b, p, P, B): (", a,
          ",", b, ",", p, ",", P, ",", B, ")")
    print("Private key of Alice is (s):", s)
    print("--------")
    
    # NOTE: Bob
    d = int(input("Enter Bob secret key:")) 
    Q = double_and_add(d, P, p, a)
    
    print("Public key of Bob is (a, b, p, P, B): (", a,
          ",", b, ",", p, ",", P, ",", B, ")")
    print("Private key of Bob is (d):", d)
    print("--------")

    print("Alice want to send message to Bob")
    M = input("Enter point to encrypt:")
    M = tuple(int(x.strip()) for x in M.split(','))
    
    M1, M2 = ecc_encrypt(M, a, b, p, P, B)
    sig = ecc_signature(d, a, n, p, M, P)

    r, s = sig

    print("Alice send to Bob coded message:", M1, ",", M2, ")")
    print("--------")

    ver = ecc_verify(s, r, a, n, M, P, Q)
    R = ecc_decrypt(M1, M2, s, p, a)
    print("Bob received message")
    print("Verify:", ver)
    print("Message:", R)
