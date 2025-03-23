from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Generate a random 16-byte encryption key
def generate_key():
    return os.urandom(16)

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Initialization vector
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))  # Pad before encrypting
    return iv + encrypted_data  # Prepend IV to the ciphertext

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]  # Extract IV from the first 16 bytes
    encrypted_text = encrypted_data[16:]  # Get the encrypted content
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_text), AES.block_size)  # Unpad after decrypting
    return decrypted_data
