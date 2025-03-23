from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import random
import string
from encrypt import encrypt_data, save_encrypted_data, save_decrypted_data, decrypt_data

app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'txt', 'doc'}
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable cache for file downloads

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to generate a random decryption key
def generate_decryption_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # 16 character key

# Route to display the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and encryption
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file_content = file.read()  # Read as binary data
        
        # Step 1: Generate a decryption key
        decryption_key = generate_decryption_key()

        # Step 2: Encrypt the file data (binary)
        encrypted_data = encrypt_data(file_content, decryption_key)
        
        # Step 3: Save the encrypted data to a file with .enc extension
        enc_filename = filename + '.enc'
        save_encrypted_data(encrypted_data, enc_filename)
        
        # Return a success message and show the decryption key and file download link
        return render_template('upload_success.html', 
                               filename=enc_filename, 
                               decryption_key=decryption_key)

    return 'Invalid file format. Please upload a valid file.'

# Route to serve encrypted files from the 'uploads' folder
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to handle file decryption
@app.route('/decrypt/<filename>', methods=['GET'])
def decrypt_file(filename):
    encryption_key = request.args.get('key')  # User will provide the key for decryption
    
    # Read the encrypted file (example: .enc file)
    try:
        with open(f"uploads/{filename}", "rb") as file:
            encrypted_data = file.read()
        
        # Step 3: Decrypt the file data
        decrypted_data = decrypt_data(encrypted_data, encryption_key)
        
        # Save the decrypted data back to its original format
        original_filename = filename.rsplit('.', 1)[0]  # Remove '.enc' to get original name
        save_decrypted_data(decrypted_data, original_filename)  # Save it with the original name (e.g., AI_Assignment.pdf)
        
        return f"File decrypted successfully! Decrypted file saved as {original_filename}"
    except FileNotFoundError:
        return "Encrypted file not found."

if __name__ == '__main__':
    # Make sure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
