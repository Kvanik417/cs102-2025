import random
from typing import Tuple

def gcd(a: int, b: int) -> int:
    while b != 0:
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
    original_phi = phi
    x0, x1 = 0, 1
    while e > 0:
        q, phi, e = phi // e, e, phi % e
        x0, x1 = x1 - q * x0, x0
    if phi != 1:
        return 0
    return x1 % original_phi

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(pk: Tuple[int, int], plaintext: str) -> int:
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk: Tuple[int, int], ciphertext: list) -> str:
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)
