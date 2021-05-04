import socket

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8820
ADD_TUP = (SERVER_ADDRESS, SERVER_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd = ""
while cmd == "" or cmd.lower() not in "exit":
    cmd = input("Enter command to the server: ").lower()
    sock.sendto(cmd.encode(), (SERVER_ADDRESS, SERVER_PORT))
sock.close()
