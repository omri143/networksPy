##############################################################################
# server.py
##############################################################################
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
JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES = ["id", "text", "answers", "correct_answer"]  # Used to change the format of
# the json structure
JSON_QUESTIONS_ATTRIBUTES = ["question", "answers", "correct"]


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
    print("[CLIENT] ", full_msg)  # Debug print
    return cmd, data


# Data Loaders #

def load_questions(path):
    """
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Receives: -
	Returns: questions dictionary
	"""
    # i - index inside the json
    questions_dict = helpers.parse_json_doc(path)
    for i in range(0, len(questions_dict["questions"])):
        questions[str(questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[0]]).zfill(4)] = {
            JSON_QUESTIONS_ATTRIBUTES[0]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[1]],
            JSON_QUESTIONS_ATTRIBUTES[1]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[2]],
            JSON_QUESTIONS_ATTRIBUTES[2]: questions_dict["questions"][i][JSON_QUESTIONS_CONVERSIONS_ATTRIBUTES[3]]
        }

    return questions


def load_user_database(path):
    """
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
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


# Implement code ...


##### MESSAGE HANDLING


def handle_get_score_message(conn, username):
    global users


# Implement this in later chapters


def handle_logout_message(conn):
    """
	Closes the given socket (in laster chapters, also remove user from logged_users dictionary)
	Recieves: socket
	Returns: None
	"""
    global logged_users


# Implement code ...


def handle_login_message(conn, data):
    """
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later


# Implement code ...


def handle_client_message(conn, cmd, data):
    """
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
    global logged_users  # To be used later


# Implement code ...


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")


# Implement code ...


if __name__ == '__main__':
    main()
