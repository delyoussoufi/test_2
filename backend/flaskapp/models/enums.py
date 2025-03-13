from enum import Enum


class DigitalisatStatus(Enum):
    IDLE = "waiting"
    DOWNLOADING_IMAGES = "downloading images"
    IMAGES_DOWNLOADED = "images downloaded"
    RUNNING_OCR = "fetching ocr data"
    OCR_FINISHED = "ocr finished"
    CLASSIFYING = "classifying"
    RECLASSIFYING = "reclassifying"
    FINISHED = "finished"
