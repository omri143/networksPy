import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****
import helpers

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678
USER_COMMANDS = ["s\t Get score", "h\t Get high score", "p\t Play a trivia question", "l\t Get logged users",
                 "q\t Quit"]


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Parameters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
    debug_msg = chatlib.build_message(code, data)
    conn.send(debug_msg.encode())
    print(debug_msg)


def recv_message_and_parse(conn):
    """
	Receives a new message from given socket,
	then parses the message using chatlib.
	Parameters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occurred, will return None, None
	"""
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    """
	The function connects the client to the server.
	:return: socket that connected to the server
	"""
    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_socket.connect((SERVER_IP, SERVER_PORT))
    return game_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit(-1)


def login(conn):
    login_state = ""
    while login_state != chatlib.PROTOCOL_SERVER["login_ok_msg"] or login_state is None:
        login_state = login_try(conn)
        if login_state == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
            print("FAILED TO CONNECT")

    print("SUCCESSFUL LOGIN")


def login_try(conn):
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    return build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], chatlib.join_data([username, password]))[0]


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    quit(0)


def build_send_recv_parse(conn, cmd, payload):
    """
    The function builds the message to the server, sends it and receives the response.
    :param conn: open socket
    :param cmd: command to send
    :param payload: data to send
    :rtype: tuple
    :return: server_response (msg_code, data)
    """
    build_and_send_message(conn, cmd, payload)
    server_response = recv_message_and_parse(conn)
    return server_response


def get_score(conn):
    """
    The function prints player's scores
    :param conn: open socket
    :return: nothing
    """
    (command, data) = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_personal_score_msg"], "")
    if command not in chatlib.PROTOCOL_SERVER["person_score_ans_msg"]:
        error_and_exit(data)
    print("Your score is: " + data)


def get_high_score(conn):
    """
        Retrieves scores table from the server.
    :param conn: open socket to the server
    :return: None
    """
    (command, data) = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_high_score_table_msg"], "")
    if command not in chatlib.PROTOCOL_SERVER["high_score_ans_msg"]:
        error_and_exit(data)
    print(data)


def play_question(conn):
    (command, data) = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"], "")
    if command in chatlib.PROTOCOL_SERVER["no_question_ans_msg"]:
        print("No questions available")
    elif command in chatlib.PROTOCOL_SERVER["send_question_msg"]:
        recv_data_parsed = chatlib.split_data(data, 6)
        print(recv_data_parsed[1])  # prints the question
        helpers.format_list_print(recv_data_parsed)
        ans = input("Enter the number of the answer: ")
        (ans_cmd, ans_data) = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_ans_msg"],
                                                    recv_data_parsed[0] + "#" + ans)
        if ans_cmd in chatlib.PROTOCOL_SERVER["correct_ans_msg"]:
            print("Correct answer")
        else:
            print("Nope, correct answer is #" + ans_data)
    else:
        error_and_exit(-1)


def get_logged_users(conn):
    (_, data) = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_in_msg"], "")
    print(data)


def main():
    sock = connect()
    login(sock)
    while True:
        for field in USER_COMMANDS:
            print(field)
        op = input("Please enter your choice: ").replace(" ", "").lower()
        if op.isalpha():
            if op == "h":
                get_high_score(sock)
            elif op == "s":
                get_score(sock)
            elif op == "q":
                logout(sock)
            elif op == "p":
                play_question(sock)
            elif op == "l":
                get_logged_users(sock)
            else:
                print("ERROR")


if __name__ == '__main__':
    main()
