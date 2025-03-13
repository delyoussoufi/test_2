import random
import secrets
import string

from flaskapp import bcrypt


def generate_id(length):
    """
    Generate a random string with the combination of lowercase and uppercase letters.

    :param length: The size of the id key
    :return: An id of size length formed by lowe and uppercase letters.
    """
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def generate_token():
    """
    Creates a token with 32(16-bits) alphanumeric characters.

    :return: A token string.
    """
    return secrets.token_hex(16)


def encrypt_password(psw: str):
    """
    Encrypts a password and return the encrypted string.

    :param psw: The string to be encrypted.
    :return: A encrypted string.
    """
    return bcrypt.generate_password_hash(psw).decode("utf-8")


def check_password(pw_hash: str, psw: str):
    """
    Tests a password hash against a candidate password. The candidate
    password is first hashed and then subsequently compared in constant
    time to the existing hash. This will either return `True` or `False`.

    Example usage of :class:`check_password_hash` would look something
    like this::

        pw_hash = bcrypt.generate_password_hash('secret', 10)
        bcrypt.check_password_hash(pw_hash, 'secret') # returns True

    :param pw_hash: The hash to be compared against.
    :param password: The password to compare.
    """
    return bcrypt.check_password_hash(pw_hash=pw_hash, password=psw)
