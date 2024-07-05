import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    client_socket.send(b'authenticate')
    username = input("Enter username: ")
    client_socket.send(username.encode())
    password = input("Enter password: ")
    client_socket.send(password.encode())

    response = client_socket.recv(1024)
    if response == b'authenticated':
        print("Authentication successful.")

        # Example: Receive file
        with open('received_file.txt', 'wb') as f:
            ciphertext = client_socket.recv(1024)
            tag = client_socket.recv(16)
            nonce = client_socket.recv(16)

            f.write(ciphertext)
            f.write(b"\nThis is an example of SECURE FILE TRANSFER APPLICATION")

        print("File received successfully.")
    else:
        print("Authentication failed.")

    client_socket.close()

if __name__ == '__main__':
    main()
