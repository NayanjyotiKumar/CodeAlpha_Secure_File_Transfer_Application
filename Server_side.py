import socket
from Crypto.Cipher import AES
import os
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)

def encrypt_file(key, file_path):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, tag, cipher.nonce

def handle_client_connection(client_socket, key):
    data = client_socket.recv(1024)
    if data == b'authenticate':
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()

        # Example: Validate username and password (could be replaced with a database query)
        if username == 'user' and password == 'password':
            client_socket.send(b'authenticated')
            logging.info(f"User {username} authenticated.")

            # Example: File transfer
            file_path = 'example_file.txt'
            if os.path.exists(file_path):
                ciphertext, tag, nonce = encrypt_file(key, file_path)
                client_socket.sendall(ciphertext)
                client_socket.sendall(tag)
                client_socket.sendall(nonce)
                logging.info(f"File {file_path} sent to user {username}.")
            else:
                logging.error(f"File {file_path} does not exist.")
        else:
            client_socket.send(b'authentication_failed')
            logging.error(f"Authentication failed for user {username}.")
    else:
        logging.error("Invalid request received.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    key = b'0123456789abcdef'  # Example encryption key

    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Connection from {address} established.")
        handle_client_connection(client_socket, key)
        client_socket.close()

if __name__ == '__main__':
    main()
