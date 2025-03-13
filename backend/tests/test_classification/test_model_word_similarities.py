import unittest

from flaskapp.classification.finder_gram_levenshtein_model import FinderGramLevenshteinModel, \
    FinderGramLevenshteinModelMultiple
from flaskapp.classification.data_structure import SearchTerm, FoundTerm, Box
from tests.test_classification import prepare_data


class TestFinderGramLevenshteinModel(unittest.TestCase):

    def test_no_ocr_data(self):
        orc_data = {"text": '', "words": []}
        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModel.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(results, [])

    def test_simple_ocr_data(self):
        orc_data = {"text": 'Berlin',
                    "words": [{'box': {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                               'confidence': 0.0, 'text': 'Berlin'}]}
        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModel.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        expect_value = [SearchTerm(value='Berlin', found_terms=[
            FoundTerm(box=Box(x0=0.0, y0=0.0, xf=2.0, yf=1.0), value='Berlin', score=0.0, score_unit='fraction_error')])]
        self.assertEqual(results, expect_value)

        results = FinderGramLevenshteinModel.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=["Berlin"],
            max_percentage_error=0.2,
        )
        self.assertEqual(results, [])

    def test_find_word(self):
        expect_objects = [
            [SearchTerm(value='Nationalgalerie', found_terms=[
                FoundTerm(box=Box(x0=0.0, y0=0.0, xf=2.0, yf=1.0), value='Nationalg*lerie,', score=0.13,
                          score_unit='fraction_error')]),
             SearchTerm(value='Gebot', found_terms=[
                FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot1', score=0.2,
                          score_unit='fraction_error'),
                FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot2', score=0.2,
                          score_unit='fraction_error'),
                FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebo*', score=0.2,
                          score_unit='fraction_error')])],
            [SearchTerm(value='Sonderauftrag', found_terms=[
                FoundTerm(box=Box(x0=1.0, y0=0.0, xf=4.0, yf=2.0), value='Sondera**trag', score=0.15,
                          score_unit='fraction_error')]),
             SearchTerm(value='Posse', found_terms=[
                FoundTerm(box=Box(x0=3.0, y0=0.0, xf=6.0, yf=1.0), value='Posse', score=0.0,
                          score_unit='fraction_error')])]]

        orc_data, look_terms = prepare_data()
        for search_obj, expect_obj in zip(look_terms, expect_objects):
            search_terms = search_obj["search_terms"]
            no_relevant_terms = search_obj["no_relevant_terms"]
            results = FinderGramLevenshteinModel.find_words(
                ocr_data=orc_data,
                search_terms=search_terms,
                no_relevant_terms=no_relevant_terms,
                max_percentage_error=0.2,
            )
            self.assertEqual(results, expect_obj)

        # TODO check cases where OCR fails to split the text, i.e: Berlin.Schö'neberg,..d6.*.Se.pt.em.bLr
        # TODO try to get Berlin or Schönenberg

    def test_find_word_multiple(self):
        # expect_objects = [
        #     [SearchTerm(value='Nationalgalerie', found_terms=[
        #         FoundTerm(box=Box(x0=0.0, y0=0.0, xf=2.0, yf=1.0), value='Nationalg*lerie,', score=0.13,
        #                   score_unit='fraction_error')]),
        #      SearchTerm(value='Gebot', found_terms=[
        #          FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot1', score=0.2,
        #                    score_unit='fraction_error'),
        #          FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot2', score=0.2,
        #                    score_unit='fraction_error'),
        #          FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebo*', score=0.2,
        #                    score_unit='fraction_error')])],
        #     [SearchTerm(value='Sonderauftrag', found_terms=[
        #         FoundTerm(box=Box(x0=1.0, y0=0.0, xf=4.0, yf=2.0), value='Sondera**trag', score=0.15,
        #                   score_unit='fraction_error')]),
        #      SearchTerm(value='Posse', found_terms=[
        #          FoundTerm(box=Box(x0=3.0, y0=0.0, xf=6.0, yf=1.0), value='Posse', score=0.0,
        #                    score_unit='fraction_error')])]]

        orc_data, look_terms = prepare_data()
        for search_obj in look_terms:
            search_terms = search_obj["search_terms"]
            no_relevant_terms = search_obj["no_relevant_terms"]
            results = FinderGramLevenshteinModelMultiple.find_words(
                ocr_data=orc_data,
                search_terms=search_terms,
                no_relevant_terms=no_relevant_terms,
                max_percentage_error=0.2,
            )
            print(results)
            # self.assertEqual(results, expect_obj)


if __name__ == '__main__':
    unittest.main()
