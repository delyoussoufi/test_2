
def prepare_data():
    look_terms = [{'category_id': 'SMB',
                   'search_terms': ['Nationalgalerie',
                                    'Gebot',
                                    'Rave',
                                    'Perlwitz',
                                    'Boeckler',
                                    'Do_not_have'],
                   'no_relevant_terms': ["Geb*t"]},
                  {'category_id': 'Linz',
                   'search_terms': ['Sonderauftrag',
                                    'Sonderbeauftrag',
                                    'Posse',
                                    'Voss, Hohenfurth'],
                   'no_relevant_terms': []}]

    orc_data = {'text': 'Nationalg*lerie, Sondera**trag another Posse  Geb*t Geb**, Gebot1',
                'words': [
                    {'box': {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'Nationalg*lerie,'},
                    {'box': {'x0': 1.0, 'xf': 4.0, 'y0': 0.0, 'yf': 2.0},
                     'confidence': 0.0,
                     'text': 'Sondera**trag'},
                    {'box': {'x0': 2.0, 'xf': 5.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'another'},
                    {'box': {'x0': 3.0, 'xf': 6.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'Posse'},
                    {'box': {'x0': 4.0, 'xf': 7.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'Geb*t'},
                    {'box': {'x0': 5.0, 'xf': 8.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': 'Geb**'},
                    {'box': {'x0': 6.0, 'xf': 8.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': 'Gebot1'},
                    {'box': {'x0': 6.0, 'xf': 8.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': 'Gebot2'},
                    {'box': {'x0': 6.0, 'xf': 8.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': 'Gebo*'},
                    {'box': {'x0': 16.0, 'xf': 18.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': ''},
                    {'box': {'x0': 18.0, 'xf': 19.0, 'y0': 0.5, 'yf': 1.5},
                     'confidence': 0.0,
                     'text': 'Berlin:'}
                ]}

    return orc_data, look_terms


def multiple_ocr_data():
    orc_data_1 = {"text": "Nationalg*lerie, Sondera**trag another",
                'words': [
                    {'box': {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'Nationalg*lerie,'},
                    {'box': {'x0': 1.0, 'xf': 4.0, 'y0': 0.0, 'yf': 2.0},
                     'confidence': 0.0,
                     'text': 'Sondera**trag'},
                    {'box': {'x0': 2.0, 'xf': 5.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'another'}]
                }
    orc_data_2 = {"text": "Berlin, another",
                'words': [
                    {'box': {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'Berlin,'},
                    {'box': {'x0': 2.0, 'xf': 5.0, 'y0': 0.0, 'yf': 1.0},
                     'confidence': 0.0,
                     'text': 'another'}]
                }
    ocr_data = [orc_data_1, orc_data_2]
    return ocr_data


def look_term_with_operators():
    return {
               'category_id': 'SMB',
               'search_terms': [
                   'Nationalgalerie & Berlin',
                   'Do_not_have'
               ],
               'no_relevant_terms': ["Geb*t"]
    }

