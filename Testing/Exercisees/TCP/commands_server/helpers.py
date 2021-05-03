import time as t
import random as rnd


def generate_random_number():
    """

    :return: random number between 1 to 10
    """
    rnd.seed()
    return rnd.randint(1, 10)


def get_time_and_date():
    """

    :return: Current time and date
    """
    return t.ctime(t.time())


