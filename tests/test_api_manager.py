#coding : UTF-8
# pylint: disable=C0111

"""
Test file for main script api_manager.py
"""

import unittest
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

    def test_get_wiki_pageid(self):
        words = ["encrier", "paris", "londres"]
        words2 = [""]
        words3 = ["sdsdsdsd"]
        words4 = ["londres", "sdsdsdsd"]
        self.assertEqual(self.wikiApi.get_wiki_pageid(words)["pageid"], 4924)
        self.assertEqual(self.wikiApi.get_wiki_pageid(words4)["pageid"], 4924)
        self.assertEqual(self.wikiApi.get_wiki_pageid(words2), {})
        self.assertEqual(self.wikiApi.get_wiki_pageid(words3), {})

    def test_get_wiki_text_return_data(self):
        self.assertTrue(type(self.wikiApi.get_wiki_text("londres", 4924)) is str)

    def test_get_wiki_text_return_nothing(self):
        self.assertTrue(type(self.wikiApi.get_wiki_text("egsrger", None)) is dict)

    def test_get_grandpy_text(self):
        sentences = "j'aime les pates. j'irai bien traverser les plaines de Mongolie. Saucisse." \
                    "Non je suis le pape et j'attends ma soeur."
        element = self.wikiApi.get_grandpy_text(sentences)
        self.assertTrue(element["grandPy_knowledge"] in sentences)


class TestMapsAPI(unittest.TestCase):
    """ Test MapsAPI class"""

    def setUp(self):
        self.maps = MapsAPI()

    def test_get_maps_output(self):
        words = ["paris"]
        self.assertEqual(self.maps.get_maps_output(words)["coordinates"], {'lat': 48.856614,
                                                                           'lng': 2.3522219})
        self.assertEqual(self.maps.get_maps_output(words)["address"], 'Paris, France')


if __name__ == '__main__':
    unittest.main()
