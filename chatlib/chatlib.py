# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_in_msg": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "send_ans_msg": "SEND_ANSWER",
    "get_personal_score_msg": "MY_SCORE",
    "get_high_score_table_msg": "HIGHSCORE"
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_in_ans_msg": "LOGGED_ANSWER",
    "person_score_ans_msg": "YOUR_SCORE",
    "high_score_ans_msg": "ALL_SCORE",
    "send_question_msg": "YOUR_QUESTION",
    "correct_ans_msg": "CORRECT_ANSWER",
    "no_question_ans_msg": "NO_QUESTIONS",
    "error_msg": "ERROR"
}

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    i = 0
    for field in msg_fields:
        if type(field) is not str:  # if the type of the object is not string
            if type(field) is list:
                msg_fields[i] = DATA_DELIMITER.join([str(e) for e in field])
            else:
                msg_fields[i] = str(field)
        i += 1
    return DATA_DELIMITER.join(msg_fields)


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """
    msg_lst = msg.split(DATA_DELIMITER)
    if len(msg_lst) == expected_fields:
        return msg_lst
    return [ERROR_RETURN]


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    data_lst = data.split(DELIMITER)  # splitting the data
    if len(data_lst) == 3:  # if the list has 3 fields (2 delimiters)
        data_lst[1] = data_lst[1].replace(" ", "")  # list structure: [command, data length , data]
        if data_lst[1].isnumeric() and int(data_lst[1]) == len(data_lst[2]):  # if the middle field contains only
            # numbers and the length of the message is correct
            msg = data_lst[2]
            cmd = data_lst[0].replace(" ", "")
        else:
            cmd = ERROR_RETURN
            msg = ERROR_RETURN
    else:
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
        # The function should return 2 values
    return cmd, msg


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    :return: str, or None if error occurred
    """
    # if the data and the cmd are according to protocol
    if (MAX_DATA_LENGTH > len(data) >= 0) and (len(cmd) < CMD_FIELD_LENGTH):
        # builds the message to the server
        full_msg = [cmd, " " * (CMD_FIELD_LENGTH - len(cmd)), DELIMITER,
                    str(len(data)).zfill(4), DELIMITER, data]
        full_msg = "".join(full_msg)  # converts the msg from list type to string type
    else:
        full_msg = ERROR_RETURN
    return full_msg
