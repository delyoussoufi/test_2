import itertools
import json
import re
from pathlib import Path
from typing import Union, List
from xml.etree import ElementTree as Et

from flaskapp.structures import OcrData
from flaskapp.structures.ocr_data_structure import Box, Word


def flatter(_list: List[List[any]]):
    return list(itertools.chain.from_iterable(_list))


class OcrDataParse:

    ABBY14_SCHEMA_V3 = 'http://www.loc.gov/standards/alto/ns-v3#'

    @classmethod
    def parse_alto_xml(cls, alto_file_path: Union[str, Path], schema=ABBY14_SCHEMA_V3):
        """
        Parse alto xml file to a data structure OcrData

        :param alto_file_path: the path to the xml file.
        :param schema: The xmlns schema for the alto.
        :return: an instance of OcrData
        """
        tree = Et.parse(alto_file_path)
        root = tree.getroot()
        ns = {'alto': schema}

        # list with xpaths for TextBlocks
        xpath_text_blocks = ['alto:Layout/alto:Page/alto:PrintSpace/alto:TextBlock']
        # add all possible nested composed blocks to xpath
        composed_block_string = 'alto:Layout/alto:Page/alto:PrintSpace/alto:ComposedBlock'
        while root.findall(composed_block_string, ns):
            xpath_text_blocks.append(f"{composed_block_string}/alto:TextBlock")
            composed_block_string = f"{composed_block_string}/alto:ComposedBlock"

        text_blocks: List[Et.Element] = flatter([root.findall(xpath, ns) for xpath in xpath_text_blocks])

        # Sort text blocks based on their IDs. Try to keep the text order.
        text_blocks.sort(key=lambda e: int(''.join(re.findall('[0-9]', e.attrib.get('ID', '0')))))

        text_lines: List[Et.Element] = flatter([t.findall('alto:TextLine', ns) for t in text_blocks])

        words: List[Et.Element] = []

        ocr_data = OcrData()
        for tl in text_lines:
            words_in_line = tl.findall('alto:String', ns)
            words += words_in_line
            string_list = [f"{text.attrib.get('CONTENT', '')}" for text in words_in_line]
            ocr_data.text += f"{' '.join(string_list)}\n"

        for word in words:
            x0, y0 = float(word.attrib.get('HPOS', 0)),  float(word.attrib.get('VPOS', 0))
            xf, yf = x0 + float(word.attrib.get('WIDTH', 0)), y0 + float(word.attrib.get('HEIGHT', 0))
            box = Box(x0=x0, y0=y0, xf=xf, yf=yf)
            word_s = Word(box=box)
            word_s.text = word.attrib.get('CONTENT', "")
            ocr_data.words.append(word_s)

        return ocr_data

    @classmethod
    def parse_alto_json(cls, alto_file_path: Union[str, Path]):
        """
       Parse alto json file to a data structure OcrData.

       :param alto_file_path: the path to the json file.
       :return: an instance of OcrData
        """
        with open(alto_file_path, mode='r', encoding='utf-8') as f:
            data: dict = json.load(f)

        page: dict = data['layout']['pages'][0]
        texts = page['texts']
        lines = flatter([text['lines'] for text in texts])

        # words = flatter([line['words'] for line in lines])
        words = []
        ocr_data = OcrData()
        for line in lines:
            words_in_line = line['words']
            words += words_in_line
            string_list = [f"{w['text']}" for w in words_in_line if float(w['confidence']) >= 0]
            ocr_data.text += f"{' '.join(string_list)}\n"

        # remove words that have negative confidence. That's manly rubbish.
        words = list(filter(lambda w: float(w['confidence']) >= 0, words))

        for word in words:
            position = word['position']
            x0, y0 = float(position['l']),  float(position['t'])
            xf, yf = float(position['r']),  float(position['b'])
            box = Box(x0=x0, y0=y0, xf=xf, yf=yf)
            word_s = Word(box=box)
            word_s.confidence = word['confidence']
            word_s.text = word['text']
            ocr_data.words.append(word_s)

        return ocr_data
