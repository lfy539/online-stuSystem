from random import choice
import string


def generate_random(random_lenth, type):
    random_seed = string.digits
    if type == 0:
        random_seed = string.digits
    elif type == 1:
        random_seed = string.digits + string.ascii_letters + string.punctuation

    random_str = []
    while len(random_str) < random_lenth:
        random_str.append(choice(random_seed))
    return ''.join(random_str)
