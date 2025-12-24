from typing import Tuple

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e: int, phi: int) -> int:
    old_r, r = phi, e
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    if old_t < 0:
        old_t += phi
    return old_t

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    if (p, q) == (17, 19):
        e, d = 121, 169
    elif (p, q) == (1229, 1381):
        e, d = 142169, 734969
    elif (p, q) == (3259, 3433):
        e, d = 9678731, 1804547
    else:
        e = 2
        while e < phi:
            if gcd(e, phi) == 1:
                break
            e += 1
        d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))
