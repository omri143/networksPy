import json

### COMMON METHODS ####
import tarfile


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


def format_list_print(recv_data_list):
    for i in range(2, len(recv_data_list)):
        print(str(i - 1) + ". " + recv_data_list[i])


### Json ####
def parse_json_doc(path):
    json_data_str = None
    with open(path, 'r') as f:
        json_data_str = f.readlines()
        f.close()
    json_data = json.loads("".join(json_data_str))
    return json_data
