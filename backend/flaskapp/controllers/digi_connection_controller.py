from flaskapp.controllers import digi
from flaskapp.http_util import response
from flaskapp.http_util.decorators import query, secure
from flaskapp.models import Right
from flaskapp.search import DigiBestandSearch
from flaskapp.services import DigiRequests


@digi.route("/bestand/search",  methods=["GET"])
@secure(Right.BESTANDE_ADD)
@query(DigiBestandSearch)
def search_bestaende(bestand_search: DigiBestandSearch):
    digi_request = DigiRequests()
    search_result = digi_request.search_bestaende(bestand_search)
    return response.dict_to_response(search_result)

