from gpb_app.config import SKIP_WORD
from gpb_app.config import WIKI_URL
import requests
import string
import re


class Parser:
    def __init__(self):
        self.expected_outputs = ["londres"]
        self.output_for_Wiki = []

    def parse(self, query):
        cleaned = self.remove_punctuation(query)
        print(cleaned)
        words = self.list_sentence(cleaned)
        print(words)
        output = self.select_words(words)
        print(output)
        return output


    def remove_punctuation(self, sentence):
        for char in list(string.punctuation):
            sentence = sentence.replace(char, "")
        # self.clean_sentence = re.sub(r'[^\w\s]', '', self.sentence)
        return sentence.lower()

    def list_sentence(self, sentence):
        return sentence.split(" ")

    def select_words(self, words):
        output_for_wiki = []
        for word in words:
            if word and word not in SKIP_WORD:
                output_for_wiki.append(word)
        return output_for_wiki


class WikiAPI:

    def get_wiki_output(self, words):
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
            page_id = search_json["query"]["search"][0]['pageid']
            try:
                data = self.get_wiki_data(page_id)
                break

            except (KeyError, IndexError, Exception):
                data = {}
        return data

    def get_wiki_data(self, page_id):
        search_payload2 = {"action": "query",
                           "format": "json",
                           "prop": "description|coordinates",
                           "pageids": page_id
                           }
        data_request = requests.get(WIKI_URL, params=search_payload2)
        data_json = data_request.json()
        coordinates = data_json['query']['pages'][str(page_id)]['coordinates'][:2][0]
        data = {
            "response": data_json['query']['pages'][str(page_id)]['description'],
            # "coordinates": data_json['query']['pages'][str(self.page_id)]
            "coordinates": {
                "lat": coordinates["lat"],
                "lng": coordinates["lon"]
            }
        }
        return data



class MapsAPI:
    def __init__(self):
        pass

if __name__ == '__main__':

    user_inputs = ["Parle moi de Londres", "Quelle est l'adresse du Louvre à Paris ?",
                                "Je suis sûr que tu_ ne sais pas ou se tr&ouve Ston/ehenge !"]
    parser = Parser()
    wiki = WikiAPI()
    for sentence in user_inputs:
        print(sentence)
        output = parser.parse(sentence)
        print(wiki.get_wiki_output(output))
        print("*" * 100)

