##############################################################################
# server.py
##############################################################################
import random
import select
import socket
import chatlib
import helpers  # JSON methods

# GLOBALS

users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "0.0.0.0"  # server ip
QUESTION_ID_LENGTH = 1  # length of question id
JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES = ["id", "text", "answers", "correct_answer"]  # Used to change the format of
# the json structure
JSON_QUESTIONS_ATTRIBUTES = ["question", "answers", "correct"]
CORRECT_ANSWER_SCORE = 5


# ### debug ###
def print_debug(txt):
    """
        The function prints debug messages
    :param txt:
    :return:
    """
    print("[DEBUG]", txt)


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    """
	   Builds a new message using chatlib, wanted code and message.
	   Prints debug info, then sends it to the given socket.
	   Parameters: conn (socket object), code (str), data (str)
	   Returns: Nothing
	   """
    debug_msg = chatlib.build_message(code, msg)
    conn.send(debug_msg.encode())
    print("[SERVER] ", debug_msg)  # Debug print


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
    print("[CLIENT - " + socket.gethostbyaddr(str(conn.getpeername()[0]))[0] + "]", full_msg)  # Debug print
    return cmd, data


# Data Loaders #

def load_questions(path):
    """
	Loads questions bank from file
	Receives:
	Returns: questions dictionary
	"""
    # i - index inside the json
    questions_dict = helpers.parse_json_doc(path)
    questions_dic = {}
    for i in range(0, len(questions_dict["questions"])):
        questions_dic[str(questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[0]]).zfill(
            QUESTION_ID_LENGTH)] = {
            JSON_QUESTIONS_ATTRIBUTES[0]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[1]],
            JSON_QUESTIONS_ATTRIBUTES[1]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[2]],
            JSON_QUESTIONS_ATTRIBUTES[2]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[3]]
        }

    for key in questions_dic.keys():
        questions[key] = helpers.parse_json_dict_to_lst(questions_dic, key, JSON_QUESTIONS_ATTRIBUTES)

    return questions


def load_user_database(path):
    """
	Loads users list from file
	Receives: -
	Returns: user dictionary
	"""
    return helpers.parse_json_doc(path)


# SOCKET CREATOR

def setup_socket():
    """
	Creates new listening socket and returns it
	Receives: -
	Returns: the socket object
	"""
    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_socket.bind((SERVER_IP, SERVER_PORT))
    return game_socket


def send_error(conn, error_msg):
    """
	Send error message with given message
	Receives: socket, message error string from called function
	Returns: None
	"""
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


# ### MESSAGE HANDLING
def handle_logged_message(conn):
    clients_list = []
    for key in logged_users:
        clients_list.append(logged_users[key])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_in_ans_msg"], ",".join(clients_list))


def handle_high_score_message(conn):
    global users
    scores = []
    # creating new list of tuples with the usernames and their score
    for dict_key in users.keys():
        scores.append((dict_key, users[dict_key]["score"]))
    # sorts the list according to the second element inside the tuple
    scores.sort(key=tuple_sort_second_element_key, reverse=True)
    str_lst = []
    for tup in scores:
        str_lst.append(tup[0] + ":" + str(tup[1]) + "\n")
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["high_score_ans_msg"], "".join(str_lst))


def handle_get_score_message(conn):
    global users
    global logged_users
    username = logged_users[conn.getpeername()]
    score = users[username]["score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["person_score_ans_msg"], str(score))


def handle_logout_message(conn):
    """
	Closes the given socket
	Receives: socket
	Returns: None
	"""
    global logged_users
    if conn.getpeername() in logged_users:
        logged_users.pop(conn.getpeername())
    print_debug(logged_users)
    conn.close()


def handle_login_message(conn, data):
    """
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Receives: socket, message code and data
	Returns: None (sends answer to client)
	"""
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users
    user_data = chatlib.split_data(data, 2)  # Splitting the data field. For login message, there are two fields
    # [username, password]
    if user_data[0] in users.keys():  # check if the username exists
        if user_data[1] == users[user_data[0]]["password"]:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
            logged_users[conn.getpeername()] = user_data[0]
            print_debug(user_data)
            print_debug(logged_users)
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Error! Wrong Password")

    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Error! User does not exists")


def create_random_question(username):
    global questions
    global users
    print_debug(questions)
    # Search for unasked question
    stop_flag = False
    question_id = None
    while not stop_flag:
        question_id = random.randint(1, len(questions))
        if str(question_id).zfill(QUESTION_ID_LENGTH) not in users[username]["asked_questions"]:
            stop_flag = True

    question_frame = chatlib.join_data([str(question_id).zfill(QUESTION_ID_LENGTH)] +
                                       questions[str(question_id).zfill(QUESTION_ID_LENGTH)][0:2])
    return question_frame, question_id


def handle_question_message(conn, username):
    global questions
    global users
    data = ""
    if all(elem in users[username]["asked_questions"] for elem in questions.keys()):
        cmd = chatlib.PROTOCOL_SERVER["no_question_ans_msg"]
    else:
        cmd = chatlib.PROTOCOL_SERVER["send_question_msg"]
        data, question_id = create_random_question(username)
        users[username]["asked_questions"].append(str(question_id))

    build_and_send_message(conn, cmd, data)


def handle_answer_message(conn, username, data):
    global users
    answer = chatlib.split_data(data, 2)  # Two fields: question_id#user_answer according to protocol
    print_debug(answer)
    if str(questions[answer[0]][2]) == str(answer[1]):
        users[username]["score"] += CORRECT_ANSWER_SCORE
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_ans_msg"], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_ans_msg"], str(questions[answer[0]][2]))


def handle_client_message(conn, cmd, data, username):
    """
	Gets message code and data and calls the right function to handle command
	Receives: socket, message code and data
	Returns: None
	"""
    global logged_users
    if cmd == chatlib.PROTOCOL_CLIENT['login_msg']:
        handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_personal_score_msg"]:
        handle_get_score_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_high_score_table_msg"]:
        handle_high_score_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["logged_in_msg"]:
        handle_logged_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_question_msg"]:
        handle_question_message(conn, username)
    elif cmd == chatlib.PROTOCOL_CLIENT["send_ans_msg"]:
        handle_answer_message(conn, username, data)
    else:
        send_error(conn, ERROR_MSG + "Unknown command")


# ### Sorting function ###

def tuple_sort_second_element_key(ele):
    """
        key function to sort list of tuples according to the second element
    :param ele: tuple
    :return:
    """
    return ele[1]


# ### Main function ###
def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions
    global logged_users
    # questions_path = input("Enter questions file path: ")
    #  users_path = input("Enter user file path: ")
    users_path = "C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\users.json"
    questions_path = "C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\questions.json"
    clients_list = []
    print("Welcome to Trivia Server!")
    server_socket = setup_socket()
    server_socket.listen()
    questions = load_questions(questions_path)
    users = load_user_database(users_path)
    (client_sock, client_add) = server_socket.accept()

    while True:
        try:
            cmd, data = recv_message_and_parse(client_sock)
            handle_client_message(client_sock, cmd, data, "Omri")
        except OSError:  # Client disconnected
            helpers.update_json(users, users_path)
            users = load_user_database(users_path)
            (client_sock, client_add) = server_socket.accept()  # waiting for a new client


if __name__ == '__main__':
    main()
