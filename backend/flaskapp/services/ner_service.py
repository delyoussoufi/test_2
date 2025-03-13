from flaskapp.http_util.exceptions import EntityNotFound
from flaskapp.models import DigitalisatImageOcrModel
from flaskapp.ofp_nlp import NerHandler, FoundEntities


class NerService:

    @classmethod
    def construct_image_ner(cls, image_id: str, **kwargs) -> FoundEntities:
        """

        :param image_id:
        :param kwargs:
        :keyword use_fishing: Default False
        :keyword clean_text: Default True

        :return:
        """

        use_fishing = kwargs.get("use_fishing", False)
        clean_text = kwargs.get("clean_text", True)

        dim: DigitalisatImageOcrModel = DigitalisatImageOcrModel.find_by_id(image_id)
        if not dim:
            raise EntityNotFound(f"Could not find DigitalisatImageOcrModel for id: {image_id}")

        return NerHandler(use_fishing=use_fishing).find_entities(dim.ocr_text, clean_text=clean_text)
