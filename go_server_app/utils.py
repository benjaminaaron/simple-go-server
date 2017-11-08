import random
import string


def gen_random_string(n, lower_case=True):
    options = string.digits + (string.ascii_lowercase if lower_case else string.ascii_uppercase)
    # via stackoverflow.com/a/23728630/2474159
    return ''.join(random.SystemRandom().choice(options) for _ in range(n))
