import os

import requests

from flaskapp.models import DigitalisatModel, DigitalisatImageModel, BestandWatcherModel, \
    DigitalisatImageOcrModel
from flaskapp.models.enums import DigitalisatStatus
from flaskapp.services import DigiRequests
from flaskapp.utils import FileUtils


class DigiProcessingService:

    def __init__(self):
        self.digi_requests = DigiRequests()

    def stream_digitalisat(self):
        bestande = (bestand for bestand in BestandWatcherModel.get_all())

        for bestand in bestande:
            bestand: BestandWatcherModel
            if bestand.is_paused():
                return
            if not self.digi_requests.has_connection():
                return
            with bestand.status_with_context():
                for dto in self.digi_requests.get_digitalisate_stream(bestand.id):
                    if DigitalisatModel.digi_digitalisat_has_ocr(dto):
                        model, is_new = DigitalisatModel.create_from_digi_digitalisat(dto)
                        if is_new:
                            model.save()

    def __stream_images_from_digitalisat(self, digitalisat: DigitalisatModel):
        try:
            # print(f"{digitalisat.folder_name} is being process.")
            digitalisat_images_iter = (dto for dto in self.digi_requests.get_digitalisat_images(digitalisat.id))
            dir_path = digitalisat.dir_path

            digitalisat.status = DigitalisatStatus.DOWNLOADING_IMAGES
            digitalisat.save()

            for dto in digitalisat_images_iter:
                image = DigitalisatImageModel.create_from_digi_image(dto)
                if not DigitalisatImageModel.find_by_id(image.id):
                    image.name = FileUtils.remove_filename_extension(image.name)
                    image.name = f"{image.id}_{image.name}.jpg"
                    image_path, size = self.digi_requests.get_image_file(image.id, dir_path, name=image.name)
                    if image_path and os.path.isfile(image_path):
                        image.image_size = size
                        image.sha1 = FileUtils.create_hash(image_path)
                        image.save()
                        # print(f"Download: {image}")
                    else:
                        # TODO What to do when image is not found or something goes wrong?
                        #  We probably need some log for this kind of error.
                        pass

            # TODO check if all images were downloaded.
            digitalisat.status = DigitalisatStatus.IMAGES_DOWNLOADED
            digitalisat.save()
        except requests.exceptions.ConnectionError:
            print("No Connection with digiproduction")

    def stream_images_from_digi(self):
        # check for ongoing downloading.
        for digitalisat in DigitalisatModel.get_downloading_images_status():
            self.__stream_images_from_digitalisat(digitalisat)

        # create an iterable to avoid a big memory usage.
        digitalisat_idle_iter = (digitalisat for digitalisat in DigitalisatModel.get_idles())
        for digitalisat in digitalisat_idle_iter:
            self.__stream_images_from_digitalisat(digitalisat)

    def __fetch_ocr_data(self, digitalisat: DigitalisatModel):
        try:
            # print(f"{digitalisat.folder_name} is being process.")
            digitalisat.status = DigitalisatStatus.RUNNING_OCR
            digitalisat.save()
            digitalisat_images_iter = (img for img in digitalisat.digitalisat_images)

            output_dir = digitalisat.ocr_dir
            ocr_finished_with_no_error = True
            for image in digitalisat_images_iter:
                image: DigitalisatImageModel
                ocr_data = self.digi_requests.get_ocr_data(image.id, output_dir=output_dir)
                if ocr_data is None:
                    ocr_finished_with_no_error = False
                else:
                    dio_model: DigitalisatImageOcrModel = \
                        DigitalisatImageOcrModel.find_by(digitalisat_image_id=image.id, get_first=True)
                    if dio_model:
                        ocr_finished_with_no_error = dio_model.update_ocr_text(ocr_data)
                    else:
                        dio_model = DigitalisatImageOcrModel.create(digitalisat_image_id=image.id, ocr_text=ocr_data)
                        dio_model.save()

            if ocr_finished_with_no_error:
                digitalisat.status = DigitalisatStatus.OCR_FINISHED
                digitalisat.save()
        except requests.exceptions.ConnectionError:
            print("No Connection with digiproduction")

    def get_ocr_data(self):

        # check for ongoing ocr.
        for digitalisat in DigitalisatModel.get_running_ocr_status():
            self.__fetch_ocr_data(digitalisat)

        for digitalisat in DigitalisatModel.get_downloaded_images_status():
            self.__fetch_ocr_data(digitalisat)
