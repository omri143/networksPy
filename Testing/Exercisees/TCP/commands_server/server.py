import socket
import Testing.Exercisees.commands_server.helpers as helpers

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))  # connects the server to any ip (External or local on port 8820
server_socket.listen(3)
print("Server has been initialized at: " + socket.gethostname())

while True:
    (client_socket, client_address) = server_socket.accept()
    print("Client connected!")
    print("Client Information" + '\n' + '-' * len("Client Information"))
    print("Host name: " + socket.gethostbyaddr(client_address[0])[0])
    print("IP address:" + client_address[0])
    command = client_socket.recv(1024).decode()
    payload = " "

    while command != "QUIT":
        if command == "RAND":
            payload = str(helpers.generate_random_number())
        elif command == "TIME":
            payload = helpers.get_time_and_date()
        elif command == "NAME":
            payload = socket.gethostname()
        else:
            payload = "ERROR"
        print(payload)
        client_socket.send(payload.encode())
        command = client_socket.recv(1024).decode()
