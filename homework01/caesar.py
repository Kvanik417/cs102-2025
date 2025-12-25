def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
        elif char.islower():
            ciphertext += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for char in ciphertext:
        if char.isupper():
            plaintext += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
        elif char.islower():
            plaintext += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
        else:
            plaintext += char
    return plaintext
