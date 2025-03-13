from flaskapp.controllers import public
from flaskapp.http_util import response


@public.route("/is-alive",  methods=["GET"])
def is_alive():
    return response.bool_to_response(True)

