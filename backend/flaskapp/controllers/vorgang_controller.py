# User APIs.
import tempfile

from flaskapp.controllers import vorgang
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure, query, post
from flaskapp.http_util.exceptions import EntityNotFound, AppException
from flaskapp.models import VorgangModel, Role, Right
from flaskapp.search import VorgangSearch
from flaskapp.services import VorgangService
from flaskapp.structures.structures import SearchResult


@vorgang.route("/search", methods=["GET"])
@secure(Right.VORGANG)
@query(VorgangSearch)
def search_vorgang(vorgang_search: VorgangSearch):
    search_result: SearchResult = VorgangService.search(vorgang_search)
    return response.model_to_response(search_result)


@vorgang.route("/<string:vorgang_id>", methods=["GET"])
@secure(Right.VORGANG)
def get_vorgang(vorgang_id: str):
    vorgang_model: VorgangModel = VorgangModel.find_by_id(vorgang_id)
    if vorgang_model is None:
        raise EntityNotFound("Der Vorgang konnte nicht ermittelt werden!")

    return response.model_to_response(vorgang_model)


@vorgang.route("/delete/<string:vorgang_id>", methods=["DELETE"])
@secure(Right.VORGANG)
def delete_vorgang(vorgang_id: str):
    vorgang_model: VorgangModel = VorgangModel.find_by_id(vorgang_id)
    if vorgang_model is None:
        raise EntityNotFound("Der Vorgang konnte nicht ermittelt werden!")

    return response.bool_to_response(vorgang_model.delete())


@vorgang.route("/vorgangImagesId/<string:vorgang_id>", methods=["GET"])
@secure(Right.VORGANG)
def get_vorgang_images(vorgang_id: str):
    vorgang_model: VorgangModel = VorgangModel.find_by_id(vorgang_id)
    if vorgang_model is None:
        raise EntityNotFound("Der Vorgang konnte nicht ermittelt werden!")

    return response.model_to_response(vorgang_model.get_images())


@vorgang.route("/create", methods=["POST"])
@secure(Right.VORGANG)
@post("category_id", "digitalisat_id", "images_ids")
def create_vorgang(category_id, digitalisat_id, images_ids):
    model = VorgangService.create(category_id, digitalisat_id, images_ids)
    if model:
        return response.model_to_response(model)
    return response.empty_response()


@vorgang.route("/pdf/<string:vorgang_id>", methods=["GET"])
@secure(Right.VORGANG_PDF)
def get_pdf(vorgang_id: str):
    model = VorgangModel.find_by_id(vorgang_id)
    if not model:
        raise AppException(f"Can't find vorgang with id {vorgang_id}")

    tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf_path = tmp_file.name
    try:
        # create pdf with images scaled by 50% of original size.
        VorgangService.to_pdf(model, pdf_path, scale=0.5)
    finally:
        tmp_file.close()
        return response.file_to_response(pdf_path, delete_after=True)
