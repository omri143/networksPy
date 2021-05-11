import socket
import select

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 5555


def print_client_sockets(client_sockets):
    """
    Prints the connected sockets
    :param client_sockets:sockets list
    :return:
    """
    for c in client_sockets:
        print("\t", c.getpeername())


def send_msg(messages_to_send, write_lst):
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in write_lst:
            current_socket.send(data.encode())
            messages_to_send.remove(message)


def main():
    print("Initializing Server....")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen()
    read_clients = []
    messages_to_send = []

    print("Server has been initialized")

    while True:
        # Listening to  available sockets
        ready_to_read, ready_to_write, err_in = select.select([server_socket] + read_clients, read_clients, [])
        for sock in ready_to_read:
            if sock is server_socket:  # if the socket belongs to the server
                (client_socket, client_address) = sock.accept()  # accepting new socket connection
                print(client_address[0] + " Has joined")
                read_clients.append(client_socket)
                print_client_sockets(read_clients)
            else:
                messages_to_send.append((sock, "Hi" + sock.getpeername()[0]))

                """
                   Try to receive data from one of the clients. If successful, the server will print the data.
                   In the other case, the program handles the exception that occurred.
                """
                try:
                    data = sock.recv(1024).decode()
                except ConnectionResetError:
                    sock.close()
                    read_clients.remove(sock)
                    print_client_sockets(read_clients)

                if data == "":
                    print(sock.getpeername()[0] + " Disconnected")
                    sock.close()
                else:
                    print(data)
        """
            Sending the messages to the clients     
        """
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                try:
                    current_socket.send(data.encode())
                    messages_to_send.remove(message)

                except OSError:
                    print("ERROR")


if __name__ == '__main__':
    main()
