import socket
import select

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 5555

print("Initializing Server....")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen()
read_clients = []
print("Server has been initialized")

while True:
    ready_to_read, ready_to_write, err_in = select.select([server_socket] + read_clients, [], [])
    for sock in ready_to_read:
        if sock is server_socket:
            (client_socket, client_address) = sock.accept()
            print(client_address[0] + " Has joined")
            read_clients.append(sock)
        else:
            print("New data arrived" + sock.recv(1024).decode())
