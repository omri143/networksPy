import json


### COMMON METHODS ####


def get_digits_count(num):
    """
    Helper method. Finds the amount of digits inside a number
    :param num: a number with n digits
    :return count: digits count
    """
    count = 0
    while not int(num) <= 0:
        count += 1
        num /= 10
    return count


def format_list_print(data_list, offset):
    for i in range(offset, len(data_list)):
        print(str(i - 1) + ". " + data_list[i])


### Json Methods ####
def read_file(path):
    """
    The function reads the file
    :param path: file path
    :return: list with all the lines
    :rtype:list
    """
    data = None
    with open(path, 'r') as f:  # Opens the file on 'read mode'
        data = f.readlines()
        f.close()
    return data


def parse_json_doc(path):
    """
    The function parses the json string into dict
    :param path: json file path
    :return: json string
    :rtype: dict, str
    """
    if ".json" in path:
        json_data = json.loads("".join(read_file(path)))
    else:
        json_data = "ERROR"
    return json_data
