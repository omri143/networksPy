import socket

SERVER_IP = "127.0.0.1"
PORT = 8821

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.sendto("Omer".encode(), (SERVER_IP, PORT))
my_socket.close()
