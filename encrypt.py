from flask import Flask, request, send_file, render_template, redirect, url_for
import os
from encrypt import encrypt_data, decrypt_data, generate_key

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        encryption_key = generate_key()

        data = file.read()
        encrypted_data = encrypt_data(data, encryption_key)

        with open(file_path + ".enc", "wb") as enc_file:
            enc_file.write(encrypted_data)

        return render_template('upload_success.html', filename=filename + ".enc", decryption_key=encryption_key.hex())

@app.route('/decrypt/<filename>', methods=['GET', 'POST'])
def decrypt_file(filename):
    if request.method == 'POST':
        decryption_key = request.form.get('key')
        
        if not decryption_key:
            return "Error: Decryption key missing. Please enter a valid key."
        
        try:
            decryption_key = bytes.fromhex(decryption_key)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if not os.path.exists(file_path):
                return "Error: File not found."

            with open(file_path, "rb") as enc_file:
                encrypted_data = enc_file.read()

            decrypted_data = decrypt_data(encrypted_data, decryption_key)

            decrypted_path = file_path.replace(".enc", "")
            with open(decrypted_path, "wb") as dec_file:
                dec_file.write(decrypted_data)

            return send_file(decrypted_path, as_attachment=True)

        except ValueError:
            return "Error: Invalid decryption key format."
    
    return render_template('decrypt.html', filename=filename)

@app.route('/decrypt.html')
def decrypt_page():
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)
