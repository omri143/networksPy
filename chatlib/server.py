##############################################################################
# server.py
##############################################################################

import socket
import chatlib

# GLOBALS
import helpers

users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	## copy from client

	print("[SERVER] ", full_msg)  # Debug print


def recv_message_and_parse(conn):
	## copy from client

	print("[CLIENT] ", full_msg)  # Debug print


# Data Loaders #

def load_questions(path):
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	json_dict = helpers.parse_json_doc(path)
	for i in range(0, len(json_dict["questions"])):
		questions[str(json_dict["questions"][i][helpers.JSON_QUESTIONS_ATTRIBUTES[0]]).zfill(4)] = {
			"question": json_dict["questions"][i][helpers.JSON_QUESTIONS_ATTRIBUTES[1]],
			"answers": json_dict["questions"][i][helpers.JSON_QUESTIONS_ATTRIBUTES[2]],
			"correct": json_dict["questions"][i][helpers.JSON_QUESTIONS_ATTRIBUTES[3]]
		}

	return questions


def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
		"test": {"password": "test", "score": 0, "questions_asked": []},
		"yossi"	:	{"password" :"123", "score": 50, "questions_asked": []},
		"master": {"password": "master", "score": 200, "questions_asked": []}
	}
	return users


# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	# Implement code ...

	return sock


def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""


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
	load_questions("C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\questions.json")
	print(questions)


# Implement code ...


if __name__ == '__main__':
	main()
