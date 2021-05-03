import socket

COMMANDS = ["TIME", "RAND", "NAME", "QUIT"]


def print_list():
    i = 0
    for item in COMMANDS:
        print(str(i + 1) + "." + item)
        i += 1


def connect_to_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock


def main():
    client_socket = connect_to_server("127.0.0.1", 8820)
    print_list()
    command = int(input("Choose an option to request from the server: "))
    while command < 4:
        client_socket.send(COMMANDS[command - 1].encode())
        print(client_socket.recv(1024).decode())
        print_list()
        command = int(input("Choose an option to request from the server: "))


if __name__ == '__main__':
    main()
