#coding : UTF-8
# pylint: disable=C0111

"""
Test file for main script api_manager.py
"""

import unittest
import unittest.mock as mock
from gpb_app.api_manager import Parser, WikiAPI, MapsAPI


class TestParser(unittest.TestCase):
    """ Test Parser class"""

    def setUp(self):
        self.parser = Parser()

    def test_remove_punctuation(self):
        sentence = "Par(*le mo,i de ce q@ue t&u ve!ux"
        clean_sentence = self.parser.remove_punctuation(sentence)
        assert clean_sentence == "parle moi de ce que tu veux"

    def test_list_sentence(self):
        sentence = 'parle moi de londres'
        self.assertEqual(self.parser.list_sentence(sentence), ['parle', 'moi', 'de', 'londres'])

    def test_select_words(self):
        words = ['parle', 'moi', 'de', 'londres']
        self.assertEqual(self.parser.select_words(words), ['londres'])


class TestWikiApi(unittest.TestCase):
    """ Test WikiAPI class"""

    def setUp(self):
        self.wikiApi = WikiAPI()
        self.mocked_response = mock.Mock()

    @mock.patch('gpb_app.api_manager.requests')
    def test_get_wiki_pageid_ok(self, mocked_requests):
        words = ["encrier", "paris", "londres", "sdsdsdsd"]
        expected_page_id = 4924
        fake_api_data = {'query': {'searchinfo': {'totalhits': 117660}, 'search':
            [{'ns': 0, 'title': 'Londres', 'pageid': expected_page_id}]}}
        self.mocked_response.json.return_value = fake_api_data
        mocked_requests.get.return_value = self.mocked_response
        answer1 = self.wikiApi.get_wiki_pageid(words)

        self.assertEqual(answer1["pageid"], expected_page_id)

    @mock.patch('gpb_app.api_manager.requests')
    def test_get_wiki_pageid_fail(self, mocked_requests):
        words = ["", "sdsdsdsd"]
        expected_empty_answer = {}
        fake_api_data = {'batchcomplete': '',
                         'query': {'searchinfo': {'totalhits': 0}, 'search': []}}
        self.mocked_response.json.return_value = fake_api_data
        mocked_requests.get.return_value = self.mocked_response
        answer2 = self.wikiApi.get_wiki_pageid(words)

        self.assertEqual(answer2, expected_empty_answer)

    @mock.patch('gpb_app.api_manager.requests')
    def test_get_wiki_text(self, mocked_requests):
        title = ["londres", "egsrger"]
        page_id = [4924, None]
        fake_api_data = {'batchcomplete': '',
                         'continue': {'gsroffset': 1, 'continue': 'gsroffset||'},
                         'query': {'pages': {'4924': {'pageid': 4924, 'ns': 0,
                         'title': 'Londres', 'index': 1,
                         'extract': "Hello lisa granhed Londres [lɔ̃dʁ]  "
                                    "(en anglais : London [ˈlʌndən] ) est la capitale et "
                                    "la plus grande ville d'Angleterre et du Royaume-Uni,."}}}}
        self.mocked_response.json.return_value = fake_api_data
        mocked_requests.get.return_value = self.mocked_response
        text_ok = self.wikiApi.get_wiki_text(title[0], page_id[0])
        text_fail = self.wikiApi.get_wiki_text(title[1], page_id[1])

        self.assertIsInstance(text_ok, str)
        self.assertIsInstance(text_fail, dict)



    def test_get_grandpy_text(self):
        sentences = "j'aime les pates. j'irai bien traverser les plaines de Mongolie. Saucisse." \
                    "Non je suis le pape et j'attends ma soeur."
        element = self.wikiApi.get_grandpy_text(sentences)
        self.assertTrue(element["grandPy_knowledge"] in sentences)


class TestMapsAPI(unittest.TestCase):
    """ Test MapsAPI class"""

    def setUp(self):
        self.maps = MapsAPI()

    @mock.patch('gpb_app.api_manager.requests')
    def test_get_maps_output(self, mocked_requests):
        words = ["paris"]
        expected_address = 'Paris, France'
        expected_coordinates = {'lat': 48.856614, 'lng': 2.3522219}
        fake_api_data = {'results': [{'geometry': {'location': expected_coordinates},
                                      'formatted_address': expected_address}]}
        mocked_response = mock.Mock()
        mocked_response.json.return_value = fake_api_data
        mocked_requests.get.return_value = mocked_response

        output = self.maps.get_maps_output(words)

        self.assertDictEqual(output["coordinates"], expected_coordinates)
        self.assertEqual(output["address"], expected_address)


if __name__ == '__main__':
    unittest.main()

