# xor_encryption.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/src/utils/xor_encryption.py

def encrypt(message: str, key: str) -> str:
    """
    Encrypts a message using XOR encryption with a given key.

    Args:
        message (str): The message to encrypt.
        key (str): The key to use for encryption.

    Returns:
        str: The encrypted message.
    """
    encrypted = ""
    for i in range(len(message)):
        # XOR each character in the message with the corresponding character in the key
        # using the modulo operator to wrap around the key if it is shorter than the message
        encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted

def decrypt(encrypted: str, key: str) -> str:
    """
    Decrypts an encrypted message using XOR encryption with a given key.

    Args:
        encrypted (str): The encrypted message to decrypt.
        key (str): The key to use for decryption.

    Returns:
        str: The decrypted message.
    """
    decrypted = ""
    for i in range(len(encrypted)):
        # XOR each character in the encrypted message with the corresponding character in the key
        # using the modulo operator to wrap around the key if it is shorter than the encrypted message
        decrypted += chr(ord(encrypted[i]) ^ ord(key[i % len(key)]))
    return decrypted
