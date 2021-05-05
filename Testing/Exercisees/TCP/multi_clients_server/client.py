import socket

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
while True:
    pass
