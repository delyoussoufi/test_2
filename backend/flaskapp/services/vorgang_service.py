import os
from datetime import datetime
from typing import List

from reportlab.lib.units import mm

from flaskapp import app_utils
from flaskapp.models import VorgangModel, DigitalisatImageModel, ScopeDataModel, DigitalisatModel
from flaskapp.report.searchable_pdf_builder import SearchablePdfBuilder
from flaskapp.search import VorgangSearch
from flaskapp.services.ocr_service import OcrDataParse
from flaskapp.structures.structures import SearchResult
from flaskapp.utils import DateUtils, StringUtils


class VorgangService:

    @staticmethod
    def create(category_id: str, digitalisat_id: str, images_ids: List[str]) -> VorgangModel:
        # create
        model = VorgangModel()
        model.id = app_utils.generate_id(16)
        model.digitalisat_id = digitalisat_id
        model.search_category_id = category_id
        model.vorgang_order = VorgangModel.get_next_order(category_id)
        model.add_digitalisat_images(images_ids)
        model.create_date = datetime.now().date()
        model.save()

        return model

    @staticmethod
    def update(vorgang_model: VorgangModel) -> VorgangModel:
        safe_model: VorgangModel = VorgangModel.find_by_id(vorgang_model.id)

        if safe_model:
            # update
            safe_model.delete_vorgang_images()
            safe_model.add_digitalisat_images([img.id for img in vorgang_model.get_images()])
            # dump all fields to safe model
            safe_model << vorgang_model
            safe_model.save()

        return safe_model

    @staticmethod
    def search(vorgang_search: VorgangSearch) -> SearchResult:
        return VorgangModel.search(vorgang_search)

    @staticmethod
    def to_pdf(vorgang_model: VorgangModel, pdf_out: str, scale=1.):
        pdf_builder = SearchablePdfBuilder(pdf_out, pagesize=(3059*scale, 4174*scale))
        # add heading
        digitalisat: DigitalisatModel = vorgang_model.digitalisat  # back ref
        scope_data: ScopeDataModel = digitalisat.scope_data

        heading_msg = "Brandenburgisches Landeshauptarchiv (BLHA),"
        pdf_builder.add_heading(heading_msg, font_size=30)

        sig_number = StringUtils.extract_signature_reference(digitalisat.signature)
        # TODO get the bestande name in a better way.
        heading_msg = f"Rep. 36A Oberfinanzpräsident Berlin-Brandenburg (II) Nr. {sig_number}"
        pdf_builder.add_heading(heading_msg, font_size=30, leading=10*mm)

        # add extra information
        starting_text = pdf_builder.height * 0.8
        pdf_builder.leading = 5 * mm
        pdf_builder.add_text(f"Registratursignatur: {scope_data.registry_signature}",
                             text_position_y=starting_text, font_size=20)
        pdf_builder.add_text(f"Name: {scope_data.title}", font_size=20)
        geburtsname = scope_data.geburtsname if scope_data.geburtsname else ''
        pdf_builder.add_text(f"Geburtsname: {geburtsname}", font_size=20)
        pdf_builder.add_text(f"Geburtsdatum: {DateUtils.convert_date_to_german_string(scope_data.geburtsdatum)}",
                             font_size=20)
        pdf_builder.add_text(f"Laufzeit: {scope_data.dat_findbuch}", font_size=20)
        pdf_builder.add_text(f"Wohnort: {scope_data.wohnort}", font_size=20)

        images_model: List[DigitalisatImageModel] = vorgang_model.get_images()
        for img in images_model:
            pdf_builder.next_page()
            alto_path, _ = img.get_ocr_files()
            if os.path.isfile(alto_path):
                ocr_data = OcrDataParse.parse_alto_xml(alto_path)
                pdf_builder.add_searchable_image(img.image_path, ocr_data=ocr_data, scale=scale)

        pdf_builder.save()
