import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8820))
    client_socket.send("hello".encode())
    data = client_socket.recv(1024).decode()
    print("The server sent " + data)
    client_socket.close()


if __name__ == '__main__':
    main()
