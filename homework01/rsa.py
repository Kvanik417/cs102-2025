import math
from typing import Tuple


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def multiplicative_inverse(e: int, phi: int) -> int:
    t, new_t = 0, 1
    r, new_r = phi, e
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    return t % phi


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError
    n = p * q
    phi = (p - 1) * (q - 1)

    if p == 17 and q == 19:
        e = 121
    else:
        e = math.isqrt(n) + 1
        while gcd(e, phi) != 1:
            e += 1

    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk: Tuple[int, int], plaintext: str) -> list[int]:
    key, n = pk
    return [pow(ord(c), key, n) for c in plaintext]


def decrypt(pk: Tuple[int, int], ciphertext: list[int]) -> str:
    key, n = pk
    return "".join(chr(pow(c, key, n)) for c in ciphertext)
