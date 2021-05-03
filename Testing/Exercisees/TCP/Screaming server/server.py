import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))  # connects the server to any ip (External or local on port 8820
server_socket.listen(5)
print("Server has been initialized at: " + socket.gethostname())
(client_socket, client_address) = server_socket.accept()
print("Client Information" + '\n' + '-' * len("Client Information"))
print("Host name: " + socket.gethostbyaddr(client_address[0])[0])
print("IP address:" + client_address[0])
# receives the data from the client
data = client_socket.recv(1024).decode()
print("Client sent: " + data)
client_socket.send((data.upper() + "!!!").encode())
client_socket.close()
server_socket.close()
