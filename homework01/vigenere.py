def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    key_len = len(keyword)
    for i, char in enumerate(plaintext):
        k = keyword[i % key_len].lower()
        shift = ord(k) - ord('a')
        if char.isupper():
            ciphertext += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif char.islower():
            ciphertext += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            ciphertext += char
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    key_len = len(keyword)
    for i, char in enumerate(ciphertext):
        k = keyword[i % key_len].lower()
        shift = ord(k) - ord('a')
        if char.isupper():
            plaintext += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        elif char.islower():
            plaintext += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            plaintext += char
    return plaintext
