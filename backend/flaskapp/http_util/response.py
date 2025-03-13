import http
import os
from io import BytesIO
from typing import Union

import flask
from flask import jsonify

from flaskapp.utils.async_utils import AsyncTime


def date_to_response(date_value):
    """
    Parse a date to an application/json.

    :param date_value: The date to parse into json response.
    :return: The Json response.
    """
    return jsonify(date_value)


def int_to_response(int_value):
    """
    Parse an int to an application/json.

    :param int_value: The integer to parse into json response.
    :return: The Json response.
    """
    return jsonify(int_value)


def string_to_response(string_value):
    """
    Parse a string to an application/json.

    :param string_value: The string to parse into json response.
    :return: The Json response.
    """
    return jsonify(string_value)


def bool_to_response(b: bool):
    """
    Parse a string to an application/json.

    :param b: The boolean to parse into json response.
    :return: The Json response.
    """
    return jsonify(b)


def dict_to_response(dto: dict):
    """
    Parse a dict to an application/json.

    :param dto: the dictionary to be parsed
    :return: The Json response.
    """
    return jsonify(dto)


def model_to_response(entities):
    """
    Parse an entity model or a list of it to an application/json.

    :param entities: Any object or a list of it that contains a method to_dict().
        This method must return a dictionary.
    :return: The Json response.
    """
    if isinstance(entities, list):
        model_dict = [entity.to_dict() for entity in entities]
    else:
        model_dict = entities.to_dict()

    return dict_to_response(model_dict)


def file_to_response(src: Union[str, BytesIO], delete_after=False, **kwargs):
    """
    Create a response from a file path using flask.send_file

    :param src: The full path to the file or a BytesIO.
    :param delete_after: If file should be deleted after creating response.
    :keyword kwargs: All valid kwargs for flask.send_file()
    :return: A file response.
    """

    max_age = kwargs.pop("max_age", 60*10)  # cache file for 10 min as default.
    rv = flask.send_file(src, max_age=max_age, **kwargs)
    if delete_after:
        def delete():
            if isinstance(src, BytesIO):
                src.close()
            else:
                if os.path.isfile(src):
                    os.remove(src)

        # delete file asynchronous to avoid permission access errors on windows manly.
        AsyncTime().wait(10, delete)
    return rv


def empty_response():
    """
    Create a null response with the right http status.

    :return: The null response with http status: 204
    """
    return "", http.HTTPStatus.NO_CONTENT


def ok_response():
    """
    Create an ok response with the right http status.

    :return: The ok response with http status: 200
    """
    return jsonify(success=True), http.HTTPStatus.OK
