import unittest
from gpb_app.api_manager import Parser, WikiAPI, MapsAPI


class TestParser(unittest.TestCase):

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


    # def test_get_wiki_text(self):
    #     results = "Londres [lɔ̃dʁ]  (en anglais : London [ˈlʌndən] ) est la capitale et la plus grande ville d'Angleterre et du Royaume-Uni,. La ville est située près de l'estuaire de la Tamise dans le sud-est de l'Angleterre. Londinium a été fondée par les Romains il y a presque 2 000 ans. La Cité de Londres, le noyau historique de Londres avec une superficie de seulement 1,12 miles carrés (2,9 km²) conserve des frontières qui suivent de près ses limites médiévales. Londres est gouvernée par le maire de Londres et l'Assemblée de Londres. Londres est considérée comme l'une des villes mondiales les plus importantes du monde,,. La ville exerce un impact considérable sur les arts, le commerce, l'éducation, le divertissement, la mode, les finances, les soins de santé, les médias, les services professionnels, la recherche et le développement, le tourisme et les transports,. Londres se classe 26e sur 300 grandes villes pour ses performances économiques. C'est l'un des plus grands centres financiers avec New York et Hong Kong, et a le cinquième ou le sixième plus gros PIB urbain mondial. C'est la ville la plus visitée mesurée par les arrivées internationales et possède le système aéroportuaire le plus fréquenté par le trafic de passagers du monde."
    #     self.assertEqual(self.wikiApi.get_wiki_text("londres", 4924), results)

    def test_get_grandpy_text(self):
        sentences = "j'aime les pates. j'irai bien traverser les plaines de Mongolie. Saucisse." \
                    "Non je suis le pape et j'attends ma soeur."
        element = self.wikiApi.get_grandpy_text(sentences)
        self.assertTrue(element["grandPy_knowledge"] in sentences)


class TestMapsAPI(unittest.TestCase):

    def setUp(self):
        self.maps = MapsAPI()

    def test_get_maps_output(self):
        words = ["paris"]
        self.assertEqual(self.maps.get_maps_output(words)["coordinates"], {'lat': 48.856614,
                                                                           'lng': 2.3522219})


if __name__ == '__main__':
    unittest.main()



