import re
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Callable, Tuple

import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from flaskapp.ofp_nlp.ner.Utils.nlp_utils import NlpUtils


@dataclass
class Entity:
    value: str
    start: int
    end: int
    label: str
    kb_id: str
    kb_url: str

    def to_dict(self):
        return asdict(self)


@dataclass
class FoundEntities:
    text: str
    entities: List[Entity] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


class NerHandler:
    _NLP_DE: Optional[Language] = None

    def __init__(self, use_fishing: bool = False):
        self._nlp_de: Language = NerHandler.create_nlp_spacy_ner(use_fishing)

    @classmethod
    def create_nlp_spacy_ner(cls, use_fishing: bool = False):
        """
         Function that finds entities using the spaCy framework

        :param use_fishing: their to use entity fishing or not in the pipeline.
        :return:
        """

        if cls._NLP_DE:
            return cls._NLP_DE

        nlp_de: Language = spacy.load('de_core_news_lg', exclude=["attribute_ruler", "lemmatizer", "sentencizer"])
        # nlp_de.add_pipe("set_custom_boundaries", before='parser')
        # nlp_de.add_pipe("find_streets", before='ner')
        nlp_de.add_pipe("find_dates", before='ner')
        # nlp_de.add_pipe("find_organizations", before='ner')
        # nlp_de.add_pipe("find_countries", before='ner')
        nlp_de.add_pipe("find_professions", before='ner')
        # nlp_de.add_pipe("entityfishing", config={"extra_info": True})
        # nlp_de.add_pipe('dbpedia_spotlight', config={'language_code': 'de'})
        if use_fishing:
            nlp_de.add_pipe('entityfishing', config={"language": "de"})
        # nlp_de.add_pipe('opentapioca')
        # print('Pipelines used :',nlp_de.pipe_names)
        # print(nlp_de.get_pipe("ner").labels)
        cls._NLP_DE = nlp_de

        return nlp_de

    @property
    def nlp_de(self):
        return self._nlp_de

    def find_entities(self, text: str, clean_text: bool = True):
        text = NlpUtils.clean_up_ocr(text) if clean_text else text

        doc: Doc = self.nlp_de(text)
        ents: Tuple[Span] = doc.ents

        return FoundEntities(text=doc.text, entities=[
            Entity(start=ent.start_char, end=ent.end_char, value=ent.text, label=ent.label_,
                   kb_url=getattr(ent._, "url_wikidata", None), kb_id=getattr(ent._, "kb_qid", None))
            for ent in ents
        ])

    @staticmethod
    def filter_entities(found_entities: FoundEntities) -> FoundEntities:
        filtered_entities = []
        for entity in found_entities.entities:
            if len(entity.value) >= 3 and re.search(r'[a-zA-ZäöüÄÖÜß\d\s]+', entity.value):
                filtered_entities.append(entity)
        filtered_found_entities = FoundEntities(text=found_entities.text, entities=filtered_entities)
        return filtered_found_entities


class NerPipelineComponents:

    @staticmethod
    def __add_pipeline_spans(doc, label, matcher: Callable):
        original_ents = list(doc.ents)
        _ents: List[Span] = [doc.char_span(*match.span(), label=label) for match in matcher(doc.text)]
        original_ents.extend([e for e in _ents if e])
        doc.ents = filter_spans(original_ents)
        return doc

    @staticmethod
    @Language.component("find_dates")
    def find_dates(doc: Doc):
        """"
        Custom pipeline that finds dates using a regex pattern
        """

        return NerPipelineComponents.__add_pipeline_spans(doc, label="DATE", matcher=NlpUtils.find_dates_in_text)

    @staticmethod
    @Language.component("find_professions")
    def find_professions(doc: Doc):
        """
        Custom pipeline that finds professions

        :param doc:
        :return:
        """
        return NerPipelineComponents.__add_pipeline_spans(doc, label="PROFESSION", matcher=NlpUtils.find_professions)
