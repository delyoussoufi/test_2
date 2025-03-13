import unittest

from flaskapp.classification.finder_gram_levenshtein_model import FinderGramLevenshteinModelMultiple
from flaskapp.classification.data_structure import SearchTerm, FoundTerm, Box
from tests.test_classification import prepare_data


class TestFinderGramLevenshteinModelMultiple(unittest.TestCase):

    def test_no_ocr_data(self):
        orc_data = {"text": '', "words": []}
        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(results, [])

    def test_simple_ocr_data(self):
        orc_data = {"text": 'Berlin',
                    "words": [{'box': {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                               'confidence': 0.0, 'text': 'Berlin '}]}
        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results[0].found_terms))

        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=["Berlin"],
            max_percentage_error=0.2,
        )
        self.assertEqual(results, [])

    def test_find_word(self):
        expect_objects = [
            [SearchTerm(value='Nationalgalerie', found_terms=[
                FoundTerm(box=Box(x0=0.0, y0=0.0, xf=2.0, yf=1.0), value='Nationalg*lerie', score=0.07,
                          score_unit='fraction_error')]),
             SearchTerm(value='Gebot', found_terms=[
                FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot1', score=0.17,
                          score_unit='fraction_error'),
                FoundTerm(box=Box(x0=6.0, y0=0.5, xf=8.0, yf=1.5), value='Gebot2', score=0.17,
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
            results = FinderGramLevenshteinModelMultiple.find_words(
                ocr_data=orc_data,
                search_terms=search_terms,
                no_relevant_terms=no_relevant_terms,
                max_percentage_error=0.2,
            )
            self.assertEqual(results, expect_obj)

    def test_find_word_multiple(self):

        orc_data = {
            "text": ' Gebot1 Berlin...Schö"neberg,..d6.*.Se.pt.em.bLr B.e.r.l.i.n',
            "words": [
                {"box": {"x0": 6.0, "xf": 8.0, "y0": 0.0, "yf": 1.5},
                 "confidence": 0.0,
                 "text": 'Berlin...Schö"neberg,..d6.*.Se.pt.em.bLr'}]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results[0].found_terms))

        search_terms = ["Schöneberg"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )

        self.assertEqual(1, len(results[0].found_terms))

        search_terms = ["Berlin Schöneberg"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(2, len(results[0].found_terms))

    def test_finder_gram_levenshtein_model_multiple_spaces(self):
        """
        Test that include search_terms with spaces.
        """
        orc_data = {
            "text": ' Gebot1 Berlin.Schö"neberg,..d6.*.Se.pt.em.bLr B.e.r.l.i.n',
            "words": [
                {"box": {"x0": 6.0, "xf": 8.0, "y0": 0.0, "yf": 1.5},
                 "confidence": 0.0,
                 "text": 'Berlin.Schö"neberg,..d6.*.Se.pt.em.bLr'},
                {"box": {"x0": 16.0, "xf": 20.0, "y0": 10.0, "yf": 12.0},
                 "confidence": 0.0,
                 "text": r'Berin'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'B.e.r.l.i.n'},
                {"box": {"x0": 7.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Schöneberg'},
                {"box": {"x0": 9.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'September'}
            ]}

        search_terms = ["Schöneberg Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        expect_obj = [SearchTerm(value='Schöneberg Berlin', found_terms=[
            FoundTerm(box=Box(x0=6.3889, y0=0.0, xf=7.0286, yf=1.5), value='Schöneberg', score=0.00,
                      score_unit='fraction_error'),
            FoundTerm(box=Box(x0=7.0, y0=1.0, xf=15.0, yf=2.0), value='Schöneberg', score=0.0,
                      score_unit='fraction_error'),
            FoundTerm(box=Box(x0=6.0, y0=0.0, xf=6.3889, yf=1.5), value='Berlin', score=0.0,
                      score_unit='fraction_error'),
            FoundTerm(box=Box(x0=1.0, y0=1.0, xf=15.0, yf=2.0), value='Berlin', score=0.0, score_unit='fraction_error'),
            FoundTerm(box=Box(x0=16.0, y0=10.0, xf=20.0, yf=12.0), value='Berin', score=0.2,
                      score_unit='fraction_error')])]

        expect_search_term = expect_obj[0]
        expect_values_score = [(e.value, e.score) for e in expect_search_term.found_terms]
        expect_values_score = sorted(expect_values_score, key=lambda value: value[0])
        results_search_term = results[0]
        results_values_score = [(e.value, e.score) for e in results_search_term.found_terms]
        results_values_score = sorted(results_values_score, key=lambda value: value[0])
        self.assertEqual(results_search_term.value, expect_search_term.value)
        for e, ee in zip(expect_values_score, results_values_score):
            self.assertEqual(e, ee)

        self.assertEqual(1, len(results))
        self.assertEqual(5, len(results[0].found_terms))

        search_terms = ["Schöneberg Paris"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(results, [])

    def test_finder_gram_levenshtein_superposition(self):
        orc_data = {
            "text": 'B.e.r.l.i.n',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'B.e.r.l.i.n'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )

        self.assertEqual(1, len(results))
        self.assertEqual(1, len(results[0].found_terms))

    def test_finder_words_with_special_characters(self):
        orc_data = {
            "text": 'Berlin:',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin:'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.0,
        )

        self.assertEqual(1, len(results))
        self.assertEqual(1, len(results[0].found_terms))

    def test_finder_words_with_excluding_terms(self):

        # Test 1
        orc_data = {
            "text": 'Gemansegalery Berlin',
            "words": [
                {"box": {"x0": 1.0, "xf": 7.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 1.0,
                 "text": 'Gemansegalery'},
                {"box": {"x0": 7.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 1.0,
                 "text": 'Berlin'},
                {"box": {"x0": 7.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 1.0,
                 "text": 'Gemansegalery-Berlin'}
            ]}
        search_terms = ["Gemansegalery -Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(0, len(results))

        search_terms = ["Gemansegalery-Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))

        # Test 2.
        orc_data = {
            "text": 'Gemansegalery Berlin Brandenburg',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Gemansegalery Berlin Brandenburg'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Brandenburg'}
            ]}
        search_terms = ["Gemansegalery -Berlin -Brandenburg"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(0, len(results))

        # Test 3.
        orc_data = {
            "text": 'Gemansegalery',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Gemansegalery'}
            ]}
        search_terms = ["Gemansegalery -Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        # expected 1 results where both found term and the search term should be Gemansegalery
        self.assertEqual(1, len(results))
        self.assertEqual("Gemansegalery -Berlin", results[0].value)  # search term
        self.assertEqual("Gemansegalery", results[0].found_terms[0].value)  # found term

        # Test 4
        orc_data = {
            "text": 'Gemansegalery Berlin Brandenburg',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Gemansegalery'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Brandenburg'}
            ]}

        search_terms = ["Gemansegalery -Berlin -Brandenburg", "Gemansegalery"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))

        # Test 5.
        orc_data = {
            "text": 'Gemansegalery Berlin Brandenburg',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Gemansegalery'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Brandenburg'}
            ]}
        search_terms = ["Gemansegalery -Berlin", "Brandenburg"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))

        # Test 6.
        orc_data = {
            "text": 'Gemansegalery Berlin Brandenburg',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Gemansegalery'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Brandenburg'}
            ]}
        search_terms = ["Gemansegalery -Berlin", "Gemansegalery Brandenburg"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))

    def test_finder_comma(self):
        orc_data = {
            "text": 'Berlin,Another_Word',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Berlin,Another_Word'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(results[0].found_terms))

    def test_finder_special_characters(self):
        orc_data = {
            "text": 'B,e:r?l!i;n',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'B.e.r.l.i.n'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
        )
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(results[0].found_terms))

    def test_finder_black_list(self):
        orc_data = {
            "text": 'B,e:r?l!i;n Other_word',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'B.e.r.l.i.n'},
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'Other_word'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
            black_list_terms=[]
        )
        self.assertEqual(1, len(results))

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
            black_list_terms=["Other_word"]
        )
        self.assertEqual(0, len(results))

        search_terms = ["Another_word"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.2,
            black_list_terms=["Other_word"]
        )
        self.assertEqual(0, len(results))

    def test_finder_words_insensitive_case_characters(self):
        orc_data = {
            "text": 'BERLIN:',
            "words": [
                {"box": {"x0": 1.0, "xf": 15.0, "y0": 1.0, "yf": 2.0},
                 "confidence": 0.0,
                 "text": 'BERLIN:'}
            ]}

        search_terms = ["Berlin"]
        results = FinderGramLevenshteinModelMultiple.find_words(
            ocr_data=orc_data,
            search_terms=search_terms,
            no_relevant_terms=[],
            max_percentage_error=0.0,
        )

        self.assertEqual(1, len(results))
        self.assertEqual(1, len(results[0].found_terms))


if __name__ == '__main__':
    unittest.main()
