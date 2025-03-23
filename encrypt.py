import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Step 1: Encrypt the binary data (file content) using AES
def encrypt_data(file_data, key):
    """Encrypt file data using AES encryption (CBC mode)."""
    key = hashlib.sha256(key.encode()).digest()  # Create a 256-bit key
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + encrypted_data).decode()

# Step 2: Decrypt the binary data
def decrypt_data(encrypted_data, key):
    """Decrypt encrypted data using AES encryption."""
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]  # Extract the IV
    encrypted_data = encrypted_data[16:]  # Extract the encrypted content
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

# Step 3: Save the encrypted data to a file
def save_encrypted_data(encrypted_data, filename):
    """Save the encrypted data (as binary) to a .enc file."""
    with open(f"uploads/{filename}", "wb") as file:
        file.write(base64.b64decode(encrypted_data))
    print(f"Encrypted file saved at: uploads/{filename}")

# Step 4: Save the decrypted file (to show how the user can view it)
def save_decrypted_data(decrypted_data, filename):
    """Save the decrypted data back to its original format (like PDF, image, etc.)."""
    with open(f"uploads/{filename}", "wb") as file:
        file.write(decrypted_data)
    print(f"Decrypted file saved at: uploads/{filename}")
