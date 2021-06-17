from prime import generate_prime_number, is_prime, randrange
from support import *


def elgama_encrypt(x, alpha, beta, p):
    """Elgama encryption

    Args:
        x : content
        alpha : primitive element of p 
        beta : random element of p
        p : random big prime
    """
    k = randrange(0, 10000000, 1)
    y1 = modexp(alpha, k, p)
    y2 = (x * modexp(beta, k, p)) % p

    return y1, y2


def elgama_decrypt(y1, y2, a, p):
    """Elgama dectryption

    Args:
        y1 : 
        y2 : 
        a : discrete logarithm of beta
        p : random big prime
    """

    return (y2 * modinv(modexp(y1, a, p), p)) % p


def elgama_signature(y, a, alpha, p):
    """ElGama signature

    Args:
        x : context
        a : discrete logarithm of beta
        alpha : primitive root of p
        p : random big prime

    Returns:
        (gama, delta)
    """
    y1, y2 = y

    k = generate_prime_number(20)
    gama = modexp(alpha, k, p)

    delta1 = ((y1 - a * gama) * modinv(k, p - 1)) % (p - 1)

    delta2 = ((y2 - a * gama) * modinv(k, p - 1)) % (p - 1)
    return (gama, delta1, delta2)


def elgama_verify(x, alpha, beta, gama, delta, p):
    """ElGama verification

    Args:
        x : context
        alpha : primitive root of p
        beta : 
        gama : 
        delta : 
        p : random big prime

    Returns:
        Boolean
    """
    return modexp(alpha, x, p) == (modexp(beta, gama, p) * modexp(gama, delta, p)) % p


if __name__ == "__main__":
    # p is random 256-bit prime

    # NOTE: Alice
    pA = generate_prime_number(256)
    alphaA = primitive(pA)
    aA = randrange(0, 10000, 1)

    betaA = modexp(alphaA, aA, pA)

    print("Public key of Alice is (p, alpha, beta):",
          pA, ",", alphaA, ",", betaA)
    print("Private key of Alice is (a):", aA)
    print("--------")
    
    # NOTE: Bob
    pB = generate_prime_number(256)
    alphaB = primitive(pB)
    aB = randrange(0, 10000, 1)

    betaB = modexp(alphaB, aB, pB)

    print("Public key of Bob is (p, alpha, beta):",
          pB, ",", alphaB, ",", betaB)
    print("Private key of Bob is (a):", aB)
    print("--------")

    print("Alice want to send message to Bob")
    message = input("Enter message to encrypt:")
    x = convertToInt(message)

    y1, y2 = elgama_encrypt(x, alphaB, betaB, pB)
    sig = elgama_signature((y1, y2), aA, alphaA, pA)
    gama, delta1, delta2 = sig

    print("Alice send to Bob coded message:", sig)
    print("--------")

    ver = elgama_verify(y1, alphaA, betaA, gama, delta1, pA) and elgama_verify(
        y1, alphaA, betaA, gama, delta1, pA)
    context = elgama_decrypt(y1, y2, aB, pB)
    print("Bob received message")
    print("Verify:", ver)
    print("Message:", convertToString(context))

    # print("ElGama encryption is (", y1, ",", y2, ")")
    # print("ElGama decryption is ", elgama_decrypt(y1, y2, a, p))

    # (gama, delta) = elgama_signature(x, a, alpha, p)
    # print(elgama_verify(x, alpha, beta, gama, delta, p))
