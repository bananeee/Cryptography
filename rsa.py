from prime import generate_prime_number, is_prime
from support import *


def rsa_encrypt(x, b, n):
    """RSA encryption ek = x^b mod n

    Args:
        x : content
        b : random number that gcd(b, phi(n)) = 1
        n : pq
    """
    return modexp(x, b, n)


def rsa_decrypt(y, a, n):
    """RSA encryption dk = y^a mod p

    Args:
        y : encrypted content
        a : modular inverse of b
        n : pq
    """
    return modexp(y, a, n)


def rsa_signature(x, a, n):
    """RSA signature sigk = x^a mod p

    Args:
        x ([type]): [description]
        a ([type]): [description]
        n ([type]): [description]

    Returns:
        [type]: [description]
    """
    return modexp(x, a, n)


def rsa_verify(x, y, b, n):
    """RSA verification verification

    Args:
        x ([type]): [description]
        y ([type]): [description]
        b ([type]): [description]
        n ([type]): [description]

    Returns:
        [type]: [description]
    """
    return x == modexp(y, b, n)


if __name__ == "__main__":
    # p, q are 512 bit primes
    # random b such taht gcd(b, phi(n)) = 1 => choose b as random prime for easy calculating

    # NOTE: Alice
    pA = generate_prime_number(512)
    qA = generate_prime_number(512)

    nA = pA*qA
    pnA = (pA-1)*(qA-1)  # phi(n)

    bA = generate_prime_number(10)
    # bA = 673
    aA = modinv(bA, pnA)

    print("Public key of Alice is (n,b): (", nA, ",", bA, ")")
    print("Private key of Alice is (p,q,a): (", pA, ",", qA, ",", aA, ")")
    print("--------")
    
    # NOTE: Bob
    pB = generate_prime_number(512)
    qB = generate_prime_number(512)

    nB = pB*qB
    pnB = (pB-1)*(qB-1)  # phi(n)

    bB = generate_prime_number(10)
    # bB = 673
    aB = modinv(bB, pnB)

    print("Public key of Bob is (n,b): (", nB, ",", bB, ")")
    print("Private key of Bob is (p,q,a): (", pB, ",", qB, ",", aB, ")")
    print("--------")
    
    print("Alice want to send message to Bob")
    message = input("Enter message to encrypt:")
    x = convertToInt(message)

    encrypt = rsa_encrypt(x, bB, nB)
    sig = rsa_signature(encrypt, aA, nA)
    
    print("Alice send to Bob code message:", sig)
    print("--------")

    ver = rsa_verify(encrypt, sig, bA, nA)
    context = rsa_decrypt(encrypt, aB, nB)
    print("Bob received message")
    print("Verify:", ver)
    print("Message:", convertToString(context))

# NOTE: Encryption
#     encrypt = rsa_encrypt(x, b, n)
#     decrypt = rsa_decrypt(encrypt, a, n)
#     print("RSA encryption is", encrypt)
#     print("RSA decryption is", decrypt)

# NOTE: Signature
    # sig = rsa_signature(x, a, n)
    # print("Signature is ", sig)
    # print("Verify result is", rsa_verify(x, sig, b, n))
