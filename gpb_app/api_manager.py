#coding : UTF-8

from gpb_app.constants import SKIP_WORD
from gpb_app.constants import WIKI_URL, MAPS_URL, MAPS_API_KEY
import requests
import string
import random


class Parser:
    """
    This class parse the user input to return a list of words.

    .remove_punctuation(): remove all the punctuation from the sentence and lower the charachters
    .list_sentence(): split the sentence to a list of words
    .select_words(): remove common words from the splited sentence.
                    common words are in constants.py

    ex :
    user input : Parle moi de Londres
    :return ["londres"]
    """

    def parse(self, query):
        # Main function who use all instances
        cleaned = self.remove_punctuation(query)
        print(cleaned)
        words = self.list_sentence(cleaned)
        print(words)
        output = self.select_words(words)
        return output

    def remove_punctuation(self, sentence):
        # Clean punctuation and lower letters
        for char in list(string.punctuation):
            sentence = sentence.replace(char, "").replace("'", " ")
        return sentence.lower()

    def list_sentence(self, sentence):
        # split sentence to words separated by a blank character
        return sentence.split(" ")

    def select_words(self, words):
        # create a list where the common words are removed
        output_for_wiki = []
        for word in words:
            if word and word not in SKIP_WORD:
                output_for_wiki.append(word)
        return output_for_wiki


class WikiAPI:
    """
    This class use the list of words obtained from the user input to return a unique sentence
    for GranPy knowledge from the WikiMedia api.

    .wikier(): Main function which return data to use (grandPy_knowledge, coordinates) for views.py
                or an empty dict if data are missing
    .get_wiki_pageid(): use parsed words to return the page_id of a word or an empty dict if fails
    .get_wiki_text(): use a word and his page_id to return a short summary of max 10 sentences
                from Wiki api
    .get_grandpy_text(): split the short summary to a list of sentences and return a random one

    ex :
    :parameter : ["londres"]
    :return : {'grandPy_knowledge': " Londres est gouvernée par le maire de Londres
                et l'Assemblée de Londres"}
    """

    def wikier(self, words):
        # return grandPy sentence if page_id exists or a fail sentence
        data = self.get_wiki_pageid(words)
        check_gpk = data.get("grandPy_Knowledge", True)
        check_pageid = data.get("coordinates", True)
        if check_gpk and check_pageid:
            page_id = data["pageid"]
            text = self.get_wiki_text(words, page_id)
            print(text)
            gp_text = self.get_grandpy_text(text)
            return gp_text

        else:
            print("je n'ai pas compris")
            return False

    def get_wiki_pageid(self, words):
        # return the page_id of a selected word if exists, else return an empty dictionnary
        search_payload = {"action": "query",
                          "format": "json",
                          "list": "search",
                          "srlimit": "1",
                          "prop": "redirects"
                          }
        for word in reversed(words):
            search_payload["srsearch"] = word
            search_request = requests.get(WIKI_URL, params=search_payload)
            search_json = search_request.json()
            try:
                page_id = search_json["query"]["search"][0]['pageid']
                data = {
                    "pageid": page_id
                }
                break
            except (KeyError, IndexError, Exception):
                data = {}
        return data

    def get_wiki_text(self, words, page_id):
        # return a short summary from Wiki api if the request succeed,
        # else return an empty dictionnary
        search_payload3 = {
            'action': 'query',
            'prop': 'extracts',
            'exintro': 1,
            'explaintext': 1,
            'format': 'json',
            'exsentences': 10,
            'generator': 'search',
            'gsrlimit': 1,
            'gsrsearch': words
        }
        for word in words:
            data_request = requests.get(WIKI_URL, params=search_payload3)
            # url = data_request.url
            data_json = data_request.json()
            print(data_json)
            try:
                summary = data_json['query']['pages'][str(page_id)]['extract']
                data = summary
                break
            except (KeyError, IndexError, Exception):
                data = {}
        # print(url)
        return data

    def get_grandpy_text(self, text):
        # return a random sentence from the wiki summary
        # if the sentence is empty or smaller then 20 character it is deleted
        sentences = text.split(".")
        for sentence in sentences:
            if sentence == "":
                sentences.remove(sentence)
            elif len(sentence) < 20:
                sentences.remove(sentence)
        gp_response = random.choice(sentences)
        data = {
            "grandPy_knowledge": gp_response
        }
        return data


class MapsAPI:
    """
    This class request Google Maps API with the parsed word to return geographical coordinates.

    ex:
    parameter : ["londres"]
    :return : {'coordinates': {'lat': 51.5073509, 'lng': -0.1277583}}
    """
    def get_maps_output(self, words):
        # replace MAPS_API_KEY by your own api key
        search_payload = {"key": MAPS_API_KEY}
        for word in words:
            search_payload["address"] = word
            search_request = requests.get(MAPS_URL, params=search_payload)
            search_json = search_request.json()
            coordinates = search_json["results"][0]["geometry"]["location"]
            data = {
                "coordinates": {
                    "lat": coordinates["lat"],
                    "lng": coordinates["lng"]
                }
            }
        return data


if __name__ == '__main__':

    """
    The code below runs some examples in the console to show how the code results step by step
    """
    user_inputs = ["Parle moi de londres", "Quelle est l'adresse du Louvre à Paris ?",
                   "Je suis sûr que tu_ ne sais pas ou se tr&ouve Ston/ehenge !", "sdjhgss"]
    parser = Parser()
    wiki = WikiAPI()
    maps = MapsAPI()
    for sentence in user_inputs:
        print(sentence)
        output = parser.parse(sentence)
        print(output)
        print(wiki.wikier(output))
        try:
            maps.get_maps_output(output)
            print(maps.get_maps_output(output))
        except:
            print("c'est le triangle des bermudes")
        print("*" * 100)
